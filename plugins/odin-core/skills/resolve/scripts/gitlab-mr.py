#!/usr/bin/env python3
"""GitLab merge-request review helper.

Self-contained: Python standard library only, no plugin-global imports.
One glab write at most per invocation; a write is never retried. The caller
owns idempotency: every accepted write returns its mutation IDs, and a later
read-back failure reports those IDs instead of repeating the mutation.

Consistency contract (single-shot CLI over the GitLab REST API via glab):
- Reads take a two-pin snapshot: the MR head SHA is fetched before and after
  the discussion/note census, and any head change fails the census instead of
  returning a mixed snapshot.
- Writes are at-most-once. Exactly-once delivery does not exist across a CLI
  subprocess boundary, so this helper issues one POST/PUT, validates the
  receipt, then reads back. There is no retry budget for mutations and no
  outbox/saga: the receipt plus read-back is the whole protocol.
- Every glab hop carries an explicit timeout and fails fast; there are no
  unbounded waits and no retries on any failure.

Endpoints (grounded in docs.gitlab.com/api/discussions and
docs.gitlab.com/cli/api, pinned in local://gitlab-mr-api-contract.json and
local://gitlab-cli-contract.json):
- GET  projects/:encoded/merge_requests/:iid
- GET  projects/:encoded/merge_requests/:iid/discussions?per_page=100 (paged)
- GET  projects/:encoded/merge_requests/:iid/notes?per_page=100 (paged)
- GET  projects/:encoded/merge_requests/:iid/discussions/:discussion_id
- POST projects/:encoded/merge_requests/:iid/discussions/:discussion_id/notes
- PUT  projects/:encoded/merge_requests/:iid/discussions/:discussion_id?resolved=true
"""

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from urllib.parse import quote, urlparse

PROVIDER = "gitlab"
DEFAULT_TIMEOUT_S = 60
PER_PAGE = 100


class HelperError(Exception):
    """Typed failure with a machine-readable code and detail payload."""

    def __init__(self, code, message, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details if isinstance(details, dict) else {}


def emit_error(err, host=None, project=None, iid=None):
    payload = {"error": err.code, "message": err.message}
    if host is not None:
        payload["host"] = host
    if project is not None:
        payload["project"] = project
    if iid is not None:
        payload["iid"] = iid
    payload.update(err.details)
    print(json.dumps(payload, indent=2, sort_keys=True), file=sys.stderr)


def check_host(raw):
    host = (raw or "").strip()
    if not host:
        raise HelperError("usage", "host must not be empty")
    if "://" in host or "/" in host or "@" in host:
        raise HelperError("usage", f"host must be a bare hostname, not a URL or path: {raw!r}")
    if any(ch.isspace() for ch in host):
        raise HelperError("usage", f"host must not contain whitespace: {raw!r}")
    return host


def check_project(raw):
    project = (raw or "").strip()
    if not project or "/" not in project:
        raise HelperError("usage", f"project must look like GROUP/PROJECT: {raw!r}")
    if project.startswith("/") or project.endswith("/"):
        raise HelperError("usage", f"project must not start or end with '/': {raw!r}")
    for segment in project.split("/"):
        if not segment:
            raise HelperError("usage", f"project has an empty path segment: {raw!r}")
        for ch in segment:
            if not (ch.isalnum() or ch in "._-"):
                raise HelperError("usage", f"project segment has an illegal character: {segment!r}")
    return project


def check_iid(raw):
    try:
        iid = int(raw)
    except (TypeError, ValueError) as err:
        raise HelperError("usage", f"mr IID must be a positive integer: {raw!r}") from err
    if iid <= 0:
        raise HelperError("usage", f"mr IID must be a positive integer: {raw!r}")
    return iid


def check_note_id(raw):
    try:
        note_id = int(raw)
    except (TypeError, ValueError) as err:
        raise HelperError("usage", f"note id must be a positive integer: {raw!r}") from err
    if note_id <= 0:
        raise HelperError("usage", f"note id must be a positive integer: {raw!r}")
    return note_id


def check_discussion(raw):
    discussion_id = (raw or "").strip()
    if not discussion_id:
        raise HelperError("usage", "discussion id must not be empty")
    if any(ch.isspace() for ch in discussion_id) or "/" in discussion_id:
        raise HelperError("usage", f"discussion id is not a single path segment: {raw!r}")
    return discussion_id


def check_timeout(raw):
    try:
        timeout_s = float(raw)
    except (TypeError, ValueError) as err:
        raise HelperError("usage", f"timeout must be a positive number of seconds: {raw!r}") from err
    if not math.isfinite(timeout_s) or timeout_s <= 0:
        raise HelperError("usage", f"timeout must be a positive finite number of seconds: {raw!r}")
    return timeout_s


def _run(argv, timeout_s, label):
    """Run one glab call exactly once with a hard timeout and no retries."""
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s, check=False)
    except subprocess.TimeoutExpired as err:
        raise HelperError(
            "timeout",
            f"glab call timed out after {timeout_s:g}s: {label}",
            {"endpoint": label},
        ) from err
    except OSError as err:
        raise HelperError(
            "subprocess_failed",
            f"could not execute glab for {label}: {err}",
            {"endpoint": label},
        ) from err


