# DStack Code

DStack workflows for writing, changing, and simplifying code.

5 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-code@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-code@dstack

# Hermes Agent
hermes plugins install gosuda/dalcom-skills/plugins/dstack-code --enable --force
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-code/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-code:<name>` in Claude Code or Hermes Agent, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| ast-grep | Use when asked to run AST-based structural search, lint, or rewrite of code when regex is too fragile. |
| deps-upgrade | Use when dependency upgrades need batching for CVEs, a major release, forced compatibility, a scheduled or vulnerability-triggered sweep. |
| dimensional-analysis | Use when code mixes units, fixed-point precisions, scaling factors, rates, prices, shares, or conversions. |
| first-load-byte-reduction | Use when a first screen needs lower transfer bytes without visual or behavioral change. |
| slicing-code-context | Use when an exact symbol, path, entrypoint, or line range can bound a focused code question or patch proposal under a fixed source budget. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
