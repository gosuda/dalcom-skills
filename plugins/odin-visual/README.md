# ODIN Visual

ODIN workflows for diagrams, decks, canvases, and visual explainers.

3 skills, category Design. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-visual@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-visual@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-visual/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-visual:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| compile-3d-workflow | Use when the user asks for direction and a compilable 3D workflow from an interview. |
| pr-review-canvas | Use when asked to render a PR review as a Cursor Canvas artifact or a standalone HTML page served on localhost (mode: html), with risky hunks foregrounded. |
| pr-walkthrough | Use when a user asks for a zoomable PR map or graph-canvas orientation. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
