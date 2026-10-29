# ODIN Release

ODIN workflows for cutting, gating, publishing, and announcing releases.

4 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-release@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-release@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-release/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-release:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| license-compliance-audit | Use for a read-only audit of LICENSE, NOTICE, and source-file SPDX headers. |
| merge-and-deploy | Use when a human runs /merge-and-deploy to merge a PR and trigger or verify deployment. |
| open-source-license-selection | Use when the user asks to choose, reconcile, or apply an open-source license and package metadata. |
| release-landing-report | Use when the user runs /release-landing-report to summarize landed changes and return a landing summary report. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
