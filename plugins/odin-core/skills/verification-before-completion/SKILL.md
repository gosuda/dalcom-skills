---
name: verification-before-completion
description: 'Use when a task, feature, or fix is called done, complete, finished, or fixed, or before a commit, PR, or next task. Not for fact-checking. Not for measuring.'
---

# Verification before completion

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A done, fixed, passes, complete, or ready claim is imminent; a commit, PR, or next-task move is about to happen; or satisfaction is about to be expressed. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. Reads only what is required to classify the claim, and executes the one named proving action. |
| Side effect | Runs the narrow proving command or scenario; edits nothing; blocks the completion claim when the output contradicts it. |
| Done | Each claim carries fresh output from exactly one proving action (or the UNVERIFIED-NO-SURFACE classification when no checkable surface exists), the claim wording matches the output, and failures are reported honestly. |

## Inputs

- Fires on: Explicit invocation, or a user utterance that contains a completion claim.
- Must supply: The specific claim being made; what would prove it; whether it has been run; the output of the check.
- Optional: The exact command or scenario run; the raw output read; any partial results.

## Procedure

1. **Handle the no-check surface.** A prose-only change is not automatically a no-check surface. Counts, paths, literal requirements, executable examples, and rendering claims remain checkable. Use UNVERIFIED-NO-SURFACE only when the claim itself has no observable check. **Done when:** the surface is classified as checkable or UNVERIFIED-NO-SURFACE.
2. **Name the proving action.** Name one proving action whose target and output can establish the claim. Include the relevant checkout or content identity, runtime and feature profile, loaded or packaged entrypoint, selected test population, and run or job identity when these affect the claim. For measurable claims, first restate the claim as a falsifiable hypothesis naming the metric, the expected direction, and the pass/fail threshold; stop if the claim cannot be so restated. Inspect the prepared target; this skill does not create worktrees, rebuild installations, mutate fixtures, repair caches, or acquire credentials. **Done when:** one precise proving action is named for the checkable surface.
3. **Run it.** Execute the named action after the last relevant edit to the code. Do not run before the edit and claim the result as post-edit evidence. **Done when:** the proving action has been executed after the last edit.
4. **Read all of it.** Read the producer's actual final status and complete diagnostics. If output is filtered or piped, retain the producer's status rather than treating the final consumer's status as the producer's result. Confirm that the intended tests, rules, paths, or branches were actually exercised. A suspiciously short run is a reason to inspect execution evidence, not a failure verdict by itself. **Done when:** the full output and exit code are read.
5. **Classify.** For an absence claim, establish that the producer succeeded and searched the intended scope. Empty output can be valid; an errored producer, empty input population, wrong target, or inactive rule cannot establish absence. For exact-content claims, compare against the authoritative full content at the required byte, line, or structural granularity. Separate proof layers. Source inspection does not establish the running process image; a host check does not establish a gated target; parser acceptance does not establish a complete request; renderer parsing does not establish styling; mocked transport does not establish a live provider path. Report PARTIAL or UNVERIFIED when the requested layer was not exercised. Verification grants no authority to retry, repair, publish, or waive the missing layer. Bind a proving action to its exact workspace, full revision or content snapshot, configuration, command, and claimed surface. A dirty worktree result proves that snapshot, not every contained commit. A result from before a rebase, repair fold, or relevant edit is not final-candidate proof. Confirm that the intended artifact or tests actually executed and that a test filter selected the intended cases. When comparing base and candidate, use comparable scenarios and independently attributable build artifacts. Group only comparable failure shapes together. For before/after claims, run the same probe against the baseline state and the changed state, compute the delta against the threshold, and classify as met, unmet, or blocked-confounded. For count or corpus claims, state the population, predicate, denominator, subgroup boundaries, and missing attributes, and judge against the claim's own threshold rather than an invented universal one. Isolate build/cache state when reuse could cause cross-revision execution; do not assume a particular build tool always has such a collision. Diagnose wrapper or environment failures from observed output before changing the environment. A wrapper parse failure, missing fixture, timeout, or inability to link is not a successful source check. Read complete output and the unmasked exit status. Search summaries may locate diagnostics but cannot prove absence of failures or completeness of a run. One green base run and one red candidate run support a comparison; they do not by themselves establish causality for an intermittent failure. An all-green result is recorded as non-reproduced with attribution unestablished, not as exoneration. Record uncertain attribution rather than imposing a fixed rerun count or declaring an untouched-path failure pre-existing. **Done when:** one classification is assigned with its justification.
6. **Report.** State the classification, the action that was run, what it showed, and the exact claim wording it does or does not support. Do not hedge; do not round up a partial result to "done." **Done when:** the report states the classification, action, output, and claim wording.

## Failure and recovery
unrun-check: The check was not executed. Report UNVERIFIED. Do not substitute a hedge or a confidence statement.

contradicted-claim: The output shows failure, error, or unexpected state. Report FAILED with the exact output. Do not suppress it, qualify it, or claim success despite the output.

timeout: The proving action did not complete. Report TIMEOUT with the partial output present. Do not treat a partial run as a pass.

stale-check: A check was run, but the code changed after it. Treat as UNVERIFIED; re-run before the claim can be made.

Partial-result rule: A partial result is reported as partial. It is not rounded up. No retry is attempted unless the user explicitly requests one; this skill does not perform that action itself.

Non-mutation rule: This skill reads and classifies. It does not write, commit, open PRs, move tickets, or change any state outside its own output.

## Output
One terminal classification (VERIFIED, PARTIAL, UNVERIFIED, UNVERIFIED-NO-SURFACE, FAILED, or TIMEOUT) with the action run (or the no-surface statement), what it showed, and the claim wording it supports or contradicts; non-VERIFIED classifications followed by one sentence stating the reason.
