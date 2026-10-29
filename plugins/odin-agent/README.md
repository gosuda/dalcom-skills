# ODIN Agent

ODIN workflows for configuring agent harnesses, MCP servers, and repository agent surfaces.

6 skills, category Productivity. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-agent@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-agent@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-agent/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-agent:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| agent-environment-retrospective | Use when a completed session needs an agent-environment retrospective. |
| agents-md | Use when a repo needs agent setup, AGENTS.md added or made lean, CLAUDE.md audited, or agent instructions scored or pruned. |
| ai-collab-protocols | Use when the user describes an AI workflow gap or uses an ambiguous cross-session reference such as 'the PR Bob mentioned'. |
| cli-for-agents | Use when asked to build or review a CLI intended for coding agents and return flag-driven, pipeline-safe, idempotent design advice. |
| inits | Use when onboarding to a repository, capturing costly conventions, constraints, or rationale, or improving AGENTS.md. |
| skill-doctor | Use when a user wants agent setup graded from conversation history. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
