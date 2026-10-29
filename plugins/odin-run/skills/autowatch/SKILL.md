---
name: autowatch
description: 'Use when the user explicitly asks for autonomous end-to-end work from request to open pull request with CI watched to decided. Not for step-by-step supervised work and never as an alias for lfg.'
---

# Autowatch

Take one request to the end state its shape calls for through the skill whose job that is, with everything unresolved recorded where the user will see it. A code change ends as an open PR whose URL you hold, with CI decided, after implementation, simplification, review, residual recording, learning capture, commit, push, and watch. Merging stays with the user unless granted for this run.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User explicitly asks for autonomous end-to-end work or invokes `autowatch` directly. Step-by-step supervised work belongs to `plan`, `work`, `fix`, or `commit-push-pr` directly. |
| Authority | Human-granted autonomy for reversible work; human-gated for every irreversible or outward act. A configured remote alone grants no publication authority. Push, PR create or edit, CI watch with pushes, and Proof publish each require the explicit grant carried by this invocation. Merge, force-push, data deletion, paid operations, and credential changes are never implied; each needs its own explicit grant for this run. When `git remote` is empty, require explicit consent to proceed local-only, then commit locally and skip push, PR, CI watch, and merge entirely. That local-only terminal is success with reduced scope, not an error to work around. |
| Side effect | At most one feature branch, local commits, one push to `origin`, one PR created or updated, bounded fix pushes, one learning record when earned, and one watch report. No second branch, no merge without its grant, no silent local-only publication. |
| Done | The request reached the end state its shape calls for with the owning skill result, residuals recorded durably, the PR URL held when a PR exists, CI decided when a PR was watched, and a final report stating DONE or the exact stop with its reason. Reporting the PR URL alone is not done. |

Parnas boundary: owns routing, work-source verification, sequencing, residual handoff, and close-out. Does not implement (`work`), diagnose (`fix`), review (`review`), adjudicate threads (`resolve`), curate learning (`compound`), author commits (`commit`), publish the PR (`commit-push-pr`), or run the watch cycle (`watch-and-repair-pr`). It calls those owners with bounded packets and reads their returns; it does not reimplement them.

## Inputs

- The request: feature, bug report, issue reference, plan path, or a result whose owner is a single skill.
- Optional assignment of planning or implementation to a model or harness on the invocation; sanitized and passed as a carrier, never searched from disk.
- Explicit grants on this invocation: permission to push, to create or edit the PR, to watch with pushes, to publish a Proof share, and, only when separately stated, to merge.

## Procedure

1. Route by what the request is. A plan path or a plan this session wrote takes the plan route. A concrete report of failing or wrong behavior takes the diagnose route. A change hanging on an unsettled judgment takes the decision route first; only a verdict supporting the change continues. Product shape with more than one plausible reading and a human present takes framing first, otherwise planning. A request whose result is not a code change goes to the skill owning that result; that invocation is the whole run. Any other code change goes to planning. When unsure take the route asking more of the evidence. Never search the plans directory for a candidate or act on a discovered file; never plan from scratch over an existing plan.
2. Produce the work source and verify it this run. On the plan route brief settled decisions and the artifact-root rule, then use the identified plan only when it passes the readiness check; a `blocked` return or an invalidated settled decision stops the run with nothing pushed. Only the absence of both a blocker and a reported plan file invokes planning once with the same arguments. On the defect route the verified diagnosis fix is the implementation. Without a verified work source stop and state why.
3. Implement through the owning skill with a return-to-caller packet naming the verified plan path. Only a valid `complete` return advances; every other status or malformed return stops the pipeline.
4. Simplify the branch diff when the change exceeds a trivial docs-only or sub-10-line edit; skip only that invocation with the reason stated.
5. Review the branch diff against the plan (omit the plan link on the defect route). A finding whose evidence shows the settled decision cannot work (infeasible, wrong thing, destructive) stops the pipeline as blocked before any shipping precondition.
6. Shipping precondition, checked before every push from here on. Run `git remote`. When empty, require explicit consent to proceed local-only; on consent make every commit the steps call for, then skip push, PR create and edit, and CI watching, and close as local-only DONE. On withheld consent stop with nothing committed. Do not invent a remote, change the URL, or proceed silently.
7. Apply and persist eligible review fixes; do not proceed while eligible fixes remain uncommitted. Record every unapplied actionable finding, conflict stamp, or flagged decision durably: in the PR body when a PR will exist, otherwise in tickets or the DONE report. Never output DONE while residuals remain only in memory. Never block DONE on tracker-write failure once the report states it. Do not prompt inside this autonomous run.
8. Capture learning only when the run produced durable reasoning the code, tests, and plan do not carry, by invoking `compound` once in non-interactive mode. `Documentation skipped` is success; the learning lands in the PR at open when one will exist.
9. Publish through `commit-push-pr` in its full or no-PR mode per the granted scope, with an explicit publication grant. Never push a set the human has not approved in shape; autowatch carries the invocation grant, not a silent default.
10. When an open PR exists and watching was granted, watch it with `watch-and-repair-pr` to CI-decided. Do not reimplement CI watching, poll by hand, or substitute another watcher. When watching was not granted or no PR exists, record CI as unwatched with its reason.
11. Close out with one line stating DONE plus the PR URL when one exists, CI decision, residuals location, and learning outcome; or the exact stop (no work source, blocked review, withheld consent, local-only, missing grant, out-of-budget) with what was left unpushed and where residuals live. A stop leaves nothing pushed that was not already pushed.

## Failure and recovery

- No work source, blocked plan or diagnosis, non-complete implementation return, or blocked review finding: stop, state the reason, leave nothing newly pushed.
- Missing push, PR, watch, publish, or merge grant: stop before that outward act; complete all reachable local work, record residuals, and report the missing grant.
- Empty remote without local-only consent: stop with nothing committed.
- Child return incomplete or malformed: stop; do not retry by broadening scope.
- Settled decision invalidated or project shipping gate unmet: stop before the external write and name the gap.
- Budget exhausted: stop at the current true state; report applied work, residuals, and the budget bound.

## Output

DONE with the owning-skill result, and for code changes the branch, commit hashes, PR URL, CI decision, residuals location, and learning outcome; or a named stop with the same accounting and nothing newly pushed beyond what the report states. No `lfg` alias is emitted or accepted.
