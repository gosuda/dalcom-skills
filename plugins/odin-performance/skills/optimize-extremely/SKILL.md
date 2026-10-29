---
name: optimize-extremely
description: 'Use when a named subsystem must be made as fast as possible through a measured-floor campaign. Not for a single bottleneck fix: use optimize. Not for read-only analysis: use fastopt or fastopt-extreme.'
---

# Optimize extremely

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A subsystem or named-target performance campaign against a measured floor; the user says "make this as fast as possible", "extremely optimize", or "grill every inefficiency" for a resolvable target. |
| Authority | Reversible local: writes only the exact VCS-tracked source-target set shown before mutation plus `.outline/optimize/<target>/`; rollback is version control. No remote mutation, credentials, paid services, deployment, or inferred repository-wide scope. One winning concern lands per atomic commit; non-wins are reverted. |
| Side effect | Measured floors, isolated candidates, adversarial behavior gates, integrated re-measurement, cold-path dispositions, and atomic optimization commits with append-only evidence. |
| Done | Hot units rebuilt against their floors with a proven win, cold units graded fixed, at-floor, or left with reasons, residue removed, verifier green, and each concern landed atomically. |

This skill replaces the historical `extremely-optimize` spelling. No alias survives; the old slug is a provenance name only. Peer routes: a single bottleneck fix is `optimize`, and read-only analysis is `fastopt` or `fastopt-extreme`. Naming a peer never executes its procedure.

## Inputs

- A named subsystem, path, symbol, diff, or otherwise resolvable target. Repository-wide work requires explicit opt-in; a bare invocation is never that opt-in.
- One representative runnable workload exercising the target with at least one second of wall clock, supplied or constructed before measurement begins.
- The repository-native verifier, supplied or discovered before any target lands.
- Explicit boundary answers before any mutation touches a boundary surface, including candidate worktrees.
- Optional explicit user limits only: time, attempts, spend, or marginal gain. No defaults are implied.

## Required references and evidence location

- Read `references/lenses.md` before dispatching candidates.
- Read `references/state-and-resume.md` before recording or resuming a run.
- Read `references/tooling.md` when selecting or constructing instrumentation.
- Read `references/experiment-mode.md` only when the request explicitly selects its broader measurable search space.
- `.outline/optimize/<target>/` is the runtime evidence namespace: run records, baselines, candidate reports, rankings, gates, integrated measurements, and native harnesses. It is an evidence location, never a callable skill alias. Never rewrite existing run records incidentally to this cutover.

## Procedure

