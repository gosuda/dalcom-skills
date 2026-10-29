---
name: simplify
description: 'Use when the user asks to simplify a diff, branch, or change-set and wants structure the change introduced or affected challenged. Not for named-module redesign: use code-simplification. Not for architecture overhaul: use architecture-simplification. Not for mechanical debris: use deslop.'
---

# Simplify: aggressive diff-local structural compression

Anchors: Dieter Rams (every remaining element earns its place), David Parnas (a module hides decisions behind its contract; caller migration is part of the work).

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to simplify a diff, PR, or branch: "simplify this diff", "tighten this PR", "challenge what this change introduced or touched". |
| Authority | Reversible local: writes the working change-set plus proven in-tree callers the diff forces, as atomic commits; rollback is version control (`git revert`). No remote mutation. Structural work beyond the forced set is emitted as a candidate, not applied. |
| Side effect | Validated survivors landed as one atomic commit per issue class; any regressing commit auto-reverted; structural candidates beyond the diff reported with file, line, and reason. |
| Done | Survivors landed green with no shim, alias, or removed-surface reference left, the post-fix audit is clean, and every out-of-scope structural finding is emitted as a candidate rather than silently dropped or force-applied. Line delta is reported evidence only, never the predicate. |

Surgical added-lines-only polish (`simplify --surgical`, "added lines only", "no caller moves") is explicit opt-in only. Without those words the aggressive default below applies.

## Inputs

Must be supplied:

- An explicit diff scope or a base resolvable from explicit, pull-request, upstream, or remote-default evidence.

Optional:

- User-named files when no git context exists (unborn HEAD or no `.git/`), or to authorize untracked files into scope.
- The literal opt-in `surgical` (or equivalent "added-lines-only" wording).

Derived from the change-set:

- One worker by default with no second agent dispatched; three parallel read-only review agents (reuse-affected / structure-affected / efficiency-affected) plus one Reviewer only when the change-set contains genuinely independent scopes. Hunk count is never the gate.

## Procedure

1. **Resolve the base from evidence, never by guessing.** Apply in order:
   - Explicit override: `simplify against <ref>` bypasses everything below and runs `git --no-pager diff "<ref>"` directly, where `<ref>` is any revision spec git accepts (`HEAD~5`, a SHA, a branch name, a tag).
   - Pull-request evidence: when the branch has an open pull request with a determinable base branch, resolve the base from that PR evidence (the base branch the branch was opened against) and diff against `git merge-base HEAD <pr-base>`.
   - Upstream evidence: when `@{upstream}` resolves (for example via `git rev-parse --abbrev-ref --symbolic-full-name @{upstream}`), resolve the base from the upstream tracking branch and diff against `git merge-base HEAD @{upstream}`.
   - Remote-default evidence: when the remote advertises a default branch reference (for example `refs/remotes/origin/HEAD`), resolve from that evidence.
   - Otherwise stop and request an explicit base (`simplify against <ref>`). Never guess `main` or `master`, and never fall back to `git diff HEAD` on a branch with committed history but no resolved base; that would silently drop committed work. Unborn HEAD (Check A: `git rev-parse --verify HEAD 2>/dev/null` fails) means user-named files only. Root commit (Check A succeeds, Check B `git rev-parse --verify HEAD^ 2>/dev/null` fails) means the working tree with surface note "scope: working-tree only, on root commit". Empty after all valid resolutions means exit 11.

   **Untracked work.** Enumerate untracked entries (`git status --porcelain` `??`). Include untracked files the user authorized into scope (named files or an explicit full-sweep authorization) by reading them directly alongside the tracked diff. Never delete an untracked file. Meaningful unauthorized untracked files are reported as out-of-scope remaining work with paths, never silently ignored and never treated as a clean pass. Done when: the tracked base is resolved from evidence or an explicit base is requested, authorized untracked files are in scope, and every other meaningful untracked file is named as remaining work.

