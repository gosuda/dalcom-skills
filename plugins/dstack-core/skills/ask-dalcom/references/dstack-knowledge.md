# DStack Knowledge

DStack workflows for memory, session continuity, decision records, and retrospectives. Install it with `claude plugin install dstack-knowledge@dstack` in Claude Code or `codex plugin add dstack-knowledge@dstack` in Codex; Claude Code invokes its skills as `/dstack-knowledge:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- After a gap or a stale claim, sync what you and the agent each believe: `/skill:mutual-sync`.
- Memory files: `/skill:memory-update` (user only) saves, `/skill:memory-clean` (user only) audits. Look back over work: `/skill:weekly-review` (user only), `/skill:work-records-summary` (user only). Turn history into workflows: `/skill:workflow-evidence-mining` (user only), `/skill:workflow-from-chats` (user only). Screen, voice, or notes captures: `/skill:riffrec-feedback-analysis`.
