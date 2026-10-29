#!/usr/bin/env python3
"""Inspect failing GitLab merge-request CI via the glab API.

Binds an explicit HOST, project path, and MR IID, resolves the MR head SHA,
selects the current head pipeline, lists its jobs (paginated), and extracts
failure snippets from failed-job traces.

Read-only: issues GET requests plus single-job trace reads only. It never
retries, reruns, cancels, creates, or deletes pipelines or jobs, and it never
prints credential values.

Exit status: 0 only for verified green (head-pipeline success with matching
head SHA). 1 when the head pipeline has failed jobs or the helper itself
fails. 2 when the state is indeterminate (running, missing, skipped, or
unrelated pipelines). A nonzero exit never means green; in particular, the
absence of failed jobs is not success.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from collections.abc import Iterable, Sequence

JsonDict = dict[str, "JsonValue"]
JsonList = list["JsonValue"]
JsonValue = JsonDict | JsonList | str | int | float | bool | None

FAILURE_MARKERS = (
    "error",
    "fail",
    "failed",
    "traceback",
    "exception",
    "assert",
    "panic",
    "fatal",
    "timeout",
    "segmentation fault",
)

DEFAULT_MAX_LINES = 160
DEFAULT_CONTEXT_LINES = 30
PENDING_TRACE_MARKERS = (
    "still in progress",
    "log will be available when it is complete",
    "job is still running",
)

FAILED_JOB_STATUSES = {"failed"}
SKIPPED_JOB_STATUSES = {"canceled", "skipped", "manual"}

SUBPROCESS_TIMEOUT = 120


class GlabResult:
    def __init__(self, returncode: int, stdout: str, stderr: str):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def run_glab(args: Sequence[str], cwd: Path) -> GlabResult:
    try:
        process = subprocess.run(
            ["glab", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return GlabResult(1, "", "glab command timed out.")
    except FileNotFoundError:
        return GlabResult(1, "", "glab executable not found on PATH.")
    return GlabResult(process.returncode, process.stdout, process.stderr)


def run_glab_raw(args: Sequence[str], cwd: Path) -> tuple[int, bytes, str]:
    try:
        process = subprocess.run(
            ["glab", *args],
            cwd=cwd,
            capture_output=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 1, b"", "glab command timed out."
    except FileNotFoundError:
        return 1, b"", "glab executable not found on PATH."
    stderr = process.stderr.decode(errors="replace")
    return process.returncode, process.stdout, stderr


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect GitLab MR CI: bind host/project/MR IID, select the head "
            "pipeline, list jobs, and extract failed-job log snippets."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--host", required=True, help="GitLab hostname.")
    parser.add_argument(
        "--project",
        required=True,
        help="Project path GROUP/PROJECT (URL-encoded by the helper).",
    )
    parser.add_argument("--mr", required=True, help="Merge request IID.")
    parser.add_argument(
        "--repo",
        default=".",
        help="Working directory; used as subprocess cwd only.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit JSON instead of text output."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cwd = resolve_cwd(Path(args.repo))
    if cwd is None:
        print("Error: --repo is not a directory.", file=sys.stderr)
        return 1

    if not ensure_glab_available(cwd, args.host):
        return 1

    try:
        iid = int(str(args.mr).strip())
    except ValueError:
        print(f"Error: --mr must be a numeric IID, got {args.mr!r}.",
              file=sys.stderr)
        return 1
    project = encode_project(args.project)

    mr = fetch_mr(args.host, project, iid, cwd)
    if mr is None:
        return 1
    head_sha = extract_head_sha(mr)
    if not head_sha:
        emit(args, summarize(args, mr, "", "missing", None,
             "MR exposes no head SHA; no pipeline can be bound to it."), [])
        return 2

    pipeline, verdict, note = select_head_pipeline(mr, head_sha)
    summary = summarize(args, mr, head_sha, verdict, pipeline, note)
    if pipeline is None or verdict in ("missing", "unrelated", "running",
                                       "skipped"):
        emit(args, summary, [])
        return 2

    jobs = fetch_pipeline_jobs(args.host, project, pipeline_id(pipeline), cwd)
    if jobs is None:
        return 1
    failed = [job for job in jobs if job_status(job) in FAILED_JOB_STATUSES]
    if not failed:
        jobs_verdict, jobs_note = completed_pipeline_jobs_verdict(jobs)
        if jobs_verdict != "green":
            summary["verdict"] = jobs_verdict
            summary["note"] = jobs_note
        elif verdict == "green":
            emit(args, summary, summarize_jobs(jobs))
            return 0
        emit(args, summary, summarize_jobs(jobs))
        return 2

    results = [
        analyze_job(
            job,
            host=args.host,
            project=project,
            cwd=cwd,
            max_lines=DEFAULT_MAX_LINES,
            context=DEFAULT_CONTEXT_LINES,
        )
        for job in failed
    ]
    summary["note"] = f"{len(failed)} failed jobs analyzed."
    emit(args, summary, results)
    return 1


def resolve_cwd(repo: Path) -> Path | None:
    if not repo.exists() or not repo.is_dir():
        return None
    return repo.resolve()


def ensure_glab_available(cwd: Path, host: str) -> bool:
    result = run_glab(["auth", "status", "--hostname", host], cwd=cwd)
    if result.returncode != 0:
        message = "\n".join(
            filter(None, [result.stderr, result.stdout])).strip()
        print(message or f"Error: glab auth failed for host {host}. "
              "Run glab auth login --hostname HOST.", file=sys.stderr)
        return False
    return True


def encode_project(project: str) -> str:
    from urllib.parse import quote

    return quote(project.strip(), safe="")


def api_get(host: str, endpoint: str, cwd: Path,
            paginate: bool) -> JsonValue | None:
    args: list[str] = ["api", "--hostname", host, endpoint,
                       "--output", "json"]
    if paginate:
        args.append("--paginate")
    result = run_glab(args, cwd=cwd)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "").strip()
        print(message or f"Error: glab api {endpoint} failed.",
              file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout or "null")
    except json.JSONDecodeError:
        payload: JsonList = []
        for line in (result.stdout or "").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                payload.append(json.loads(line))
            except json.JSONDecodeError:
                print("Error: unable to parse API JSON payload.",
                      file=sys.stderr)
                return None
        return payload


def fetch_mr(host: str, project: str, iid: int,
             cwd: Path) -> JsonDict | None:
    data = api_get(host, f"projects/{project}/merge_requests/{iid}",
                   cwd, paginate=False)
    if not isinstance(data, dict):
        print("Error: unexpected MR JSON shape.", file=sys.stderr)
        return None
    return data


def select_head_pipeline(
    mr: JsonDict,
    head_sha: str,
) -> tuple[JsonDict | None, str, str]:
    declared = mr.get("head_pipeline")
    if not isinstance(declared, dict) or declared.get("id") is None:
        return None, "missing", (
            "The MR records no head pipeline; no CI is bound to the current "
            "revision, never green.")
    if pipeline_sha(declared) != head_sha:
        return None, "unrelated", (
            "The MR head moved past its recorded head pipeline; "
            "that pipeline is unrelated to the current revision, never green.")
    return classify_pipeline(declared)


def fetch_pipeline_jobs(host: str, project: str, pipeline_id_value: JsonValue,
                        cwd: Path) -> list[JsonDict] | None:
    data = api_get(
        host, f"projects/{project}/pipelines/{pipeline_id_value}/jobs",
        cwd, paginate=True)
    if data is None:
        return None
    items = data if isinstance(data, list) else [data]
    jobs = [item for item in items if isinstance(item, dict)]
    if len(jobs) != len(items):
        print("Error: unexpected jobs JSON shape.", file=sys.stderr)
        return None
    return jobs


def extract_head_sha(mr: JsonDict) -> str:
    diff_refs = mr.get("diff_refs")
    if isinstance(diff_refs, dict) and diff_refs.get("head_sha"):
        return str(diff_refs["head_sha"])
    if mr.get("sha"):
        return str(mr["sha"])
    return ""


def pipeline_sha(pipeline: JsonDict) -> str:
    return str(pipeline.get("sha") or "")


def pipeline_id(pipeline: JsonDict) -> JsonValue:
    return pipeline.get("id")


def pipeline_status(pipeline: JsonDict) -> str:
    return normalize(pipeline.get("status"))


def job_status(job: JsonDict) -> str:
    return normalize(job.get("status"))


def classify_pipeline(
    pipeline: JsonDict,
) -> tuple[JsonDict | None, str, str]:
    status = pipeline_status(pipeline)
    if status == "success":
        return pipeline, "green", ""
    if status == "failed":
        return (pipeline, "failed",
                f"Head pipeline {pipeline_id(pipeline)} reported failure.")
    if status in SKIPPED_JOB_STATUSES:
        return (pipeline, "skipped",
                f"Head pipeline {pipeline_id(pipeline)} ended as {status}; "
                "a skipped pipeline is not a pass.")
    return (pipeline, "running",
            f"Head pipeline {pipeline_id(pipeline)} is {status or 'unknown'}; "
            "incomplete checks are not diagnosed.")


def authoritative_ci_jobs(jobs: list[JsonDict]) -> list[JsonDict]:
    return [job for job in jobs if job_status(job) not in SKIPPED_JOB_STATUSES]


def completed_pipeline_jobs_verdict(jobs: list[JsonDict]) -> tuple[str, str]:
    if not jobs:
        return ("missing", "Pipeline returned no jobs; no CI is proven, never green.")
    authoritative = authoritative_ci_jobs(jobs)
    if not authoritative:
        return ("skipped", "Pipeline returned only skipped jobs; a skipped set is not a pass, never green.")
    incomplete = [job for job in authoritative if job_status(job) != "success"]
    if incomplete:
        return ("running", "Pipeline jobs include incomplete work; incomplete checks are not diagnosed, never green.")
    return ("green", "")


def analyze_job(
    job: JsonDict,
    host: str,
    project: str,
    cwd: Path,
    max_lines: int,
    context: int,
) -> JsonDict:
    job_id = job.get("id")
    pipeline_ref = job.get("pipeline")
    base: JsonDict = {
        "name": job.get("name", ""),
        "jobId": job_id,
        "stage": job.get("stage", ""),
        "status": job_status(job),
        "pipelineId": pipeline_ref.get("id")
        if isinstance(pipeline_ref, dict) else pipeline_ref,
        "webUrl": job.get("web_url", ""),
    }
    log_text, log_error = fetch_job_trace(host, project, job_id, cwd)
    if log_error and is_pending_message(log_error):
        base["status"] = "log_pending"
        base["note"] = log_error
        return base
    if log_error:
        base["status"] = "log_unavailable"
        base["error"] = log_error
        return base
    base["status"] = "ok"
    base["logSnippet"] = extract_failure_snippet(
        log_text, max_lines=max_lines, context=context)
    base["logTail"] = tail_lines(log_text, max_lines)
    return base


def fetch_job_trace(host: str, project: str, job_id: JsonValue,
                    cwd: Path) -> tuple[str, str]:
    returncode, payload, stderr = run_glab_raw(
        ["api", "--hostname", host, f"projects/{project}/jobs/{job_id}/trace"],
        cwd=cwd,
    )
    if returncode != 0:
        message = (stderr or payload.decode(errors="replace")).strip()
        return "", message or "glab api job trace failed"
    return payload.decode(errors="replace"), ""


def summarize_jobs(jobs: list[JsonDict]) -> list[JsonDict]:
    return [
        {
            "name": job.get("name", ""),
            "jobId": job.get("id"),
            "stage": job.get("stage", ""),
            "status": job_status(job),
        }
        for job in jobs
    ]


def normalize(value: JsonValue) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return ""
    return str(value).strip().lower()


def is_pending_message(message: str) -> bool:
    lowered = message.lower()
    return any(marker in lowered for marker in PENDING_TRACE_MARKERS)


def extract_failure_snippet(log_text: str, max_lines: int,
                            context: int) -> str:
    lines = log_text.splitlines()
    if not lines:
        return ""
    marker_index = find_failure_index(lines)
    if marker_index is None:
        return "\n".join(lines[-max_lines:])
    start = max(0, marker_index - context)
    end = min(len(lines), marker_index + context)
    window = lines[start:end]
    if len(window) > max_lines:
        window = window[-max_lines:]
    return "\n".join(window)


def find_failure_index(lines: Sequence[str]) -> int | None:
    for idx in range(len(lines) - 1, -1, -1):
        lowered = lines[idx].lower()
        if any(marker in lowered for marker in FAILURE_MARKERS):
            return idx
    return None


def tail_lines(text: str, max_lines: int) -> str:
    if max_lines <= 0:
        return ""
    return "\n".join(text.splitlines()[-max_lines:])


def summarize(args: argparse.Namespace, mr: JsonDict, head_sha: str,
              verdict: str, pipeline: JsonDict | None, note: str) -> JsonDict:
    return {
        "provider": "gitlab",
        "host": args.host,
        "project": args.project,
        "iid": args.mr,
        "mr_state": mr.get("state", ""),
        "head_sha": head_sha,
        "verdict": verdict,
        "sha_match": pipeline is not None
        and pipeline_sha(pipeline) == head_sha,
        "pipeline": summarize_pipeline(pipeline),
        "note": note,
    }


def emit(args: argparse.Namespace, summary: JsonDict,
         results: Iterable[JsonDict]) -> None:
    record = dict(summary)
    record["results"] = list(results)
    if args.json:
        print(json.dumps(record, indent=2))
    else:
        render_results(record)


def summarize_pipeline(pipeline: JsonDict | None) -> JsonDict:
    if pipeline is None:
        return {}
    return {
        "id": pipeline.get("id"),
        "status": pipeline.get("status", ""),
        "sha": pipeline.get("sha", ""),
        "ref": pipeline.get("ref", ""),
        "source": pipeline.get("source", ""),
        "web_url": pipeline.get("web_url", ""),
    }


def render_results(record: JsonDict) -> None:
    print(f"MR !{record['iid']} on {record['host']}/{record['project']}: "
          f"verdict {record['verdict']}.")
    print(f"MR state: {record.get('mr_state', '')}")
    head_sha = str(record.get("head_sha") or "")
    if head_sha:
        print(f"Head SHA: {head_sha[:12]} "
              f"(match: {'yes' if record.get('sha_match') else 'no'})")
    pipeline = record.get("pipeline")
    if isinstance(pipeline, dict) and pipeline:
        print(f"Pipeline: {pipeline.get('id', '')} "
              f"({pipeline.get('status', '')})")
        if pipeline.get("ref") or pipeline.get("sha"):
            print(f"Pipeline ref/SHA: {pipeline.get('ref', '')} "
                  f"{str(pipeline.get('sha', ''))[:12]}")
        if pipeline.get("web_url"):
            print(f"Pipeline URL: {pipeline['web_url']}")
    if record.get("note"):
        print(f"Note: {record['note']}")
    results = record.get("results")
    if not isinstance(results, list):
        results = []
    for result in results:
        if not isinstance(result, dict):
            continue
        print("-" * 60)
        print(f"Job: {result.get('name', '')}")
        if result.get("jobId") is not None:
            print(f"Job ID: {result['jobId']}")
        if result.get("stage"):
            print(f"Stage: {result['stage']}")
        print(f"Status: {result.get('status', 'unknown')}")
        if result.get("webUrl"):
            print(f"Details: {result['webUrl']}")
        if result.get("note"):
            print(f"Note: {result['note']}")
        if result.get("error"):
            print(f"Error fetching logs: {result['error']}")
            continue
        snippet = result.get("logSnippet") or ""
        if snippet:
            print("Failure snippet:")
            print(indent_block(str(snippet), prefix="  "))
        elif "logSnippet" in result:
            print("No snippet available.")
    print("-" * 60)


def indent_block(text: str, prefix: str = "  ") -> str:
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


if __name__ == "__main__":
    raise SystemExit(main())
