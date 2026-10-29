#!/usr/bin/env python3
"""Validate odin-learning/v1 knowledge records.

Reads the machine contract from references/schema.md (same skill directory),
parses the target Markdown YAML frontmatter with a standard-library safe
subset parser, and enforces required fields, types, enums, arrays, dates,
and the unknown-field policy. Fail-closed: anything the parser cannot
represent is a validation failure, never a silent skip.

Usage:
    python3 scripts/validate-record.py <doc-path>
    python3 scripts/validate-record.py --self-test

Exit codes:
    0 - parser-safe and schema-valid (or self-test fully passed)
    1 - validation failure, or self-test case failure (diagnostics on stdout/stderr)
    2 - usage error or schema-load failure
"""
import os
import re
import sys
from datetime import date as _date
from pathlib import Path

EXIT_OK = 0
EXIT_INVALID = 1
EXIT_USAGE = 2

MACHINE_MARKER = "machine-contract"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
TAG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PLAIN_LEAD_BAD = set("[]{}&*!|>%@`\"'#,")
DOUBLE_ESCAPES = set("0abtnvfre \"\\/N_LP")
HEX_LEN = {"x": 2, "u": 4, "U": 8}

# Gate scripts run on whatever python3 the machine carries, so this file must
# parse on the oldest interpreter a contributor might carry. Keep it
# MIN_PYTHON-clean: no match, no X | Y annotations, and no f-string
# replacement fields at all (every message below uses % formatting), so the
# 3.12 f-string tokenizer change cannot affect this file.
MIN_PYTHON = (3, 9)


def _usage(msg):
    sys.stderr.write("validate-record: %s\n" % msg)
    return EXIT_USAGE


def _strip_comment(line):
    # Full-line comments carry no data; drop them before parsing. This covers
    # the machine contract's marker line and any comment-only record lines.
    if line.lstrip(" ").startswith("#"):
        return ""
    out = []
    in_single = False
    in_double = False
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if in_single:
            out.append(ch)
            if ch == "'":
                if i + 1 < n and line[i + 1] == "'":
                    out.append("'")
                    i += 2
                    continue
                in_single = False
            i += 1
            continue
        if in_double:
            out.append(ch)
            if ch == "\\":
                if i + 1 < n:
                    out.append(line[i + 1])
                    i += 2
                    continue
            elif ch == '"':
                in_double = False
            i += 1
            continue
        if ch == "'":
            in_single = True
            out.append(ch)
            i += 1
            continue
        if ch == '"':
            in_double = True
            out.append(ch)
            i += 1
            continue
        if ch == "#" and out and out[-1] in (" ", "\t"):
            break
        out.append(ch)
        i += 1
    return "".join(out).rstrip()


def _split_flow(text):
    """Split top-level commas; return (parts, error)."""
    parts = []
    cur = []
    in_single = False
    in_double = False
    depth = 0
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_single:
            cur.append(ch)
            if ch == "'":
                if i + 1 < n and text[i + 1] == "'":
                    cur.append("'")
                    i += 1
                else:
                    in_single = False
            i += 1
            continue
        if in_double:
            cur.append(ch)
            if ch == "\\" and i + 1 < n:
                cur.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                in_double = False
            i += 1
            continue
        if ch == "'":
            in_single = True
            cur.append(ch)
            i += 1
            continue
        if ch == '"':
            in_double = True
            cur.append(ch)
            i += 1
            continue
        if ch == "[":
            depth += 1
            cur.append(ch)
            i += 1
            continue
        if ch == "]":
            if depth == 0:
                return None, "unbalanced bracket in flow list"
            depth -= 1
            cur.append(ch)
            i += 1
            continue
        if ch == "," and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    if in_single or in_double:
        return None, "unterminated quote in flow list"
    if depth != 0:
        return None, "unbalanced bracket in flow list"
    parts.append("".join(cur).strip())
    return parts, None


