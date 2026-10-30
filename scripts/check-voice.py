#!/usr/bin/env python3
"""Enforce voice invariants over authored prose and external carriers.

Invariants:
- Bold runs: >= 2 consecutive labels or >= 5 consecutive lead-ins trip the gate.
- Dashes: >= 5 em/en dashes within a 600-character window trip the gate.
- Headings: title-cased minor words past position one trip the gate.
- Banned vocabulary: AI-marker words outside exempt ban-list subjects trip the gate.
- Quotes: curly quotes in prose trip the gate.
- Scope: gate git-tracked markdown files excluding vendored assets, plus harness carriers.
"""

import contextlib
import io
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from carriers import CARRIERS

BANNED = re.compile(
    r"\b(delve[sd]?|delving"
    r"|leverages|leveraging|leverage(?=\s+(?:the|a|an|this|that|these|those|our|your|its|their|existing)\b)"
    r"|seamless(?:ly)?"
    r"|underscores|underscoring|underscored"
    r"|holistic(?:ally)?"
    r"|synerg(?:y|ies|istic))\b",
    re.I,
)

BAN_LIST_SUBJECTS = frozenset(
    {
        "docs/specs/voice.md",
        "plugins/odin-writing/skills/copywriting/SKILL.md",
        "plugins/odin-writing/skills/copywriting-prose-creator/SKILL.md",
    }
)
BOLD_LABEL = re.compile(
    r"^\s*(?:[-*+]\s*)?\*\*"
    r"(?:[^*\n]{2,}\*\*[^*\n]*:"
    r"|[^*\n]{2,}:\s*\*\*)"
)
MINOR_WORD = re.compile(
    r"^#{2,6} \S+ .*\b(?:The|A|An|Of|And|For|To|In|On|With|From|Is|Are|But|Or|As|At|By)\s+[A-Z]"
)
CURLY = re.compile(r"[\u2018\u2019\u201c\u201d]")
DASH = re.compile(r"[\u2014\u2013]")

DASH_WINDOW = 600
DASH_RUN = 5
BOLD_RUN = 2
BOLD_LEAD = re.compile(r"^\s*(?:[-*+]\s*)?\*\*[^*\n]{2,}\*\*")
BOLD_LEAD_RUN = 5


def writable(path):
    """Return True if path can be opened for writing, False otherwise."""
    try:
        os.close(os.open(path, os.O_WRONLY))
    except OSError:
        return False
    return True


def git_tracked(pathspecs):
    """Repository-relative paths tracked by the git index matching pathspecs."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", *pathspecs],
            cwd=ROOT, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        sys.exit("check-voice: git is not installed, and the gate's scope comes from the index. "
                 "Refusing to fall back to a directory walk, which would silently change scope.")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"check-voice: git cannot report the tracked files for {ROOT} "
                 f"({exc.stderr.strip().rstrip('.')}). This path is not a work tree, or its index "
                 "is unreadable. Refusing to fall back to a directory walk, which would silently "
                 "change scope.")
    return [path for path in result.stdout.split("\0") if path]


def carrier_targets(carriers):
    """Filter carriers to present files; abort if an unwritable carrier has findings."""
    present = []
    for carrier in carriers:
        if not carrier.is_file():
            print(f"check-voice: skipping {carrier} (absent on this machine)", file=sys.stderr)
            continue
        if not writable(carrier):
            blocking = audit(carrier)
            if blocking:
                sys.exit(f"check-voice: {carrier} cannot be written and carries "
                         f"{len(blocking)} finding(s); repair its permissions or remove it, "
                         "because they cannot be fixed here")
        present.append(carrier)
    return present


_FATE = "plugins/odin-core/skills/let-fate-decide"


def _fate_vendored():
    """Pinned upstream inventory loaded from the fate skill's draw script."""
    draw_module = runpy.run_path(str(ROOT / _FATE / "scripts" / "draw.py"), run_name="draw")
    return frozenset(f"{_FATE}/{rel}" for rel in draw_module["expected_asset_files"]())


VENDORED_UPSTREAM = _fate_vendored()


def repo_targets():
    """Every tracked markdown file, minus verbatim upstream."""
    return sorted(ROOT / path for path in git_tracked(["*.md"])
                  if path not in VENDORED_UPSTREAM)


