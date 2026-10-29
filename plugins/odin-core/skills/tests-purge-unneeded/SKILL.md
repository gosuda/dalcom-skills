---
name: tests-purge-unneeded
description: 'Use when a legacy, slow, or duplicate test suite needs purging, a post-refactor sweep is due, or types cover a contract.'
---

# Purge unneeded tests

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A legacy, slow, or duplicate test suite is being cleaned up, a post-refactor sweep is due, or the type system already covers an asserted contract. |
| Authority | Reversible local: deletes only VCS-tracked test files and makes temporary production mutations for mutation proof only in enumerated VCS-tracked production files, all reverted before the next step or before reporting; rollback is version control recovery. No remote, VCS-history, credential, paid, published, or deployed mutation. Shows the exact deletion set before cutting. |
| Side effect | Deletes proved-useless tracked tests in batches, keeps anything whose matched proof fails, and runs the full suite after each batch. |
| Done | Each deleted test has one recorded proof of its matching class, the full suite passes, and no protected boundary test was removed without proved subsumption. |

## Inputs

- Test suite root (required): directory or glob identifying the test files to audit.
- Language or framework (optional): if omitted, detect from project config files (package.json, Cargo.toml, pyproject.toml, go.mod, pom.xml, build.gradle).
- Scope constraint (optional): limit audit to specific directories, file patterns, or changed-files-only mode.
- Production sources under test (required for cold execution): the files the tests exercise must be readable. If they are not readable, stop as blocked instead of guessing.

## Refusals

- Will not delete a test whose matched proof failed; it is load-bearing.
- Will not delete a protected boundary test (protocol compliance, error semantics, security invariants, real-I/O integration, concurrency semantics, `unsafe` contracts, property invariants) unless surviving coverage demonstrably preserves its required cases and detects the relevant defects through proved subsumption. Meaningful coverage is protected, not every existing file.
- Will not invent a mutant for every deletion and will not infer worthlessness from one missed mutant. Proof class must match the case.
- Will not persist any production-code mutation beyond the proof step.
- Will not delete a test whose failure mode cannot be articulated after investigation; keep it pending human review.
- Will not write strategy documents or marketing copy as part of a purge.
- Will not expand scope beyond the declared root or constraint to resolve a finding.

## Procedure

