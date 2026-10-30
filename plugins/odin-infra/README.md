# ODIN Infra

ODIN workflows for CI, deployment, observability, cost, and infrastructure tooling.

5 skills, category Infrastructure. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-infra@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-infra@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-infra/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-infra:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| ci-cd | Use when setting up or modifying CI/CD pipelines, quality gates, test runners, or deployment pipeline configuration through workflow files. |
| environment-contract-audit | Use when environment-dependent code, templates, or deployment configuration changes, or when runtime configuration is missing. |
| observability | Use when adding telemetry, composing an observability surface, reviewing alerts, shipping a production feature, or diagnosing a production issue. |
| terraform-style-check | Use when writing, reviewing, or generating Terraform HCL that must pass fmt and validate. |
| workflow-capacity-audit | Use for a read-only audit of CI workflow capacity, duplication, queue time, runner compatibility, and required-check safety. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
