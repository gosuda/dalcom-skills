---
name: code-review
description: 'Use when a named diff or pull request needs review for bugs, regressions, tests, and standards. Not for reviewing requirements or plans, handling feedback already left on a PR, or shipping the change.'
---

# Code review

Anchors: David Parnas (review hides no defect behind familiarity; every finding names its evidence), Dieter Rams (an adequate change needs no findings).

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A named diff, branch range, or pull request needs review against intended behavior and project requirements. |
| Authority | Read-only by default. Applies corrections only on explicit apply authorization in the invocation, and then only inside the reviewed scope. No pushes, PR opens, ticket filings, branch switches, or working-tree checkouts to reach the scope. |
| Side effect | Findings with code evidence and consequences, coverage with explicit limits, and a clear verdict; optionally authorized local corrections with checks. |
| Done | Required review and validation are complete, retained findings are supported by source, the caller has the result with coverage limits, and any authorized corrections are checked. |

## Inputs

- The reviewed scope: explicit revision range, branch with determinable base, or PR identity. Required. Resolve the base from explicit input or PR/upstream/remote-default evidence; never guess the base. Uncommitted work is reviewed only from the checkout that holds it.
- Scope mode and depth signals: full vs focused signals from size, risk, and touched surfaces. Required to record; depth follows risk, never a fixed count.

Judge the code against intended behavior and project requirements, not a preferred rewrite. Serious defects matter even in a small diff. An adequate change needs no findings.

## Procedure

1. Resolve and summarize intent. Establish what the change intends, its plan or requirement source when one exists, and the scope mode. Record what is in scope and what is explicitly out of scope.
2. Select lenses from risk. Always cover correctness, regressions, tests, and applicable standards for the touched surfaces. Add conditional lenses only on evidence: security for trust boundaries, data handling, or auth; concurrency for shared state; migration for schema, wire, or persisted shapes; performance only for measured hot paths. Name the selected lenses with one-line reasons.
3. Review against evidence. Every finding cites file:line, the offending code, the requirement or behavior it violates, and the consequence that justifies action. No invented issues and no style-only findings. Check claims against the whole change and project facts; reviewer suspicion is not a finding until verified.
4. Report with coverage. Deliver the verdict, findings ordered by consequence, and explicit coverage: what was examined, which lenses ran, and limits (unreadable paths, unavailable evidence, deferred surfaces). Note uncertainty rather than stopping to ask: this skill never blocks on questions.
5. Apply only when authorized. An explicit apply authorization in the invocation permits local corrections inside the reviewed scope with the narrowest applicable checks. Report-only is the default; a nested workflow later repair owns follow-through. Never push, open PRs, or file tickets from this review.

## Failure and recovery

- Scope unresolvable or unreadable: return blocked with the missing identity or path. Dispatch no review on an unreachable scope.
- Evidence insufficient for a lens: mark the lens limited in coverage, not failed; do not invent findings.
- Adequate change: return the clean verdict with coverage. Do not manufacture findings.
- Apply requested without authority or beyond scope: refuse the excess and report the boundary.

## Output

Return the verdict, findings with file:line evidence and consequences, coverage and limits, and, when apply ran, the corrected files with check results. No machinery narration and no downstream action follow from a report-only review.
