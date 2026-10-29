---
name: developer-lifecycle-messaging
description: 'Use when drafting consent-segmented newsletter, onboarding, activation, or re-engagement messages from real product behavior. Not for sending, list imports, or unsolicited win-back.'
disable-model-invocation: true
---

# Developer lifecycle messaging

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks for newsletter, onboarding, activation, release-update, or re-engagement drafts for developers. This is the owner of onboarding messaging drafts; onboarding implementation stays with product and DX owners. |
| Authority | Read-only drafting in chat. Consent-segmented: audience segment, suppression, stop-on-activation, unsubscribe mechanics required per draft set. No sending, list import, personal-data enrichment, unsolicited win-back, or vendor dependency. |
| Side effect | Drafts with cadence, suppression, and factual-claim records in chat. Nothing sent or stored remotely. |
| Done | Each draft has subject, body, segment, cadence, suppression and stop conditions, unsubscribe path, and claim provenance; churn diagnosis stays a separate product-feedback concern and no win-back contacts the unconsented. |

## Not for

- Sending, scheduling, or managing lists. Drafts only; the human sends through approved systems.

## Inputs

- `purpose` (required): newsletter issue, onboarding step, activation nudge, release update, or re-engagement, with the triggering behavior.
- `segment` (required): who receives it and what consent covers them.
- `evidence` (required): the real product behavior, docs path, or release fact behind the message.

## Procedure

1. Fix purpose, segment, and consent basis. State suppression (who must not receive it) and stop-on-activation conditions. **Done when:** segment, consent, suppression, and stop conditions are written.
2. Draft subject and body in plain developer language: one message per draft, outcome first, exact next step with path or command. **Done when:** each draft has one message and one next step.
3. For onboarding and activation drafts, map each message to the product step it unblocks (signup, first key, first call, first deploy) without owning that step implementation. **Done when:** every onboarding message names its unblocked step and the owning surface.
4. Record factual-claim provenance per draft: every claim beside its source. **Done when:** no claim lacks a source.
5. Set cadence and unsubscribe mechanics: frequency cap, sequence length, exit on activation, one-step unsubscribe. **Done when:** each draft set has caps, exits, and unsubscribe.
6. Refuse unsolicited win-back and enrichment: no reactivating the unconsented, no list imports, no personal-data enrichment. **Done when:** no draft targets a segment without stated consent.

## Failure and recovery

- Consent basis missing: stop and name it; do not draft around it.
- Evidence missing for the promised outcome: narrow the promise or name the missing proof.

## Output

Draft set with subjects, bodies, segments, consent and suppression records, cadence and stop conditions, unsubscribe paths, onboarding step mapping, and claim provenance.