1. Resolve one target and bound the write surface to that target plus `.outline/optimize/<target>/`. Record the exact tracked source-target set, evidence paths, run-created worktrees, and any necessary native harness locations before mutation. Preserve user changes; rollback undoes this run's changes, never the whole target or unrelated commits. Work one target at a time in ranked order inside the authorized scope. No architecture-wide redesign or unrelated sweep. Done when: one target, its exact source set, workload, and verifier are resolved and bounded.
2. Require the representative runnable workload and the repository-native verifier before optimization begins. If no workload can exercise the target, take the no-workload terminal outcome and commit nothing. Done when: the workload and verifier are fixed, or the run ends with its blocker.
3. Pin the baseline with `hyperfine --warmup 3 --min-runs 10 '<cmd>'` on a release build with representative inputs and the same workload used throughout. Record median, standard deviation, minimum, and maximum, with variance reported. Accept a baseline only with standard deviation below 20 percent of median; this single strict condition applies everywhere in the campaign and its references. Record the top self-time function or widest plateau as the hot-path locator. A unit is hot when it holds at least 5 percent of measured time or its call count scales with input size as confirmed by instrumentation; sampling disagreement does not erase the call-count case. Write both hot and cold lists. Done when: a stable baseline and both lists are recorded, or the run ends noisy or with no measurable hotspot.
4. Work the hot list in descending time share. For each unit, state its contract from callers, tests, and signature, never from its own internals. Compute its floor from that contract alone: bytes that must move at achievable bandwidth, the algorithmic lower bound at a measured per-operation cost, and syscalls or round-trips the protocol cannot avoid. Show the arithmetic with `eval`, never as unsupported prose. Divide measured cost by floor for headroom. A unit within 2x of its justified floor is finished. Done when: every hot unit has its contract, floor arithmetic, headroom multiple, and within-2x verdict recorded.
5. Classify every consumer channel as interior (every caller in tree, nothing persisted or shipped) or boundary (public API, wire or on-disk format, config running in someone else's deployment, plugin point). Reflection, string dispatch, generated callers, external integration, wire formats, persisted data, deployed configuration, and plugin points stay boundaries until evidence resolves them. Obtain explicit boundary decisions before any mutation, including candidate worktrees. Interior status removes the consent requirement; it never authorizes deleting required behavior. Done when: every channel is classified and every boundary surface has its explicit answer before any candidate touches it.
6. Derive the replacement from the contract and floor without copying the old structural design, choosing the data layout that puts the floor in reach: contiguity, batching, hot and cold fields split, or one pass where there were three. Then audit the old implementation branch by branch, classifying each behavior as essential and folded in, or residue and cut, each with a one-line reason covering guards, ordering, errors, state transitions, and side effects. A branch never read is a feature deleted by accident. Done when: the replacement is derived from contract and floor and every old branch is classified.
7. Dispatch isolated candidates sharing the same scope, boundary decisions, workload, baseline, behavior contract, and allowed approximation. Use one transformation per candidate across the five disjoint lenses: `algo`, `data`, `cache`, `concur`, `arch`. For a single function under 50 lines with one evident concern, report `auto-skip` and run a reported single-candidate search, never a proof exemption. After reporting, candidates are read-only. Done when: five isolated candidates are dispatched, or the `auto-skip` single search is reported.
8. Measure each candidate under the same benchmark protocol. Return lens, change summary, before and after medians, speedup ratio, behavior assessment, readability cost, and patch. Append each candidate record before scoring. Record failed and error attempts durably with a distinct failed status; they are never reused as completed results. Done when: every candidate outcome is appended with its failure status distinguished.
9. Score remaining candidates as `speedup_ratio * behavior_safety * (1 - readability_cost * 0.3)`, where exact behavior is 1.0, a confirmed approximation is 0.7, and unsafe or undisclosed behavior is 0.0. An approximation is viable only when the request authorizes it and the changed contract is confirmed; otherwise reject it. Rank winner and runner-up and append the ranking. Done when: scores, ranks, and the appended ranking are recorded, or the run ends with no viable candidate.
10. Run the adversarial behavior gate on the leader: output identity, error semantics, public contracts, empty and boundary inputs, negative values, applicable NaNs, and concurrent call sequences. Append every verdict and failure scenario. On failure discard that candidate and consider the next ranked candidate. Reject unconfirmed approximations and behavior-breaking candidates. Done when: one candidate passes every gate with verdicts appended, or all candidates are discarded.
11. Apply only the gate-cleared patch to the main worktree. Re-measure with the same workload using three warm-ups and at least ten measured runs; append the integrated median, variance, and speedup. Discard the patch when `baseline_median / integrated_median < 1.05`. Run the repository verifier and cover every essential behavior no test reached. Done when: the integrated measurement proves at least 1.05x with behavior covered, or the target is restored with the blocker recorded.
12. Grill the cold paths before recording completion. Every cold unit takes one verdict: `fixed` naming the cost that fell, `at-floor`, or `left` with its reason, and a rejected complexity-for-microseconds proposal is always `left`, never `fixed` or `at-floor`. Consider retained memory, allocations, repeated I/O, larger-input complexity, startup and build cost, artifact size, and dependency weight. Perform necessary cold fixes with their relevant proof now. Keep independent concerns in separate atomic commits; revert any unfinished current concern without undoing already completed valid commits. Done when: every cold unit has its verdict with reason, and every authorized cold fix carries its proof.
13. Land each concern atomically: delete the old unit and every symbol reachable only from it, commit exactly the named target as one optimization concern with hot path, lens, rationale, baseline and integrated medians with variance, ratio, and any confirmed approximation contract. Remove only run-created `agent-*` worktrees; preserve the log and benchmark evidence. Append the authoritative terminal run record with status and class. Exit 0 is possible only after the full target contract, including cold dispositions, is satisfied. Done when: concerns are landed atomically, residue is gone, evidence is preserved, and the terminal record is appended.
14. Follow `references/state-and-resume.md` for all recording and resume. Resume only when the target, revision, and workload fingerprint matches and a fresh baseline falls inside the recorded standard-deviation band; then reuse valid completed candidates and run only missing work, never auto-retrying a completed failed candidate unchanged. Preserve stale records and append a new run instead of truncating. Every clean terminal outcome appends its terminal status and class; an `in-progress` record as the last line alone means a genuine crash. Done when: recording, resume, staleness, and terminal-status rules are honored.
15. Follow `references/tooling.md` for profiler and harness selection. Benchmark instrumentation outside `.outline/` is permitted only at the predeclared native harness locations. Remove run-created temporary instruments after preserving reproducible measurement evidence; retain intentional regression coverage. Done when: instrumentation is selected, placed, and cleaned per the reference.
16. Use `references/experiment-mode.md` only for an explicitly named measurable configuration, threshold, preprocessing, or similar search target. Keep harness-before-hypotheses, variance checks, immediate durable results, crash markers, batch strategy digests, backlog updates, dependency approval, degeneracy checks, rubric-specific evaluation, stratified samples, and diagnostic metrics. Append evaluation transitions keyed to an experiment rather than rewriting its original measured record; reconstruct best state from events. A paid or remote judge is outside local authority; never invoke one merely because the reference describes a judge rubric. Done when: the extension runs only under its explicit selection with append-only outcomes, or is not used.
17. Continue while the authorized objective remains reachable and investigation makes verified progress. No default maximum promotion attempts, no default experiment count limit, no automatic plateau termination, and no default marginal-gain stopping threshold apply; the 1.05x integrated gate, the 2x floor classification, and the measurement-noise condition are proof criteria, not round caps. Diagnose recurring failures rather than retrying them identically. Explicit user time, attempt, spend, or marginal-gain limits bind; reaching one with work outstanding yields an incomplete result with evidence and a safe tree, never success. Done when: the target contract completes, or the run ends incomplete with its limit named.

Work one target at a time. Half-rebuilt is the forbidden state: finish a target or revert it. Scope equals the ask; never escalate a named target into a repository-wide campaign.

## Failure and recovery

| Class | Recovery |
|---|---|
| No workload | The target cost cannot be reproduced on demand. Construct a runnable workload or stop; commit nothing. |
| Noisy baseline | Standard deviation at or above 20 percent of median and not cleared. Clear the noise or stop; no candidate promotion. |
| No measurable hotspot | No unit reaches 5 percent and no input-scaling call count is confirmed. Report the blocker; commit nothing. |
| No headroom | Every hot unit sits within 2x of its justified floor. Terminal; required cold dispositions still complete; commit nothing as a win. |
| No win | No candidate or integrated result clears 1.05x. Revert the replacement or target patch; keep the original. |
| Failed correctness gate | Repository checks or adversarial gates fail. Revert the patch; keep evidence. |
| Unconfirmed approximation | The request did not authorize the approximation or the changed contract was not confirmed. Discard that candidate. |
| Unclassified divergence | Old behavior is neither folded in as essential nor cut as residue. Complete the branch walk. |
| Mixed concerns | A commit mixes concerns. Split before retrying. |
| Unauthorized boundary touch | A boundary was touched without an explicit answer. Restore it and settle the question. |
| Interruption or crash | Finish the interrupted target or revert it; resume only through fingerprint and baseline agreement. Never ship half-rebuilt. |
| Explicit limit reached | Time, attempt, spend, or marginal-gain limit met with work outstanding. Restore unfinished run changes, preserve evidence, report incomplete scope. Never report success. |
| Scope exceeded | Untouched-scope work ran. Revert the untargeted work. |

Partial-result rule: a target that has not reached the done predicate is reverted to its pre-campaign state; no half-rebuilt target remains. Non-wins and untargeted work are reverted. Never swallow an error or pretend the done predicate holds.

## Output

On success return exit 0 with the commit identifiers, target, selected lens, benchmark command, baseline and integrated statistics, measured speedup, behavior-gate verdicts, repository checks, cold-path verdicts, and durable log path. On failure return the exact terminal class, unchanged or rolled-back target state, measurements obtained, and the precise blocker. Never report a worktree-only result as a landed win.