def _parse_json(stdout, label):
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as err:
        raise HelperError(
            "malformed_payload",
            f"glab returned unparseable JSON for {label}: {err}",
            {"endpoint": label},
        ) from err


def _refuse_failed(proc, label):
    if proc.returncode != 0:
        raise HelperError(
            "subprocess_failed",
            f"glab call failed (exit {proc.returncode}): {label}",
            {"endpoint": label, "exit": proc.returncode, "stderr": (proc.stderr or "")[:2000]},
        )


def fetch_single_object(host, endpoint, timeout_s):
    """GET one JSON object (MR identity, single discussion). No pagination."""
    argv = ["glab", "api", "--hostname", host, endpoint, "-X", "GET", "--output", "json"]
    proc = _run(argv, timeout_s, endpoint)
    _refuse_failed(proc, endpoint)
    if not (proc.stdout or "").strip():
        raise HelperError(
            "malformed_payload",
            f"glab returned an empty body for {endpoint}; never an empty success",
            {"endpoint": endpoint},
        )
    payload = _parse_json(proc.stdout, endpoint)
    if not isinstance(payload, dict):
        raise HelperError(
            "malformed_payload",
            f"expected a JSON object for {endpoint}, got {type(payload).__name__}",
            {"endpoint": endpoint},
        )
    return payload


def fetch_complete_list(host, endpoint, timeout_s):
    """GET a complete paginated JSON array via the documented --paginate flag."""
    argv = ["glab", "api", "--hostname", host, endpoint, "-X", "GET",
            "--paginate", "--output", "json"]
    proc = _run(argv, timeout_s, endpoint)
    _refuse_failed(proc, endpoint)
    if not (proc.stdout or "").strip():
        raise HelperError(
            "malformed_payload",
            f"glab returned an empty body for {endpoint}; never an empty success",
            {"endpoint": endpoint},
        )
    payload = _parse_json(proc.stdout, endpoint)
    if not isinstance(payload, list):
        raise HelperError(
            "malformed_payload",
            f"expected a JSON array for {endpoint}, got {type(payload).__name__}",
            {"endpoint": endpoint},
        )
    return payload


def get_mr(host, project, iid, timeout_s):
    """Fetch MR identity, enforcing IID match and a present head SHA."""
    endpoint = f"projects/{quote(project, safe='')}/merge_requests/{iid}"
    obj = fetch_single_object(host, endpoint, timeout_s)
    if obj.get("iid") != iid:
        raise HelperError(
            "wrong_identity",
            f"MR identity mismatch: asked for iid {iid}, got {obj.get('iid')!r}",
            {"endpoint": endpoint, "returned_iid": obj.get("iid")},
        )
    web_url = obj.get("web_url")
    if isinstance(web_url, str) and web_url:
        parsed = urlparse(web_url)
        want_host, _, want_port = host.lower().partition(":")
        if (parsed.hostname or "").lower() != want_host:
            raise HelperError(
                "wrong_identity",
                f"MR web_url host {parsed.hostname!r} does not match requested host {host!r}",
                {"endpoint": endpoint, "web_url": web_url},
            )
        try:
            got_port = parsed.port
        except ValueError as err:
            raise HelperError(
                "wrong_identity",
                f"MR web_url {web_url!r} carries an unparsable port",
                {"endpoint": endpoint, "web_url": web_url},
            ) from err
        if want_port and str(got_port or "") != want_port:
            raise HelperError(
                "wrong_identity",
                f"MR web_url port {got_port!r} does not match requested host {host!r}",
                {"endpoint": endpoint, "web_url": web_url},
            )
    references = obj.get("references")
    full_ref = references.get("full") if isinstance(references, dict) else None
    suffix = f"!{iid}"
    if isinstance(full_ref, str) and full_ref.endswith(suffix):
        if full_ref[: -len(suffix)].lower() != project.lower():
            raise HelperError(
                "wrong_identity",
                f"MR full reference {full_ref!r} does not match requested project {project!r}",
                {"endpoint": endpoint, "full_reference": full_ref},
            )
    head_sha = obj.get("sha")
    if not isinstance(head_sha, str) or not head_sha:
        raise HelperError(
            "malformed_payload",
            f"MR {iid} response carries no head sha",
            {"endpoint": endpoint},
        )
    return obj, head_sha


