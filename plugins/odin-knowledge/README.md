# ODIN Knowledge

ODIN workflows for memory, session continuity, decision records, and retrospectives.

19 skills, category Productivity. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-knowledge@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-knowledge@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-knowledge/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-knowledge:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| catchup | Use when the human returns after a gap, cannot follow the project, asks what happened, or wants a visual HTML recap page. |
| continual-learning | Use when asked to mine prior chats on a scheduled or watcher tick and maintain project memory. |
| docs-and-adrs | Use when making an architectural decision, changing a public API, shipping a feature, or recording a codebase term. |
| domain-modeling | Use when pinning down domain terminology, maintaining the domain model, or recording a glossary term or ADR. |
| explain | Use when a scoped question about how or why something has its current shape, or what happened over a work window, needs an evidence-grounded answer. |
| handoff | Use when work reaches a session boundary or the user asks to hand off, delegate, or get a clipboard-ready prompt. |
| history-source-registry | Use when a coding-agent session store is added or its format drifts, to document its layout, roles, quirks. |
| memory-clean | Use when a human asks to audit memory, find stale or duplicate memories, or needs tidy's ICM-state audit. |
| memory-update | Use when the user explicitly says to save something to memory or scan this session for memories. |
| mutual-sync | Use when the user and agent may hold different pictures of current state after a gap, sync request, or exposed stale claim. |
| recall | Use when asked to recover prior work and current status before resuming. |
| retro | Use when a finished session, period, milestone, or cycle needs an evidence-backed look-back, or an existing system needs its unexplained rationale recovered. |
| retune | Use when a skill corpus degrades on a new model and needs measurement-first retuning against a registered bar. |
| riffrec-feedback-analysis | Use when a Riffrec capture or other screen, voice, or notes artifact needs interpretation into bug or requirements evidence. |
| ssotize-audit-fold | Use when asked to find duplication, check consistency, establish or repair SSOT, consolidate facts, or when the user says "consolidate this" or "ssotize this". |
| weekly-review | Use when asked to summarize authored work over the last week or a named date range, commit range, or branch. |
| work-records-summary | Use when the user asks to discover, group, and summarize work records across multiple systems for a given period or project. |
| workflow-evidence-mining | Use when authorized workflow history may contain a repeated process worth extracting and replay-testing. |
| workflow-from-chats | Use when a user asks to mine recent chats for workflow preferences. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
