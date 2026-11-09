# DStack Git

Git workflows for commits, branches, GitHub pull requests, GitLab merge requests, review feedback, and issues. Install it with `claude plugin install dstack-git@dstack` in Claude Code or `codex plugin add dstack-git@dstack` in Codex; Claude Code invokes its skills as `/dstack-git:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- Pick the publish target first. A feature branch with a pull request: core `/skill:commit-push-pr`. The checked-out branch with no pull request: `/skill:commit-push-current` (user only). Straight to the default branch: `/skill:commit-push-main` (user only). One issue or pull request per logical change: `/skill:atomic-issues-prs` (user only).
- After the pull request exists: `/skill:watch-and-repair-pr` watches it, fixes and pushes review feedback on its own branch, replies to and resolves the threads, and waits for every expected review until the pull request is clean or blocked. Review threads reach core `/skill:resolve-pr-comments` through it, or directly when you approve the exact replies yourself. Conflicts go to `/skill:resolve-merge-conflicts`, a queue of open pull requests to `/skill:gate-and-merge` (user only), an aging pull request to `/skill:modernize` (user only), and a landed change to `/skill:post-merge-cleanup` (user only). `/skill:make-pr-easy-to-review` (user only) reshapes one pull request for its reviewers.
- Local branches and checkouts: `/skill:worktree` for an isolated worktree, `/skill:git-branchless` (user only) for stacks and fixups, `/skill:git-cleanup` (user only) for stale branches and worktrees.
- Issues: `/skill:propose-issue` (user only) files one, `/skill:triage` (user only) moves incoming issues and pull requests through states, `/skill:issue-triage` (user only) handles a configured Slack issue report.
- The author's pull request lane: `/skill:atomic-issues-prs`, core `/skill:commit-push-pr`, core `/skill:resolve-pr-comments`, `/skill:resolve-merge-conflicts`, `/skill:gate-and-merge`, then `/skill:post-merge-cleanup`, with core `/skill:ci-fix` whenever checks go red.