2. **Detect with the smallest sufficient force over the full default range.** Default detection range is added lines plus modified lines plus affected structure (proven in-tree callers the diff forces). Surgical range is added lines only. Default is a single worker that reads the whole default range. Dispatch three parallel read-only agents in one `task` call (a `tasks` array of three items, never three sequential messages) only when the change-set contains genuinely independent scopes (two or more disjoint file sets or independent concerns where reuse, structure, and efficiency review would not overlap and parallel review adds signal); hunk count never decides. Otherwise do not dispatch them. The old unconditional three-agent mandate is not followed. Each agent, when used, receives its axis prompt plus `"\n\n---\n\nDIFF:\n"` plus the captured diff. Every agent is `Explore`-typed, read-only, edits nothing, and shares no mutable state. The spawn message asserts independence: reuse-affected owns graft-to-existing-utility plus forced-caller migration, structure-affected owns shape compression over the default range, efficiency-affected owns unnecessary work and hot-path bloat over the default range. In default mode every axis ranges over added, modified, and affected structure, and any axis may migrate proven forced in-tree callers when its survivor cannot land clean without that migration; the reuse-affected axis is the primary migration carrier (inline the wrapper at every forced call site, then delete it). In surgical mode every axis collapses to added lines only, remove-only, and never migrates. Axes in default mode:
   - reuse-affected (migration-capable): REPLACE (new code where an identical-behavior utility exists, cited with path and line, including forced callers outside the hunks), DUPLICATE (same logic added twice in the change-set or split between the change-set and forced callers), INLINE-COULD-USE-UTILITY (new helper the existing utility already covers), STDLIB-REIMPLEMENT (new code the standard library or platform already provides).
   - structure-affected (migration-capable when forced): redundant nesting or conditionals, dead code or unused imports, and copy-paste variation over added, modified, and affected structure, behavior-preserving. Cross-module redesign and canonical-owner disputes are not survivors here; they route out at step 3.
   - efficiency-affected: unnecessary work, missed concurrency only where the surrounding code already uses it, hot-path bloat, recurring no-op updates, unnecessary existence checks, listener or handle leaks, and overly broad operations, all over added, modified, and affected structure.

   Done when: the worker findings, or all three agent findings when the independent-scope exception applies, have returned.

3. **Compose and adjudicate once, without spending a second agent on the single-worker path.** Single-worker path: the worker is the detector and the orchestrator is the adjudicator; no Reviewer agent is dispatched, so the one-worker accounting holds, but worker findings never land on the worker's say-so alone. Every finding must carry per-finding source-line proof before it lands: the exact file and line of the offending code, the diff hunk it belongs to, and for reuse-affected the path and line of the existing utility plus a one-line behavior-equivalence note, or for structure-affected and efficiency-affected the cited cause or cost in the actual code. The orchestrator lands only proof-complete findings (deduplicated by `{axis, file, line, issue-class}`); any finding without complete proof is dropped or routed as a candidate, never applied. Independent-scope path: merge findings by `{axis, file, line, issue-class}`, deduplicate structurally identical cross-axis reports (keep once, attribute to the first reporter, note the second axis as co-signer), then dispatch one read-only Reviewer agent with the composed list, the captured diff, and this four-check charter: completeness (every hunk and forced caller that warrants attention covered, systematic blind spots flagged), consistency (no two survivors contradict), accuracy (each finding cites the real code and the real existing utility or cost), scope (every finding is landable inside this authority). The Reviewer output is the validated survivor set for that path only. On either path, only findings beyond the forced set (named-module redesign, canonical-owner decision where two existing abstractions both claim to be canonical, architecture-level collapse) are not survivors, do not pass through adjudication, and are emitted directly as `code-simplification` or `architecture-simplification` candidates with file, line, and reason. A non-empty raw list with an empty survivor set is exit 12: report attached, no patch applied. Done when: a proof-gated or Reviewer-validated survivor set exists, or candidates plus exit 12 are reported.

