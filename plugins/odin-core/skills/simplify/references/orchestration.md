# `simplify`: orchestration recipe

Detection force, composition rule, Reviewer audit contract for the independent-scope path, fix sequencing, and behavior gate for the `simplify` skill. Read alongside `../SKILL.md` steps 1 through 5; this file never overrides that contract.

## Phase 1: base resolution from evidence (shell intent)

Resolve the base in this order; never guess `main` or `master`:

1. **Explicit override**: `simplify against <ref>` bypasses everything below and runs `git --no-pager diff "<ref>"` directly, where `<ref>` is any revision spec git accepts (`HEAD~5`, a SHA, a branch name, a tag).
2. **Pull-request evidence**: when the branch has an open pull request with a determinable base branch, diff against `git merge-base HEAD <pr-base>`.
3. **Upstream evidence**: when `@{upstream}` resolves, diff against `git merge-base HEAD @{upstream}`.
4. **Remote-default evidence**: when the remote advertises a default branch reference (for example `refs/remotes/origin/HEAD`), resolve from that evidence.
5. Otherwise stop and request an explicit base (`simplify against <ref>`). Never fall back to `git diff HEAD` on a branch with committed history but no resolved base; that silently drops committed work.

Unborn HEAD (`git rev-parse --verify HEAD` fails) means user-named files only. Root commit (`HEAD` verifies but `HEAD^` does not) means the working tree is the scope; note `scope: working-tree only, on root commit`. Empty after all valid resolutions means exit 11.

**Untracked work.** Enumerate untracked entries (`git status --porcelain` `??`). Read authorized untracked files (user-named or explicit full-sweep authorization) alongside the tracked diff. Never delete an untracked file. Report meaningful unauthorized untracked files as out-of-scope remaining work with paths; never ignore them silently and never treat them as a clean pass.

## Phase 2: detection force (single worker default)

Default is a single worker over added lines plus modified lines plus affected structure (proven in-tree callers the diff forces). Dispatch three parallel read-only agents in one `task` call (a `tasks` array of three items, never three sequential messages) only when the change-set holds genuinely independent scopes (two or more disjoint file sets or independent concerns where reuse, structure, and efficiency review do not overlap). Hunk count never decides. Each used item receives its axis prompt plus the captured diff after the `DIFF:` marker.

Surgical range (`simplify --surgical`, `added lines only`, or `no caller moves`) is explicit opt-in only: every axis collapses to added lines, remove-only, and never migrates callers. In default mode every axis ranges over added, modified, and affected structure, and any axis may migrate proven forced in-tree callers when its survivor cannot land clean without that migration; the reuse-affected axis is the primary migration carrier.

Independence argument the orchestrator includes only when it dispatches the three-agent exception:

> "Three agents dispatched in parallel for independent scopes. Axes are disjoint for this run: reuse-affected owns graft to existing utility plus forced-caller migration, structure-affected owns shape compression over the default range, efficiency-affected owns unnecessary work and hot-path bloat over the default range. All three agents are read-only; none edits files; none reads or writes shared mutable state."

Agent type for each invocation: `Explore` (read-only).

## Phase 3: composition, audit, fix

### Composition

Single-worker path: the worker detects and the orchestrator adjudicates; no Reviewer agent runs. Every finding must carry per-finding source-line proof before it lands: the exact file and line of the offending code, the diff hunk it belongs to, and for reuse-affected the path and line of the existing utility plus a one-line behavior-equivalence note, or for structure-affected and efficiency-affected the cited cause or cost in the actual code. The orchestrator lands only proof-complete findings, deduplicated by `{axis, file, line, issue-class}`; a finding without complete proof is dropped or routed as a candidate, never applied.

Independent-scope path: merge findings by `{axis, file, line, issue-class}`. Tag each finding with its axis. When two axes report the same `{file, line}` with structurally identical patterns, deduplicate: keep the finding once, attribute to the first reporter, note the second axis as a co-signer. Then dispatch one Reviewer agent (also `Explore`-typed, read-only) with the composed list, the captured diff, and the four-check charter below.

### Reviewer audit (independent-scope path only)

