# ODIN Core

Core ODIN gates every session runs: intent, scope, verification, and hand-off checks.

27 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-core@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-core@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-core/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-core:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| architect | Use when non-trivial code needs a design, codebase architecture needs improving through survey and deepening, or one module needs targeted interface narrowing, seams, or testability. |
| askme | Use when eliciting intent/scope/referents or gating long/bundled/high-stakes/hard-to-undo work: exhaustive/collaborative/adversarial/grill/gate/batch/interview/proposal/pairing. |
| autolearn | Use when a verified non-trivial fix lands or existing solution docs need refresh. |
| autoplan | Use when the user runs /autoplan on a plan or idea. |
| clarify | Use when the user says "clarify", "what is ambiguous here", or when a prompt or spec reads as under-specified before planning. |
| code-simplification | Use when the user names a module, file set, or dependency slice and wants it structurally smaller with its consumer contract preserved. |
| commit | Use when asked to commit working-tree changes as typed atomic local commits. |
| commit-push-pr | Use when asked to commit and push a feature branch, with or without a pull request. |
| compound | Use when the user explicitly asks to save, curate, or consolidate what was learned, or closes a meaningful knowledge-work session. |
| do-it-now | Use when the user asks to finish the whole task now, clear active todos, or unblock undone implementation without deferred phases or follow-up remainders. |
| enforce-workflow-constraints | Use when any bounded workflow starts or reaches an action, path, proposal, or merge boundary. |
| fix | Use when the user asks to fix a local bug, make a verifier pass, or implement an already-adjudicated repair. |
| grill-core | Use when the cause is unknown, the fault recurs as a class, or a review comment needs a root-design repair rather than a patch. |
| ground-latest | Use when starting or scaffolding a codebase or service, migrating, refactoring, or picking language, framework, or dependency, or latest, LTS, or modern way. |
| necessary-work | Use when work is about to grow past the ask, the task may already be done, or the user requests only the minimum. |
| no-comments | Use when asked to remove source comments by replacing them with clear code or accessible documentation. |
| no-excuses | Use when a material claim rests on missing proof, an untested assumption, or unresolved counterevidence that investigation can still settle. |
| parallel-launch | Use when work splits into independent sub-tasks or cross-domain research. |
| plan-complete | Use when a plan must be proven complete before implementation begins. |
| post-change-check-gate | Use when an artifact or skill has just changed and is about to be called done, committed, or handed off. |
| resolve | Use when a single feedback batch needs adjudication and repair, locally or on one PR: verify each finding against code, fix valid items, and prove them. |
| resolve-pr-comments | Use when handling GitHub PR review threads, top-level comments, or review bodies on one named PR in a single batch: enumerate completely, judge against current code, repair valid findings at the root, and post only explicitly approved replies and resolutions. |
| review-fix-loop | Use when review and repair must repeat to an evidenced end state, locally or across one or more PRs. |
| simplify | Use when the user asks to simplify a diff, branch, or change-set and wants structure the change introduced or affected challenged. |
| subagent-driven | Use when a user says execute with subagents or hands over an ordered multi-task plan. |
| tests-purge-unneeded | Use when a legacy, slow, or duplicate test suite needs purging, a post-refactor sweep is due, or types cover a contract. |
| verification-before-completion | Use when a task, feature, or fix is called done, complete, finished, or fixed, or before a commit, PR, or next task. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