4. **Apply survivors, one issue class per atomic commit.** Land survivors with the proven in-tree callers and their tests in the same commit. Production caller edits outside the diff hunks are authorized when they are proven in-tree callers the survivor forces (same atomic commit, same VCS rollback, no remote); callers beyond the forced set are never edited here and route out as candidates instead. Sequence: duplicate commit first (reuse-affected survivors plus any survivor flagged `issue-class: duplicate`), then excess-surface commit (structure-affected plus efficiency-affected survivors flagged `issue-class: excess-surface`), then structure commit (remaining structure-affected plus efficiency-affected structure survivors). A commit that would bundle more than one issue class is split before merge (exit 15). Commit messages use a capitalized imperative subject, 50 characters target and 72 hard, no trailing period. After each commit run the narrowest applicable verifier first (compiler or typechecker), then the repository's own test command (`just test` or `make test` target when present, else the ecosystem command such as `cargo test`, `pytest`, `npm test`, `dune runtest`, `go test ./...`). On red, auto-revert that commit via `git revert HEAD --no-edit`, stop that class, keep prior green commits (exit 13). Permitted test edits are mechanical migration to the new internal contract only (imports, call sites, fixture wiring, renamed symbols), each with a recorded reason. Forbidden: deleting, suppressing, skipping, or weakening tests or assertions to force green, and adding parser exceptions or duplicate-resolution logic to fit the cut. Test shrinkage of any other kind is a `tests-purge-unneeded` decision under its own mutation-proof contract, never taken here. Done when: every survivor class is landed green with its forced callers, or reverted with its failing check recorded.

5. **Audit the simplify patch itself, then sweep residue.** Audit the applied chain for unneeded surface, duplicated logic, structure without cause, or a broken consumer contract. Any hit reverts the entire simplify chain via `git revert <first-simplify-commit>^..HEAD --no-edit` and exits 14; the skill may re-plan and re-invoke once on the corrected understanding. Otherwise grep code, tests, docs, configs, error messages, and log lines for string references to every removed concept. Zero survivors, or the candidate is reclassified not-dead with its reason. Done when: the chain is green, the self-audit is clean, and residue search is empty. Authorized untracked files are re-read after the change; no untracked file is ever deleted by this audit.

## Failure and recovery

| Exit code | Trigger | Recovery |
|---|---|---|
| 0 | Clean | none |
| 11 | Empty tracked diff with no authorized files after all resolutions | Pass-through, no work to do; meaningful unauthorized untracked files are still reported as remaining work |
| 12 | Findings emitted but survivor set empty after audit | Report attached, no patch applied |
| 13 | Behavior regression on a fix commit | Offending commit auto-reverted; stop that class; already-landed green commits remain |
| 14 | Post-fix audit caught new bloat in the simplify patch | Entire simplify chain reverted; may re-plan and re-invoke |
| 15 | Mixed-concern commit (more than one issue class) | Split before merge |

Partial-result rule: commits landed green before a failure remain. A rollback never reverts previously successful class commits and never touches untracked files. When three agents are used, anything other than one `task` call with a three-item `tasks` array is rejected at the validation gate before any agent runs. A red baseline stops all cutting: report the failing tests first; never cut on unproven ground. If no verifier exists, every fix is unverified, the limitation is stated, and the done predicate is not claimed.

## Output

Terminal classification with an exit code. On exit 0: the change-set is compressed over added, modified, and affected structure with one atomic commit per issue class, every fix commit green, forced callers migrated where the survivor required it, no new bloat introduced, residue search empty, authorized untracked files integrated without deletion, unauthorized meaningful untracked files named as remaining work, and findings beyond the forced set emitted as `code-simplification` or `architecture-simplification` candidates with file, line, and reason. On any other exit: the attached report names the survivor set or candidate list, the failing check where applicable, authorized versus remaining untracked files, and the remaining work.
