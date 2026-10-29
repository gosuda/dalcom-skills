---
name: optimize
description: 'Use when one named path or performance symptom needs a single measured fix. Not for read-only hot-path hypotheses: use fastopt. Not for a full measured-floor campaign: use optimize-extremely.'
---

# Optimize

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A request to improve one named path or one performance symptom, including latency, allocations, bundle weight, query cost, or a frontend performance metric. A supplied benchmark does not select a campaign. |
| Authority | Reversible local only: the named target, necessary in-scope correctness coverage, one explicitly bounded local measurement instrument, and one authorized regression guard. No remote changes, credentials, deployment, paid services, inferred infrastructure changes, or automatic optimization commit. |
| Side effect | One targeted change measured under identical conditions, kept only past noise with behavior and checks green, otherwise reverted. |
| Done | The named bottleneck is measurably improved past noise, required behavior and repository checks pass, a regression guard holds the metric, and every kept or reverted attempt has a ledger entry. |

## Inputs

A resolvable target and symptom or metric, representative measurement conditions, and discoverable repository-native verification. Discover facts from the tree before asking the user for missing information. If the request is a full campaign, name `optimize-extremely` as the owner rather than widening this workflow.

## Procedure

1. Resolve the target, the measurement method, and the exact write surface before editing. Record existing user changes on the target so this run never discards them. Done when: the target, method, and write surface are stated and user changes are preserved.
2. Establish a measured baseline. Record the metric, units, tool, input, conditions, result, and available noise evidence. A symptom is not proof of its cause. Done when: all seven baseline facts are recorded or the run stops as blocked.
3. Identify the specific bottleneck from relevant evidence: query plan, CPU trace, heap profile, bundle analysis, or frontend measurement. Done when: the bottleneck is named with the evidence that selects it.

When instrumentation cannot separate a stage's useful work from dispatch overhead, first estimate whether removing that stage entirely could meet the target. If mutation is authorized, disable only that stage in an isolated, temporary experiment under the same workload and measurement protocol. Label the result an attribution bound, not a correct implementation or shippable speedup, and restore the experiment without overwriting unrelated changes. Before rebuilding a reverted design, measure the dominant operation across input sizes and distinguish write-only staging that can be deleted from state coupled to live behavior. For synchronous regex prescreens, measure adversarial inputs at the supported size limit and check both complexity and match semantics after a rewrite. A timeout on the same blocked execution thread is not an interruption mechanism. Oversized input must follow the documented safety posture; do not truncate away a risky suffix.

4. Apply one complete targeted change. Examples are examples only: a cache, index, pagination strategy, or memoization layer each requires evidence and preserved semantics. Done when: one change is fully coded.
5. Re-measure with the same metric, method, workload, and conditions. Make one change at a time. Done when: the after-measurement under identical conditions is recorded.
6. Keep only an improvement distinguishable from measured noise with required behavior and repository checks passing. Revert neutral results, regressions, and wins obtained by dropping required work. Done when: the change is kept past noise and green, or reverted with its reason.
7. Hold the metric with a guard inside authority: use an existing effective guard, or add an authorized synthetic CI performance budget or field-monitor definition for the primary metric. Do not deploy a monitor or add CI outside authority. Done when: a guard holds the metric, or the missing guard is reported as the completion blocker without declaring success.
8. Return a ledger entry for each kept or reverted attempt: hypothesis, baseline, result, metric, tool, noise assessment, correctness result, and verdict. Done when: every attempt has its entry.

This owner does not use five candidates, floor arithmetic, a 5 percent hotspot threshold, a universal 1.05x win rule, cold-list grading, or atomic campaign commits. Those belong to the campaign.

Peer routes: broader read-only hot and cold analysis is `fastopt-extreme`, hypothesis-only hot-path design is `fastopt`, and a full measured-floor campaign is `optimize-extremely`. Naming a peer never executes its procedure.

## Failure and recovery

- Baseline unavailable: measurement tools or the codebase cannot produce the metric. Result: blocked. Do not proceed without baseline evidence.
- No bottleneck found: profiling shows no measurable code-level cause. Report the uncertainty and whether environmental or statistical noise is suspected.
- Fix inside noise: the gain is within the baseline noise band. Revert. Neutral is a revert.
- Correctness regression: tests fail or behavior changes. Revert immediately. Correctness gates the metric.
- Beyond authority: the fix needs unavailable credentials, remote mutation, deployment, paid services, or infrastructure changes. Document the requirement and stop without widening authority.

Partial-result rule: reverted code leaves no trace. Kept ledger entries remain so discarded ideas are not re-profiled.

## Output

Return the code change with before and after measurements under identical conditions, plus one ledger entry per attempt stating hypothesis, baseline value, result value, metric name, tool, noise assessment, correctness result, and verdict. On failure, return the exact blocked or reverted state, the measurements obtained, and the precise blocker.
