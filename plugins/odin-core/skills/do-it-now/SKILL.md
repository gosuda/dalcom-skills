---
name: do-it-now
description: 'Use when the user asks to finish the whole task now, clear active todos, or unblock undone implementation without deferred phases or follow-up remainders. Not for bypassing approvals, cutting requested scope, or authorizing publish, deploy, or irreversible changes.'
---

# Do it now

Finish the complete authorized scope. Internal sequencing organizes the work; it never divides the deliverable.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user asks to finish now, ship now, clear active todos, unblock undone work, no phases, or the work would otherwise split into phases, staged rollouts, follow-up PRs, or TODO-later remainders |
| Authority | The underlying assignment sets permitted actions. An implementation request permits its authorized reversible local changes. A plan-only or read-only request permits the complete plan or analysis, not implementation. This skill grants no authority to commit, publish, deploy, use credentials, spend, discard data, or change public contracts |
| Side effect | Each authorized backlog item is resolved in the permitted form: implementation work lands as real behavior with migrated callers and finished proof, plan-only work lands as a complete plan, and read-only work lands as verified findings. Completed items close with evidence, stale blockers clear, reachable blockers drive forward with informative actions, usable worker outputs are salvaged, independent ready work is dispatched, and integration is carried to delivery. No stub, placeholder, no-op, unsupported fallback, or follow-up remainder stands in for requested behavior |
| Done | Every requested outcome and named acceptance criterion is satisfied in the permitted form in the authorized surface, with evidence obtained after the last relevant change, and any scope change carries explicit user approval |

## Inputs

- The ask (required): the requested outcomes and every named acceptance criterion, including integration, consumer migration, documentation, and proof the ask puts in scope.
- The authorized backlog (as available): active todos, task lists, undone implementation, claimed blockers, and worker outputs. Refreshing this backlog never expands scope beyond what the ask authorizes.
- The current specification or plan and relevant implementation (as available): use a sufficiently clear specification or plan directly. Collapse phased steps into one execution order rather than separate deliveries. Do not require a new planning or question workflow.
- Approval boundaries (as applicable): which actions need human approval before they run, such as publish, deploy, credential use, payment, data deletion, or public contract changes.

## Procedure

1. Use the existing specification or plan when it establishes the scope, constraints, and acceptance criteria. Execute authorized work without asking for reconfirmation. Refresh active todos, open tasks, undone implementation, blockers, and usable worker outputs from the task list, plan, and working tree. Resolve repository and tool facts directly. Ask only when an unresolved choice materially changes the outcome or the next action needs authority the user has not granted.
2. Verify and close what is already done. Check each claimed-complete item against its actual state and acceptance evidence, not its list status. Close only items the evidence supports. Reopen items whose evidence is stale, partial, or contradicted, and carry them as open work below.
3. Clear stale blockers with available evidence. Re-examine each claimed blocker against the current tree, configuration, captured output, and completed work above. A blocker whose condition no longer holds is cleared with the evidence that clears it. A blocker held only by an outdated status, an old log, or a superseded assumption is re-tested through an authorized observation before it is allowed to stop anything.
4. Account for the whole remaining ask. List requested outcomes, acceptance criteria, affected consumers, and approval boundaries. Do not redefine the task around the subset that was easiest to implement.
5. Execute in dependency order and dispatch independent ready work. Use internal phases, separate local commits when authorized, and delegated work when useful. Continue through integration to final delivery. A finished internal phase, a worker return, or an updated task list is progress, never a stopping condition. Size and phase boundaries are never reasons to stop.
6. Implement real behavior on every required path. Migrate affected callers and remove obsolete paths inside the authorized scope. Finish required tests and documentation. Do not leave TODO, stub, placeholder, raised NotImplemented, or labels such as foundation, phase 2, later, or follow-up where the ask requires behavior.
7. Drive each remaining blocker with informative unblock actions. Inspect the cause, salvage every usable partial worker output instead of discarding it, and take the next authorized action that produces new information or changes the blocking condition. An actionable blocker, one with an authorized informative action available, is work to execute, never a reason to stop. Do not convert an executable next step into advice for the user or a remainder for another turn.
8. Reconcile the integrated result against the original ask. Check every acceptance criterion, including error paths and consumer contracts the change affects, and confirm every backlog item is closed with evidence or reported as blocked below.
9. Obtain completion evidence after the last relevant change with the assignment permitted verification actions. Read the result and exit status where applicable. Match each claim to evidence at that scope. Source presence, compilation, and worker assurances do not substitute for a required behavior check. When verification is prohibited, finish the permitted deliverable and state exactly which behavioral claims remain unverified. Do not run a prohibited check and do not claim unperformed checks passed.
10. Return the completed deliverable with concise evidence. Report what exists and works now, not an intended rollout or an implementation promise.

## Scope changes and blockers

- Never cut scope because the work is large, is inconvenient, or has reached an internal phase boundary. Never expand scope because the backlog refresh surfaced adjacent ideas. The authorized backlog bounds the work in both directions.
- When a genuine constraint requires a scope change, state the concrete conflict, the exact proposed change, and its consequences, then obtain user approval before adopting it. Until approval, the original scope remains the obligation. Finish independent reachable work while waiting only when doing so preserves a coherent state and stays inside granted authority.
- When completion depends on an unavailable prerequisite or ungranted authority, stop before the blocked action, finish independent reachable work, and report the exact missing prerequisite, the affected outcome, and what enables continuation. Preserve a coherent local state. A blocked or partial result is not complete, and a truthful blocker is not a placeholder. Actionable blockers do not qualify: while an authorized informative action remains, the obligation is to act.
- Permission, security, credential, and paid boundaries hold. Publish, deploy, credential use, payment, data deletion, and public contract changes run only on explicit human invocation for that action. Core placement grants no additional authority. No fabricated evidence ever substitutes for a missing observation.
- Plan-only remains plan-only. A plan-only or read-only assignment permits the complete plan or analysis, including verified findings and concrete corrections, not implementation.

## Failure and recovery

- Unshipped remainder found (TODO, stub, placeholder, NotImplemented, phase-2, later, follow-up): write the real implementation inside the authorized scope.
- Completed item without supporting evidence: reopen it and carry it through the procedure. Do not close todos by status alone.
- Stale blocker cleared by new evidence: record the clearing evidence and proceed. Do not preserve the old blocked status.
- Usable worker output discarded or ignored: recover the usable portion, integrate it, and obtain fresh evidence for the integrated result.
- Genuine constraint conflicts with the full ask: propose the exact scope change with reasons and wait for approval. Do not ship the reduced scope first and report it as done.
- Prerequisite or authority missing: finish what is independently reachable, name the precise blocker, and stop the blocked path. Do not invent certainty around the blocked outcome.
- Verification prohibited or unavailable: name the unverified claims and the exact restriction. Do not label them verified.
- Failed edit or verification on owned work: repair the source. When recovery requires undoing an owned edit, preserve unrelated and intervening user changes. Never restore a stale file over them.

## Output

Return the complete requested artifact or integrated change, the backlog disposition with each todo closed by evidence or carried as blocked, cleared stale blockers with their clearing evidence, salvaged worker outputs reused, the acceptance evidence actually obtained after the last relevant change, and any explicit user-approved scope change with its reason.

When blocked, separate completed work from the exact unmet requirement, name the missing prerequisite or approval, and state what enables continuation. Do not describe a partial result as shipped or done.