def check_thread_notes(thread_notes, discuss_id):
    """Every thread note must carry an integer id; fail otherwise."""
    for note in thread_notes:
        if not isinstance(note, dict) or not isinstance(note.get("id"), int):
            raise HelperError(
                "malformed_payload",
                f"discussion {discuss_id!r} holds a note without an integer id; census unusable",
                {"discussion_id": discuss_id},
            )


def check_census(discussions, notes):
    """Every census element must carry its identity fields; fail otherwise."""
    for index, discussion in enumerate(discussions):
        discuss_id = discussion.get("id") if isinstance(discussion, dict) else None
        if not isinstance(discuss_id, str) or not discuss_id:
            raise HelperError(
                "malformed_payload",
                f"discussion #{index} has no string id; census unusable",
                {"index": index},
            )
        thread_notes = discussion.get("notes")
        if not isinstance(thread_notes, list):
            raise HelperError(
                "malformed_payload",
                f"discussion {discuss_id!r} carries no notes array; census unusable",
                {"discussion_id": discuss_id},
            )
        check_thread_notes(thread_notes, discuss_id)
    for index, note in enumerate(notes):
        if not isinstance(note, dict) or not isinstance(note.get("id"), int):
            raise HelperError(
                "malformed_payload",
                f"root note #{index} has no integer id; census unusable",
                {"index": index},
            )


def read_census(host, project, iid, timeout_s):
    """Read MR head plus the full discussion and note census (head-pinned)."""
    _, head_before = get_mr(host, project, iid, timeout_s)
    base = f"projects/{quote(project, safe='')}/merge_requests/{iid}"
    discussions = fetch_complete_list(host, f"{base}/discussions?per_page={PER_PAGE}", timeout_s)
    notes = fetch_complete_list(host, f"{base}/notes?per_page={PER_PAGE}", timeout_s)
    _, head_after = get_mr(host, project, iid, timeout_s)
    if head_before != head_after:
        raise HelperError(
            "head_changed",
            f"MR head changed during census ({head_before} -> {head_after}); prior evidence is stale",
            {"head_before": head_before, "head_after": head_after,
             "discussions_fetched": len(discussions), "notes_fetched": len(notes)},
        )
    check_census(discussions, notes)
    return head_before, discussions, notes


def cmd_list(host, project, iid, timeout_s):
    head_sha, discussions, notes = read_census(host, project, iid, timeout_s)
    print(json.dumps({
        "provider": PROVIDER,
        "host": host,
        "project": project,
        "iid": iid,
        "head_sha": head_sha,
        "discussions": discussions,
        "notes": notes,
        "coverage": {
            "discussions_fetched": len(discussions),
            "notes_fetched": len(notes),
            "discussions_complete": True,
            "notes_complete": True,
            "head_stable": True,
            "complete": True,
        },
    }, indent=2, sort_keys=True))


def cmd_thread(host, project, iid, timeout_s, note_id):
    head_sha, discussions, _ = read_census(host, project, iid, timeout_s)
    matches = []
    for discussion in discussions:
        if not isinstance(discussion, dict):
            raise HelperError(
                "malformed_payload",
                "discussion census contains a non-object entry",
                {"note_id": note_id},
            )
        thread_notes = discussion.get("notes")
        if not isinstance(thread_notes, list):
            raise HelperError(
                "malformed_payload",
                f"discussion {discussion.get('id')!r} carries no notes array",
                {"note_id": note_id, "discussion_id": discussion.get("id")},
            )
        for note in thread_notes:
            if isinstance(note, dict) and note.get("id") == note_id:
                matches.append(discussion)
                break
    if not matches:
        raise HelperError(
            "note_not_found",
            f"note {note_id} is in no discussion of this census (root notes live outside threads)",
            {"note_id": note_id, "discussions_searched": len(discussions)},
        )
    if len(matches) > 1:
        raise HelperError(
            "ambiguous_note",
            f"note {note_id} appears in {len(matches)} discussions; refusing to guess",
            {"note_id": note_id,
             "discussion_ids": [d.get("id") for d in matches if isinstance(d, dict)]},
        )
    discussion = matches[0]
    print(json.dumps({
        "provider": PROVIDER,
        "host": host,
        "project": project,
        "iid": iid,
        "head_sha": head_sha,
        "note_id": note_id,
        "discussion_id": discussion.get("id"),
        "discussion": discussion,
    }, indent=2, sort_keys=True))


