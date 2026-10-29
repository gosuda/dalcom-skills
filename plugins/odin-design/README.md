# ODIN Design

ODIN workflows for interface design, prototypes, and visual fidelity.

9 skills, category Design. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-design@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-design@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-design/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-design:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| design | Use when starting UI work, defining palettes or tokens, fixing AI-generic UI, or persisting a design system to DESIGN.md (modes: implement, persist). |
| design-gate-brainstorming | Use when creative work is requested with no approved design, or a raw idea or repository must be developed into an approved design document. |
| final-grain | Use when asked to push an already-working artifact to finished composition, texture, and feel. |
| fixed-view-visual-benchmark | Use when a visual needs repeatable fixed-view rendering and independent rubric scoring. |
| frontend-fidelity-rebuild | Use when an authorized reference surface needs a clean-room frontend reconstruction across static, motion, and responsive fidelity. |
| frontend-ui-engineering | Use when asked to build or modify production-quality components, layouts, state, and pages with WCAG 2.1 AA and real content. |
| prototype | Use when committing the wrong product answer would be expensive to unwind and a cheap sketch cannot settle how it should work, feel, or read. |
| thumbnail-accuracy-scorecard | Use when thumbnail concepts need real-size, accuracy-first scoring without misleading claims. |
| ui-animation | Use when asked to build spring, easing, gesture, and choreographed animations with correct physics and reduced-motion support. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
