# DStack Writing

DStack workflows for documentation, editorial prose, and copy.

14 skills, category Writing. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-writing@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-writing@dstack
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-writing/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-writing:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| articulate | Use when the user knows what they mean but cannot express it completely or clearly. |
| copywriting | Use when asked to write or fix product/marketing copy, landing pages, UI strings, brand voice, AI tells, an end-of-article CTA, or a hook/lede. |
| docs-update | Use when documentation has drifted from code changes and the user asks to synchronize it. |
| docs-writing | Use when asked to write, restructure, or audit documentation with Diataxis types, or to draft a feature docs page or diagram source. |
| good-readme | Use when the user asks to create, rewrite, review, or polish an open-source README. |
| humaniseur-fr | Use when the user supplies French text that reads like AI output and asks to naturalize it. |
| humanizer-korean-plain | Use when Korean prose reads as AI-generated, translated, or bureaucratic and needs plain, natural Korean while keeping meaning. |
| humanizer-korean-ste | Use when Korean technical documents such as runbooks, procedures, manuals, or operating guides need controlled wording: one action per step, conditions before actions, unified terms, and warnings placed before risky steps. |
| humanizer-plain-english | Use when asked to make English plain, clear, natural, and readable while keeping its meaning and voice. |
| humanizer-simple-english-asd-ste100 | Use when asked to rewrite technical English toward ASD-STE100 Simplified Technical English: short, unambiguous sentences, one instruction per step, consistent terms, and AI-style padding removed. |
| proof | Use when asked to publish, read, comment on, suggest to, or pull a Proof collaborative markdown document. |
| reorder | Use when asked to reorder a drifted listing under one stated principle, moving items only and rewording nothing. |
| rewrite-clean-v0 | Use when a document or file has been edited piecemeal and reads as sediment. |
| rhythmic-taste | Use when the user says "give this rhythm", "vary the structure", or "the sections all read the same". |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