def default_targets(carriers=CARRIERS):
    """Every tracked markdown file plus harness carriers, minus verbatim upstream."""
    return repo_targets() + carrier_targets(carriers)


def prose_only(text):
    """Drop fenced blocks and inline spans, preserving line count for accurate reporting."""
    out = []
    fenced = False
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else re.sub(r"`[^`\n]*`", "", line))
    return "\n".join(out)


def dash_run(prose):
    """Longest dash run inside one window, with the line it starts on."""
    hits = [m.start() for m in DASH.finditer(prose)]
    worst = 0
    where = 0
    for i, start in enumerate(hits):
        j = i
        while j < len(hits) and hits[j] - start <= DASH_WINDOW:
            j += 1
        if j - i > worst:
            worst = j - i
            where = prose.count("\n", 0, start) + 1
    return worst, where


def bold_runs(prose):
    """Maximal runs of lines opening with a bold span, as (first line, length, label count)."""
    runs = []
    start = 0
    length = 0
    labels = 0
    for number, line in enumerate(prose.split("\n"), start=1):
        if BOLD_LEAD.match(line):
            if length == 0:
                start = number
            length += 1
            labels += bool(BOLD_LABEL.match(line))
        elif line.strip():
            if length:
                runs.append((start, length, labels))
                length = 0
                labels = 0
    if length:
        runs.append((start, length, labels))
    return runs


def classify_run(labels):
    """Classify a run: ('label', BOLD_RUN) if labels >= 2 else ('lead', BOLD_LEAD_RUN)."""
    if labels >= 2:
        return "label", BOLD_RUN
    return "lead", BOLD_LEAD_RUN


def bold_findings(prose):
    """One finding per tripping bold run, reported at the run's first line."""
    found = []
    for start, length, labels in bold_runs(prose):
        kind, threshold = classify_run(labels)
        if length < threshold:
            continue
        if kind == "label":
            found.append((start, f"{length} consecutive bold lines, {labels} with labels; "
                                 "use a list or table"))
        else:
            found.append((start, f"{length} consecutive bold lead-ins; "
                                 "use a list, a table, or plain text"))
    return found


def label(path):
    """Repository-relative path when inside the tree, absolute otherwise."""
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def audit(path):
    prose = prose_only(path.read_text(encoding="utf-8", errors="replace"))
    rel = label(path)
    found = []

    for line, message in bold_findings(prose):
        found.append(f"{rel}:{line}: {message}")

    worst, line = dash_run(prose)
    if worst >= DASH_RUN:
        found.append(f"{rel}:{line}: {worst} dashes within {DASH_WINDOW} characters")

    for number, line_text in enumerate(prose.split("\n"), start=1):
        if MINOR_WORD.match(line_text):
            found.append(f"{rel}:{number}: title-case heading; use sentence case")

    if str(rel) not in BAN_LIST_SUBJECTS:
        for match in BANNED.finditer(prose):
            line = prose.count("\n", 0, match.start()) + 1
            found.append(f"{rel}:{line}: AI-marker word '{match.group(0)}'")

    for match in CURLY.finditer(prose):
        line = prose.count("\n", 0, match.start()) + 1
        found.append(f"{rel}:{line}: curly quote; use a straight quote")

    return found


L1 = "**Latency** is the first thing to measure.\n"
L2 = "**Throughput** follows from it.\n"
L3 = "**Allocation** decides both.\n"
L4 = "**Locality** then sets the ceiling.\n"
L5 = "**Occupancy** is what is left to tune.\n"
D1 = "**Discipline (defend at boundaries, trust interior, fail fast; ban slop, keep craft):**\n"
D2 = "**Security (OWASP Top 10:2025, CWE Top 25 2025):**\n"
S1 = "**Scope**: what this covers.\n"
S2 = "**Response language:** All English.\n"

