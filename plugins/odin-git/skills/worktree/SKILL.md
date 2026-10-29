---
name: worktree
description: 'Use when work needs an isolated git worktree: new work, an existing ref, a gated feature workspace, a manifest-tracked loop run, or a candidate patch captured without touching the current checkout. Not for plain branches: work in the current checkout.'
---

# Worktree isolation

## Contract

| Field | Bound contract |
|---|---|
| Trigger | New isolated work, an existing ref needing isolation, feature work needing a gated workspace with setup and baseline tests, a run needing a manifest-tracked worktree, or a candidate patch that must be captured without touching the current checkout. |
| Authority | Reversible local: writes only the worktree directory, `.worktrees/` or `.loop-worktrees/` entries, the gitignore entry, symlinked hooks, manifest bookkeeping, or a fresh temporary worktree plus binary-safe patch. Rollback is removing the worktree and reverting those entries. Capture mode never writes the original checkout. Loop-run never passes `--force` to `git worktree remove`. No remote mutation. |
| Side effect | Creates or attaches an isolated worktree the harness can see and manage, or captures a patch from an ephemeral worktree. Feature-gate also runs setup and the baseline suite. Loop-run also maintains a status manifest. |
| Done | New-work and isolate-existing-ref have an isolated workspace the harness can see, with no phantom state. Feature-gate adds a green baseline or a surfaced failure. Loop-run adds a manifest where every worktree has a legal status. Capture mode writes and returns a patch path plus command results with the original checkout unchanged. |

Ownership boundary: owns isolation placement, gitignore tracking, hook linkage, loop manifest discipline, and ephemeral capture. Does not choose branch semantics, author commits (`commit`), push or open PRs (`commit-push-pr`), or watch PRs (`watch-and-repair-pr`).

## Inputs

1. Mode (required): `new-work`, `isolate-existing-ref`, `feature-gate`, `loop-run`, `capture-isolated-patch`. Default `new-work` when no ref, gate, lifecycle, or capture is requested.
2. Ref to isolate (`isolate-existing-ref` only): PR or MR head, branch, or commit.
3. New branch name (optional): derived from the work description when omitted.
4. Base branch (optional): origin default branch, else `main`.
5. Setup command (`feature-gate`, optional): for example `pnpm install --frozen-lockfile`. When omitted no setup runs.
6. `runId` (`loop-run`, required): single path segment, used verbatim as path segment and branch suffix.
7. `pattern` (`loop-run`, required at create): short label kept on the manifest entry.
8. Status for mark (`loop-run`, required): exactly `active`, `rejected`, `escalated`, `merged`, or `stale`.
9. Cleanup set (`loop-run`, optional): status CSV default `rejected,escalated`, plus optional age cutoff `<n>s|m|h|d`.
10. Command (`capture-isolated-patch`, required): shell command producing the candidate change; runs with the ephemeral worktree as its working directory.
11. Base ref (`capture-isolated-patch`, optional): defaults to current `HEAD`.
12. Repo path (`capture-isolated-patch`, optional): defaults to the current working directory.

## Procedure

