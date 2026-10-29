---
name: spec-driven
description: 'Use when starting a project or feature, requirements are unclear, or a change crosses modules. Accepts new specs and already-approved specs via the existing-spec entry.'
---

# Spec-driven development

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A new project or feature is starting, requirements are unclear, the change touches multiple modules, or the task exceeds roughly 30 minutes. |
| Authority | Reversible local: writes only files and VCS scoped to the current working tree; rollback is version control. No remote mutation, credential exposure, or irreversible action. |
| Side effect | Writes and commits a spec, records human-approved plan and tasks, and implements through offensive-first tests. All writes are local; no external service calls. |
| Done | A reviewed, approved spec covering six areas is saved to the repo and the implementation follows it. |

## Inputs

- The user request (required). The requester must approve the spec before planning begins.
- The scope anchor (required): the module, package, or directory boundary the work affects.

## Procedure

1. Check scope before specifying. Most requests describe one capability; specify directly for those. Decompose first only when one requirement bundles several independently testable capabilities: distinct capabilities with their own consumers or data, acceptance criteria that cluster into separately shippable groups, or one capability that could be cut without rewriting the others. Propose a small capability map with a module table and build order, stable kebab-case module ids chosen once, one-way dependency arrows with no cycles, and contracts living in the provider module spec. Save the approved map at the project root and name each module spec after its id. Done when: a single-capability request proceeds directly, or a multi-capability map with boundaries, direction, and build order is approved before any module spec.
2. Surface assumptions first. List every assumption being made and require explicit correction. Do not silently fill ambiguous requirements. Done when: every assumption is listed and corrected or confirmed.
3. Write the spec covering six core areas. Objective states what is being built and why, who the user is, and what success looks like. Commands record full executable commands with flags for build, test, lint, and dev for the stack the project actually uses. Project structure captures where source, tests, and docs live. Code style shows one real snippet in the project language with naming and formatting rules. Testing strategy sketches the seams where the feature will be tested, prefers an existing seam over a new one, and records framework, locations, coverage expectations, and which level covers each concern. Boundaries use three tiers: always do, ask first, and never do. Keep the artifact format the project already uses when one exists; this skill owns clarification, content, and approval gates, not the external tool format. Reframe vague requirements as testable success criteria and confirm the targets. Done when: all six areas are written with testable success criteria.
4. Present the spec to the human. Do not advance until the human reviews and approves it. Once the spec is saved, summarize it, list open questions, and stop the turn. Do not start planning or code in the same turn. Done when: the human approves the spec in a later turn.
4a. **Existing approved spec entry.** When the invocation supplies an already-approved spec, skip steps 1–4 and enter at step 5 (Plan from the validated spec). Map every requested behavior to at least one spec statement; list each unmapped request as a spec gap and stop until the gap is approved as a spec addition. Align implementation to the spec; when a decision changes, update the spec first. A spec may describe approved new behavior that contradicts current implementation — that is a migration directive, not a conflict to surface-and-stop. Never treat a previously pushed commit as exhausting authority for new reversible local edits.
5. Plan from the validated spec. Identify major components and dependencies, determine implementation order, note risks and mitigations, separate parallel from sequential work, and define verification checkpoints between phases. Done when: the plan is written.
6. Present the plan to the human. Do not advance until the human reviews and approves it. Done when: the human approves the plan.
7. Break the plan into discrete tasks. Each task completes in one focused session, has explicit acceptance criteria, includes a verification step with test, build, or manual check, is ordered by dependency, and touches no more than about five files. Done when: the task list is written.
8. Present the task list to the human. Do not advance until the human reviews and approves it. Done when: the human approves the task list.
9. Implement through offensive-first tests, one task at a time. For each task turn its acceptance criteria into attacks that must fail red for the right reason, implement until the attacks stop breaking the code, and never bend a test or fixture to reach green. Load only the spec sections and source files the current task needs. Done when: every task is implemented and verified against its acceptance criteria.
10. Keep the spec alive. When decisions or scope change, update the spec first, then implement. Commit the spec to version control alongside the code. Reference the spec section each change implements. Done when: the spec reflects the current decision and is committed.

## Failure and recovery

- Human withholds approval: do not proceed to the next phase. Surface the specific objection and wait.
- Scope widens mid-implementation: stop. Return to the spec. Update it, get approval, then proceed.
- Assumption surfaces after the spec is written: surface it immediately; do not proceed until the human resolves or approves it.
- No spec written or saved: the done predicate is not met. Implement nothing until the spec exists and is approved.
- One spec spans several independently testable capabilities without an approved map: stop and map first. Module boundaries decided during implementation are not approved.
- Non-converged: when the human never approves, the skill ends with no implementation. State this outcome explicitly.

## Output

A reviewed, approved spec saved to a file in the repository covering all six areas, a human-approved plan, a human-approved task list, and implementation that follows that spec through offensive-first tests. The spec is a living document committed to version control.
