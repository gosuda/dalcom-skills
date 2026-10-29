---
name: retune
description: 'Use when a skill corpus degrades on a new model and needs measurement-first retuning against a registered bar. Not for word-reduction passes, single-skill edits, or static audits presented as retuning. Explicit request only; never auto-invoked.'
---

# Retune a corpus for a new model

Anchors: David Parnas (behavior is the contract; prose edits without measured effect are not repairs), Dieter Rams (cut only what measurement proves removable).

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A corpus performs worse on a named target model and the user requests retuning it. |
| Authority | Read-only measurement plus explicitly authorized corpus edits in the named corpus path. No test weakening, no harness invention billed as behavior proof, no publication, remote, credential, paid, or destructive mutation. Explicit user request only; this skill never auto-invokes and never runs headless self-improvement. |
| Side effect | A corpus whose measured behavior on the target model clears a pre-registered bar, with regression classes removed and each removal attributable, or an explicit unsupported claim. |
| Done | The registered bar is cleared and reported with what stayed unmeasured, or the run reports the specific claim it could not support. A green test suite alone is not done. |

## Inputs

- The target model and the symptom. Required.
- The corpus path (default `./skills` only when the invocation names no other corpus). Required to fix before editing.
- The acceptance bar: consecutive clean runs or equivalent bar with its count. Required to register before any change.

Word reduction is a non-goal. Leanness is a separate program; report completion, not word counts.

## Procedure

1. Check the measurement gate first. Require all three: a run archive or harness producing per-run tool-call traces, terminal markers, and final messages; a build selector letting one runner compare two corpus checkouts; a repeatable task the corpus executes end to end. When any is missing, stop and name what to build. Never present a static audit as retuning.
2. Mine history before spending runs, then establish the noise floor. Run the harness against two identical corpus copies at the same commit; the observed difference is the floor every later claim must clear. Register the bar in writing before any change exists. A bar chosen after results is not a bar.
3. Audit adversarially with independent contexts: one worker per skill proposes cuts, a separate worker defends existing prose. When no independent worker facility exists, report that as a blocker and stop the audit rather than arguing both sides in one context.
4. Cut in surgical passes, one problem per change. Fan out by disjoint file ownership, never by item. Never edit a test to make a suite green: a removed string a test pins is a finding to report, not a test to weaken. Sort every stop by who is on the other side before touching it; workflows that exist to stop and ask are the product, not the defect.
5. Measure after each pass and let the failure choose the next fix until the registered bar clears. Then stop. Report what stayed unmeasured: a cleared bar never implies coverage it does not have.
6. Ship the corpus change with what each commit preserves and removes attributable. Keep the bar, floor, and measurement evidence with the result.

## Failure and recovery

- Measurement gate missing: blocked with the exact missing piece. No fallback audit.
- No independent audit contexts: blocked audit; no single-context adversarial result.
- Bar not cleared: report the failing sites and the next fix they select; do not claim success.
- Explicit limit reached: stop incomplete with evidence and remaining scope. Limit exhaustion is not convergence.

## Output

Return the target model, harness found, floor and bar, passes with attributable removals, measurement evidence per pass, unmeasured scope, and the cleared or blocked verdict. Never report prose reduction as behavior proof.