def read_body_file(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            body_text = handle.read()
    except OSError as err:
        raise HelperError(
            "body_read_failed",
            f"cannot read body file {path}: {err}",
            {"body_file": path},
        ) from err
    except UnicodeDecodeError as err:
        raise HelperError(
            "body_read_failed",
            f"body file {path} is not valid UTF-8",
            {"body_file": path},
        ) from err
    if not body_text.strip():
        raise HelperError(
            "empty_body",
            f"body file {path} is empty; refusing to post an empty reply",
            {"body_file": path},
        )
    return body_text


def cmd_reply(host, project, iid, timeout_s, discussion_id, body_file):
    body_text = read_body_file(body_file)
    mr_obj, head_before = get_mr(host, project, iid, timeout_s)
    base = f"projects/{quote(project, safe='')}/merge_requests/{iid}"
    single = f"{base}/discussions/{quote(discussion_id, safe='')}"
    before = fetch_single_object(host, single, timeout_s)
    if before.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"discussion identity mismatch: asked for {discussion_id!r}, got {before.get('id')!r}",
            {"endpoint": single, "discussion_id": discussion_id},
        )
    tmp_path = ""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                         delete=False, encoding="utf-8") as tmp:
            json.dump({"body": body_text}, tmp)
            tmp_path = tmp.name
        endpoint = f"{single}/notes"
        argv = ["glab", "api", "--hostname", host, endpoint, "-X", "POST",
                "--input", tmp_path, "--output", "json"]
        proc = _run(argv, timeout_s, endpoint)
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError as err:
                print(f"warning: could not remove temp file {tmp_path}: {err}",
                      file=sys.stderr)
    _refuse_failed(proc, endpoint)
    receipt = _parse_json(proc.stdout, endpoint)
    if not isinstance(receipt, dict) or not isinstance(receipt.get("id"), int):
        raise HelperError(
            "missing_receipt",
            f"reply POST returned no note id for discussion {discussion_id!r}",
            {"endpoint": endpoint, "discussion_id": discussion_id},
        )
    for key, want in (("project_id", mr_obj.get("project_id")), ("noteable_id", mr_obj.get("id"))):
        got = receipt.get(key)
        if isinstance(got, int) and isinstance(want, int) and got != want:
            raise HelperError(
                "wrong_identity",
                f"reply POST receipt {key} {got} is outside the requested scope ({want}); do not re-post",
                {"endpoint": endpoint, "discussion_id": discussion_id, "note_id": receipt.get("id")},
            )
    note_id = receipt["id"]
    try:
        after = fetch_single_object(host, single, timeout_s)
    except HelperError as err:
        raise HelperError(
            err.code,
            f"{err.message}; reply was accepted as note {note_id}, do not re-post",
            {"discussion_id": discussion_id, "note_id": note_id, **err.details},
        ) from err
    if after.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"read-back discussion identity mismatch: asked for {discussion_id!r}, "
            f"got {after.get('id')!r}; do not re-post",
            {"endpoint": single, "discussion_id": discussion_id, "note_id": note_id},
        )
    after_notes = after.get("notes")
    if not isinstance(after_notes, list) or not any(
            isinstance(n, dict) and n.get("id") == note_id for n in after_notes):
        raise HelperError(
            "readback_mismatch",
            f"reply was accepted as note {note_id} but is absent on read-back; do not re-post",
            {"discussion_id": discussion_id, "note_id": note_id},
        )
    try:
        _, head_after = get_mr(host, project, iid, timeout_s)
    except HelperError as err:
        raise HelperError(
            err.code,
            f"{err.message}; reply was accepted as note {note_id}, do not re-post",
            {"discussion_id": discussion_id, "note_id": note_id, **err.details},
        ) from err
    if head_before != head_after:
        raise HelperError(
            "head_changed",
            f"reply was accepted as note {note_id} but MR head moved "
            f"({head_before} -> {head_after}); do not re-post",
            {"discussion_id": discussion_id, "note_id": note_id,
             "head_before": head_before, "head_after": head_after},
        )
    print(json.dumps({
        "provider": PROVIDER,
        "host": host,
        "project": project,
        "iid": iid,
        "head_sha": head_after,
        "discussion_id": discussion_id,
        "note_id": note_id,
        "accepted": True,
        "readback": True,
        "note": receipt,
    }, indent=2, sort_keys=True))


