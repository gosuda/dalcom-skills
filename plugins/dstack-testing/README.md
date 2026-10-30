# DStack Testing

DStack workflows for tests, properties, mutation, and behavioral verification.

7 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-testing@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-testing@dstack
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-testing/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-testing:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| browser-qa | Use when the user runs /browser-qa for report-only QA results without entering a fix loop. |
| browser-testing | Use when building, debugging, or verifying browser-rendered code, or running browser tests for PR- or branch-affected pages. |
| control-cli | Use when asked to reproduce, profile, or verify CLI/TUI behavior. |
| control-ui | Use when asked to verify or reproduce browser or Electron UI behavior with before-and-after evidence and no leftover processes. |
| lighter-checks | Use when verification is looping, would re-run untouched code, or duplicates an established proof. |
| run-smoke-tests | Use when asked to run smoke tests or verify a local build, applying only minimal unblocking fixes. |
| writing-tla-plus-specs | Use when a protocol, concurrent algorithm, or design needs a model-checked TLA+ or Alloy spec, or a TLC or Apalache trace needs reading. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
