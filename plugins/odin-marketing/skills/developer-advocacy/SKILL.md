---
name: developer-advocacy
description: 'Use when preparing a conference talk, workshop, demo, podcast appearance, or building-in-public brief. Not for unsolicited pitches, submissions, or fabricated reach figures.'
disable-model-invocation: true
---

# Developer advocacy

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User names a public appearance or building-in-public effort and supplies the technical substance. |
| Authority | Read-only brief in chat. No unsolicited pitches, conference submissions, podcast outreach, recording, publishing, or fabricated attendee or reach figures. Explicit permission required before using names, quotes, or recordings. |
| Side effect | A brief the human submits or performs. Nothing submitted or recorded. |
| Done | Audience, problem, angle, takeaways, prerequisites, technical proof, and risk notes are present; every product claim is source-backed; permissions for names, quotes, and recordings are recorded. |

## Not for

- Submitting CFPs, contacting organizers, or publishing appearances. Preparation only; the human acts.

## Inputs

- `occasion` (required): talk, workshop, demo, podcast, or building-in-public series, with the venue or show where known.
- `material` (required): the technical substance with sources.
- `permissions` (optional): recorded consent for any named person, quote, or recording. Absence means do-not-use.

## Procedure

1. Fix audience, problem, angle, and the takeaways the audience keeps. **Done when:** each is singular enough to fit the slot length.
2. State prerequisites and setup the audience needs, including versions and fallback when live demo fails. **Done when:** prerequisites are complete and the fallback is written.
3. Back every product claim with a source; mark the rest unverified and cut or verify them. **Done when:** no claim lacks a source or a resolved flag.
4. Record permissions for names, quotes, customer stories, and recordings. Without permission the material stays out. **Done when:** each sensitive item has a permission record or is excluded.
5. Note risks: hostile questions, competitive framing, disclosure duties, NDA boundaries. **Done when:** each risk has a handling line.
6. Shape the brief to the occasion: CFP abstract shape, workshop timing, demo beats, podcast talking points, series cadence. **Done when:** the brief matches the occasion norms with reasons.

## Failure and recovery

- Permissions missing: exclude the material and note what permission would unlock it.
- Substance too thin for the slot: narrow the promise or name the missing proof.

## Output

An advocacy brief: audience, problem, angle, takeaways, prerequisites, technical proof with sources, permission records, risk notes, and the occasion-shaped plan.
