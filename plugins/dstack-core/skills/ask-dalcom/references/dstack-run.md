# DStack Run

DStack workflows for executing plans, orchestrating subagents, and bounded autonomous loops. Install it with `claude plugin install dstack-run@dstack` in Claude Code or `codex plugin add dstack-run@dstack` in Codex; Claude Code invokes its skills as `/dstack-run:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- A large task in several parts: core `/skill:autoplan` reviews it, `/skill:diamond-task` partitions it into disjoint write sets, then core `/skill:workflows-driven` or core `/skill:autopilot` runs it.
- Splitting work: `/skill:size-the-run` first when the effort is unclear, `/skill:partition-scopes-to-subagents` for non-overlapping scopes, `/skill:schedule-dependency-waves` when units declare dependencies, `/skill:diamond-task` when one issue or pull request is too large for one worker, `/skill:orchestration-patterns` for role panels and coupling, `/skill:implement-spec` (user only) to turn a complete ticket graph into one integration branch.
- Loops and watching: `/skill:watch-for` polls a target until a predicate holds, `/skill:watch-for-structured` (user only) and `/skill:watch-for-harness-mode` (user only) turn a watch into an on-call classifier or a reusable watcher, `/skill:cybernetic-loop` runs a bounded loop against a falsifiable invariant, `/skill:diagnose-loop-health` treats a loop that misbehaves, `/skill:feedback-sweep` and `/skill:figure-it-out` match work to a playbook.
- Steps only a human can take, such as credentials, dashboards, or a cutover: `/skill:wizard`. Long autonomous goal runs: `/skill:goal-prompt-drafting` drafts the objective. Records and contests: `/skill:show-me-your-work`, `/skill:append-run-log` (user only), `/skill:artifact-arena` (user only), `/skill:scheduler` (user only), and `/skill:guardrail-carve-run` for guardrail-adjacent runs.
