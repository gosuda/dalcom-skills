---
name: contraint-driven
description: 'Use when no quality bar is written down, when setting up constraints, or when implementing under non-negotiable budgets, limits, or API rules. Not for one-off spikes or remote, credential, publish, deploy changes.'
---

# Constraint-driven development

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Establishing a project quality bar as a written contract, or implementing under explicit non-negotiable constraints such as performance budgets, platform limits, or legal or API rules. |
| Authority | Reversible local: writes only the constraints record and constrained code changes in the working tree; rollback is undo. No VCS history, credential, or remote mutation. |
| Side effect | A constraints record and the code changes that satisfy it, both local and revertible. |
| Done | The bar is written with numbers and checks, all stated constraints verifiably pass in the delivered change, no unrelated behavior regressed, and no check was weakened to reach green. |

## Inputs

- Required: the set of non-negotiable constraints the change must satisfy, each stated as a measurable predicate with a target value and a checkable condition. A constraint that arrives as prose without a measurable form must be converted to one before any code is written.
- Optional: an existing constraints record that already governs the target tree.
- Optional: the target numbers when the user has them; otherwise measure the current state and hold the line.

## Procedure

1. Read the target tree once to learn language, stack, test runner, and any existing constraints record. Report what was found in two lines, then ask only what is left. Do not ask for what is readable. Done when: the stack and test runner are known and the existing record, when present, is read.
2. Ask at most four questions, each with a usable default so lack of an answer still produces a working config. Ask which dimensions beyond the floor matter, whether a mid-task failure blocks or warns, whether to measure today and hold the line or adopt a supplied number, and what slowest check is tolerated before handoff. Stop at four. Done when: the four answers or their defaults are recorded.
3. Write one CONSTRAINTS.md file at the repo root. Include a floor that is always enforced without setup: no new suppression comments, no unimplemented stubs, no skipped or deleted tests without a reason in the commit message, no secrets in source, and the file itself does not get weakened to make a change pass. Add an enforced table with one row per dimension carrying Dimension, Rule, Checked by, and Runs at; every row names the command that produces the verdict, and a dimension with a number and no command is an aspiration, not a constraint. Add a measured table with today value and direction for ratchets. Add an exceptions table with ID, Rule, Path, Reason, Owner, and Expires. Then point the project instructions at the file with one line: read CONSTRAINTS.md before writing code and do not weaken it to make a change pass. Done when: every number has a stated reason and every enforced row names its check command.
4. Install only what each chosen dimension needs, using the project existing config and de facto checkers where they exist: types, lint, coverage on changed lines, secrets scanning with redaction, code and dependency security scanning, page performance against a running URL, bundle budgets, accessibility scanning, architecture boundary checks, and mutation on touched files where the budget allows. Add the project own scripts so the checks reproduce without an agent: a fast check after an edit, a task check when done, and a full check in CI. The CONSTRAINTS.md file is canonical; scripts are convenience wrappers that must mirror it, and on drift the file wins. Lighthouse and axe need a running URL and belong against a preview deploy or a started local server; when the project has no URL to hit, drop the dimension rather than inventing a check that cannot run. Scope expensive checks to the diff. Read coverage from the suite already-written output intersected with the diff rather than running the suite twice. Done when: each chosen dimension has a runnable mechanism or is explicitly dropped as inapplicable.
5. Bound the change scope before mutating: list the files the work will touch. Constraints apply to the diff, not the whole tree, unless a constraint is explicitly project-wide. Capture the baseline: run each constraint checked-by command against the current tree and record the measured value. This baseline is the floor: the delivered change must not produce a worse value for any constraint. Done when: the change scope is bounded and every constraint has a recorded baseline value.
6. Implement the change. After each edit run the fast subset of checks scoped to the touched files. Done when: the change is implemented and the fast checks pass for each edit.
7. Validate against the baseline guard and the bar guard. For each constraint, re-run its checked-by command on the delivered change and compare against the baseline; tightening is silent and loosening is a violation. Watch the diff for the five cheap roads to green: a threshold moved, a test made easier, a checker silenced including istanbul ignore, Stryker disable, nosemgrep, and gitleaks allow, unfinished work such as a stub, empty catch, or TODO standing for implementation, and a new exceptions row. Compare CONSTRAINTS.md against its branch-point state; loosening must be loud. Rank checks by circularity: external checks encode outside facts, project checks encode human-owned rules, and the project own suite is the only genuinely circular kind; keep at least one external check in the bar. Adapt the bundled floor-guard reference rather than inventing a second checker. Done when: every constraint is re-measured with none worsened, and no bar-weakening move remains in the diff.
8. Run the full check set: every constraint checked-by command against the complete change, plus the project test suite. Scope expensive checks to the touched files. Done when: every checked-by command runs and the test suite passes.

## Failure and recovery

- Unmeasurable constraint: stop and convert it to a measurable predicate with a target value before any code change. Do not proceed on prose. Do not substitute a self-invented target for a missing number.
- Baseline guard violation: a constraint worsened against its baseline. Fix the code, or route the deviation through a tracked exception with an owner and an expiry; never weaken the constraints record to make a change pass.
- A constraint cannot be re-measured after the change: the constraint is unverified. Do not treat the change as clean; report that the guard could not run and hold the change for a human.
- A constraint fails at task end: fix the code, not the constraint. Relaxing a threshold is a separate human decision recorded as an exception, not a side effect of implementation.
- Interview without a live user in CI or autonomous runs: apply the floor only, note that choice, and flag the rest for a human.
- Partial result: deliver only the subset of changes for which every constraint verifiably holds and revert the rest. Never claim the done predicate holds for work that was not checked.

## Output

CONSTRAINTS.md naming each invariant with its check and baseline value, the delivered code change in which every constraint holds without regression, and a check-run report stating which constraints passed, which baseline-guard violations were flagged with none on success, and any constraint that could not be checked and why.

## Verification and defaults

- Verification: CONSTRAINTS.md exists, every number has a stated reason, every enforced row names its check, exceptions carry owner and expiry, instructions point at the file, and a trial run on the current branch produces no failures the user disagrees with.
- Defaults with reasons: changed-line coverage at least 80 percent, high enough to force a test and low enough to allow a config line; project coverage holds today value; mutation at least 60 percent to start; dependencies nothing at high or above; LCP at most 2500ms and CLS at most 0.1 per Core Web Vitals good; accessibility zero critical or serious axe violations; exception lifetime 90 days; ratchet tolerance 0.5 percent. State the number and the reason together.
- Escalation: start written only, then scripted checks wired into the edit hook and CI, then a dedicated runner when the config outgrows a shell script. A first run can be floor-only with no installs.
