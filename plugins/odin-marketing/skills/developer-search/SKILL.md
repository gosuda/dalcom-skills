---
name: developer-search
description: 'Use when mapping technical search opportunities by exact query, intent, and source evidence. Not for inventing search volume, rankings, or time-to-result promises.'
---

# Developer search

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks which technical queries to target and what page each needs. |
| Authority | Read-only. Public search evidence and supplied console or rank data only, treated as optional inputs. No credentials required, no rank guarantees. |
| Side effect | A search opportunity map in chat. Nothing else changes. |
| Done | Every row carries exact query, intent class, source evidence, recommended page type, competing answer, freshness trigger, and measurable success signal; no invented volume, ranking, traffic, or timeline remains. |

## Not for

- SEO deployment, page building, or vendor-automated campaigns. Rank trackers and consoles are optional evidence sources only.

## Inputs

- `queries` (required): candidate exact queries, or a topic the user authorizes for query discovery from public sources.
- `evidence` (optional): Search Console exports, rank-tracker data, or docs analytics the user supplies.

## Procedure

1. Record each exact query verbatim and classify intent: error-message, how-to, implementation, comparison, or reference. Keep intents distinct; they need different page types. **Done when:** every query has an intent class.
2. Attach source evidence per query: observed discussions, docs gaps, competing answers, or supplied console data with dates. **Done when:** every query has evidence or an explicit gap flag.
3. Recommend the page type per query (error reference, tutorial, comparison brief, API reference section) and name the competing answer it must beat fairly. **Done when:** each query maps to one page type and one named competitor answer.
4. Set freshness triggers (release cadence, API change, new error text) and a measurable success signal per row (indexed page,.docs click-through on a real path, resolved-question rate). **Done when:** each row has a trigger and a signal.
5. Purge invented numbers: volumes, rankings, traffic forecasts, and timelines appear only with an authoritative source and date, otherwise `UNVERIFIED` or omitted. **Done when:** no number lacks a source.

## Failure and recovery

- No evidence for a query: keep it as a candidate with the gap named, or drop it at user choice.
- Supplied console data unavailable: proceed on public evidence and mark rows accordingly.

## Output

A search opportunity map with exact queries, intent classes, evidence, page types, competing answers, freshness triggers, success signals, and the verification note on every number.
