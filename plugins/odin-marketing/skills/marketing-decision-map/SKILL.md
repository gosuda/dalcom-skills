---
name: marketing-decision-map
description: 'Use when a marketing initiative is too broad for a brief and needs its decisions charted before action. Not for executing the selected strategy or tracking tasks.'
---

# Marketing decision map

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User names an unclear marketing initiative plus an observable destination. |
| Authority | Read-only by default. Writes a map file only when the user explicitly names a writable path. No credentials, publication, outreach, or remote mutation. |
| Side effect | A decision map in chat, or at the named path when requested. Nothing else changes. |
| Done | Destination, constraints, confirmed decisions, current frontier, blocked questions, fog, and out-of-scope boundary are stated; at most one consequential decision is resolved per continuation; no recommendation is recorded as a decision without user confirmation. |

## Not for

- Executing the selected strategy, running campaigns, or tracking production tasks.
- Wayfinding for non-marketing planning; that belongs with general planning owners.

## Inputs

- `initiative` (required): the unclear marketing effort to chart.
- `destination` (required): the observable outcome the map points at.
- `context` (optional): current user instructions and explicitly selected project material. Supplied, never inferred into a file.
- `output_path` (optional): writable path for the map. Chat-only when omitted.

## Procedure

1. Fix the destination in observable terms and record standing constraints and notes. **Done when:** destination and constraints are written and observable.
2. Sort what is known into confirmed decisions, current frontier (answerable now), blocked questions (prerequisite missing), fog (unknown and currently unknowable), and out of scope. **Done when:** every item sits in exactly one bucket.
3. Apply only materially relevant lenses: outcome, market, audience, problem, value, position, journey, channel, expression, economics, measurement, risk. Skip lenses with no bearing and say so. **Done when:** used lenses are named; skipped lenses are named with a reason.
4. In chart mode, stop before resolving the first consequential decision and present the map. **Done when:** the map is presented with an untouched frontier.
5. In continue mode, resolve exactly one frontier decision: state the options, the evidence, the recommendation, and ask for confirmation. Record it as a decision only on explicit user confirmation. **Done when:** zero or one decision is confirmed and recorded as user-confirmed.
6. Never convert the map into a task tracker or production plan. **Done when:** the output contains no tasks, owners, or dates beyond decision sequencing.

## Failure and recovery

- No observable destination: stop and ask for one; do not chart motion as progress.
- Material conflict in supplied context: stop, name the conflict, do not resolve by assumption.
- Partial result: present the charted portion, mark the uncharted remainder as fog.
- No mutation on failure; chat output only unless a path was already approved for a completed map.

## Output

A decision map: destination, notes and constraints, confirmed decisions (each marked user-confirmed with its basis), current frontier, blocked questions with prerequisites, fog, out-of-scope boundary, and the single next decision when in continue mode.
