# DStack Knowledge

DStack workflows for memory, session continuity, decision records, and retrospectives.

8 skills, category Productivity. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-knowledge@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-knowledge@dstack
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-knowledge/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-knowledge:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| memory-clean | Use when a human asks to audit memory or find stale or duplicate memories. |
| memory-update | Use when the user explicitly says to save something to memory or scan this session for memories. |
| mutual-sync | Use when the user and agent may hold different pictures of current state after a gap, sync request, or exposed stale claim. |
| riffrec-feedback-analysis | Use when a Riffrec capture or other screen, voice, or notes artifact needs interpretation into bug or requirements evidence. |
| weekly-review | Use when asked to summarize authored work over the last week or a named date range, commit range, or branch. |
| work-records-summary | Use when the user asks to discover, group, and summarize work records across multiple systems for a given period or project. |
| workflow-evidence-mining | Use when authorized workflow history may contain a repeated process worth extracting and replay-testing. |
| workflow-from-chats | Use when a user asks to mine recent chats for workflow preferences. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
