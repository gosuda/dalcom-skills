---
name: resolve-merge-conflicts
description: 'Use when a merge, rebase, cherry-pick, or stash pop stops on conflicts. Not for people-mediation conflicts.'
---

# Resolve merge conflicts

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A merge, rebase, cherry-pick, or stash pop stops on conflicts: `git` exits with unmerged paths. |
| Authority | Reversible local: writes only conflicted-file edits, staged resolutions, regenerated lockfiles, and integration continuation (committing a merge, `git rebase --continue`, `git cherry-pick --continue`, and `git stash drop` only after the resolution is committed); runs scoped checks; rollback is `git merge --abort`, `git rebase --abort`, `git cherry-pick --abort`, or `git checkout -- <file>`. No remote mutation. No push, no tag, no force-push. |
| Side effect | Edits conflicted files, stages resolutions, regenerates lockfiles with package manager tooling, runs scoped checks, completes the in-progress integration. |
| Done | No unmerged paths, no conflict markers in any tracked file, scoped checks pass, integration is committed and complete. |

## Refusal

Not for people-mediation or team-interpersonal conflicts: resolve-merge-conflicts handles text conflicts in tracked files where git stops on unmerged paths. The shared word "conflict" is the only overlap. Not for remote, credential, publish, deploy, or other irreversible changes.

## Inputs

The repository root and the set of conflicting files are supplied by the in-progress git state. `git status` and `git diff --name-only --diff-filter=U` are authoritative for the conflict list.

Optional context:
- Ancestor / current / incoming: `git show :1:<file>`, `git show :2:<file>`, `git show :3:<file>`.
- Validation command: any command the human specifies; otherwise discover the project's own type checker, tests, and formatter.

## Procedure

1. **Detect the conflict state.** Run `git status`. Identify which integration is in progress (merge, rebase, cherry-pick, or stash pop) and enumerate the unmerged paths. If zero unmerged paths, the trigger condition is not met; stop.
   *Done when: the conflict-stop type is named and every unmerged path is listed.*

When asked to find conflict stops across worktrees, enumerate registered worktrees from structured porcelain records, resolve each exact gitdir relative to its own workspace, and record the operation markers, unmerged entries, and read errors per workspace. Do not parse commit OIDs as paths. A complete zero-result scan reports trigger-not-met with its enumerated coverage; an unreadable workspace is unknown, not clear. Report a live worker's integration without taking it over. Newly created workspaces invalidate the earlier coverage set.

2. **Gather context for each conflicted file.** Read the three versions, ancestor (`:1:`), current side (`:2:`), incoming side (`:3:`), via `git show`. Use `read` with the `:conflicts` selector to enumerate marker blocks; fall back to ranged `read` calls for files the selector returns empty. Use `difft` for side-by-side comparison when either intent is unclear.
   *Done when: every conflicted file's three versions and conflict-marker blocks have been examined.*

3. **Read the primary sources for both sides.** Read the commit messages, pull requests, and original issues or tickets for both changes. State why each side exists in one sentence before editing any hunk. If neither side's commit, PR, or linked issue expresses a clear intent, stop and report the ambiguous files, asking the human to supply the missing intent before continuing; do not guess an intent to drive the resolution.
   *Done when: each side's intent is stated and recorded, or ambiguous files are reported and the skill pauses for human input.*

4. **Resolve each hunk.** Preserve both intents when they fit together. When they genuinely conflict, choose the side that matches the integration's stated goal, name the trade-off, and record the discarded intent so the finishing commit message can name both sides' intents and the resolution rationale. Invent no new behaviour. Remove all conflict markers from each resolved file.
   *Done when: no conflict markers remain in any tracked file and every conflict resolution has its trade-off and any discarded intent recorded.*

When both sides independently rewrote the same subsystem, build a decision table from the complete original versions: each required behavior, its source evidence, the chosen implementation shape, and any discarded intent. Review history may inform the decision but recency or number of reviews does not choose the winner. Preserve compatible intents within the integration's stated goal; escalate genuinely conflicting contracts rather than inventing behavior. Inspect auto-merged code and the losing implementation's behavior tests for stale aliases, disconnected helpers, and assumptions invalidated by the selected contract, while remaining within this integration's scope.

Interpret index stage 1 as the common ancestor, stage 2 as the current side, and stage 3 as the incoming side. Name what current and incoming mean for this merge, rebase, cherry-pick, or stash application before choosing a side; ours/theirs labels are operation-dependent. Preserve both stated intents rather than applying a blanket side choice.

