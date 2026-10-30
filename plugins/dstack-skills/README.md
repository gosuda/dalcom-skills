# DStack Skills

DStack workflows for authoring, auditing, benchmarking, and publishing agent skills.

8 skills, category Productivity. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-skills@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-skills@dstack
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-skills/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-skills:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| cascade-dedup | Use when prompt-doctrine is duplicated, drifted, or conflicting across output-style embeds and external harness AGENTS files. |
| dedup-skills | Use when asked to deduplicate a skill tree, fold overlapping skills, or cut the skill count: analyze, gate per family, then fold. |
| generate-my-taste | Use when asked to generate a personal taste skill from local evidence. |
| model-challenge | Use when a user requests an independent Codex or Gemini review of uncommitted code, a branch diff, or a specific commit. |
| model-retuning | Use when asked to run /model-retuning to retune a skill corpus for a new model, measurement-first. |
| review-plugin-submission | Use when asked to review a plugin for marketplace readiness via a read-only audit of published quality gates. |
| skill-gap-finder | Use when the user suspects no installed skill covers a task and wants proof. |
| skill-scanner | Use when a user asks to scan, audit, or validate a skill for security issues. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
