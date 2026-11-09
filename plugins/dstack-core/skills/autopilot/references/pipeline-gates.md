# Autopilot: pipeline gates and the autofix-then-halt state machine

This file is the authoritative source for every phase gate, its autofix arm, and halt behavior. `SKILL.md` summarizes the process; this file defines the exact criteria, invariants, and state machine. It is self-contained: on any conflict within autopilot, this file governs both mechanics and doctrine directly. No external baseline or peer doctrine is needed to interpret or enforce these gates.

## The autofix-then-halt state machine

One generic transition runs every phase. `P` is the current phase, `gate(P)` its gate, `A(P)` its autofix arm (may be none).

```
RUN(P):        invoke the phase's skill
CHECK(P):      evaluate gate(P)
                 pass            -> ADVANCE
                 fail, A(P) none -> HALT(P)
                 fail, A(P) set  -> AUTOFIX(P)      [only if not already attempted this phase]
AUTOFIX(P):    invoke A(P) exactly ONCE; then RECHECK(P)
RECHECK(P):    evaluate gate(P)
                 pass            -> ADVANCE
                 fail            -> HALT(P)          [never a second AUTOFIX]
ADVANCE:       P := next phase in {execute, simplify, review, finalize, report}; goto RUN(P)
HALT(P):       stop the chain; collect residual findings from P; route to report with halt=P
```

Invariants the machine enforces:

- Once: `AUTOFIX(P)` fires at most one time per phase. A failing `RECHECK` always routes to `HALT`, never back to `AUTOFIX`. Looping an arm to green hides a bad plan and compounds risk across a growing surface.
- No red advance: `ADVANCE` is reachable only from a passing `CHECK`/`RECHECK`. A red gate never enters the next phase.
- Report is terminal and unconditional: Both the success tail (after finalize passes) and every `HALT(P)` route to `report`.
- Publication authority: Remote publication, pushing, pull request creation, and remote mutation require explicit human authority naming the exact target. Local work is reversible with version control as rollback; without explicit publication authority covering the exact branch and remote, the chain remains local-only.
- Local-only execution: When `git remote` is empty or `mode:local` is active, no remote is invented or contacted; finalize runs local checks and creates atomic commits locally.
- Receipts: a gate passes only on a receipt another reader can check. Execute: each verifier command with its exit code and the names of the new or changed tests its output shows. Simplify: the `simplify result` block, quoted. Review: the reviewer's verdict with its critical and high counts. Finalize: the finalizer report with its check results and the commits or the pull request URL. An autofix arm: the `grill-core` root cause line. A gate without its receipt has failed: report it as HALT with the reason `no receipt`, never as passed. A phase reports `skipped` only when an earlier HALT kept it from starting.
- Inherited failures: a failure is inherited only when the preflight baseline holds the same identity and the diff does not touch the file it names. Every other failure is red. Inherited failures never block, and the report lists them on its `inherited:` line. Review applies the same rule: a critical or high finding in code the diff does not touch is inherited and does not block.

## Precondition: before execute

The chain begins only when an approved plan exists: one the user approved through Claude Code's built-in plan mode (`ExitPlanMode`), or an equivalent written plan the user has approved. autopilot never produces it; "scope unknown" is not autofixable and has no arm. Fails → do not start; HALT before execute and hand off to upstream `askme` / planning, where the user must supply an execution-ready task.

## Preflight: before execute

Before the first edit, record two facts that the gates and the report use.

1. Verifier commands: resolve the repo-native build, type-check, and test commands from repository files (task runner, manifest, CI workflow) and name each one.
2. Baseline failures: run those commands once on the pre-change tree and record every failure by identity: test name, or diagnostic rule plus path plus message. An empty set is a clean baseline. This set is the only evidence that may later call a failure inherited.

## Per-phase gate definitions

The semantic phases are **execute**, **simplify**, **review**, **finalize**, and **report**. Gate names correspond directly to each gated phase: **execute**, **simplify**, **review**, and **finalize**. `grill-core` is an autofix arm attached to `execute` (for verifier failure) and `review` (for critical and high findings), not an independent phase. `report` is terminal and gateless, running unconditionally on success or halt.

