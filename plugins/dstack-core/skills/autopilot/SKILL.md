---
name: autopilot
description: 'Use when a human has a delivery plan, or an approved one from autoplan or brainstorm, and wants the full chain run under phase gates, including a reply of approved, approve all, run it, or go on right after a plan was presented. Not for planning, open-ended debugging, or single-step execution.'
---

# Autopilot

You run a delivery plan from first edit to observed close-out, under phase gates that halt the chain the moment something is unproven or unauthorized. You never write the plan. A plan is the entry ticket, and without one you stop before touching anything and send the work back to planning.

## Read the invocation

Control tokens come off first: `mode:local` selects the local-only finalize, and `workflowz` is a harness keyword. Neither names a subject. The free-text arguments that remain are the subject: a plan file path, a `local://` reference, or inline plan text.
`/skill:<name>` tokens in the arguments are routing hints; drop them before reading the subject.
`orchestrate`, `continue`, `go`, and `do it now` resume the current run and never restart it.
With no free-text subject, take the first source that yields exactly one candidate: a plan approved (an accepted `ExitPlanMode`, or an approval message) or written in this session, then a plan file path named earlier in this session.
Print `subject: <what> (<how found>)` as the first output line.
When no source yields one, stop at plan intake with one line: `autopilot needs a plan: pass a plan path, or run /autoplan-and-autopilot with your idea.`

## Start only with a plan

You need a feature description, an execution plan, the repository, acceptance criteria, and a close-out condition. Scope limits, an assigned executor, the target branch, remote and PR destination, required checks, and shipping instructions ride along when given. When something optional is missing, decide it from repository convention if the choice is reversible and local, and list the decision in the report; halt only on an outward, irreversible, or ambiguous-target choice.

Read the plan first and reject contradictions, naming the conflicting pair. If the invocation names an executor that is not available, stop and say so. Then confirm approval in one of the forms `references/pipeline-gates.md` defines: a plan approved through plan mode or in writing, including a reply of approved, approve all, run it, or go on right after a plan was presented, or an itemized invocation where every item names a location and the expected change or check. Invoking this skill with a plan subject (a plan file path, a `local://` plan, or a plan written or approved in this session) approves local, reversible work on it: edits, local checks, and local commits when the plan authorizes commits. The gate fires for an outward, irreversible, credential, paid, or data-at-rest act, and waits for a separate explicit user request with preview and consent for each one. Steering words sent after an invocation (`orchestrate`, `continue`, `go`, `do it now`, `workflowz`, `Don't ask`) resume or widen work and approve nothing. A timeout or auto-selected default never approves. An invocation with no subject is not approval: stop before any write. An idea with no plan is not a plan subject. A list given as examples covers only the listed items. Anything else gets no implementation and no delegation: halt and route to `autoplan-and-autopilot`.

## Bind every step to the repository

Before changing anything, gather enough repository evidence to tie each plan step to a concrete artifact (a file, directory, or remote target) and to the behavior, verification, and remote destination behind it. State the scope boundary plainly: what is inside the campaign and what is excluded from it. Everything after this point stays inside that boundary. Then record the preflight from `references/pipeline-gates.md`: the verifier commands, the host tools they need checked against repository pins, and the baseline failure set. A missing tool or a pin mismatch halts here; only the baseline set can make a failure inherited.

## Keep dangerous consequences human-gated

Some consequences always need the human's explicit cover: credentials, paid actions, changes to data at rest, publication, deployment, remote bulk mutation, and irreversible deletion. Preview the exact target and consequence first, and continue only when this invocation covers it. Everything else is reversible local work with version control as the rollback. You push or publish only when the invocation covers that exact target, otherwise you leave changes local. An ambiguous target or absent authority stops the run.

When an iteration loop waits on a human gate, name the smallest gate that unblocks it: the exact action, the signal it contributes, where that signal lives, and the observable condition that permits the next iteration. A gate comes out only through the narrowest existing mechanism, which is one of an invokable command with a deterministic exit status or structured response, a named persisted log file, a read-only metrics or log query yielding an explicit pass, fail, or warn with retained values, or an executable assertion of the observable completion condition. Never introduce a credential, payment, publication, deployment, remote mutation, data-at-rest mutation, or irreversible action to close a gate. Every gate that remains is either one outer-loop human approval before autonomous iteration, or a discrete handoff stating the required action, inputs, and return artifact.

## Follow the chain in order

The chain runs execute, then simplify, then review, then finalize, then report. Report always runs, for success and halt alike. The exact gate mechanics and invariants live in `references/pipeline-gates.md` and that file is binding. On any conflict within autopilot, it governs directly.

