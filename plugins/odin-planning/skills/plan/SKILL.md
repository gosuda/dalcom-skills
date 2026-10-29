---
name: plan
description: 'Use when multi-step work needs a structured implementation plan that preserves outcomes and constraints. Not for exploratory framing, executing the work, or running tests to learn from results.'
---

# Plan the work

Anchors: David Parnas (HOW the work is built is decided once, from evidence, before execution), Dieter Rams (a plan earns length only through decisions execution cannot invent).

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user or a calling workflow asks to plan, break down, deepen, or continue planning multi-step work, including software and non-software tasks. |
| Authority | Research, decision, and plan writing only. No production code changes, test execution, environment setup, VCS, credential, paid, published, deployed, remote, or destructive mutation. Directional pseudocode or grammar sketches may communicate design; changing code to see what happens belongs to execution. |
| Side effect | A decision-explicit plan at the selected output contract with sources, depth, and handoff. |
| Done | The output contract done condition holds: direct states the change with its handoff, chat brief delivers with its save-or-execute offer, durable presents the handoff menu and fires the selected action; a pipeline run additionally returns plan, confidence, and review state to its caller. Writing, confidence, and an offered document review are milestones, never the completion claim by themselves. |

## Inputs

- The goal, requirements path, existing plan path to deepen, or task statement. Required.
- Output preference when supplied. Contracts: direct (statable, doable, and verifiable in one pass with no user-weighable decision), chat brief (bounded with at most one user-weighable decision and no risk surface), durable (everything else). Required to decide during scoping from bounded inline reads without dispatching workers.

An explicit invocation always produces a plan. Never classify a direct request as not-a-planning-task and route out. When the tier is uncertain after scoping reads, take the heavier one. A surfaced decision, risk surface (auth, payments, migrations, external contracts), or multi-pass verification moves the run heavier before emitting anything.

## Procedure

1. Establish output, resume, and scope. Resolve the output contract first. Resume or deepen an existing plan in place preserving stable IDs; enrich requirements-only material without minting a parallel plan. Find and preserve the upstream artifact; never plan past an unreached bootstrap prerequisite. Ask blocking questions through the available question facility (one at a time); without one, render numbered choices. When no feature description was supplied, ask what to plan and wait.
2. Research from evidence. Read the smallest deciding surfaces: entry points, definitions, callers, tests, schemas, configuration, and existing patterns. Distinguish inspected facts from proposed changes. Use separable read-only workers only for genuinely separable uncertainties; the coordinator reconciles with evidence and gaps. Never reconstruct a missing required reference from memory: stop before the action it governs and report the blocker with recovery.
3. Decide and structure. Resolve technical choices from the objective, constraints, inspected evidence, and conventions. Prefer the smallest coherent reliable design. Record the chosen design with its concrete reason; keep rejected alternatives only when the rejection explains a boundary. Evidence that invalidates an earlier settled decision stops the write and returns the exact invalidation with reason instead of resolving it silently.
4. Compose at the contract. Direct: the change with its handoff offer. Chat brief: the brief with its one-line save-or-execute offer. Durable: the full plan with requirements trace, structure, verification sketch naming concrete checks (never generic run-tests text and never an invented command), and failure handling. Write the plan before presenting options, then complete confidence.
5. Offer document review for durable plans; do not require it. The default offer is non-interactive review of the durable plan. When accepted, incorporate the result; when declined or unavailable, record the limit and continue. Completion never claims review that did not run.
6. Hand off explicitly. In interactive runs ask what to do next with the plan path and act only on the selected action. In pipeline runs return the plan, confidence, and review state for the caller to decide. Rendering a menu, receiving a selection, or announcing a route is not completion until the selected action fires.

## Failure and recovery

- Missing goal or unreadable source: blocked with what is missing and recovery. Invent no scope.
- Required reference unreadable: stop before the governed action; in pipeline return blocked with phase, blocker, recovery path, and any preserved artifact.
- Conflicting requirements or unreachable prerequisite: finish reachable sections, then return explicitly incomplete with the conflict, sources, affected decisions, and needed access.
- User withholds a needed decision: preserve settled work and return incomplete; never assume.
- Explicit limit reached: stop incomplete with evidence; limit exhaustion is not success.

## Output

Return the plan (inline, brief, or path), the output contract selected with why, confidence state, document-review state (completed, declined, or unavailable), and the explicit handoff. No execution follows from planning alone.
