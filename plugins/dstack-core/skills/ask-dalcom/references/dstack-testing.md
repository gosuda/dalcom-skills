# DStack Testing

DStack workflows for tests, properties, mutation, and behavioral verification. Install it with `claude plugin install dstack-testing@dstack` in Claude Code or `codex plugin add dstack-testing@dstack` in Codex; Claude Code invokes its skills as `/dstack-testing:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- Browser-rendered code: `/skill:browser-testing` builds and runs tests; `/skill:browser-qa` (user only) reports without fixing.
- CLI or TUI behavior with evidence: `/skill:control-cli`; UI behavior before and after: `/skill:control-ui`; a local build smoke test: `/skill:run-smoke-tests` (user only).
- Verification that keeps re-running untouched code: `/skill:lighter-checks`. Protocols and concurrent algorithms: `/skill:writing-tla-plus-specs`.
