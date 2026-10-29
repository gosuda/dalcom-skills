---
name: content-evidence-brief
description: 'Use when designing a long-form marketing or developer content piece from a source pack before drafting. Not for publishing the article or cross-posting it.'
---

# Content evidence brief

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User supplies one topic or source pack plus a target reader and a useful outcome. |
| Authority | Read-only. Brief, outline, and evidence map in chat. No publishing, cross-posting, account use, or distribution action. |
| Side effect | An editorial brief the user can hand to a writing owner. Nothing published. |
| Done | Reader, situation, outcome, angle, evidence map, structure, section purposes, and unresolved gaps are stated; facts, firsthand experience, quotations, interpretation, and recommendation are separated; no publishable article is produced by default. |

## Not for

- Drafting the full article, publishing, or distributing it. Hand the approved brief to `technical-article-writer` or the relevant `odin-writing` owner.

## Inputs

- `topic` (required): the piece subject, or a source pack of supplied material.
- `reader` (required): one target reader in one situation.
- `outcome` (required): the one useful outcome the reader gets.
- `sources` (optional): approved sources or an explicit read-only research request.

## Procedure

1. Fix one reader, one situation, one outcome. Reject multi-reader briefs; split them. **Done when:** reader, situation, and outcome are each singular and explicit.
2. Map the evidence: list every usable fact, firsthand experience, quotation, and interpretation with its source. Mark gaps visibly. **Done when:** each evidence item carries a source or a gap flag.
3. Keep facts, experience, quotations, interpretation, and recommendation in separate labeled sections. Never silently turn one case into a general claim. **Done when:** no general claim lacks multi-case support stated beside it.
4. Derive structure from the material, not from a formula: choose the structure family and state each section purpose in one line. **Done when:** every section has a purpose tied to the reader outcome.
5. Add optional channel or format adaptations only as notes (length, code depth, visual needs), never as finished adaptations. **Done when:** adaptations are advisory and the master brief stands alone.
6. Run final QA: every factual claim traces to the source map; quotations are verbatim with provenance; gaps are visible; no invented data, quotes, or results. **Done when:** the QA checklist passes or the failing items are named.

## Failure and recovery

- Source pack too thin for the promised outcome: narrow the outcome or name the missing sources; do not pad with invention.
- Reader or outcome missing: ask once, stop until supplied.

## Output

An editorial brief: reader/situation/outcome, angle, evidence map with sources and gaps, structure family with section purposes, adaptation notes, and the QA record.
