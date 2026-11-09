# DStack Skills

DStack workflows for authoring, auditing, benchmarking, and publishing agent skills. Install it with `claude plugin install dstack-skills@dstack` in Claude Code or `codex plugin add dstack-skills@dstack` in Codex; Claude Code invokes its skills as `/dstack-skills:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- No skill seems to fit: core `/skill:skill-gap-finder` names the owner or writes a brief proving the gap.
- Writing a skill: core `/skill:writing-for-agents`, core `/skill:unslop`, a dstack-writing humanizer such as `/skill:humanizer-simple-english-asd-ste100`, `/skill:cascade-dedup` (user only) when the change touches doctrine shared across skills, then core `/skill:verification-before-completion` before the commit. dstack-planning `/skill:taste` checks the result for overkill.
- Tree upkeep: `/skill:dedup-skills` (user only), `/skill:cascade-dedup`, core `/skill:skill-scanner` for security, `/skill:review-plugin-submission` (user only) for marketplace readiness. New models: `/skill:model-retuning` (user only), `/skill:model-challenge` (user only). A personal taste skill: `/skill:generate-my-taste` (user only).
