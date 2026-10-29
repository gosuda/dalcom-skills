---
name: autolearn
description: 'Use when a verified non-trivial fix lands or existing solution docs need refresh. Not for unverified fixes, retrospective analysis, or remote migration.'
---

# Autolearn

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A non-trivial fix is verified (observed working, not hoped working), an abandoned attempt finished with a useful anti-pattern, or explicit refresh invocation. |
| Authority | Reversible local only: writes the operating repo's `docs/solutions/` and repo-root `CONCEPTS.md`; rollback is version control. No remote, publish, deploy, credential, or paid mutation. Schema conversion grants no commit or push authority. |
| Side effect | Writes or refreshes solution docs and vocabulary entries; stages only surfaces this skill wrote or edited. |
| Done | One validated technical learning exists, existing docs are classified and acted on, or an explicit determination that nothing qualifies. |

## Inputs

- The verified fix or solved problem from conversation history or the codebase (required for capture; must be supplied or derivable).
- Optional scope for refresh: subdirectory, frontmatter match, filename partial, or content keyword.
- Memory provenance: any injected auto-memory block is supplementary context, never primary evidence. Tag memory-derived lines that land in a doc with `(auto memory [claude])`. When memory conflicts with code or conversation, prefer code or conversation.
- Explicit approval for writes in headless runs (`consent:write`); explicit approval for cross-branch consolidation (`consent:cross-branch`).

The skill directory resolves from this skill's own directory: `references/schema.md`, `references/concepts.md`, `scripts/validate-record.py`, `assets/solution-template.md`. Never invoke a peer skill at runtime for these contracts.

## Procedure

### 0. Route the mode

Strip `mode:` and `consent:` tokens before treating the remainder as context or scope. Accepted tokens: `mode:refresh [scope]`, `mode:headless`, `consent:write`, `consent:cross-branch`. Unknown or repeated tokens are errors.

- Capture (default): document one solved technical problem.
- Vocabulary capture: a durable reusable project term surfaces; reconcile `CONCEPTS.md`.
- Memory handoff: a fact about the user, preferences, or cross-project context surfaces; do not write it into `docs/solutions/` or `CONCEPTS.md`; surface it as a handoff candidate for the memory system.
- Refresh: maintain existing docs and vocabulary (see Refresh below).
- Headless: overlays any mode; skip questions, never pause, apply safe actions, mark genuinely uncertain docs `stale`.

Trigger phrases ("that worked", "it is fixed", "tests pass now") permit evaluation, never fabrication. One run may write a learning doc, reconcile a concept, and flag a handoff candidate.

Done when: the mode is routed and control tokens are stripped.

### 1. Reject-by-default gate

Verify all three preconditions:

1. The problem is solved, not in progress. A finished abandoned attempt counts: its learning is the anti-pattern, the specific failure reason, and when retrying would make sense.
2. The solution is verified: observed working.
3. It was non-trivial: not a typo or obvious one-liner.

Then apply all three filters in order: would this be forgotten without a record; is it already covered (updating beats duplicating); is the claim scope-qualified (repo-specific versus general). The same gate governs vocabulary: precise local meaning, not already defined, scope-qualified to this project.

Nothing clears the gate: say so in one line and exit. That is a valid result.

Done when: preconditions and filters are evaluated with a pass or a one-line exit.

### 2. Capture research (parallel, read-only)

Scan any injected memory block for related entries and carry matches as labeled supplementary context. Then dispatch three read-only researchers that write nothing:

1. Context Analyzer: pick the track (bug versus knowledge), `problem_type`, category directory, and slug filename (`[sanitized-problem-slug].md`, no date suffix). Return a frontmatter skeleton with no invented enums.
2. Solution Extractor: extract the substance (bug: Problem, Symptoms, What Did Not Work, Solution with code, Why This Works, Prevention; knowledge: Context, Guidance, Why This Matters, When To Apply, Examples).
3. Related-Docs Finder: grep `docs/solutions/` frontmatter on keywords, read frontmatter of candidates, fully read strong matches only. Score overlap across problem, cause, solution, references, and prevention: High (4-5), Moderate (2-3), Low (0-1).

Without subagents, run the same pass inline and record the degraded coverage. Wait for all three before assembling.

Done when: all three return and their results are assembled.

### 3. Capture: assemble and write

1. Overlap gate: High goes to updating the existing doc (keep path, add `last_updated`); Moderate creates normally and notes a consolidation candidate; Low creates normally.
2. Read `assets/solution-template.md` and assemble the doc with the track's section structure. Read rationale records for overlap only; never rewrite one to the solution schema.
3. Frontmatter per the local `references/schema.md`; quote values the validator requires quoted.
4. Write `docs/solutions/<category>/<slug>.md` (category from the schema map).
5. Validate from the skill directory:

```bash
python3 scripts/validate-record.py docs/solutions/<category>/<slug>.md
```

Quote, rewrite, and re-run until exit 0. A non-zero exit blocks the write.
6. Read the file back to confirm it landed as intended.
7. When a durable term surfaced that clears the gate, reconcile `CONCEPTS.md` per the local concepts contract.

Done when: the validator exits 0 on the written file and the file has been read back.

### 4. Refresh check (selective)

