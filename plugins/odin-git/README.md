# ODIN Git

ODIN workflows for commits, branches, pull requests, review feedback, and issue tracking.

23 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-git@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-git@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-git/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-git:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| atomic-issues-prs | Use when the user says "atomic PRs" or requests one issue or PR per logical change. |
| commit-push-current | Use when a human explicitly asks to commit and push to the checked-out branch with no branch creation and no pull request. |
| commit-push-main | Use when a human explicitly asks to commit and push directly to the default branch, with no feature branch and no pull request. |
| create-branch | Use when the user asks to create a new branch or start work on one. |
| create-pull-request | Use when asked to create or update a PR, shape or revise its description, or link issue references to its body. |
| finish-branch-menu | Use when implementation is complete, the test suite is green, and an integration decision is needed for a development branch or worktree. |
| gate-and-merge | Use when landing a queue of open PRs: gate each PR, sweep its review feedback to root cause, then merge, repair, hold, or close it. |
| git-branchless | Use when asked for multi-commit stack edits, rebases, fixups, or stacked-PR publishing with branchless git idioms. |
| git-cleanup | Use when the user explicitly invokes branch or worktree cleanup for a repo with accumulated local branches. |
| git-guardrails | Use when a repository needs Git safety controls: guard destructive commands, set up gitignore or fix gitignore when untracked files keep appearing, or install or repair a repository-local pre-commit hook from project gates, including package-manager-native commit-time checks. |
| github-backlog-triage | Use when the user invokes backlog triage for a GitHub repo's open issues and PRs. |
| issue-intake | Use when filing an approved task spec as a GitHub issue with a local archive and optional worktree implementer. |
| issue-triage | Use when a human invokes triage on a new configured Slack issue report. |
| make-pr-easy-to-review | Use when a human explicitly asks to reshape or annotate one pull request for review. |
| modernize | Use when a human explicitly asks whether an aging pull request should still land, whether an old PR should be rebased, or whether a stale branch should be revived. |
| post-merge-cleanup | Use when a landed merge, release, or completed change needs its cleanup surface reconciled. |
| propose-issue | Use when the user asks to propose an issue, file or open a bug report, or turn a reported defect into a tracked issue. |
| resolve-merge-conflicts | Use when a merge, rebase, cherry-pick, or stash pop stops on conflicts. |
| review-and-ship | Use when a human directly requests review and publication of an existing diff or delegated work. |
| setup-repo-skills | Use when the user wants one-time repository setup for tracker, triage labels, and domain conventions. |
| triage | Use when issues or external pull requests must move through a category and state machine with verification, grilling, and agent-ready briefs. |
| watch-and-repair-pr | Use when a human explicitly invokes a watcher cycle for an open pull request that must move toward mergeable or blocked. |
| worktree | Use when work needs an isolated git worktree: new work, an existing ref, a gated feature workspace, a manifest-tracked loop run, or a candidate patch captured without touching the current checkout. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