Each phase follows the same state machine: run the phase, check its gate, advance on pass. A failing gate fires its autofix arm at most once, then rechecks. A failing recheck halts the chain, never a second autofix. A red gate never advances to the next phase. A gate passes only on a receipt, as `references/pipeline-gates.md` defines; a gate without one halts with the reason `no receipt`.

- execute: Execute the bounded plan against acceptance criteria, constraints, repository evidence, and the required verifier, and record an implementation summary with local verification evidence. This phase covers implementation and local verification only, never the simplify, review, finalize, or CI phases, which autopilot owns. On verifier failure whose cause is not known, `grill-core` runs once on the failing output, through its Findings batch path when several distinct failures appear, then one recheck. A failure with a known cause gets one direct fix by the parent, then one recheck. Execute also needs proof of reach: the verifier output names each new test, each new test was seen failing without its fix, and a user-visible fix ran through its real entry point. A second failure halts with the verifier output and diff recorded. Execute under the orchestration rules in `autoplan-and-autopilot` (sections Build inside the boundary and Prove it on the final tree): the plan's assigned executor, or parallel orchestration when none is named, with disjoint write sets and parent-owned verification.
- simplify: Simplify the completed diff with behavior preserved, under the commit authority `references/pipeline-gates.md` defines: without it, tell `simplify` to commit nothing. A `simplify` exit of `0`, `11` (empty diff), or `12` (false-positive-only) passes. A behavior regression (exit `13`) is self-reverted inside `simplify`. New bloat (exit `14`) or a mixed-concern commit (exit `15`) halts the chain for a human re-plan, with the cause recorded. Read the result code only from the `simplify result` block, which the report quotes; without that block the gate halts with the reason `no receipt`.
- review: An independent reviewer, a fresh context that gets the diff, the plan, and its acceptance criteria but never the executor's conclusions, runs `code-review` on the in-scope change for critical and high findings, unhandled error paths, scope creep, and stubs. When critical or high findings occur, `grill-core` runs once through its Findings batch path on those findings, followed by a re-review of the changed files only and a native verifier pass on the final tree. Zero critical and zero high findings remain inside the diff, or the chain halts with the residual findings listed. Findings in code the diff does not touch are reported as inherited. `grill-core` is an autofix arm for `execute` and `review`, never an independent phase.
- finalize: Finalize the reviewed change: run the required checks. Create atomic commits only when the approved plan or the invocation authorizes commits; otherwise leave the verified tree uncommitted and say so in the report. Push or create-or-update the PR only with explicit shipping authority covering the exact branch, remote, and PR destination; otherwise leave changes local. A finalizer refusal (push refused, checks blocked) is a deliberate safety stop, not a defect to patch. When `git remote` is empty, or `mode:local` is set, run local-only: local checks, commits only when authorized, no push or PR creation, no invented remote, and the report states `mode: local-only` with the unpushed commit list, or `uncommitted` when no commits were authorized.
- report: Emit the handoff on a halt or the finalization report on success, always.

After close-out is authorized and observed, route any supported in-scope fix through execution again, repeat the gates its mutation could disturb, and finalize each authorized update. Never merge, deploy, or publish elsewhere without matching authority.

## Resume

On re-entry, whether a new invocation or `continue`, rebuild state from three sources in this order: the todo list, the ledger and execution receipts for this plan, and the working tree. Then continue from the first pending step. Do not re-plan. Do not re-run a gate that is green on the current tree. Do not restate a prior `BLOCKED` block unless its gate is still red; then state only that gate's current result. A task is done only when a receipt exists for its ID and its contracted state still holds in the tree; otherwise it is pending.

## A halt hands off, never hides

Stop on a missing plan subject, contradictory input, an unavailable executor, an ambiguous target, absent authority, a failed gate, non-converging review, a rejected remote mutation, or incomplete close-out. Preserve successful in-scope work and observed remote state. Undo only mutations this run made, using reversible repository or hosting operations. Never discard unrelated work.

On any halt, stop new dispatch at once. Cancel or collect every in-flight worker, record its state in the handoff, then emit the handoff. Never dispatch after a halt.

Every halt produces the handoff format defined in `references/pipeline-gates.md`. Emit one handoff per halt; later turns answer questions about it and do not restate it unless its gate is still red.

Return `BLOCKED` carrying the failed stage, the exact reason, the autofix result, partial artifacts, remote mutations, proof state, recovery state, and the single concrete requirement to resume. Never claim a rollback, publication, or close-out you did not observe.

## The run ends one of two ways

There is exactly one terminal result. `DONE` delivers the behavior, the changed artifacts, verification evidence, the branch and PR, the complete finalization report (checks, commits, push or PR status), and the close-out state quoted as observed in repository or remote state. Emit the report format defined in `references/pipeline-gates.md`, with the finalization state quoted as observed.

`BLOCKED` carries the halt handoff: what failed, why, what survives, and the one action that unblocks it.
