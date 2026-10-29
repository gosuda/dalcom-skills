---
name: plan
description: 'Use when multi-step work needs a structured implementation plan that preserves outcomes and constraints. Not for exploratory framing, executing the work, or running tests to learn from results.'
---

# Plan

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to plan, break down, deepen, or continue planning multi-step work, or execution cannot proceed without a decided plan. |
| Authority | Research, decision, and plan writing only. No code changes, test execution, environment setup, VCS, credential, paid, published, deployed, remote, or destructive mutation. Sketches communicate design; changing code to see what happens belongs to execution. |
| Side effect | A decision-explicit plan at the selected contract with sources and handoff. |
| Done | direct states the change with handoff; brief delivers with save-or-execute offer; durable presents the handoff and fires the selected action. Writing alone is never done. |

## Inputs

- Goal, requirements path, existing plan path to deepen, or task statement.
- Output contract decided from bounded inline reads without dispatching workers: direct (statable, doable, verifiable in one pass, no user-weighable decision), brief (bounded, at most one user-weighable decision, no risk surface), durable (everything else). Uncertain tier takes the heavier one; any surfaced decision, risk surface, or multi-pass verification moves heavier before emitting.

## Guards

- Reuse valid existing spec or plan: resume or deepen in place preserving stable IDs; never mint a parallel plan; never plan past an unreached bootstrap prerequisite.
- Separate inspected facts from proposed changes in every section.
- State the bounded consumer and the invariants and bounds the plan must hold; a plan without both is not emittable.
- Default clean replacement: migrate every caller in the same change; leave no obsolete paths, shims, or aliases.
- UI scope states places, affordances, and connections only; never pixel positions, field lists, or ticket breakdowns.
- Name concrete verification per claim against reusable inputs; never generic run-tests text, never an invented command, dependency, or unsupported claim; never assert fixture-oracle content.
- No deferred scope: no TODO, future-work, or placeholder passes as complete; unfinished returns incomplete with blocker and recovery.
- Missing or unreadable required reference stops the governed action: report blocker with recovery; never reconstruct it from memory.
- Evidence invalidating a settled decision stops the write: return the invalidation with reason instead of resolving it silently.
- Ask only for a decision blocking progress; never interrogate by default; never route an explicit planning request out as not-a-planning-task.
- Prefer inline over a new file; a durable artifact uses a human-readable semantic name with no IDs or date prefixes.

## Failure and recovery

- Missing goal or unreadable source: blocked with what is missing and recovery; invent no scope.
- Required reference unreadable: stop before the governed action; report phase, blocker, recovery, and preserved artifact.
- Conflicting requirements or unreachable prerequisite: finish reachable sections, return explicitly incomplete with conflict, sources, affected decisions, and needed access.
- Withheld decision or limit reached: preserve settled work, return incomplete; limit exhaustion is never success.

## Output

Return the plan (inline, brief, or path), contract selected with why, confidence, document-review state (completed, declined, or unavailable), and the explicit handoff. Never claim review that did not run.