def _parse_double(text):
    if len(text) < 2 or not text.endswith('"'):
        return None, "double-quoted scalar never closes"
    i = 1
    n = len(text) - 1
    buf = []
    while i < n:
        ch = text[i]
        if ch == "\\":
            if i + 1 >= n:
                return None, "trailing backslash in double-quoted scalar"
            nxt = text[i + 1]
            if nxt in HEX_LEN:
                need = HEX_LEN[nxt]
                hexpart = text[i + 2:i + 2 + need]
                if len(hexpart) != need or not all(
                        c in "0123456789abcdefABCDEF" for c in hexpart):
                    return None, "bad hex escape in double-quoted scalar"
                buf.append(chr(int(hexpart, 16)))
                i += 2 + need
                continue
            if nxt not in DOUBLE_ESCAPES:
                return None, "unknown escape in double-quoted scalar"
            conv = {"0": "\0", "a": "\a", "b": "\b", "t": "\t",
                    "n": "\n", "v": "\v", "f": "\f", "r": "\r",
                    "e": "\x1b"}.get(nxt, nxt)
            buf.append(conv)
            i += 2
            continue
        if ch == "\n" or ch == "\t":
            return None, "control character in double-quoted scalar"
        if ch == '"':
            return None, "unescaped quote in double-quoted scalar"
        buf.append(ch)
        i += 1
    return "".join(buf), None


def _parse_scalar(token, field):
    t = token.strip()
    if t == "":
        return None, "empty scalar for '%s'" % field
    if t.startswith("'"):
        if len(t) < 2 or not t.endswith("'"):
            return None, "single-quoted scalar never closes for '%s'" % field
        inner = t[1:-1].replace("''", "\x00")
        if "'" in inner:
            return None, "bare single quote must be doubled for '%s'" % field
        return inner.replace("\x00", "'"), None
    if t.startswith('"'):
        val, err = _parse_double(t)
        if err is not None:
            return None, "%s for '%s'" % (err, field)
        return val, None
    if t.startswith("["):
        if not t.endswith("]"):
            return None, "flow list never closes for '%s'" % field
        inner = t[1:-1].strip()
        if inner == "":
            return [], None
        items = []
        parts, err = _split_flow(inner)
        if err is not None:
            return None, "%s for '%s'" % (err, field)
        for raw in parts:
            if raw == "":
                return None, "empty item in flow list for '%s'" % field
            v, err = _parse_scalar(raw, field)
            if err is not None:
                return None, err
            if not isinstance(v, str):
                return None, "flow list item must be a string for '%s'" % field
            items.append(v)
        return items, None
    if t in ("true", "false"):
        return (t == "true"), None
    if t in ("null", "~"):
        return None, "null value not allowed for '%s'" % field
    if t[0] in PLAIN_LEAD_BAD:
        return None, "value for '%s' starts with reserved indicator; quote it" % field
    if t[0] in "-?:":
        return None, "value for '%s' starts with reserved indicator; quote it" % field
    if t[0] == "[" or t[0] == "{":
        return None, "value for '%s' starts with reserved indicator; quote it" % field
    if ": " in t:
        return None, "value for '%s' contains ': '; quote it" % field
    if "\t" in t:
        return None, "tab character in value for '%s'" % field
    return t, None


