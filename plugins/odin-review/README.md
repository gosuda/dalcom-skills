# ODIN Review

ODIN workflows for reviewing diffs, branches, and implementations against their specs.

7 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-review@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-review@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-review/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-review:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| interrogate | Use when asked to "interrogate" or run an adversarial multi-model review of a supplied code artifact. |
| no-hide | Use when the user asks to detect clever-concealment patterns that obscure real code structure. |
| perspective-complete-review | Use when one named review viewpoint must run fix cycles until a fresh reviewer finds nothing. |
| pr-impact-quiz | Use when the user invokes this skill to generate targeted questions proving the author understands the change's codebase effect. |
| review | Use when asked to review a pull request or merge request, examine code changes, find bugs, or audit a branch, in standard or depth mode. |
| show-review | Use when the user wants a per-finding visual walk through a diff, PR, or MR. |
| visual-diff-review | Use when asked to review a diff and produce a 7-section visual page. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