Recommend a narrow refresh only when the new fix contradicts or supersedes an older doc, the work invalidated references (refactor, migration, rename, dependency bump), or the finder surfaced strong candidates. Otherwise capture first and skip refresh explicitly.

Done when: a refresh recommendation is made or explicitly skipped.

### 5. Vocabulary capture

`CONCEPTS.md` at the operating repo root is the shared glossary with `compound` as its co-writer. Follow the bundled concepts contract: locate or create only when a term clears the gate, search before adding, add one well-shaped entry, read back to confirm no duplicate heading. Never scaffold an empty file.

Done when: the term is reconciled or no term clears the gate.

### 6. Refresh: maintain existing docs

Scope: every `.md` under `docs/solutions/`, excluding `README.md`. A `[scope]` hint narrows in order: subdirectory name, frontmatter `module`/`component`/`tags` match, filename partial, content keyword. No match reports the miss and exits.

Classify every candidate into exactly one outcome:

| Outcome | When | Action |
|---|---|---|
| Keep | Still accurate and useful | No edit; say why it stays trustworthy. |
| Update | Core solution correct, references drifted | Evidence-backed in-place edits. |
| Consolidate | Two or more docs overlap heavily, all correct | Merge unique content into the canonical doc, repoint references, delete the subsumed doc only with explicit authority. |
| Replace | Old guidance misleads, better answer known | Write a validated successor, then delete the old file. |
| Delete | Domain gone, fully redundant, inbound references absent or decorative | Delete only with explicit authority; never archive into `_archived/`. |

Rules: evidence over scorecards; prefer no-write Keep; match docs to reality; no low-value churn (typo or polish-only edits are not refreshes); age alone is never stale; rewriting the Solution section is Replace, not Update. Before Delete, grep repo markdown for citations: decorative citations may be cleaned, substantive citations force Replace, unclear citations force a stale mark.

Consolidation requires identical `record_kind` values (rationale with rationale, solution with solution). Preserve every input's `origin_records` as the ordered union; never drop an input tuple. Cross-branch conversion needs `consent:cross-branch` plus a complete lossless field and body mapping; without both, leave both inputs unchanged and report that cross-branch consolidation is blocked.

After every write, update, consolidation, or replacement, run the bundled validator until exit 0 and read the file back. Preserve `origin_records` unchanged on refresh edits.

Headless: attempt safe actions, mark genuinely uncertain docs `status: stale` with `stale_reason` and `stale_date`, record failed writes as Recommended rather than retrying into a mess. Emit Applied versus Recommended sections plus per-file path, classification, evidence, and action.

Done when: every in-scope doc is classified and acted on, and the refresh report is emitted.

### 7. Canonical migration

Migration is explicit and approved, never incidental. Bind the exact source set, destinations, and window first. Classify each source per `references/schema.md` (canonical, `legacy-autolearn-v0`, `legacy-compound-v0`, explicitly scoped `legacy-keep-why-v0`, `unmigrated`, `ahead-blocked`). Convert autolearn shapes to `record_kind: solution` and compound shapes to `record_kind: rationale`; never force either branch's fields onto the other. Preserve dates (missing or invalid dates stay `unmigrated`), preserve tags and body meaning, move legacy body detail into body sections, and attach complete `origin_records` digested from original bytes. All-or-nothing per set: any `unmigrated` source leaves the whole set unchanged. Only named files are in scope; undiscovered external stores are reported, never read or migrated. The pre-migration commit is the restore point; without version control, block rather than inventing a backup store. Publish atomically; on failure restore every touched file.

Done when: every destination validates and provenance is complete, or the set returns `unmigrated`/`deferred` with sources unchanged.

### 8. Commit

One learning per commit. Stage only surfaces this skill wrote or edited. Never stage unrelated dirty files. Commit locally by the operating repo's flow; skip when nothing changed. Never push: publication needs a separate explicit authority.

Done when: the commit exists with only this skill's surfaces staged, or is skipped as empty.

## Failure and recovery

- Nothing qualifies: one-line exit; valid, not a failure.
- Validation failure: quote the named field, rewrite, re-run until exit 0; never declare success while failing.
- Overlap collision: High overlap updates the existing doc; duplicating is drift.
- Insufficient evidence for Replace: mark `stale` in place rather than guessing a successor.
- Late-discovered substantive citation: reclassify off Delete.
- Partial refresh failure: record as Recommended, do not retry into a mess.
- Rollback: revert the local commit or restore the file from history; all writes stay under version control.

## Output

One validated learning doc at `docs/solutions/<category>/<slug>.md` (or an updated doc), optionally a `CONCEPTS.md` entry and a handoff candidate, or a one-line qualification failure. In refresh mode, a report classifying every scanned doc into Keep, Update, Consolidate, Replace, Delete, or stale with applied and recommended actions.

## Sources

Extends the prior `odin-knowledge` autolearn procedure (evaluation gate, three read-only researchers, overlap discipline, Bug and Knowledge tracks, refresh loop, memory provenance and handoff, local commits) onto the canonical `odin-learning/v1` union owned by `compound`. Retrospective analysis is owned by `retro`; this skill keeps durable technical capture only. No STRATEGY.md prerequisite is retained. Upstream MIT attributions remain in `licenses/NOTICE`.
