---
name: developer-audience-context
description: 'Use when grounding developer marketing in a confirmed audience profile of persona, pains, alternatives, and trust signals. Not for inventing quotes, benchmarks, or audience facts.'
---

# Developer audience context

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to define, update, or apply a developer audience profile for marketing work. |
| Authority | Read-only. Chat output only. No file writes, no canonical store, no credentials, no outreach, no publication. Optional public source reads. |
| Side effect | An audience profile in chat that the user may supply as evidence to other work. Nothing stored or changed. |
| Done | All ten dimensions are present or explicitly marked unknown; every factual claim and quote carries provenance; no invented quotes, testimonials, benchmarks, user counts, or audience facts remain; no file was created. |

## Not for

- Writing or maintaining a shared context file. There is no canonical audience store. Every other marketing skill accepts supplied sources directly and MUST NOT require any artifact from this skill.
- Prescribing voice or tone. Voice prescription stays with `copywriting-tone-of-voice-creator` and the `copywriting` voice chart; this skill owns observed audience evidence only, and references `TONE.md` or `VOICE.md` as completed input without writing them.

## Inputs

- `product` (required): what is offered, in the user own words or supplied docs.
- `evidence` (required): supplied docs, READMEs, issues, docs pages, or explicitly requested read-only research. Tool mentions (search consoles, rank trackers, listeners) are optional evidence inputs, never required dependencies.

## Procedure

1. Collect the ten dimensions: product, persona, places, problems, alternatives, differentiators, verbatim language, trust signals, conversion actions, voice observations. **Done when:** each dimension is filled from evidence or marked unknown.
2. Record provenance per item: source and observation date. Verbatim language must be exact quotes with sources; never paraphrase into quotation marks. **Done when:** every claim and quote traces to a source or an explicit unknown.
3. Check trust signals against reality: docs quality, examples that run, error coverage, maintenance signs, license clarity. **Done when:** each trust signal cites an observed artifact.
4. State conversion actions as observed or plausible paths, never as guaranteed funnels. **Done when:** each action names its evidence or its assumption flag.
5. Voice observations describe how the audience speaks; they do not instruct how the brand speaks. **Done when:** no voice prescription appears.
6. Present the profile in chat only. Never create a file, store, or canonical path. **Done when:** the artifact is delivered in chat and the working tree is untouched.

## Failure and recovery

- Evidence too thin: deliver the profile with unknowns explicit and name the smallest evidence that would fill each gap.
- Fictional example material supplied as format reference: use its shape only; never copy its testimonials, numbers, or names as facts.
- Unverifiable numeric claims (audience sizes, conversion benchmarks): mark `UNVERIFIED` or omit; never preserve them as defaults.

## Output

An audience profile in chat covering the ten dimensions with per-item provenance, explicit unknowns, and verbatim quotes with sources. No other skill requires this output; it is one optional input among supplied sources.
