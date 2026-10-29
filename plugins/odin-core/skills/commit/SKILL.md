---
name: commit
description: 'Use when asked to commit working-tree changes as typed atomic local commits. Not for push, PR, or remote publication: use commit-push-pr.'
---

# Git commit

Shape messages to repository conventions. Two modes: `create` stages and commits working-tree changes as typed atomic local commits; `rewrite` rewords messages of `HEAD` or a short unpushed range while the tree stays byte-identical.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Create: user asks to commit or save staged or unstaged changes, create a typed branch, or format history for changelog generation. Rewrite: user asks to clean up a finished message or bring messages of `HEAD` or a short unpushed range to handoff-ready form. |
| Authority | Reversible local: create writes only the local index, one local feature branch, and local commits; rewrite writes only local commit messages. Rollback is `git reset --hard <prior-HEAD>`, `git branch -D <created-branch>`, and the reflog with original refs. No remote mutation. |
| Side effect | Local working tree, local index, local branch refs, local commit objects; rewrite touches messages only. |
| Done | Create: each logical concern is committed with an explicit named file list and a value-communicating message; `git status` confirms success; hashes and subjects are reported. Rewrite: `git diff <old>..<new>` is empty, dates preserved by position, and `git log` alone carries the handoff. |

Ownership boundary: this skill owns local commits, local branch placement, and message shape. It does not push, open or edit a PR/MR, compose a PR/MR body, watch CI, or resolve review threads. Push and PR/MR publication belong to `commit-push-pr` (which also owns title and body composition, including the `## Demo`/`## Screenshots`/`## Evidence` section and preserved `Related:`/`Fixes` trailers); watching belongs to `watch-and-repair-pr`.

## Inputs

- `mode`: `create` (default) or `rewrite`.
- Working-tree state (`git status`, `git diff HEAD`), current branch (`git branch --show-current`), recent history (`git log --oneline -10`): required in create, gathered by the skill.
- Remote default (`git rev-parse --abbrev-ref origin/HEAD`): optional; falls back to the forge viewer matching the verified remote (GitHub `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`, GitLab `glab repo view -F json` reading its `default_branch` field). When every resolver fails, report `DEFAULT_BRANCH_UNRESOLVED` and stop any step that needs the default; never guess. Select the forge from the verified remote URL; never assume GitHub.
- Repo commit convention in already-loaded instructions: optional, used directly.
- Issue number when one exists: optional; prefixed into branch name and footer.
- Target platform (GitHub or GitLab): required only when closing issues cross-repo. No forge command runs for this input; the platform only shapes the cross-repo closing footer written into the commit message.
- Rewrite target (`HEAD` or `HEAD~N..HEAD`) and intended text: required in rewrite; confirmation required when any target is already pushed.

## Procedure

1. Select the mode. `rewrite` only when the user asks to reword existing messages; otherwise `create`.
2. Gather context, each probe as its own call: `git status`, `git diff HEAD`, `git branch --show-current`, `git log --oneline -10`, `git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo DEFAULT_BRANCH_UNRESOLVED`. Strip `origin/` from the default. On unresolved or bare `HEAD`, try the forge viewer matching the verified remote (`gh repo view` on GitHub, `glab repo view -F json` reading `default_branch` on GitLab); when every resolver fails, report `DEFAULT_BRANCH_UNRESOLVED` and stop any step that needs the default; never guess. Treat this as a snapshot; re-read the staged set immediately before committing.
3. Determine the message convention: (1) repo conventions already in context, (2) clear pattern in recent commits, (3) seven-rule fallback with conventional-commit types (`feat`, `fix`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `ref`/`refactor`, `perf`, `meta`, `license`, `revert`). With conventional commits default to `fix:` over `feat:` when ambiguous; user override wins. Subject is imperative and names the outcome, not the file list.
4. Rewrite mode only:
   1. List exact targets with `git log --format='%H %an <%ae> %ad %cn <%ce> %cd' <range>`. Record each target tree SHA (`git rev-parse <sha>^{tree}`) and author/committer dates by position.
   2. Check `git branch -r --contains <sha>`; when any target is pushed, stop and require explicit confirmation.
   3. Reword with `git rebase` plus `GIT_SEQUENCE_EDITOR` and `git commit --amend`, scoped to the range. Never create a new change.
   4. Re-sign with recorded `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` by position.
   5. Verify `git diff <old>..<new>` is empty, dates match by position, and the log carries the handoff with the diff hidden. On drift, abort and restore original refs from the reflog.
