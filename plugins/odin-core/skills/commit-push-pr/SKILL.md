---
name: commit-push-pr
description: 'Use when asked to commit and push a feature branch, with or without a pull request. Not for a PR body alone: use create-pull-request.'
---

# Commit, push, and optionally open a pull request

Commit the working tree and push the feature branch to `origin`. In pull-request mode, open or update the PR with `gh`; in no-PR mode stop after the push. Description-only and description-update modes compose or refresh a PR body without committing. Commit authoring belongs to `commit`; title and body rules belong to `create-pull-request`. This skill adds branch placement, PR-target resolution, evidence placement, the push, and the `gh` call.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to commit and push a feature branch with or without a PR, or asks for a PR description draft, rewrite, or refresh. |
| Authority | Human-gated: local commits, at most one local feature branch, and one push to `origin/<branch>`; pull-request mode also creates or edits one PR through `gh`. No remote action without an exact preview and approval. Rollback is `git reset --hard <prior-HEAD>`, `git branch -D <created-branch>`, and `gh pr close` or `gh pr edit` restoring the prior body. Never force-push. No STRATEGY.md, no Compound config layers, no guessed default branch. |
| Side effect | Local commits, at most one branch, one `git push` to `origin`; pull-request mode also creates or edits one PR; description modes write no commits when no work exists. |
| Done | No-PR: `git status --porcelain` empty and `git rev-list --left-right --count origin/<branch>...HEAD` prints `0 0`. Pull-request: those plus `gh pr view --json url,title,state` returns `OPEN`. Description-only: a drafted title and body are returned and applied only when asked. Description-update: the existing PR body is refreshed only after approval. |

Parnas boundary: owns branch placement, push-set statement, PR-target choice, push, and PR create/edit plumbing. Does not invent message conventions (`commit`), title and body prose (`create-pull-request`), or CI watching (`watch-and-repair-pr`).

## Inputs

- Mode: `pull-request` (default full workflow), `no-pull-request`, `description-only`, `description-update`. Stack is an opt-in modifier only when the user explicitly asks for stacked PRs; never propose a stack for one logical change.
- Working tree, branch, history, remotes, remote default, existing PR, `gh` auth: gathered by the skill; see procedure.
- PR target (origin versus upstream, base, head): required in pull-request mode.
- User-supplied evidence (URL, embed, path): optional.
- Human decisions: detached HEAD, unpushed default-branch commits, ambiguous target, description rewrite approval.

## Procedure

