---
name: competitive-content
description: 'Use when preparing an honest alternative or comparison page brief or draft from source-backed claims. Not for false claims, implied endorsement, or uncited testimonials.'
disable-model-invocation: true
---

# Competitive content

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks for an alternative or comparison page against named competitors. |
| Authority | Read-only drafts in chat. No publication, no trademark-domain tactics, no keyword bidding, no logo or endorsement implication. Explicit human approval before any handoff to a writing or design owner. |
| Side effect | A comparison brief or draft plus a legal-review flag list in chat. Nothing published. |
| Done | Every comparison claim traces to product documentation or a cited observation; competitor strengths are stated honestly; migration guidance, update date, and legal flags are present; no false claim, implied endorsement, unlicensed asset, or uncited testimonial remains. |

## Not for

- Live comparison pages or SEO deployment. Hand the approved brief to `copywriting` for final copy; page build and deployment belong elsewhere.

## Inputs

- `subject` (required): the product and the named alternatives being compared.
- `evidence` (required): product docs, competitor docs, and cited observations with dates.
- `migration` (optional): known migration paths, limits, and rollback notes.

## Procedure

1. Build the comparison table with nuanced states (full, partial, beta, not available, unknown) instead of checkmark binaries. **Done when:** every cell has a state plus its source.
2. State competitor strengths honestly alongside gaps. **Done when:** each compared alternative has at least one fairly stated strength with a source.
3. Write migration guidance: path, effort, limits, rollback. **Done when:** migration states its limits or marks them unknown.
4. Stamp the update date and the recheck trigger per volatile claim. **Done when:** every volatile claim has a date and a recheck condition.
5. Flag legal review triggers: trademarks, logos, endorsement language, performance claims. **Done when:** each trigger names the exact passage and the question for review.
6. Verify: no false claims, no implied endorsement, no unlicensed logos, no uncited testimonials, no dependency on missing upstream pages. **Done when:** the verification pass names its result per risk.

## Failure and recovery

- Evidence missing for a material claim: mark unknown or drop the claim; never assert it.
- Legal flag cannot be cleared here: keep the flag and stop that passage; the page ships around it only after human legal review.

## Output

A comparison brief or draft with a sourced table, honest strengths, migration path, update date, legal-review flags, and the verification record.
