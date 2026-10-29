# ODIN TypeScript

ODIN workflows for modern TypeScript development.

5 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-typescript@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-typescript@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-typescript/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-typescript:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| node-internals-diagnosis | Use when Node.js segfaults, addon crashes, leaks, event-loop anomalies, thread-pool saturation, V8 deoptimizations, or binding.gyp failures need diagnosis. |
| nodejs-graceful-shutdown | Use when asked to implement or fix service termination: SIGTERM or SIGINT, connection draining, health-check signaling. |
| nodejs-service-foundations | Use when asked to set up or harden Node.js service foundations: env validation, logging, typed errors, type stripping, and shutdown wiring. |
| typescript-best-practices | Use when TypeScript needs shaping toward narrow types, unions, exhaustive variants, and strict flags. |
| typescript-type-hardening | Use when TypeScript has type errors, failing inference, or needs type mechanism repair (generics, infer, mapped, branded). |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
