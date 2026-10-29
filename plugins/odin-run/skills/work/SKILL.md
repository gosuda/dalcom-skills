---
name: work
description: 'Use when implementing from a plan, spec, clear build request, or settled ticket, orchestrated or standalone. Not for open-ended debugging, exploration, or read-only research.'
disable-model-invocation: true
---

# Work execution

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Implementation starts from a plan or spec path, a clear build request, or a settled ticket (never an open-ended bug). |
| Authority | Reversible local: writes only named local artifacts; never commits, pushes, or opens a PR; rollback is version control. No remote mutation. Finalization belongs to a separate finalizer reachable only in standalone mode. |
| Caller mode | Orchestrated or standalone, set by the caller. Orchestrated: a supervisor passes an explicit orchestrated signal. Standalone: invoked directly by a human. The mode governs where execution stops. |
| Side effect (orchestrated) | Implements plan units, runs local verification, returns a structured result. No review, commit, push, or PR. |
| Side effect (standalone) | Implements plan units, runs local verification, then delegates finalization to review-and-ship with explicit delegated authority. |
| Done (orchestrated) | All plan units implemented and locally verified; structured result returned. |
| Done (standalone) | All plan units implemented and locally verified; finalization delegated to review-and-ship. |

## Inputs

- `$ARGUMENTS`: plan path, spec path, or bare work description. Blank auto-detects the newest implementation-ready code plan in `docs/plans/`. A non-empty string is a path only when it resolves to an existing readable file.
- Plan document (path input resolves to file): read metadata before body.
- Bare prompt (no file resolves): scan work area, assess complexity, route.
- Caller mode signal: orchestrated (from a supervisor) or standalone (from a human).
- Named TDD seams: the plan or ticket states which seams carry behavioral tests. No named seam is inferred.
- Repository test, typecheck, and lint commands for the changed surface.

## Procedure

### Phase 0: input triage

1. Route the input following `references/execution-detail.md`: plan document (classify `artifact_readiness`), blank invocation (auto-select newest implementation-ready plan), or bare prompt (scan and assess complexity). Stop on requirements-only, invalid readiness, or ambiguous artifacts. Done when input is routed to Phase 1 or stopped with a named blocking condition.

### Phase 1: quick start

2. Read plan and clarify (skip if arriving from Phase 0 with a bare prompt). Build a section map first, then read metadata, `Goal Capsule`, `Verification Contract`, `Definition of Done`, the `Implementation Units` heading list, and only the active unit section plus referenced excerpts. Note `Execution note`, `Deferred to Implementation`, and `Scope Boundaries` before starting. Ask clarifying questions now when anything is unclear. Never edit the plan body during execution. Done when relevant sections are read and clarifications are resolved.
3. Setup environment. Determine current and default branch. On a feature branch with an opaque name, suggest renaming. On the default branch, offer a new branch, a worktree, or explicit permission to work on default. Done when branch strategy is confirmed.
4. Create task list (skip when Phase 0 routed as Trivial). Derive tasks from implementation units, dependencies, files, test targets, and verification criteria. Preserve unit IDs as prefixes. Carry each unit `Execution note` and `Patterns to follow`. Use each unit `Verification` field as the primary done signal. Done when the task list carries ID prefixes and dependencies.
5. Choose execution engine and strategy. Probe the harness per `references/execution-detail.md`. Prefer subagents for structured multi-unit plans. Parallelize independent units only after confirming harness isolation. Never nest worktrees. Done when engine and dispatch strategy are confirmed.

### Phase 2: execute

6. Task execution loop: for each task in priority order, mark in-progress; read referenced files; check for existing matching work; reuse existing patterns and tests; implement following project conventions and the unit `Execution note`; add, update, or remove tests; run the TDD cadence from the named seams (below); run the System-Wide Test Check from `references/execution-detail.md`; mark complete only when both pass. Done when the task is implemented and verified.
7. TDD seam cadence. At every named seam, write the failing behavioral test first and watch it fail for the contracted reason before implementing. Run the typechecker regularly during implementation. Run the owning single-file tests after each behavior-bearing change. Run the full suite once at the end of the unit, not as a substitute for seam tests. A named seam with no behavioral test blocks local verification until the test exists. Done when every named seam has a failing-first test and the typecheck plus single-file plus full-suite cadence is recorded.
8. Simplify opportunistically: at phase boundaries, when a verified finding names duplicated logic or a special case the general path absorbs, or when the change spans more than one concern, reread the changed units and remove dead branches, repeated logic, tiny one-use wrappers, and absorbed special cases. Preserve observable behavior and rerun changed-path checks. Done when the simplification pass is complete with behavior preserved.
9. Track progress: update the task tracker as tasks complete. Note blockers using plan IDs; never invent IDs the plan does not supply. For long-running work, write progress to `local://work-<run-id>-progress.json` so state survives context compaction. Done when progress is recorded.