1. Bound scope. List every test file path under the audit root. Do not expand scope beyond the declared constraint. Done when every file path in the audit set is listed and reported.
2. Investigate candidates aggressively. For each test, read the production code it exercises and its direct callers. Check for stale claims (the asserted flag, symbol, behavior, or error path no longer exists), empty ceremony (tautology, mock-only, coverage-driven, trivial snapshot, just-in-case with no named bug), duplicated ownership (two tests cover the same case; map to the stronger owner), and noise (implementation-coupled private-method assertions that pin internals rather than behavior). Classify with reasons using `references/keep-vs-delete-table.md` and the language reference (`references/rust.md`, `references/typescript.md`, `references/python.md`). A constructor that only assigns parameters is direct pass-through and the compiler covers it; a constructor that validates, normalizes, defaults, transforms, or deserializes runs real logic and its test is a real-bug test no matter how trivial the result type looks. Done when every test is classified candidate or not-candidate with a reason.
3. Articulate the bug and select the proof class. For each candidate write one sentence of the form "this test fails when ___ goes wrong." Name a concrete failure mode a real code change could plausibly introduce. If no such sentence can be written after reading the code, mark the test unarticulable and keep it pending human review. Otherwise select the cheapest sufficient proof class from the table in step 5: A (compiler guarantee), B (demonstrated tautology), C (proved subsumption), or D (meaningful mutation). Done when each candidate has a failure sentence plus a selected class, or is kept as unarticulable.
4. Guard the protected boundary. If a candidate verifies protocol compliance, error semantics, security enforcement, real-I/O behavior, concurrency semantics, an `unsafe` contract, or a property invariant, deletion is allowed only through class C: name the surviving tests, map each required case to a surviving assertion, and require that the survivors detect the relevant defect class. Redundant security coverage stays unless the same attack path is proved covered elsewhere. Done when each boundary candidate is kept or has a complete subsumption mapping.
5. Execute the matched proof. Apply only the selected class.

   | Class | Proof |
   |---|---|
   | A compiler guarantee | Cite the enforcing check and the language reference. No production edit. |
   | B demonstrated tautology | Show the outcome follows from the test itself. Record the evidence. No production edit. |
   | C proved subsumption | Run the named surviving tests on current code (they must pass) and record a per-assertion table mapping every assertion in the deleted test to a specific surviving check; extend the surviving suite or keep the test for anything unmatched. |
   | D meaningful mutation | Modify the VCS-tracked production file to introduce exactly the named bug, run the candidate test, record survived or caught, then revert immediately before the next step. If caught, keep and record. Never leave a mutation in the tree. Do not use a second mutant to overrule a settled class A, B, or C verdict. |
   Have a reviewer who did not build a class C subsumption mapping confirm each entry exercises the same observable behavior before deleting; return disputed entries to extension-or-keep.

   Done when every remaining candidate has a recorded proof result.
   Before mutating an enumerated production file, preserve its actual pre-probe content, including uncommitted work. Apply one attributable mutation and verify that it landed. Run the intended test and record the selected test population, producer status, and specific behavioral result. A compilation or setup failure does not show that the test catches the claimed bug.

   Restore from the preserved pre-probe content before the next mutation or any deletion. Verify content identity against that preserved state, not merely against HEAD, and confirm the relevant tests again. Isolate or invalidate runtime artifacts when needed so the run exercises the intended source rather than stale mutant code. Do not delete unrelated caches.

   A caught mutation keeps the test. A survived mutation is only a candidate-specific deletion witness, still subject to the existing boundary and language protections. Restoration failure stops the purge and reports the affected files; it must not be hidden by a passing suite.
6. Delete in batches. Delete only tests whose matched proof records uselessness (compiler guarantee holds, tautology demonstrated, subsumption proved, or named mutation survived). Before committing each batch, search the declared audit root and constraint for live references to each deleted path and update or remove them; annotate historical records instead of rewriting them, and stop the batch on unresolved dangling references. Each batch is an atomic commit with a rationale naming the proof class and evidence. Run the full suite after each batch. On regression, revert the batch and investigate. Done when all proved-useless tests are deleted in atomic commits and the suite passes after each batch.
7. Report. Emit the output artifact. Done when the deletion report is emitted.

## Failure and recovery

| Failure class | Condition | Recovery |
|---|---|---|
| Framework not detected | Cannot identify test runner or language | Abort. Report: test framework not detected; manual identification required. |
| Production sources unreadable | Cannot read the code the tests exercise | Block. Report: production sources unreadable; no classification attempted. |
| Bug articulation failed | Cannot name a concrete failure mode after reading code | Keep the test. Report: candidate kept pending human review; failure mode unclear. |
| Static guarantee unclear | Mixed codebase, `any`/`unknown`/unchecked-parse leaks, or untyped mode | Keep the test. Report: language carve-out ambiguous; boundary shape may be a real-bug test. |
| Matched proof failed | Mutant caught, subsumption gap found, tautology claim false, or compiler claim false | Revert any mutation. Keep the test. Report: load-bearing; proof failed. |
| Suite regressed | Full suite fails after batch deletion | Revert the batch via VCS. Report: regression detected; batch rolled back. |
| Mutation left unreverted | Interruption left a production edit in the tree | Revert before any further edit. Report exactly which file was restored. |

Partial-result rule: successful batches stand. Rolled-back batches do not invalidate successful ones. Non-mutation rule: no production mutation persists beyond its proof step.

## Output

A deletion report listing deleted tests (file path, test name, proof class, evidence summary, batch commit hash), kept tests (file path, test name, reason kept), and final suite pass/fail status, ordering: deleted, kept, suite status.
