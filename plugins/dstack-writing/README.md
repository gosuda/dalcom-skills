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
| docs-update | Use when documentation has drifted from code changes and the user asks to synchronize. |
| docs-writing | Use when asked to write, restructure, or audit documentation with Diataxis types, or to draft a feature docs page or diagram source. |
| good-readme | Use when the user asks to create, rewrite, review, or polish an open-source README, including shop-window READMEs. |
| humaniseur-fr | Use when the user supplies French text that reads like AI output and asks to naturalize it. |
| humanizer-korean-plain | Use when Plain English·Plain Language 원칙으로 한국어 작성·교정·검토, 쉽게 써 줘·명확하게 고쳐 줘·관료적인 표현 줄이기·쉬운 한국어/plain Korean·독자 중심 설명문·이메일·공지·README용, 의미·조건·전문용어 보존, 엄격 통제·절차는 humanizer-korean-ste 우선, 원문보존·맞춤법만 요청 시 문체 유지 |
| humanizer-korean-ste | Use when Korean tech docs need unofficial ASD-STE controlled wording, single-step procedures, unified terms; not for plain readability (use humanizer-korean-plain), official or English STE. |
| humanizer-plain-english | Use when asked to make English plain, clear, natural, and readable while keeping its meaning and voice. |
| humanizer-simple-english-asd-ste100 | Use when asked to rewrite technical English for STE compliance, stripping ambiguity and AI-style patterns. |
| proof | Use when asked to publish, read, comment on, suggest to, or pull a Proof collaborative markdown document. |
| reorder | Use when asked to reorder a drifted listing under one stated principle, moving items only and rewording nothing. |
| rewrite-clean-v0 | Use when a document or file has been edited piecemeal and reads as sediment. |
| rhythmic-taste | Use when the user says "give this rhythm", "vary the structure", or "the sections all read the same". |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