Reviewer audit charter (four checks):
1. **Completeness**: did the three axes between them cover every hunk and forced caller that warrants attention? Flag systematic blind spots.
2. **Consistency**: do any findings contradict each other (for example `extract this into a helper` against `inline this helper`)? Flag and resolve.
3. **Accuracy**: for each finding, verify the citation against the real code and the real existing utility or cost. Discard findings whose `path:line` does not match the diff or whose `existing-utility` does not exist.
4. **Scope**: flag findings that cannot land inside this authority. Production caller edits outside the diff hunks are authorized only when they are proven in-tree callers the survivor forces; callers beyond the forced set are never edited here.

The Reviewer output is the **validated survivor set** for that path only. The orchestrator applies survivors and drops non-survivors; no re-litigation in either direction.

On either path, findings beyond the forced set (named-module redesign, canonical-owner decision where two existing abstractions both claim to be canonical, architecture-level collapse) are not survivors and are emitted directly as `code-simplification` or `architecture-simplification` candidates with file, line, and reason. Auto-apply covers only deterministic mechanical removals that cannot change behavior (dead prints, trailing whitespace, isolated commented-out blocks, unreachable placeholders); everything else is reported. Never edit flag-only material to force green: secrets and credentials, live-surface placeholders, crash-on-failure shortcuts, and any finding needing control-flow or architectural judgment.

If the survivor set is empty after a non-empty raw findings list, attach the report and apply no patch (exit 12).

### Fix sequencing

Group survivors by `issue-class`. Apply in this order, one atomic commit per class:

1. **Duplicate commit**: apply all reuse-affected survivors (and any other axis survivors flagged `issue-class: duplicate`), with the proven in-tree callers and their tests in the same commit.
2. **Excess-surface commit**: apply all structure-affected plus efficiency-affected survivors flagged `issue-class: excess-surface`, with the proven in-tree callers and their tests in the same commit.
3. **Structure commit**: apply all remaining structure-affected plus efficiency-affected structure survivors, with the proven in-tree callers and their tests in the same commit.

Commit message format uses a capitalized imperative subject, 50 characters target and 72 hard, no trailing period; recommended:

Remove <class> from <scope>, followed by 2-4 lines describing the survivors applied in this commit, citing file:line pairs.

A commit that would bundle survivors from more than one class is split before merge (exit 15).

## Behavior gate (after every commit)

After each fix commit, run the narrowest applicable verifier first (compiler or typechecker), then the repository test command (`just test` or `make test` target when present, else the ecosystem command such as `cargo test`, `pytest`, `npm test`, `dune runtest`, `go test ./...`). A red baseline stops all cutting: report the failing tests first and never cut on unproven ground. If no verifier exists, every fix is unverified, the limitation is stated, and the done predicate is not claimed. On red after a fix commit, revert that commit via `git revert HEAD --no-edit`, stop that class, and keep prior green commits (exit 13). Permitted test edits are mechanical migration to the new internal contract only (imports, call sites, fixture wiring, renamed symbols), each with a recorded reason. Forbidden: deleting, suppressing, skipping, or weakening tests or assertions to force green, and adding parser exceptions or duplicate-resolution logic to fit the cut. Other test shrinkage is a `tests-purge-unneeded` decision under its own contract, never taken here.

## Post-fix audit (no new bloat, no residue)

After the final commit, audit the simplify patch itself for unneeded surface, duplicated logic, structure without cause, or a broken consumer contract. Any hit reverts the entire simplify chain via `git revert <first-simplify-commit>^..HEAD --no-edit` and exits 14; the skill may re-plan and re-invoke once on the corrected understanding. Otherwise search code, tests, docs, configs, error messages, and log lines for string references to every removed concept. Zero survivors, or the candidate is reclassified not-dead with its reason. Re-read authorized untracked files after the change; never delete an untracked file.

## Exit code summary (matches SKILL.md)

| Code | Trigger |
|---|---|
| 0 | Survivors applied, behavior gate green, no new bloat, residue search empty |
| 11 | Empty tracked diff with no authorized files after all resolutions |
| 12 | Findings emitted but survivor set empty after audit; report attached, no patch applied |
| 13 | Behavior regression on a fix commit; offending commit auto-reverted, prior green commits remain |
| 14 | Post-fix audit caught new bloat in the simplify patch; entire chain reverted |
| 15 | Mixed-concern commit (more than one issue class); split before merge |
