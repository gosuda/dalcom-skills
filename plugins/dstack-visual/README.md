# DStack Visual

DStack workflows for diagrams, decks, canvases, and visual explainers.

3 skills, category Design. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-visual@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-visual@dstack

# Hermes Agent
hermes plugins install gosuda/dalcom-skills/plugins/dstack-visual --enable
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-visual/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-visual:<name>` in Claude Code, `$<name>` in Codex, `dstack-visual:<name>` in Hermes Agent, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| compile-3d-workflow | Use when the user asks for direction and a compilable 3D workflow from an interview. |
| pr-review-canvas | Use when asked to render a PR review as a Cursor Canvas artifact or a standalone HTML page served on localhost (mode: html), with risky hunks foregrounded. |
| pr-walkthrough | Use when a user asks for a zoomable PR map or graph-canvas orientation. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