def _parse_mapping(lines):
    data = {}
    errors = []
    order = []
    i = 0
    n = len(lines)
    while i < n:
        lineno, raw = lines[i]
        if "\t" in raw:
            errors.append("line %d: tab indentation is not allowed" % lineno)
            i += 1
            continue
        code = _strip_comment(raw)
        if code.strip() == "":
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent != 0:
            errors.append("line %d: unexpected indentation" % lineno)
            i += 1
            continue
        if ":" not in code:
            errors.append("line %d: expected 'key: value'" % lineno)
            i += 1
            continue
        key, _, rest = code.partition(":")
        key = key.strip()
        if not KEY_RE.match(key):
            errors.append("line %d: bad key name" % lineno)
            i += 1
            continue
        if key in data:
            errors.append("line %d: duplicate key '%s'" % (lineno, key))
            i += 1
            continue
        val = rest.strip()
        if val != "":
            if val == "|":
                errors.append("line %d: block scalars are not supported" % lineno)
                i += 1
                continue
            if val == ">":
                errors.append("line %d: block scalars are not supported" % lineno)
                i += 1
                continue
            if val.startswith("{"):
                errors.append("line %d: flow mappings are not supported" % lineno)
                i += 1
                continue
            v, err = _parse_scalar(val, key)
            if err is not None:
                errors.append("line %d: %s" % (lineno, err))
                i += 1
                continue
            data[key] = v
            order.append(key)
            i += 1
            continue
        j = i + 1
        items = []
        item_lines = []
        while j < n:
            l2, r2 = lines[j]
            if "\t" in r2:
                errors.append("line %d: tab indentation is not allowed" % l2)
                j += 1
                continue
            c2 = _strip_comment(r2)
            if c2.strip() == "":
                j += 1
                continue
            ind2 = len(r2) - len(r2.lstrip(" "))
            if ind2 == 0:
                break
            stripped = c2.strip()
            if not stripped.startswith("-"):
                if key == "origin_records":
                    if ":" not in stripped:
                        errors.append("line %d: origin field must be 'key: value'" % l2)
                        j += 1
                        continue
                    item_lines.append((l2, ind2, stripped))
                    j += 1
                    continue
                errors.append("line %d: expected '- item'" % l2)
                j += 1
                continue
            if stripped == "-":
                errors.append("line %d: empty list item" % l2)
                j += 1
                continue
            content = stripped[1:].strip()
            item_lines.append((l2, ind2, content))
            j += 1
        if not item_lines:
            errors.append("line %d: key '%s' has no value and no list items" % (lineno, key))
            i = j
            continue
        if key == "origin_records":
            maps = []
            k = 0
            bad = False
            base_ind = item_lines[0][1]
            while k < len(item_lines):
                l2, ind2, content = item_lines[k]
                if ind2 != base_ind:
                    errors.append("line %d: inconsistent origin item indent" % l2)
                    bad = True
                    k += 1
                    continue
                if ":" not in content:
                    errors.append("line %d: origin item must be 'key: value'" % l2)
                    bad = True
                    k += 1
                    continue
                first_k, _, first_v = content.partition(":")
                first_k = first_k.strip()
                cur = {}
                v, err = _parse_scalar(first_v.strip(), first_k)
                if err is not None:
                    errors.append("line %d: %s" % (l2, err))
                    bad = True
                    k += 1
                    continue
                if not KEY_RE.match(first_k):
                    errors.append("line %d: bad origin key" % l2)
                    bad = True
                    k += 1
                    continue
                cur[first_k] = v
                k += 1
                while k < len(item_lines) and item_lines[k][1] > base_ind:
                    l3, _, c3 = item_lines[k]
                    if ":" not in c3:
                        errors.append("line %d: origin field must be 'key: value'" % l3)
                        bad = True
                        k += 1
                        continue
                    fk, _, fv = c3.partition(":")
                    fk = fk.strip()
                    if not KEY_RE.match(fk):
                        errors.append("line %d: bad origin key" % l3)
                        bad = True
                        k += 1
                        continue
                    if fk in cur:
                        errors.append("line %d: duplicate origin key '%s'" % (l3, fk))
                        bad = True
                        k += 1
                        continue
                    vv, err = _parse_scalar(fv.strip(), fk)
                    if err is not None:
                        errors.append("line %d: %s" % (l3, err))
                        bad = True
                        k += 1
                        continue
                    cur[fk] = vv
                    k += 1
                maps.append(cur)
            if bad:
                i = j
                continue
            data[key] = maps
            order.append(key)
            i = j
            continue
        vals = []
        bad = False
        for l2, ind2, content in item_lines:
            if ":" in content and ": " in content and not (
                    content.startswith("'") or content.startswith('"')):
                errors.append("line %d: nested mappings are not supported here" % l2)
                bad = True
                continue
            v, err = _parse_scalar(content, key)
            if err is not None:
                errors.append("line %d: %s" % (l2, err))
                bad = True
                continue
            if not isinstance(v, str):
                errors.append("line %d: list item must be a string" % l2)
                bad = True
                continue
            if v == "":
                errors.append("line %d: empty list item" % l2)
                bad = True
                continue
            vals.append(v)
        if bad:
            i = j
            continue
        data[key] = vals
        order.append(key)
        i = j
    return data, errors