For replay from a synthetic or copied parent, compare the ancestor and lane versions with the actual target-base objects. Parent lines absent from the real base are suspected scaffolding, not an automatic deletion set. Reconstruct the lane's intended delta on the real base and verify ordering and initialization invariants; an imported early recovery call can break behavior outside the lane's apparent concern.

For intentional subsystem deletion, read the removal rationale and the branch's distinct additions. Preserve the removal when it governs the integration, move still-required behavior to its retained owner, and inspect cleanly merged additions and callers on the removed surface. Report incompatible or unpreserved behavior rather than silently dropping it or leaving a placeholder. For two implementations of the same intent, preserve the approved contract shape and combine only distinct semantic gains. Inspect whole affected functions against both parents, including automatically merged tails. Preserve distinct test cases from both sides even when their module names collide.

Checks must cover the affected invariants and relevant feature/configuration surfaces, not merely marker removal. Attribute failures with revision-bound comparable evidence. A clean replay followed by red checks is a diagnostic result, not automatically API drift and not an independent trigger for this stopped-integration skill. Recovery never blanket-restores files containing pre-existing or sibling edits; preserve the exact pre-resolution state before any user-requested rollback.

5. **Regenerate lockfiles with tooling.** If a lockfile is among the conflicting files, regenerate it with the project package manager rather than hand-editing.
   *Done when: lockfiles are regenerated, or confirmed not among the conflicted set.*

6. **Stage resolved files.** Run `git add <file>` for each resolved file. Confirm `git status` shows zero unmerged paths.
   *Done when: no unmerged paths remain in `git status`.*

7. **Run scoped checks.** Discover the repository's own commands. Run the type checker, tests, and formatter in that order when they exist. Scope runs to the resolution; fix only failures introduced by the integration. If a pre-existing failure blocks progress, stop and report it without suppressing or working around it.
   *Done when: scoped checks pass, or pre-existing failures are reported without suppression.*

8. **Finish the integration.** Complete the in-progress operation:
   - Merge: commit the merge with a message that names both sides' intents and the resolution rationale, including any discarded intent recorded in Step 4.
   - Rebase: `git rebase --continue` until every commit is replayed and no conflict remains.
   - Cherry-pick: `git cherry-pick --continue` (or commit, then continue if multiple commits remain).
   - Stash pop: the stash is applied after resolution; run `git stash drop` only after the resolved changes are committed, so the stash stays recoverable until the resolution is in history.
   *Done when: `git status` shows no conflicts and the integration is complete.*

## Failure and recovery

| Failure class | Condition | Recovery |
|---|---|---|
| No conflict present | `git status` reports zero unmerged paths | Stop; trigger condition not met |
| Unresolvable hunk | Both sides are logically incompatible without introducing incorrect behaviour | Leave the file marked, do not stage it, report the hunk and the competing intent |
| Lockfile regeneration fails | Package manager cannot regenerate the lockfile | Do not hand-edit the lockfile; report the failure and leave it unresolved |
| Scoped check failure | A check introduced by the integration fails | Fix only integration-introduced failures; report pre-existing failures without suppression |
| Unresolved marker | Any `<<<<<<<` found after staging | Stop; report the path and line range |
| Intent ambiguity | Neither side's commit, PR, or linked issue expresses a clear intent | Stop; report the ambiguous files and ask the human to supply the missing intent before continuing |
| Scope creep | Resolving one conflict reveals additional unrelated conflicts or issues | Stop at the current merge/rebase/cherry-pick/stash scope; do not refactor, clean up, or fix code outside the conflicted hunks |
| Non-convergence | Two resolution attempts produce the same check failure | Stop; report the conflict pair, both attempted resolutions, and the failure output |

Partial-result rule: If fewer than all conflicted files are resolved, the run is incomplete. Do not commit, do not claim success. Report every unresolved hunk by file and line range.

Rollback (user-requested only): `git merge --abort`, `git rebase --abort`, `git cherry-pick --abort` restore the pre-conflict VCS state at any point before a commit is made. `git checkout -- <file>` discards a staged-but-uncommitted resolution for a single file. A hard `git reset --hard` is never offered as a recovery path; it is the user's own action if they choose it.

## Output

A per-file report listing each resolved hunk, the chosen resolution, and any unresolved remainder; lockfile regeneration result; scoped-check outcome (pass or named failure); final `git status` summary.