def cmd_resolve(host, project, iid, timeout_s, discussion_id):
    _, head_before = get_mr(host, project, iid, timeout_s)
    base = f"projects/{quote(project, safe='')}/merge_requests/{iid}"
    single = f"{base}/discussions/{quote(discussion_id, safe='')}"
    current = fetch_single_object(host, single, timeout_s)
    if current.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"discussion identity mismatch: asked for {discussion_id!r}, got {current.get('id')!r}",
            {"endpoint": single, "discussion_id": discussion_id},
        )
    thread_notes = current.get("notes")
    if not isinstance(thread_notes, list) or not thread_notes:
        raise HelperError(
            "malformed_payload",
            f"discussion {discussion_id!r} carries no notes array; resolvability unknown",
            {"endpoint": single, "discussion_id": discussion_id},
        )
    for entry in thread_notes:
        if (not isinstance(entry, dict) or not isinstance(entry.get("id"), int)
                or not isinstance(entry.get("resolvable"), bool)
                or not isinstance(entry.get("resolved"), bool)):
            raise HelperError(
                "malformed_payload",
                f"discussion {discussion_id!r} holds an unusable note entry; resolvability unknown",
                {"endpoint": single, "discussion_id": discussion_id},
            )
    resolvable = [entry for entry in thread_notes if entry.get("resolvable") is True]
    if not resolvable:
        raise HelperError(
            "nonresolvable",
            f"discussion {discussion_id!r} has no resolvable notes; refusing to resolve",
            {"endpoint": single, "discussion_id": discussion_id},
        )
    if all(n.get("resolved") is True for n in resolvable):
        print(json.dumps({
            "provider": PROVIDER,
            "host": host,
            "project": project,
            "iid": iid,
            "head_sha": head_before,
            "discussion_id": discussion_id,
            "resolved": True,
            "mutated": False,
        }, indent=2, sort_keys=True))
        return
    endpoint = f"{single}?resolved=true"
    argv = ["glab", "api", "--hostname", host, endpoint, "-X", "PUT", "--output", "json"]
    proc = _run(argv, timeout_s, endpoint)
    _refuse_failed(proc, endpoint)
    updated = _parse_json(proc.stdout, endpoint)
    if not isinstance(updated, dict):
        raise HelperError(
            "missing_receipt",
            f"resolve PUT returned no discussion object for {discussion_id!r}; do not re-send",
            {"endpoint": endpoint, "discussion_id": discussion_id},
        )
    if updated.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"resolve PUT returned discussion {updated.get('id')!r}, not {discussion_id!r}; do not re-send",
            {"endpoint": endpoint, "discussion_id": discussion_id},
        )
    updated_notes = updated.get("notes")
    if not isinstance(updated_notes, list) or not updated_notes:
        raise HelperError(
            "missing_receipt",
            f"resolve PUT response for {discussion_id!r} carries no notes array to confirm; do not re-send",
            {"endpoint": endpoint, "discussion_id": discussion_id},
        )
    for entry in updated_notes:
        if (not isinstance(entry, dict) or not isinstance(entry.get("id"), int)
                or not isinstance(entry.get("resolvable"), bool)
                or not isinstance(entry.get("resolved"), bool)):
            raise HelperError(
                "malformed_payload",
                f"resolve PUT response for {discussion_id!r} holds an unusable note entry; do not re-send",
                {"endpoint": endpoint, "discussion_id": discussion_id},
            )
    resolvable_updated = [entry for entry in updated_notes if entry.get("resolvable") is True]
    if not resolvable_updated or not all(entry.get("resolved") is True for entry in resolvable_updated):
        raise HelperError(
            "missing_receipt",
            f"resolve PUT response does not confirm resolution of {discussion_id!r}; do not re-send",
            {"endpoint": endpoint, "discussion_id": discussion_id},
        )
    try:
        after = fetch_single_object(host, single, timeout_s)
    except HelperError as err:
        raise HelperError(
            err.code,
            f"{err.message}; resolve was accepted for {discussion_id!r}, do not re-send",
            {"discussion_id": discussion_id, **err.details},
        ) from err
    if after.get("id") != discussion_id:
        raise HelperError(
            "wrong_identity",
            f"read-back discussion identity mismatch: asked for {discussion_id!r}, "
            f"got {after.get('id')!r}; do not re-send",
            {"endpoint": single, "discussion_id": discussion_id},
        )
    after_notes = after.get("notes")
    if not isinstance(after_notes, list) or not after_notes:
        raise HelperError(
            "malformed_payload",
            f"read-back discussion {discussion_id!r} carries no notes array; do not re-send",
            {"endpoint": single, "discussion_id": discussion_id},
        )
    for entry in after_notes:
        if (not isinstance(entry, dict) or not isinstance(entry.get("id"), int)
                or not isinstance(entry.get("resolvable"), bool)
                or not isinstance(entry.get("resolved"), bool)):
            raise HelperError(
                "malformed_payload",
                f"read-back discussion {discussion_id!r} holds an unusable note entry; do not re-send",
                {"endpoint": single, "discussion_id": discussion_id},
            )
    resolvable_after = [entry for entry in after_notes if entry.get("resolvable") is True]
    if not resolvable_after or not all(entry.get("resolved") is True for entry in resolvable_after):
        raise HelperError(
            "readback_mismatch",
            f"resolve was accepted for {discussion_id!r} but read-back is unresolved; do not re-send",
            {"discussion_id": discussion_id},
        )
    try:
        _, head_after = get_mr(host, project, iid, timeout_s)
    except HelperError as err:
        raise HelperError(
            err.code,
            f"{err.message}; resolve was accepted for {discussion_id!r}, do not re-send",
            {"discussion_id": discussion_id, **err.details},
        ) from err
    if head_before != head_after:
        raise HelperError(
            "head_changed",
            f"resolve was accepted for {discussion_id!r} but MR head moved "
            f"({head_before} -> {head_after}); do not re-send",
            {"discussion_id": discussion_id,
             "head_before": head_before, "head_after": head_after},
        )
    print(json.dumps({
        "provider": PROVIDER,
        "host": host,
        "project": project,
        "iid": iid,
        "head_sha": head_after,
        "discussion_id": discussion_id,
        "resolved": True,
        "mutated": True,
    }, indent=2, sort_keys=True))