def _extract_frontmatter(text):
    """Split Markdown YAML frontmatter; return (numbered_lines, error)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, "file does not start with '---' frontmatter delimiter line"
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
        if lines[i].strip().startswith("```"):
            break
    if end_idx is None:
        return None, "frontmatter not closed (no '---' line after the opening delimiter)"
    numbered = [(k + 1, v) for k, v in enumerate(lines[1:end_idx])]
    return numbered, None


def _load_machine(schema_path):
    try:
        text = Path(schema_path).read_text(encoding="utf-8")
    except OSError as exc:
        return None, ["cannot read schema: %s" % exc]
    lines = text.split("\n")
    in_fence = False
    buf = None
    for raw in lines:
        s = raw.strip()
        if s.startswith("```"):
            if not in_fence and "yaml" in s:
                in_fence = True
                buf = []
                continue
            if in_fence:
                joined = "\n".join(buf)
                if MACHINE_MARKER in joined:
                    numbered = [(k + 1, v) for k, v in enumerate(buf)]
                    data, errs = _parse_mapping(numbered)
                    if errs:
                        return None, ["schema machine block: " + e for e in errs]
                    return data, []
                in_fence = False
                buf = None
                continue
            continue
        if in_fence:
            buf.append(raw)
    return None, ["schema machine block with '%s' not found" % MACHINE_MARKER]


def _need_keys(cfg):
    keys = ["schema_value", "record_kinds", "rationale_required",
            "rationale_optional", "rationale_type_enum",
            "rationale_confidence_enum", "rationale_status_enum",
            "rationale_evidence_enum", "solution_required", "solution_optional",
            "problem_type_enum", "bug_track", "root_cause_enum",
            "resolution_type_enum", "severity_enum", "category_enum",
            "solution_status_enum", "solution_evidence_enum",
            "migration_origin_enum", "origin_required", "category_map"]
    missing = [k for k in keys if k not in cfg]
    return missing


def _check_date(value, field):
    if not isinstance(value, str) or not DATE_RE.match(value):
        return "field '%s' must be ISO YYYY-MM-DD" % field
    try:
        _date.fromisoformat(value)
    except ValueError:
        return "field '%s' is not a valid calendar date" % field
    return None


def _check_str_list(value, field, lo, hi):
    if not isinstance(value, list):
        return "field '%s' must be a list" % field
    if len(value) < lo or len(value) > hi:
        return "field '%s' must have %d-%d items" % (field, lo, hi)
    for item in value:
        if not isinstance(item, str) or item == "":
            return "field '%s' has an empty item" % field
    return None


def _validate(data, cfg, doc_path):
    problems = []
    for k in ("schema_value",):
        _ = k
    schema_value = cfg["schema_value"]
    if data.get("schema") != schema_value:
        problems.append("field 'schema' must be exactly '%s'" % schema_value)
    rk = data.get("record_kind")
    if rk not in ("rationale", "solution"):
        problems.append("field 'record_kind' must be 'rationale' or 'solution'")
        return problems
    derr = _check_date(data.get("date"), "date")
    if derr is not None:
        problems.append(derr)
    cmap = {}
    for entry in cfg["category_map"]:
        if not isinstance(entry, str) or "=" not in entry:
            problems.append("schema category_map entry is malformed")
            break
        a, _, b = entry.partition("=")
        cmap[a.strip()] = b.strip()
    if rk == "rationale":
        allowed = set(cfg["rationale_required"]) | set(cfg["rationale_optional"])
        for k in data:
            if k not in allowed:
                problems.append("unknown field '%s' for rationale record" % k)
        for k in cfg["rationale_required"]:
            if k not in data:
                problems.append("missing required field '%s'" % k)
        if "type" in data and data["type"] not in cfg["rationale_type_enum"]:
            problems.append("field 'type' has an unsupported value")
        if "confidence" in data and data["confidence"] not in cfg["rationale_confidence_enum"]:
            problems.append("field 'confidence' must be high, medium, or low")
        if "source" in data and (
                not isinstance(data["source"], str) or data["source"] == ""):
            problems.append("field 'source' must be a non-empty string")
        if "tags" in data:
            e = _check_str_list(data["tags"], "tags", 1, 8)
            if e is not None:
                problems.append(e)
            else:
                for t in data["tags"]:
                    if not TAG_RE.match(t):
                        problems.append("tag '%s' must be lowercase hyphen-separated" % t)
                        break
        if "status" in data and data["status"] not in cfg["rationale_status_enum"]:
            problems.append("field 'status' has an unsupported value")
        if "evidence" in data and data["evidence"] not in cfg["rationale_evidence_enum"]:
            problems.append("field 'evidence' has an unsupported value")
        if "retire_when" in data and (
                not isinstance(data["retire_when"], str) or data["retire_when"] == ""):
            problems.append("field 'retire_when' must be a non-empty string")
        if "last_updated" in data:
            e = _check_date(data["last_updated"], "last_updated")
            if e is not None:
                problems.append(e)
        for sol_only in ("title", "category", "module", "problem_type",
                          "component", "severity", "symptoms", "root_cause",
                          "resolution_type", "applies_when"):
            if sol_only in data:
                problems.append("solution-only field '%s' must not appear on rationale" % sol_only)
    else:
        allowed = set(cfg["solution_required"]) | set(cfg["solution_optional"])
        for k in data:
            if k not in allowed:
                problems.append("unknown field '%s' for solution record" % k)
        for k in cfg["solution_required"]:
            if k not in data:
                problems.append("missing required field '%s'" % k)
        for k in ("title", "module", "component"):
            if k in data and (
                    not isinstance(data[k], str) or data[k] == ""):
                problems.append("field '%s' must be a non-empty string" % k)
        if "category" in data and data["category"] not in cfg["category_enum"]:
            problems.append("field 'category' has an unsupported value")
        if "problem_type" in data and data["problem_type"] not in cfg["problem_type_enum"]:
            problems.append("field 'problem_type' has an unsupported value")
        if "severity" in data and data["severity"] not in cfg["severity_enum"]:
            problems.append("field 'severity' must be critical, high, medium, or low")
        pt = data.get("problem_type")
        if isinstance(pt, str) and pt in cmap:
            if "category" in data and data["category"] != cmap[pt]:
                problems.append("category must be '%s' for problem_type '%s'" % (cmap[pt], pt))
        is_bug = isinstance(pt, str) and pt in cfg["bug_track"]
        if is_bug:
            for k in ("symptoms", "root_cause", "resolution_type"):
                if k not in data:
                    problems.append("bug track requires field '%s'" % k)
        if "symptoms" in data:
            hi = 5
            lo = 1 if is_bug else 1
            if not isinstance(data["symptoms"], list):
                problems.append("field 'symptoms' must be a list")
            elif len(data["symptoms"]) < lo or len(data["symptoms"]) > hi:
                problems.append("field 'symptoms' must have 1-5 items")
            elif any(not isinstance(x, str) or x == "" for x in data["symptoms"]):
                problems.append("field 'symptoms' has an empty item")
        if "root_cause" in data and data["root_cause"] not in cfg["root_cause_enum"]:
            problems.append("field 'root_cause' has an unsupported value")
        if "resolution_type" in data and data["resolution_type"] not in cfg["resolution_type_enum"]:
            problems.append("field 'resolution_type' has an unsupported value")
        if "applies_when" in data:
            e = _check_str_list(data["applies_when"], "applies_when", 1, 5)
            if e is not None:
                problems.append(e)
        if "tags" in data:
            e = _check_str_list(data["tags"], "tags", 1, 8)
            if e is not None:
                problems.append(e)
            else:
                for t in data["tags"]:
                    if not TAG_RE.match(t):
                        problems.append("tag '%s' must be lowercase hyphen-separated" % t)
                        break
        if "related_components" in data:
            e = _check_str_list(data["related_components"], "related_components", 1, 20)
            if e is not None:
                problems.append(e)
        if "status" in data and data["status"] not in cfg["solution_status_enum"]:
            problems.append("field 'status' has an unsupported value")
        if data.get("status") == "stale":
            if "stale_reason" not in data or not isinstance(
                    data["stale_reason"], str) or data["stale_reason"] == "":
                problems.append("stale records require a non-empty 'stale_reason'")
            if "stale_date" not in data:
                problems.append("stale records require 'stale_date'")
            else:
                e = _check_date(data["stale_date"], "stale_date")
                if e is not None:
                    problems.append(e)
        if "last_updated" in data:
            e = _check_date(data["last_updated"], "last_updated")
            if e is not None:
                problems.append(e)
        if "supersedes" in data and (
                not isinstance(data["supersedes"], str) or data["supersedes"] == ""):
            problems.append("field 'supersedes' must be a non-empty string")
        if "evidence" in data and data["evidence"] not in cfg["solution_evidence_enum"]:
            problems.append("field 'evidence' has an unsupported value")
        for rat_only in ("type", "confidence"):
            if rat_only in data:
                problems.append("rationale-only field '%s' must not appear on solution" % rat_only)
    if "origin_records" in data:
        ors = data["origin_records"]
        if not isinstance(ors, list) or len(ors) == 0:
            problems.append("field 'origin_records' must be a non-empty list")
        else:
            seen = set()
            for item in ors:
                if not isinstance(item, dict):
                    problems.append("origin_records items must be mappings")
                    break
                want = set(cfg["origin_required"])
                if set(item.keys()) != want:
                    problems.append("origin item must hold exactly path, sha256, migration_origin, historical")
                    break
                if not isinstance(item["path"], str) or item["path"] == "":
                    problems.append("origin 'path' must be a non-empty string")
                    break
                if not isinstance(item["sha256"], str) or not SHA_RE.match(item["sha256"]):
                    problems.append("origin 'sha256' must be 64 lowercase hex characters")
                    break
                if item["migration_origin"] not in cfg["migration_origin_enum"]:
                    problems.append("origin 'migration_origin' has an unsupported value")
                    break
                if item["historical"] is not True:
                    problems.append("origin 'historical' must be true")
                    break
                tup = (item["path"], item["sha256"], item["migration_origin"], True)
                if tup in seen:
                    problems.append("duplicate origin tuple")
                    break
                seen.add(tup)
    return problems


def _self_cases():
    a64 = "a" * 64
    b64 = "b" * 64
    r_base = (
        "---\n"
        "schema: odin-learning/v1\n"
        "record_kind: rationale\n"
        "date: 2026-10-01\n"
        "type: caveat\n"
        "confidence: high\n"
        "source: session context 2026-10-29\n"
        "tags:\n"
        "  - parser-caveat\n"
        "---\n"
        "Body.\n"
    )
    r_origin_two = (
        "---\n"
        "schema: odin-learning/v1\n"
        "record_kind: rationale\n"
        "date: 2026-10-01\n"
        "type: lesson\n"
        "confidence: medium\n"
        "source: session context 2026-10-29\n"
        "origin_records:\n"
        "  - path: docs/solutions/old-a.md\n"
        "    sha256: " + a64 + "\n"
        "    migration_origin: legacy-compound-v0\n"
        "    historical: true\n"
        "  - path: docs/solutions/old-b.md\n"
        "    sha256: " + b64 + "\n"
        "    migration_origin: legacy-compound-v0\n"
        "    historical: true\n"
        "---\n"
        "Body.\n"
    )
    r_flow_tags = r_base.replace(
        "tags:\n  - parser-caveat\n", "tags: [parser-caveat, second-tag]\n")
    r_unknown_key = r_base.replace(
        "source: session context 2026-10-29\n",
        "source: session context 2026-10-29\ntitle: Something\n")
    r_bad_enum = r_base.replace("confidence: high\n", "confidence: confirmed\n")
    r_missing_source = r_base.replace("source: session context 2026-10-29\n", "")
    r_bad_date = r_base.replace("date: 2026-10-01\n", "date: 2026/10/29\n")
    r_block_scalar = r_base.replace(
        "source: session context 2026-10-29\n", "source: |\n")
    r_unquoted_colon = r_base.replace(
        "source: session context 2026-10-29\n", "source: session: context\n")
    s_base = (
        "---\n"
        "schema: odin-learning/v1\n"
        "record_kind: solution\n"
        "date: 2026-10-01\n"
        "title: 'Fix: restore the build graph'\n"
        "category: build-errors\n"
        "module: build\n"
        "problem_type: build_error\n"
        "component: build-graph\n"
        "severity: high\n"
        "symptoms:\n"
        "  - build fails on clean checkout\n"
        "root_cause: config_error\n"
        "resolution_type: config_change\n"
        "---\n"
        "Body.\n"
    )
    s_unquoted_title = s_base.replace(
        "title: 'Fix: restore the build graph'\n",
        "title: Fix: restore the build graph\n")
    s_missing_bug_fields = (
        "---\n"
        "schema: odin-learning/v1\n"
        "record_kind: solution\n"
        "date: 2026-10-01\n"
        "title: Broken build\n"
        "category: build-errors\n"
        "module: build\n"
        "problem_type: build_error\n"
        "component: build-graph\n"
        "severity: high\n"
        "---\n"
        "Body.\n"
    )
    s_category_mismatch = s_base.replace(
        "category: build-errors\n", "category: test-failures\n")
    r_origin_no_historical = (
        "---\n"
        "schema: odin-learning/v1\n"
        "record_kind: rationale\n"
        "date: 2026-10-01\n"
        "type: lesson\n"
        "confidence: medium\n"
        "source: session context 2026-10-29\n"
        "origin_records:\n"
        "  - path: docs/solutions/old-a.md\n"
        "    sha256: " + a64 + "\n"
        "    migration_origin: legacy-compound-v0\n"
        "---\n"
        "Body.\n"
    )
    r_origin_duplicate = (
        "---\n"
        "schema: odin-learning/v1\n"
        "record_kind: rationale\n"
        "date: 2026-10-01\n"
        "type: lesson\n"
        "confidence: medium\n"
        "source: session context 2026-10-29\n"
        "origin_records:\n"
        "  - path: docs/solutions/old-a.md\n"
        "    sha256: " + a64 + "\n"
        "    migration_origin: legacy-compound-v0\n"
        "    historical: true\n"
        "  - path: docs/solutions/old-a.md\n"
        "    sha256: " + a64 + "\n"
        "    migration_origin: legacy-compound-v0\n"
        "    historical: true\n"
        "---\n"
        "Body.\n"
    )
    return [
        ("valid rationale with plain and block-list scalars", r_base, True),
        ("valid rationale with nested origin_records list", r_origin_two, True),
        ("valid rationale with quoted and flow-list scalars", r_flow_tags, True),
        ("valid solution with quoted title", s_base, True),
        ("unquoted colon-space scalar is rejected", s_unquoted_title, False),
        ("unquoted colon-space source is rejected", r_unquoted_colon, False),
        ("block scalar is rejected fail-closed", r_block_scalar, False),
        ("unknown solution-only key on rationale is rejected", r_unknown_key, False),
        ("enum mismatch is rejected", r_bad_enum, False),
        ("missing required field is rejected", r_missing_source, False),
        ("bug track missing bug fields is rejected", s_missing_bug_fields, False),
        ("category and problem_type mismatch is rejected", s_category_mismatch, False),
        ("origin item missing historical is rejected", r_origin_no_historical, False),
        ("duplicate origin tuple is rejected", r_origin_duplicate, False),
        ("non-ISO date is rejected", r_bad_date, False),
        ("JSON object without delimiters is rejected",
         '{"schema": "odin-learning/v1"}\n', False),
    ]


def run_self_test():
    skill_dir = Path(__file__).resolve().parent.parent
    schema_path = skill_dir / "references" / "schema.md"
    cfg, schema_errs = _load_machine(str(schema_path))
    if cfg is None:
        sys.stdout.write("self-test: schema load failed\n")
        for e in schema_errs:
            sys.stdout.write("  %s\n" % e)
        return EXIT_USAGE
    missing = _need_keys(cfg)
    if missing:
        sys.stdout.write("self-test: schema machine block is missing keys\n")
        return EXIT_USAGE
    cases = _self_cases()
    passed = 0
    failed = []
    for name, doc, expect in cases:
        numbered, ferr = _extract_frontmatter(doc)
        if ferr is not None:
            got = False
        else:
            data, perrs = _parse_mapping(numbered)
            if perrs:
                got = False
            else:
                got = (_validate(data, cfg, "<self-test>") == [])
        if got == expect:
            passed += 1
        else:
            failed.append(name)
    total = len(cases)
    sys.stdout.write("self-test: %d/%d passed\n" % (passed, total))
    for name in failed:
        sys.stdout.write("  FAIL: %s\n" % name)
    return EXIT_OK if not failed else EXIT_INVALID


def main(argv):
    if "--self-test" in argv:
        return run_self_test()
    if len(argv) != 2:
        sys.stderr.write("validate-record: usage: %s <doc-path>\n" % os.path.basename(argv[0]))
        return EXIT_USAGE
    doc_path = argv[1]
    if not os.path.isfile(doc_path):
        sys.stderr.write("validate-record: file not found: %s\n" % doc_path)
        return EXIT_USAGE
    skill_dir = Path(__file__).resolve().parent.parent
    schema_path = skill_dir / "references" / "schema.md"
    cfg, schema_errs = _load_machine(str(schema_path))
    if cfg is None:
        sys.stderr.write("FAIL: %s\n" % doc_path)
        for e in schema_errs:
            sys.stderr.write("  %s\n" % e)
        return EXIT_USAGE
    missing = _need_keys(cfg)
    if missing:
        sys.stderr.write("FAIL: %s\n" % doc_path)
        sys.stderr.write("  schema machine block is missing keys\n")
        return EXIT_USAGE
    try:
        text = Path(doc_path).read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write("FAIL: %s\n  cannot read file: %s\n" % (doc_path, exc))
        return EXIT_INVALID
    numbered, ferr = _extract_frontmatter(text)
    if ferr is not None:
        sys.stderr.write("FAIL: %s\n" % doc_path)
        sys.stderr.write("  %s\n" % ferr)
        return EXIT_INVALID
    data, parse_errs = _parse_mapping(numbered)
    if parse_errs:
        sys.stderr.write("FAIL: %s\n" % doc_path)
        for e in parse_errs:
            sys.stderr.write("  %s\n" % e)
        return EXIT_INVALID
    problems = _validate(data, cfg, doc_path)
    if problems:
        sys.stderr.write("FAIL: %s\n" % doc_path)
        for e in problems:
            sys.stderr.write("  %s\n" % e)
        return EXIT_INVALID
    sys.stdout.write("OK: %s\n" % doc_path)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv))
