# DStack Code

DStack workflows for writing, changing, and simplifying code. Install it with `claude plugin install dstack-code@dstack` in Claude Code or `codex plugin add dstack-code@dstack` in Codex; Claude Code invokes its skills as `/dstack-code:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- Structural search or a codemod where regex is too fragile: `/skill:ast-grep`.
- Dependency upgrades, CVE sweeps, and major releases: `/skill:deps-upgrade`; the author runs core `/skill:ground-latest` with it to pick the target versions.
- Units, rates, money, or fixed point: `/skill:dimensional-analysis`. A first screen that ships too many bytes: `/skill:first-load-byte-reduction` (user only). A question bounded by one symbol, path, or line range: `/skill:slicing-code-context`.