def build_parser():
    parser = argparse.ArgumentParser(
        description="GitLab merge-request review helper (read census, thread lookup, reply, resolve)")
    parser.add_argument("--host", required=True, help="GitLab hostname, e.g. gitlab.com")
    parser.add_argument("--project", required=True, help="Namespaced path, e.g. GROUP/PROJECT")
    parser.add_argument("--mr", required=True, help="Merge-request IID (project-scoped)")
    parser.add_argument("--timeout", default=DEFAULT_TIMEOUT_S,
                        help=f"Seconds per glab call (default {DEFAULT_TIMEOUT_S:g})")
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("list", help="Emit MR head plus the full discussion/note census")
    thread_p = sub.add_parser("thread", help="Find the discussion containing a note")
    thread_p.add_argument("--note", required=True, help="Numeric note id")
    reply_p = sub.add_parser("reply", help="Post exactly one reply in a discussion")
    reply_p.add_argument("--discussion", required=True, help="Discussion id (hex string)")
    reply_p.add_argument("--body-file", required=True, help="File carrying the reply body")
    resolve_p = sub.add_parser("resolve", help="Resolve one resolvable discussion")
    resolve_p.add_argument("--discussion", required=True, help="Discussion id (hex string)")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        host = check_host(args.host)
        project = check_project(args.project)
        iid = check_iid(args.mr)
        timeout_s = check_timeout(args.timeout)
        if args.operation == "list":
            cmd_list(host, project, iid, timeout_s)
        elif args.operation == "thread":
            cmd_thread(host, project, iid, timeout_s, check_note_id(args.note))
        elif args.operation == "reply":
            cmd_reply(host, project, iid, timeout_s,
                      check_discussion(args.discussion), args.body_file)
        elif args.operation == "resolve":
            cmd_resolve(host, project, iid, timeout_s, check_discussion(args.discussion))
        else:
            raise HelperError("usage", f"unknown operation: {args.operation!r}")
    except HelperError as err:
        host = getattr(args, "host", None)
        project = getattr(args, "project", None)
        raw_iid = getattr(args, "mr", None)
        try:
            iid = int(raw_iid)
        except (TypeError, ValueError):
            iid = raw_iid
        emit_error(err, host, project, iid)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