SELF_TEST = (
    ("colon-bearing label with an internal colon is caught", D1 + D2, (True, "label")),
    ("colon-bearing label without an internal colon is caught", S1 + S2, (True, "label")),
    ("mid-sentence emphasis is not caught",
     "You **MUST** use the gate, and you **SHOULD NOT** skip it.\n"
     "This line carries **bold emphasis** but no label colon.\n", (False, None)),
    ("bold label inside a fenced block is not caught", "```\n" + D1 + D2 + "```\n", (False, None)),
    ("run of five colon-less lead-ins is caught", L1 + L2 + L3 + L4 + L5, (True, "lead")),
    ("run of four colon-less lead-ins is not caught", L1 + L2 + L3 + L4, (False, None)),
    ("blank lines do not break a lead run",
     "\n".join((L1, L2, L3, L4, L5)) + "\n", (True, "lead")),
    ("lead-ins inside a fenced block are not caught", "```\n" + L1 + L2 + L3 + L4 + L5 + "```\n",
     (False, None)),
    ("mid-sentence emphasis is not caught at any density",
     "Measure **latency** before anything else.\nThen weigh **throughput** against it.\n"
     "Watch **allocation**, which decides both.\nMind **locality**, which sets the ceiling.\n"
     "Tune **occupancy** last, if at all.\nReport **variance**, never a single run.\n",
     (False, None)),
    ("alternating label and lead run of five is caught",
     S1 + L1 + S2 + L2 + "**Allocation:** decides both.\n", (True, "label")),
    ("one label plus four leads is caught as a lead run",
     S1 + L1 + L2 + L3 + L4, (True, "lead")),
    ("two labels plus one lead is caught at the label threshold",
     S1 + S2 + L1, (True, "label")),
    ("one label plus three leads is not caught", S1 + L1 + L2 + L3, (False, None)),
    ("bulleted colon-bearing labels are caught", "- **Scope:** a.\n- **Domain:** b.\n",
     (True, "label")),
    ("bulleted plain labels are not caught", "- Scope: a.\n- Domain: b.\n", (False, None)),
    ("run of five over-long lead-ins is caught",
     "".join(f"**{w} {'padding ' * 18}** opens a long line {i}.\n"
             for i, w in enumerate(("Latency", "Throughput", "Allocation", "Locality",
                                    "Occupancy"))),
     (True, "lead")),
    ("two over-long colon-bearing labels are caught as a label run",
     "".join(f"**{w} {'padding ' * 18}:** value {i}.\n" for i, w in enumerate(("Scope", "Domain"))),
     (True, "label")),
)


def run_verdict(prose):
    """(caught, kind) for the first bold run that trips its threshold."""
    for _, length, labels in bold_runs(prose):
        kind, threshold = classify_run(labels)
        if length >= threshold:
            return True, kind
    return False, None


