# DStack Research

DStack workflows for source-backed investigation, verification, and design rationale. Install it with `claude plugin install dstack-research@dstack` in Claude Code or `codex plugin add dstack-research@dstack` in Codex; Claude Code invokes its skills as `/dstack-research:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- A named library or API is core `/skill:research`; the author follows it with `/skill:github-solution-research` when a bug, integration failure, or API question needs solutions others found.
- A thorough sourced report: `/skill:deep-research` (user only). How a code path works, gotchas included: `/skill:how`. Docs or plans that may have drifted from the code, or a stalled project to restart: `/skill:drift-detect`.