1. Determine the mode. For `capture-isolated-patch` require `command` and resolve base and repo path; for other modes do not create a worktree for single-task work that belongs on a branch in the current checkout.
2. Capture mode: verify `repo-path` is a work tree and `base-ref` resolves, both scoped to `repo-path`: `git -C <repo-path> rev-parse --is-inside-work-tree` and `git -C <repo-path> rev-parse --verify <base-ref>`. Stop and name the failing check before creating anything when either fails. Other modes: detect existing isolation by comparing the resolved absolute git dir against the resolved absolute common git dir: `git rev-parse --absolute-git-dir` and `(cd "$(git rev-parse --git-common-dir)" && pwd -P)`. Equal means a normal checkout; continue to step 5. Different continues to step 3.
3. Capture mode: create an ephemeral worktree at a fresh temp path with `git -C <repo-path> worktree add --detach <tmp-path> <base-ref>`; record the path and report the git error when creation fails. Other modes after a different-path result: run `git rev-parse --show-superproject-working-tree`. Non-empty means a submodule: in feature-gate stop and report that isolation must run from the superproject; otherwise treat as a normal checkout and continue to step 5. Empty means already isolated: report `git rev-parse --show-toplevel` and the current branch, work in place, and in isolate-existing-ref mode check the named ref out here unless already current. Never nest a worktree inside the harness-managed tree.
4. Capture mode: run `command` inside the ephemeral worktree, capturing stdout, stderr, and exit code; do not commit, push, or merge. After it returns run `git -C <tmp-path> add -N .`, compute `git -C <tmp-path> diff --binary <base-ref>`, and write that binary-safe diff to a patch file under the worktree parent temp directory. A non-zero command exit still extracts the patch. On success remove the worktree with `git -C <repo-path> worktree remove --force <tmp-path>` and return the patch path, exit code, and outputs; on extraction failure preserve the worktree and return its path plus the reason. The original checkout stays untouched. Stop after this branch.
5. Prefer the harness native worktree primitive (for example `EnterWorktree`, `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag). Use it and continue to the mode steps. A behind-the-back `git worktree add` creates phantom state the harness cannot see or clean up.
6. When no native tool exists and steps 2-3 found no existing isolation, follow `references/git-fallback.md`: run from the repo root; choose a meaningful branch name from the work description, never an opaque generated name; ensure `.worktrees/` is gitignored with the trailing-slash probe `git check-ignore -q .worktrees/` before creating anything; best-effort refresh the base with `git fetch origin <from-branch>` and continue with the local ref when no origin or a differently named remote exists; create per mode (new work with `-b`, existing branch or tag directly, PR via `git fetch origin pull/<n>/head:pr-<n>` then `git worktree add .worktrees/pr-<n> pr-<n>` on a local branch, never a detached `FETCH_HEAD`; for push-tracking back to the PR create detached then run `gh pr checkout <n>` inside, which is fork-safe); when git reports the ref is already checked out elsewhere report that path and stop rather than forcing a second worktree; then `cd` into it and report path and branch. In feature-gate mode, when creation fails fall back to in-place work on the current branch and report the reason. On sandbox or permission failure report it and ask with the platform blocking question tool whether to work in the current checkout or stop; never proceed without explicit confirmation and never retry silently.
  For an MR use `glab mr checkout <iid> [-b <branch>] [-R GROUP/PROJECT] [--worktree <path>]`, which is fork-safe and resolves the source project head; a manual fallback is `git fetch <remote> merge-requests/<iid>/head:mr-<iid>` then `git worktree add .worktrees/mr-<iid> mr-<iid>` on a local branch, never a detached `FETCH_HEAD`. Derive the forge from the verified request URL or the checkout remote and never guess across forges; on forks bind source and target projects separately (including self-managed hosts) and fetch from the source-project remote when checking out by hand. For push-tracking back to the MR, create detached then run `glab mr checkout <iid>` inside. When git reports the ref is already checked out elsewhere, report that path and stop rather than forcing a second worktree, exactly as with a PR.
7. Feature-gate mode after the worktree exists (or in place after fallback): (a) when the worktree directory is not already ignored, add it to `.gitignore` without committing and report the pending change; (b) symlink the worktree hooks directory to the parent hooks found via `git rev-parse --git-common-dir`, reporting and continuing without hooks on failure; (c) run the supplied setup inside the worktree, surfacing non-zero output and stopping; (d) run the project baseline suite inside the worktree, surfacing failures with a proceed-or-investigate question.

When the requested isolated workspace will support a comparison or regression proof, record its resolved path, base revision, and actual source state. A revision name alone does not identify uncommitted test or generated-input overlays; enumerate those separately under the caller's existing authority.

Keep independently compared checkouts' build and runtime scratch separate unless the build system's safe reuse is established. Record artifact directories and prerequisites for each target. Prefer new owned scratch over deleting a shared cache. If an existing checkout is synchronized, verify the intended inputs, including required generated files, and establish that its executable or imported artifact corresponds to those inputs using the build system's own evidence.

Do not infer stale output from elapsed time alone, require recompilation when a verified content-addressed artifact is valid, or restore a pinned reference from an arbitrary HEAD. Missing isolation, unresolved artifact identity, or an unavailable prerequisite blocks the affected proof.

Preserve the active mode's cleanup rules. Never remove unrelated caches, force-remove a dirty comparison worktree, or discard caller changes to obtain a clean proof. Report retained paths and why they remain.
8. Loop-run mode under `.loop-worktrees/`: (a) bind the root with `git rev-parse --is-inside-work-tree`; the manifest is `.loop-worktrees/manifest.json` shaped exactly `{"version":1,"worktrees":[]}` and the mutex is `.loop-worktrees/.manifest.mutex`; on any other existing shape stop without rewriting; add `.loop-worktrees/` to `.gitignore`; (b) serialize each read-modify-write with exclusive mutex create, clearing a mutex older than 30 seconds and retrying to a 30-second deadline, releasing on every path; pure reads take no mutex; (c) create refuses a non-single-segment `runId` and an already-`active` id, runs `git worktree add -b loop/<runId> .loop-worktrees/<runId> <base>`, replaces any prior same-id entry and appends the new record, writing tmp-then-rename; (d) mark rejects any status outside the five-value set and writes tmp-then-rename without deleting entries; (e) cleanup selects only requested statuses (never `active`) older than any cutoff, runs `git worktree remove .loop-worktrees/<id>` without `--force`, records refusals as skipped, and rewrites without removed ids; (f) reconcile compares `git worktree list --porcelain` against the manifest, reports orphans and removes only on explicit instruction still without `--force`, and drops entries whose directories no longer exist.
9. Report the absolute path, current branch, mode, and creation method (native tool or git fallback); or the existing path and branch when already isolated.

Bind a workspace to its exact registered path, gitdir, common object store, current full OID, branch or detached state, owner, and dirty-state inventory before reuse or cleanup. Matching commit subjects are not proof that its work is merged. Inspect unique commits and content equivalence together with staged, unstaged, and untracked state. A file introduced after a stale workspace's base is not evidence that the stale workspace intentionally deleted it.

Preserve abandoned or parked work before removal. Applying a retained stash or patch without conflict does not prove semantic restoration against a newer anchor; compare the intended content and contract. Retain the recovery object until its content is verified. Loop-run cleanup continues to refuse force; no source lesson broadens that rule.

For a linked-worktree submodule problem, inspect the superproject gitlink and available local module store before a network workaround. If using that store, obtain a locally available ref containing the required object and verify the checkout equals the pinned gitlink. Do not stage a gitlink change unless requested. An unusual submodule checkout shape is not permission for forced worktree deletion.

## Failure and recovery

- Bad capture input, capture creation failure, non-zero command exit, or extraction failure: handled in step 4 with the original checkout unchanged.
- Already isolated: do not create another; report the existing path and proceed in place or check the named ref out there.
- Ref already checked out elsewhere: report its path; never double-checkout one branch.
- Worktree already exists or cannot be removed while current: switch to it, remove it, or `cd` out first, then remove.
- Sandbox or permission error: ask and proceed only on explicit confirmation; feature-gate falls back in place with a reported reason.
- Submodule in feature-gate: stop; isolation must run from the superproject.
- Setup or baseline failure: surface output and stop or ask proceed-or-investigate; do not claim a green workspace.
- Loop-run manifest, mutex, id, branch, or status violations: stop or refuse as named in step 8; manifest writes are tmp-then-rename under the mutex; a manifest write failure after a successful add rolls back with `git worktree remove` then `git branch -D loop/<runId>`.
- Non-converged isolation with no confirmed fallback: return blocked with the exact error and inspected paths.

## Output

Capture mode: patch path, exit code, outputs, or preserved worktree on extraction failure. Other modes: absolute path, branch, mode, and creation method; feature-gate adds setup and baseline status; loop-run adds manifest rows and cleanup or reconcile lines. Done only when the active mode predicate holds.