def ignored_witness():
    """An ignored file that exists in the tree, or None on a clean clone."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--others", "--ignored", "--exclude-standard"],
        cwd=ROOT, capture_output=True, text=True, check=True)
    found = [p for p in result.stdout.split("\0") if p and (ROOT / p).is_file()]
    for path in found:
        if not path.startswith((".git/", ".outline/")):
            return path
    return found[0] if found else None


def ignored_case(got):
    """Invariant: git index returns nothing for an existing ignored path."""
    witness = ignored_witness()
    return got == [] and (witness is None or Path(witness).is_file())


def carrier_witness_probe():
    """Controlled carrier inputs: present carrier is targeted, absent is skipped."""
    dir_ = tempfile.mkdtemp()
    try:
        present = Path(dir_) / "present.md"
        present.write_text("Controlled carrier prose.\n", encoding="utf-8")
        absent = Path(dir_) / "absent.md"
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            targets = [str(c) for c in carrier_targets([present, absent])]
        return targets, str(present), str(absent), buf.getvalue()
    finally:
        shutil.rmtree(dir_, ignore_errors=True)


def carrier_witness_case(probe):
    targets, present, absent, notice = probe
    return (present in targets and absent not in targets
            and "skipping" in notice and "absent on this machine" in notice)


def untracked_witness_probe():
    """Probe that untracked, non-ignored markdown files in the tree are not targeted."""
    without = len(repo_targets())
    dir_ = tempfile.mkdtemp(dir=ROOT)
    try:
        witness = Path(dir_) / "witness.md"
        witness.write_text("**Scope:** a.\n**Domain:** b.\n", encoding="utf-8")
        targets = repo_targets()
        return (witness in targets, len(targets), without, bool(audit(witness)))
    finally:
        shutil.rmtree(dir_, ignore_errors=True)


def untracked_witness_case(probe):
    picked_up, with_count, without_count, carries = probe
    return not picked_up and with_count == without_count and carries


def vendored_case(got):
    """Invariant: all 92 vendored paths are tracked by git but excluded from repository targets."""
    tracked = set(git_tracked(sorted(VENDORED_UPSTREAM)))
    return (tracked == set(VENDORED_UPSTREAM)
            and not any(str(ROOT / path) in got for path in VENDORED_UPSTREAM))


def authored_sibling_case(got):
    """Invariant: fate skill authored siblings remain repository targets."""
    siblings = (f"{_FATE}/SKILL.md",
                f"{_FATE}/agents/draw.md",
                f"{_FATE}/references/SOURCE-MAP.md")
    return all(str(ROOT / path) in got for path in siblings)


def scope_parity_case(got):
    """Invariant: target set equals tracked markdown files minus VENDORED_UPSTREAM."""
    expected = {str(ROOT / path) for path in git_tracked(["*.md"])
                if path not in VENDORED_UPSTREAM}
    return set(got) == expected


TARGET_CASES = (
    ("a tracked markdown file is a target",
     lambda: git_tracked(["AGENTS.md"]),
     lambda got: "AGENTS.md" in got),
    ("a path that exists but is not tracked is not a target",
     lambda: git_tracked(["AGENTS.md", ".git"]),
     lambda got: Path(".git").exists() and ".git" not in got),
    ("an ignored file inside the repository is not a target",
     lambda: git_tracked([ignored_witness() or ".outline/whatever.md"]),
     ignored_case),
    ("harness carriers are targets when present and skipped when absent",
     carrier_witness_probe,
     carrier_witness_case),
    ("an untracked non-ignored markdown file is not a target",
     untracked_witness_probe,
     untracked_witness_case),
    ("the verbatim-upstream inventory holds exactly 92 paths",
     lambda: list(VENDORED_UPSTREAM),
     lambda got: len(got) == 92),
    ("vendored fate assets are tracked but not repository targets",
     lambda: [str(p) for p in repo_targets()],
     vendored_case),
    ("authored fate siblings stay repository targets",
     lambda: [str(p) for p in repo_targets()],
     authored_sibling_case),
    ("every other tracked markdown file stays a repository target",
     lambda: [str(p) for p in repo_targets()],
     scope_parity_case),
    ("explicit file arguments still gate a vendored path",
     lambda: [str(p) for p in explicit_targets([sorted(VENDORED_UPSTREAM)[0]])],
     lambda got: len(got) == 1 and got[0].endswith(sorted(VENDORED_UPSTREAM)[0])),
)


def self_test():
    """Run every bold and scope case against the compiled rule; return the exit code."""
    failed = 0
    for name, text, (want_caught, want_kind) in SELF_TEST:
        caught, kind = run_verdict(prose_only(text))
        ok = caught == want_caught and (not caught or kind == want_kind)
        failed += not ok
        detail = f"kind={kind}" if caught else "not caught"
        want = f"{want_kind} at its threshold" if want_caught else "clean"
        print(f"{'PASS' if ok else 'FAIL'}: {name} ({detail}, expected {want})")
    for name, select, holds in TARGET_CASES:
        got = select()
        ok = holds(got)
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}: {name} ({len(got)} path(s) selected)")
    total = len(SELF_TEST) + len(TARGET_CASES)
    print(f"check-voice self-test: {total - failed}/{total} passed",
          file=sys.stderr if failed else sys.stdout)
    return 1 if failed else 0


def explicit_targets(argv):
    """Explicit file arguments gate whatever they name, including a vendored path."""
    return [Path(a).resolve() for a in argv]


def main(argv):
    if argv == ["--self-test"]:
        return self_test()
    if argv:
        targets = explicit_targets(argv)
    else:
        targets = default_targets()

    findings = []
    checked = 0
    for path in targets:
        if not path.is_file():
            continue
        checked += 1
        findings.extend(audit(path))

    if findings:
        for finding in findings:
            print(finding, file=sys.stderr)
        print(f"check-voice: {len(findings)} finding(s) across {checked} file(s)", file=sys.stderr)
        return 1

    print(f"voice ok {checked} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
