---
name: no-excuses
description: 'Use when a material claim rests on missing proof, an untested assumption, or unresolved counterevidence that investigation can still settle. Not for unrelated research, actions outside the granted authority, or bypassing required approvals.'
---

# No excuses

A reachable evidence gap is work to finish, not a disclaimer to append.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A task, conclusion, or proposed completion claim depends on an untested assumption, missing observation, or unresolved counterevidence, and an authorized action can still settle it |
| Authority | The underlying assignment sets permitted actions. Use authorized reads and observations. Make reversible local repairs only when the assignment authorizes implementation. A research, review, or plan-only assignment stays read-only. This skill grants no authority to install tools, use credentials, incur charges, publish, deploy, mutate remote state, or change a public or data contract |
| Side effect | Each material obligation ends resolved with decisive evidence, or narrowed to a precise blocker naming the missing prerequisite or approval |
| Done | No material obligation remains open while an authorized informative action exists. Resolved claims carry evidence. Blocked claims name the exact prerequisite. Hedged wording never substitutes for reachable evidence |

## Inputs

- The weak claim (required): the precise statement, the decision or acceptance criterion that depends on it, and the observation that would support or contradict it. Ignore uncertainty that cannot affect the requested result.
- The task, repository, and available tools (as available): these set the evidence sources, access limits, and prohibitions that bound the investigation.

## Procedure

1. State the weak claim precisely. Name the decision or acceptance criterion that depends on it and the observation that would settle it. Set aside uncertainty that cannot change the requested result.
2. Convert the uncertainty into evidence obligations. For each one, name the question to settle, the source or surface to inspect, and the observation needed. Use a short list for independent obligations. Do not create a tracking artifact unless the task needs one.
3. Obtain evidence from the actual relevant source. Read the implementation and its consumers for source claims, authoritative material for external contract claims, and the real runtime or delivered artifact for behavior claims. A mock result, compilation success, an old log, or a worker assurance proves only what it actually covers.
4. Resolve available paths first. Inspect existing configuration, read captured output, and use established mechanisms before asking the user for information. An empty search or a failed tool call is not proof of absence or impossibility. Change the query, source, or method when another authorized action can reduce the uncertainty. Do not rerun a user-reported failure merely to establish that it happened; investigate its cause.
5. Investigate counterevidence. Compare the claim against failing observations, alternate paths, version differences, and environmental conditions that could change the conclusion. Separate an observed fact from an inference about runtime behavior.
6. Act on the result. When evidence reveals a defect the assignment authorizes fixing, repair the cause, update affected consumers and documentation, then obtain the evidence the changed claim needs. When the assignment is read-only, deliver the supported finding and the concrete correction without editing.
7. Continue while evidence changes the diagnosis or exposes a reachable next action. Do not use an arbitrary attempt cap. Do not repeat an unchanged check expecting a different answer. Inspect the failure and choose an action with new information or a changed relevant condition. Stop an obligation only when it is resolved or its next necessary action needs an unavailable prerequisite or ungranted authority. Finish independent reachable obligations before returning.

## Blockers and recovery

A blocker must name the exact unresolved question and the claim it prevents, the required source, access, environment, decision, or approval, the evidence already obtained with the materially different approaches attempted, why the remaining available actions cannot answer the question, and the specific prerequisite that permits continuation.

- A temporarily failed tool is a problem to investigate, not automatically an unreachable prerequisite.
- Missing permission is not permission to bypass a boundary.
- Explicit prohibitions on tests, gates, or other actions remain in force.
- Rewording a material claim as likely, adding not verified, or reporting a failing check does not close an obligation while an authorized informative action remains.
- A genuine blocker is reported as blocked with its precise prerequisite. It is never hidden with invented certainty.

## Output

Return the resolved conclusion or the completed authorized repair with the decisive evidence and the limits of that evidence. Distinguish observed facts, supported inferences, and unresolved obligations.

When blocked, state the precise prerequisite, the affected result, and what enables continuation. Do not claim the whole task complete while a material obligation remains open.
