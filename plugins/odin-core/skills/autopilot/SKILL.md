---
name: autopilot
description: 'Use when a human has an approved delivery plan and wants the full chain run under phase gates. Not for planning, open-ended debugging, or single-step execution.'
---

# Autopilot

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A human explicitly invokes `/autopilot` with a feature description and an approved execution plan. |
| Authority | Human-gated: previews the exact target and consequence before credentials, paid actions, data-at-rest changes, publication, deployment, remote bulk mutation, or irreversible deletion, continuing only when the invocation covers that consequence; every other write is reversible local, with version control as the rollback. Push or publish only when the invocation explicitly covers that exact target; otherwise leave changes local. |
| Side effect | Implements the bounded approved plan, simplifies the resulting diff with behavior preserved, reviews the in-scope change to zero critical and high findings, then finalizes with required checks, atomic commits, and authorized push or PR creation. All work stays inside the approved scope. |
| Done | Return `DONE` only after the requested close-out state is observed. Otherwise return `BLOCKED` with a resumable handoff. |

## Inputs

Required: feature description, approved plan, repository, acceptance criteria, and close-out condition.

Optional: scope limits; assigned executor; target branch, remote, and PR destination; required checks; shipping instructions. Derive an omitted value only when repository evidence gives one safe, unique answer.

## Procedure

1. Parse the plan, scope, assignments, acceptance criteria, repository, required proof, shipping destination, and close-out condition. Reject contradictions and unavailable assigned executors. Done when: every required input is parsed and bound to a concrete value, contradictions are rejected with the conflicting pair named, and unavailable executors are reported; or the run stops on the first unresolvable input.
2. Confirm that the human approved the plan. If not, stop before implementation and route to planning. Done when: an approval record is confirmed; the plan was approved through plan mode or an equivalent written approval; or the run stops and routes to planning with no delegation.
3. Inspect enough repository evidence to bind the plan to exact artifacts, behavior, verification, and remote targets. Keep the campaign inside the approved scope. Done when: every plan step maps to a named repository artifact (file, directory, or remote target) and the scope boundary is stated with the artifacts inside it and the artifacts excluded from it.
4. Preview each risky consequence. Stop when authority is absent or the target is ambiguous. When an iteration loop waits on a human gate, name the smallest gate: the exact action, the signal it contributes, where that signal lives, and the observable condition permitting the next iteration. Remove a gate only with the narrowest existing mechanism: an invokable command with a deterministic exit status or structured response, a named persisted log file, a read-only metrics or log query yielding an explicit pass, fail, or warn with retained values, or an executable assertion of the observable completion condition. Never introduce credentials, payment, publication, deployment, remote mutation, data-at-rest mutation, or irreversible action to close a gate. Classify each remaining gate as needing one outer-loop human approval before autonomous iteration or as a discrete handoff stating the required action, inputs, and return artifact. Done when: every credential, paid, data-at-rest, publication, deployment, remote bulk, or irreversible consequence is previewed with its exact target, or the run stops naming the absent authority or ambiguous target.
5. Execute the bounded plan inside the approved scope against acceptance criteria, constraints, repository evidence, and the required verifier; record an implementation summary with local verification evidence. On verifier failure apply one targeted repair pass and one recheck; a second failure halts the chain. Done when: the implementation summary with passing local verification is recorded, or the gate halts the chain with the verifier failure and diff recorded.
6. Simplify the completed diff inside the approved scope with behavior preserved. Halt on new bloat or mixed-concern with the cause recorded. Done when: simplification preserves behavior, or the chain halts with the cause recorded.
7. Review the in-scope change for critical and high findings, unhandled error paths, scope creep, and stubs. Allow at most one targeted fix pass plus re-review of the changed files. Halt on residual critical or high findings. Done when: zero critical and zero high findings remain on the changed files, or the chain halts with the residual findings listed.
8. Finalize the reviewed change: run the required checks, create atomic commits, and only with explicit shipping authority covering the exact branch, remote, and PR destination push or create-or-update the PR; otherwise leave changes local. Done when: checks are green with PR created or updated (full mode) or commits made and push skipped (local-only), or finalization is blocked with its reason.
9. Observe authorized close-out. Run any supported in-scope fix through execution again, repeat affected gates, and finalize each authorized update. Do not merge, deploy, or publish elsewhere without matching authority. Done when: the close-out condition named in the inputs is observed in repository or remote state, or the run stops for absent authority.
10. Return the terminal classification and include the finalization report. The halt handoff format in `references/pipeline-gates.md` is binding. Done when: the terminal result is `DONE` with the finalization report attached and close-out state quoted, or `BLOCKED` with the failed stage, reason, and next action named.

## Failure and recovery

Stop on a missing approved plan, contradictory input, unavailable executor, ambiguous target, absent authority, failed gate, non-converging review, rejected remote mutation, or incomplete close-out. Preserve successful in-scope work and observed remote state. Recover only mutations made by this run, using reversible repository or hosting operations; never discard unrelated work.

Return `BLOCKED` with the failed stage, exact reason, autofix result, partial artifacts, remote mutations, proof state, recovery state, and the single concrete requirement to resume. Never claim rollback, publication, or close-out without observing it.

## Output

Exactly one terminal result:

- `DONE`: delivered behavior, changed artifacts, verification evidence, branch and PR, the complete finalization report (checks, commits, push or PR status), and observed close-out state.
- `BLOCKED`: failed stage, reason, partial result, remote state, proof and recovery status, and the next required action.