5. Create mode: when `git status` shows no staged, modified, or untracked files, report nothing to commit and stop. Do not use `git diff HEAD` alone; it misses untracked files.
6. Create mode, detached HEAD: ask whether to create a feature branch with the platform blocking question tool; on yes derive a typed name (step 7), run `git checkout -b <branch-name>`, re-read the branch; on no continue detached with the commit.
7. Create mode, branch name: `<type>/[issue-]<description>`, lowercase, hyphens, under 50 chars. Match the type to the work.
8. Create mode, logical commits: one concern per commit. Split by mechanism, never by file alone. When one file carries two mechanisms, write the filtered patch from `git diff -- <file>`, keep one mechanism, and stage with `git apply --cached <patch>`. A lint, format, or whitespace sweep is its own commit. Order commits so each leaves the tree building.
Partition by contract dependency, not file count or line distance. Tables joined by a boot-time registry guard, signature changes and their callers, and mutually dependent repair hunks belong together when either half alone breaks the tree. Each published slice must be coherent without its successor. A green dirty union does not prove the staged tree or individual commits.

Generate real unified or binary-safe patches with the external diff disabled on the diff subcommand. Use smaller context or explicit content reconstruction only when needed to isolate a concern. Re-read the candidate hunks after each commit or base change; regenerate rather than blindly rewriting stale offsets. Inspect the staged content, not merely its stat or rendered display. Preserve the intended final tree across a split with exact object/tree comparison.

Distinguish a standalone formatting sweep from mechanical formatting required by a behavior repair. Keep a standalone sweep separate; attribute repair-required formatter changes to the owning concern when constructing an explicitly authorized unpublished series. Do not place all formatting in the last commit by default. Folding, recutting committed blobs, or rewriting a published series requires authority covering that history operation; create mode and message-only rewrite mode do not silently grant it.
9. Create mode, default branch with work: automatically create a feature branch first. Before creating it, verify the base resolves, the name is unused (`git branch --list <branch-name>` must be empty), and the working tree is clean or its dirty files are surfaced for user decision; a blocked check changes nothing. Then run `git checkout -b <branch-name>`, confirm with `git branch --show-current`. Do not ask; committing on the default branch is not an option. Default branch with no work: report nothing to do and stop.
10. Create mode, per-group gate: run the repo-native type-checker or linter for that group before staging it. A failing group is not ready; skip it and name the failure. Skip silently when neither is configured.
11. Create mode, stage and commit each group with named files only. Never `git add -A` or `git add .`. Honor `exclude:<paths>`: those files stay uncommitted and are named in the report. Write the full message (subject, blank line, optional body) to a file outside the repo with the file-write tool, then run as two calls per group:

```bash
git add file1 file2 file3
```

```bash
git commit -F <message-file> -- file1 file2 file3
```

The `-F` file avoids shell quoting for `$`, quotes, backticks, and multiline bodies. The trailing path list is required: a bare `git commit` would sweep anything already staged. Never include customer names, emails, secrets, PII, a Claude signature, AI attribution, or a `Co-authored-by` trailer for an AI agent. When the commit carries someone else's ported work, end with one `Co-authored-by: Name <email>` trailer per credited person, copied exactly from their commits or patch trailers; when no email is recorded, name them in the body instead of guessing.
Before changing a shared index, establish exclusive ownership and record existing staged paths, modes, and blob identities. Leave foreign staged entries unchanged; an ordinary commit without pathspec includes the whole index, so do not commit while unapproved staged entries remain in that index. Use an isolated construction index or workspace when necessary, without racing the real index.
12. Run `git status` after the commit; report hash and subject.

## Failure and recovery

- Clean tree: report nothing to commit; no mutation.
- Declined branch on detached HEAD: stop; no commit.
- Gate failure: that group stays unstaged; committed groups remain; report the failing gate.
- Sensitive or unrelated file in scope: exclude by naming files; never broaden to `add -A`.
- Breaking change stated only in body: add `!` or a `BREAKING CHANGE:` footer.
- Pushed target in rewrite without confirmation: stop; do not rewrite.
- Tree drift or date slip in rewrite: abort, restore original refs from the reflog, report.
- Partial result: committed groups are real; name uncommitted groups and the reason.

Preserve recoverable original content before reconstruction, including tracked, staged, unstaged, and relevant untracked files. Never use add-all as a final sweep over shared work. A failed split remains uncommitted; it is not permission for blanket restore, reset, or force publication.

## Output

Create: local commits on a typed branch plus a report of hashes, subjects, excluded paths, and confirming `git status`. Rewrite: rewritten messages over the exact range with empty tree diff, dates preserved by position, and verification results.