### Phase 3: local verification and mode split

10. Run local verification: execute the project test suite and lint check for the changed surface. Fix failures immediately. Never suppress a check or widen scope to unrelated code. Done when tests and lint pass for the changed surface.
11. Mode split.
    - Orchestrated mode: stop. Return a structured result with implementation summary, verification results, diff summary, working-tree state, and residuals or blockers. Never review, commit, push, or create a PR.
    - Standalone mode: delegate finalization to review-and-ship with explicit delegated shipping authority, implementation context, and residuals. review-and-ship owns review, commit packaging, publication classification, checks, push, and PR. Never ship directly.

## Single-ticket mode

A single settled ticket or spec is the narrow entry of the end-to-end pipeline. Phase 0 routes it here instead of building a multi-unit task list. Read the settled plan or ticket end to end and extract the contract: the behavior promised, the inputs and outputs that define it, and the seams the plan names for behavioral tests. Implement the contract in code following existing conventions, reuse existing patterns, and write behavioral tests at each named seam from the caller perspective (each test must fail on a plausible bug, never restate the source). Follow the TDD seam cadence: failing test first, regular typecheck, owning single-file tests per change, full suite once at the end.

Never reopen or redesign the plan during single-ticket execution. When the plan is ambiguous, contradictory, or missing a named seam, stop and report the gap; never infer scope. When the implementation reopens a settled plan decision, revert the overreach and implement only what the plan names. When scope widens beyond the plan, revert the unrelated changes. Work never commits partial or complete results; the finalizer owns commit packaging. When the procedure cannot reach the done predicate, report the blocker and leave the partial diff for the caller to inspect or revert.

## Closing chain: work, review-fix-loop, offensive simplify

1. Work first. Complete the skill's own implementation path before any closing pass.
2. Review-fix-loop with native gates. Run the skill's own gates to green: the System-Wide Test Check plus local verification, honoring the mode split. Continue while each cycle shows verified progress against a distinct finding. Stop as blocked or non-converged when a finding repeats without progress, results oscillate, checks are unavailable, or correction would widen the bounded scope. Never widen scope to unrelated code.
3. Offensive simplify last. Re-derive the general case from contracts, delete old structure with no shims, aliases, or flags, collapse special cases, migrate every caller in the same change, one concern per atomic increment. This skill commits nothing; the zero-commits rule stands. Ask first before removing any live consumer surface. Run the skill's verifier after each increment; revert the increment on red. Close with a compression pass (dead branches, duplicated logic, one-use wrappers) with behavior preserved and checks green.

## Failure and recovery

| Failure | Rule |
|---|---|
| Requirements-only plan | Stop. Request an implementation-ready plan. |
| Invalid readiness value | Stop. Request plan repair. |
| Non-code or unclassified mode | Stop. Request explicit human decision. |
| Blank invocation with no implementation-ready plan | Stop. Ask for an explicit path. |
| Ambiguous plan | Stop. Report the specific gap. Never guess or redesign. |
| Large work with user declining planning pass | Proceed with task list and execution. |
| Harness isolation unavailable for parallel | Fall back to serial subagents or inline. |
| Contending units in shared workspace | Fall back to serial. |
| Serial unit review diff out of scope | Fix before next unit. |
| Local verification cannot reach green | Report the failure and any partial fix in the structured result (orchestrated) or pass to review-and-ship as a blocker (standalone). Never ship. |
| Single-ticket plan ambiguous or contradictory | Stop. Report the specific gap. Never guess or redesign. |
| Single-ticket implementation reopens a settled decision | Revert the overreach. Implement only what the plan names. |
| Named seam has no behavioral test | Add the test before local verification. Never defer. |
| Single-ticket scope widens beyond the plan | Revert unrelated changes. Keep only the contracted work. |

Partial-result rule: report what is implemented and verified. Never claim done when tests fail. In orchestrated mode, name residuals in the structured result. In standalone mode, pass residuals to review-and-ship.

## Output

- Orchestrated mode: structured result with implementation summary, verification results, diff summary, working-tree state, and residuals or blockers.
- Standalone mode: implementation and local verification complete; finalization delegated to review-and-ship. The final report comes from review-and-ship.
- Blocked: a terminal yield naming the blocker and what was tried.

Zero commits, pushes, or PRs are attributable to this skill in either mode. This skill is the `implement` owner from the source report; no second `implement` skill is created.
