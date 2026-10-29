---
name: open-source-adoption
description: 'Use when planning open-source adoption through README quality, contributor funnel, and sustainable maintenance. Not for fake stars, coordinated votes, or fabricated metrics.'
---

# Open source adoption

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks how an open-source project earns users and contributors. |
| Authority | Read-only planning in chat. No fake stars, coordinated upvotes, fabricated downloads, astroturfing, automated release promotion, or contributor quotas. |
| Side effect | An adoption plan in chat. No repository or remote changes. |
| Done | README and quickstart, contributor funnel from user to maintainer, issue and PR onboarding, launch sequence, maintenance expectations, and value metrics are present; every health claim traces to repository facts. |

## Not for

- Growth hacking or metric fabrication. The funnel is user, star, issue, PR, regular contributor, maintainer, earned step by step.

## Inputs

- `repo` (required): the project with its actual current state (README, license, contributing docs, issue and PR posture).
- `capacity` (optional): maintainer time available. Defaults to a low sustainable band when omitted.

## Procedure

1. Assess the README and quickstart against a first-time contributor walk: install, run, change one thing. **Done when:** each walk step has a pass or gap finding with the path cited.
2. Map the contributor funnel with the real entry points: good first issues, docs fixes, discussion venues, review turnaround the team can sustain. **Done when:** each funnel stage names its real pathway or its absence.
3. Design issue and PR onboarding: templates, labels, response expectations the stated capacity can meet. **Done when:** expectations fit the stated capacity.
4. Plan the launch sequence: order of surfaces, readiness per surface, and what must be true before each (never coordinated voting or brigade behavior). **Done when:** each surface has readiness criteria.
5. State maintenance expectations honestly: cadence, support scope, sunset signals. **Done when:** promises fit capacity and sunset signals are named.
6. Set value metrics from observable facts (merges from newcomers, time to first contribution the team already measures, docs-driven arrivals). **Done when:** each metric names its existing measurement source.

## Failure and recovery

- Capacity too thin for the ambition: cut the plan to the sustainable core and name the cut.
- License or health claims unverifiable: mark unknown; do not assert a clean bill of health.

## Output

An adoption plan: README and quickstart findings, contributor funnel with real pathways, issue and PR onboarding, launch sequence with readiness gates, maintenance expectations, and value metrics.
