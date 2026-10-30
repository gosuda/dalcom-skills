# ODIN Research

ODIN workflows for source-backed investigation, verification, and design rationale.

4 skills, category Research. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-research@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-research@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-research/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-research:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| deep-research | Use when the user asks to research a topic and produce a thorough sourced report. |
| drift-detect | Use when roadmap, plans, or docs may have drifted from code, or when restarting a stalled project. |
| github-solution-research | Use when a bug, integration failure, dependency issue, unclear API usage, implementation blocker, or tool-capability need calls for GitHub solutions. |
| how | Use when the user asks "how does X work" and wants an architecture walkthrough of the code path or subsystem, including its gotchas. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