| Gate | Phase / operation | Pass criteria (exact) | Autofix arm A(P) | On RECHECK still-fail |
|------|---------------|-----------------------|------------------|-----------------------|
| execute | execute (orchestrated) | Orchestrated execution covers implementation and local verification only, returning a structured summary; the plan's steps are implemented, the repo-native verifier (build / type-check / test, as the repo defines) exits clean apart from inherited failures, and proof of reach holds: the verifier output names each new or changed test (a selection that matched zero tests proves nothing), each new test was observed failing with its fix absent, and a user-visible fix ran once through its real entry point (the binary, CLI, endpoint, or screen a user touches). It must not run the simplify, review, finalize, or CI phases; autopilot owns those. | `grill-core` once on the failing verifier output, through its Findings batch path when the output holds more than one distinct failure | HALT → hand off the verifier failure and the diff so far |
| simplify | simplify | `simplify` ran and its quoted `simplify result` block shows code `0`, `11` (empty diff), or `12` (false-positive-only); behavior preserved. The code is read only from that block. | none distinct, `simplify` self-reverts a behavior regression (its exit `13`) internally | HALT on exit `14` (new bloat) or `15` (mixed-concern commit): these need a human re-plan |
| review | review (`code-review` by an independent reviewer) | An independent reviewer ran `code-review` on the in-scope diff against the approved plan and its acceptance criteria and returned a verdict with file-and-line findings. After at most one `grill-core` pass and a re-review of the changed files by the same reviewer, no critical or high finding remains inside the diff. | `grill-core` once through its Findings batch path on the critical and high findings, then re-review of the changed files only | HALT → hand off residual critical/high findings |
| finalize | finalize (local checks, atomic commits, authorized push/PR) | Finalizer report returned: checks green and PR created/updated (full mode), or commits made and push skipped (local-only). The report carries review findings, check results, publication classification, and PR URL or local-only status. | none; a finalizer refusal (push refused, checks blocked) is a deliberate safety stop, not a defect to patch | HALT → hand off the finalizer's blocked report and the unpushed commits |

`grill-core` is an autofix arm (supporting `execute` and `review`), not an independent phase, and has no separate gate. `report` is the terminal reporting phase; it evaluates no gate and always runs.

An independent reviewer is a fresh context, a subagent where the harness has one, that receives the diff, the approved plan, and the acceptance criteria, and never the executor's summary or conclusions. With no subagent facility, re-read the diff from disk, run `code-review` inline, and say so on the report's `gates:` line.

## Local-only detection

Run `git remote`. Empty output → local-only; also forced by `mode:local`.

Local-only effect:
- finalize: the finalizer runs the local check suite, makes atomic commits, and skips push and PR creation. No remote is invented. The report states `mode: local-only` with the unpushed commit list.
- report: report still runs and the report states `mode: local-only` with the unpushed commit list.

## Halt handoff format

On `HALT(P)`, the report phase emits a handoff so the next operator resumes without re-deriving state:

```
HALT at <phase> (gate <gate-name>)
reason:        <one line — what the gate measured and why it stayed red>
autofix tried: <A(P) name + outcome | none — not autofixable>
residual:      <the findings / verifier output / refusal that remain>
state:         <commits made (sha + subject), pushed? PR url?, working-tree dirty?>
next:          <the single action that unblocks: e.g. "return to plan mode for a narrower approved plan", "resolve test X", "authorize push to <branch>">
```

## Report format (success or halt)

```
autopilot report
mode:          <full | local-only> [+ headless]
task:          <one line>
phases:        execute <✓ | HALT> · simplify <✓ | HALT | skipped> · review <✓ | HALT | skipped> · finalize <✓ | local-only | HALT | skipped> · report ✓
autofix:       <grill-core firings in phase order, one per phase that fired: execute: <root cause line>; review: <root cause line> | not needed, every gate passed on its first check>
gates:         <per gate, pass or fail with its receipt: execute verifier commands, exit codes, and new test names; the quoted simplify result block; the reviewer verdict with critical and high counts; finalize checks plus commits or the pull request URL>
inherited:     <baseline failures and out-of-diff findings left as found | none>
commits:       <sha + subject per commit>
remote:        <pushed branch / PR url | local-only, not pushed>
outcome:       <shipped | HALT at <phase> (gate <gate-name>), see handoff above>
```