1. Gather context, each probe as its own call: `git status`, `git diff HEAD`, `git branch --show-current`, `git log --oneline -10`, `git remote`, `git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo DEFAULT_BRANCH_UNRESOLVED`. In pull-request modes also run `gh pr view --json url,title,state 2>/dev/null || echo NO_OPEN_PR` and `gh auth status >/dev/null 2>&1 || echo GH_NOT_AUTHENTICATED`. When no `origin` exists, skip remote-default and PR-target resolution; after any detached-HEAD decision, commit on the current branch and end with a local-only report. Otherwise strip `origin/`; on unresolved try `git ls-remote --symref origin HEAD`, then verified `gh repo view --json defaultBranchRef`. When every resolver fails, report `DEFAULT_BRANCH_UNRESOLVED` and stop; never guess. Description-only and description-update with a pasted PR ref skip working-tree gating and resolve that ref directly.
2. Resolve the existing-PR state. Run `gh pr list --head <branch> --state open --json number,url,title,body,state,isDraft,headRefName,headRepositoryOwner` only when the branch name is non-empty; on detached HEAD skip it until a branch exists. Exit 0 with `[]` means no open PR. Non-zero means unknown (missing `gh`, unauthenticated, offline): never treat it as none; resolve auth or connectivity and stop until presence is known. On a fork checkout target the base with `-R <base-owner>/<repo>` and pass the branch name only; `--head <owner>:<branch>` silently returns `[]` and opens a duplicate. With results match `headRepositoryOwner` and `headRefName` to the current head; on an ambiguous multi-fork match stop and show candidates.
3. In pull-request mode resolve the PR target. The branch always pushes to `origin`; this step decides only where the PR is filed. With an `upstream` remote the target is `upstream`. Otherwise read `gh repo view <origin-slug> --json nameWithOwner,parent,defaultBranchRef`; a non-null `parent` is the target candidate. Ask only when no single target is clear (no upstream and two or more non-origin candidates, parent disagrees with upstream, or origin shares no merge-base with the target). A fork that is only behind its parent is not ambiguous. For an organization-owned origin where `gh --head` cannot file, push then report the compare URL and stop.
4. Classify the branch. Detached HEAD: ask whether to create a branch; on yes create and continue, on no stop. Default branch with no work: stop. Default branch with work: create a feature branch from a fresh default tip (`git fetch --no-tags origin refs/heads/<default>:refs/remotes/origin/<default>`, then `git checkout -b <branch> <base>`; on uncommitted-overwrite refusal stash, checkout, pop; on fetch failure stop rather than branching from HEAD). Never silently carry foreign commits: when `git log origin/<default>..HEAD` is non-empty, ask whether to carry them or base on `origin/<default>`. Feature branch: continue.
5. Author commits with `commit`. Its atomicity, staging discipline, named-file commit, and message-file rules apply. Do not restate them. Description-only and description-update skip this step.
6. State the push set. New to origin (`git ls-remote --heads origin <branch>` empty): list `git log --oneline origin/<default>..HEAD`, materializing the tracking ref first when this skill created the branch. Existing: refresh the tracking tip (`git fetch --no-tags origin refs/heads/<branch>:refs/remotes/origin/<branch>`; on failure stop without pushing) and list `git log --oneline origin/<branch>..HEAD`. On no `origin`, report local-only with the commit list and stop. On failed fetch with no fetched base, stop; never preview from HEAD alone.
7. Decide evidence before composing. User-supplied artifact goes into the body as `## Demo`, `## Screenshots`, or `## Evidence` by kind. User asked but supplied none: ask for it or tell them to capture it; do not invent it. No observable behavior (internal plumbing, type-only, pure refactor, inert docs): skip without asking, classified by runtime purpose, not extension. Otherwise add a concise validation note of what was exercised and its result, or state plainly why no run was possible. Never label test output `Demo` or `Screenshots`. Do not block the PR on a missing visual.
8. Compose with `create-pull-request`. Give it the base remote from step 3 so the diff is taken against the right base. Preserve any existing `Related:` or `Fixes` trailer on rewrite. Description-only: run this step on the pasted or resolved PR ref and print the draft; apply only when asked. Description-update: resolve the open PR by the Context rule, compose in PR mode against its current body, preview, confirm, then apply with `gh pr edit`.
9. Preview the exact remote mutations and wait for approval. Show push target plus commit list; in pull-request mode add target, base, head, title, and the first two sentences of the body. On refusal stop with nothing pushed and no PR created or edited. On approval re-run the step 6 listing; on any difference re-preview and wait again. Then push with `git push -u origin HEAD`, never force-push. Write the body to a temp file and pass `--body-file`, never inline `--body` or stdin. New same-repo PR: `gh pr create --base <default> --title "<TITLE>" --body-file "$BODY_FILE"`. New upstream PR: add `--repo <upstream-slug> --base <default> --head <fork-owner>:<branch>`. Existing PR: pushed commits are already on it; ask whether to rewrite the description, then `gh pr edit --title "<TITLE>" --body-file "$BODY_FILE"` (add `--repo` for upstream). Escape `"`, backticks, `$`, and `\` in the title. Re-verify PR presence immediately before create: a matching PR takes the existing-PR path, exit-0 `[]` creates, non-zero blocks. After create, re-read `gh pr view --json body`; when empty, re-apply from the same body file and confirm with a fresh read.
10. Verify: no-PR requires empty porcelain and `0 0` counts. Pull-request additionally requires `OPEN` with the previewed title. Report branch, hashes, subjects, PR URL, created versus updated, and verification.

## Failure and recovery

- `gh` missing or not authenticated in pull-request modes: stop before any commit; instruct install or `gh auth login`.
- Clean tree with nothing to push: report nothing to do; no mutation.
- Detached HEAD declined, preview declined, ambiguous target unanswered, commit list changed since approval: stop with nothing pushed.
- Fetch, tracking-refresh, or no-base failures: stop before the push; never fall back to an unanchored listing.
- No `origin`: local-only report; never add or guess a remote.
- Diverged push rejection: report counts; never force-push.
- PR create failure after push: report the exact `gh` error; the branch stays for retry.
- Empty body after create: re-apply and confirm; never leave a silent empty body.

## Output

No-PR: pushed branch plus verification report. Pull-request: pushed branch plus created or updated PR with verification. Description-only: drafted title and body with no remote mutation unless asked. Description-update: refreshed PR body after approval with verification. Local-only or declined paths report commits left unpushed.
