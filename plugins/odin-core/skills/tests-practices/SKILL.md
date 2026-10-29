---
name: tests-practices
description: 'Use when developing a fix or feature test-first, plan a TDD build, or work red-to-green in slices. Every test is invariant-based or offensive: it states a quantified property or an attack with an independent oracle, detects a named realistic fault, and survives behavior-preserving refactors. Not for hardening: use tests-adversarial. Not for deleting weak tests: use tests-purge-unneeded.'
---

# Offensive-first test practices

Classic agent TDD rots in a known way: the red test is written as a polite specification, the implementation drifts, and the agent, without noticing the drift, bends fixtures, weakens assertions, and patches contracts with ad-hoc changes until green appears. The work is paid for twice and the suite proves nothing. This skill inverts the stance. Red is an attack, not a description: before any implementation, write the tests that try to BREAK the contract, boundary raids, invariant violations, error-path probes, adversarial orderings. Green means the attacks failed to break the code, never that a saved output was matched.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Develop a fix or feature test-first, plan a multi-step TDD build from a spec, or work behaviour red-to-green in slices. |
| Authority | Reversible local: writes only named test and source files; rollback is VCS revert of the implementation commit. No remote mutation. Tests and implementation never change in the same repair step. |
| Side effect | Adds an attack suite and the minimal implementation that survives it, one vertical slice at a time; multi-step work also writes a plan document. |
| Done | Per slice: every clause has an attack or invariant property that failed red for the right reason and passes green unweakened, each naming its independent oracle; one mutation probe the suite caught; every test maps to a confirmed seam; zero fixture oracles, snapshots, or unsubsumed fixed regressions. |

## Inputs

- Target and requirement (required): the behavior to build or fix, and the public seam where it is observed. A seam is confirmed with the user before any test exists at it.
- Contract source (required): spec, caller evidence, worked literal, or stated invariant, the independent truth attacks are derived from. Never the implementation's own logic.
- Test framework (optional if discoverable): the project's runner. Stop and report if absent and not discoverable; never install one unasked.

## Test admission

Every test in the suite is admitted only when it states all five, in the test name or its leading lines:

1. Property under attack: the quantified invariant or clause being broken, not a scenario label.
2. Scope and seam: the confirmed public seam under test; no test exists at an unconfirmed seam.
3. Independent oracle: the source of the expected value, derived without running the implementation and without reading a saved output. Reusable input data and setup helpers are allowed; saved expected outputs, snapshots, and recomputed implementation rules are never oracles.
4. Distinct fault: one plausible consumer-visible fault this test detects, named concretely (off-by-one bound, inverted branch, dropped error, lost update under reorder, truncated write accepted as complete).
5. Negative control: red evidence that the test fails for the predicted mode against absent or faulted code, not just any failure. An attack that passes against absent code is tautological: discard and rewrite it.

Equivalent-implementation control: each test binds the public seam only and survives behavior-preserving refactors (rename, restructure, reimplementation of internals). A test that breaks under a refactor that preserved observable behavior is implementation-coupled and is deleted, never repaired by coupling the code back to it.

There is no weak-test escape: history, coverage count, green status, prior approval, or single-occurrence regression fear never admits a test that fails this bar.

## Refusals

- Never weaken an assertion, bend a fixture, skip a test, or loosen a contract to reach green. Any such edit during a green phase is a stop-the-line violation: revert it, then either fix the implementation or declare a contract change and re-attack from red.
- Never edit a test and its implementation in the same repair step. Test-fixing and code-fixing are separate cycles, each with a named justification.
- Never accept a tautological attack (expected value recomputed the way the code computes it) or an implementation-coupled one (mocks internals, tests private methods, asserts call counts or order, reads storage around the interface). Attacks fire at confirmed public seams only.
- Banned as proof: fixture oracles (saved expected outputs), contract snapshots, naive fixed single-path regressions unsubsumed by a quantified property, and coverage, history, or count-driven retention. Reusable inputs stay allowed; oracles stay independent.
- Not for hardening existing code with no behavior change, use tests-adversarial. Not for deleting weak tests, use tests-purge-unneeded.

## Procedure

1. **State the contract under attack.** From the spec, callers, and independent literals, write the clauses the code must honor: valid behavior, boundaries, invariants, error semantics. Where a clause quantifies over inputs, state it as a property (for all valid inputs, the relation holds; for all invalid inputs, the rejection holds and prior state is unchanged) rather than as one worked path. Confirm the seam with the user. Done when: clauses are listed with an independent truth source each, and the seam is confirmed.
2. **Attack first.** For the current slice, write the breaking suite before any implementation: for each clause, the boundary raid, the invalid input, the invariant violation, the error-path probe, the adversarial ordering that would expose a sloppy implementation. Prefer one quantified property per clause over a pile of fixed paths; fixed paths survive only when subsumed as documented members of a stated property, never as standalone proof. Run it. Every attack must fail red **for the right reason**, assert the failure mode, not just any failure. Done when: the suite is red with each failure matching its predicted mode.
3. **Implement until the attacks stop breaking it.** Minimal but real: only enough code to survive the suite, no speculative features, no refactor of unrelated code. Rerun until green. If green cannot be reached, revert the implementation and try a different minimal approach; the attacks do not move. Done when: the suite is green with tests byte-identical to their red state.
4. **Grill the green.** Diff every test, fixture, and contract file against its red-phase state. Any drift is a violation: revert it, classify the change (implementation bug -> fix code; genuine contract change -> declare it, update the clause list, return to step 2). A drift that introduces a saved-output oracle, a snapshot, or a weakened property is rejected outright, never declared as a contract change. Done when: the diff over test surfaces since red is empty or every change is a declared contract change with its own re-attack.
5. **Probe the suite's teeth.** Mutate the implementation once, flip the fix, invert a branch, off-by-one a bound, and confirm at least one attack catches it; then revert the mutation. A suite that survives its mutation probe proves nothing and returns to step 2 for a sharper attack. Done when: the probe was caught and the revert is clean.
6. **Advance by vertical slice.** Commit the slice (attack suite + implementation, one commit naming the behavior), then take the next clause or seam from step 2. Multi-step work runs from a plan document listing one attack-entry per requirement, ordered by dependency; the plan's only execution mode is offensive-first; there is no implementation-first option. Done when: all agreed seams are exhausted and every test in the tree maps to a confirmed seam.

## Failure and recovery

| Failure class | Rule |
|---|---|
| Green by test-bending | The signature drift this skill exists to kill. Revert the test edit, keep the red, fix the code or declare the contract change out loud. |
| Oracle violation | The test leans on a saved output, snapshot, or recomputed rule. Discard the oracle and re-derive it from the independent source; if none exists, stop and report the missing prerequisite. |
| Attack cannot be written | Missing prerequisite (unclear requirement, unconfirmed seam, no framework). Stop and report; never proceed to implementation on an unattacked contract. |
| Implementation cannot survive within the slice | Revert the implementation, keep the attacks. Try a different minimal approach or stop and report; partial result = red suite + its output, never a weakened green. |
| Mutation probe survives | The suite is decorative. Sharpen the attack before touching more implementation. |
| Existing suite breaks | Revert; narrow the change until only the new slice's behavior moves. |

Partial-result rule: completed slices are retained; a blocked cycle never invalidates prior green slices and never claims the done predicate.

## Output

Per slice, in order: attack files, red run output (failure modes matched), green run output, mutation-probe evidence, implementation commit SHA. Multi-step work prepends the plan document path.
