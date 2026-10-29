---
name: refactor-break-compat
description: 'Use when modernizing APIs, removing compat shims, killing feature flags, or rewriting a subsystem cleanly. Not for additive refactors that must preserve the old path.'
---

# Breaking refactors

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Modernizing APIs, removing compat shims, killing feature flags, rewriting a subsystem cleanly. |
| Authority | Human-gated: requires explicit human invocation, previewing target and consequence before any irreversible deletion; otherwise reversible local: writes only VCS-tracked refactor targets; rollback is version control. No remote mutation. |
| Side effect | Deletes compat/adapter/flag code and rewrites every caller in the manifest and affected tests; local-delete-unrecoverable. |
| Done | Zero-residue grep, all callers on new contract, tests green on new behavior (exit 0). |

## Refusals

- Additive refactors that keep the old path: rejected. This skill demolishes the old path. Use a regular refactor if the old path must survive.
- Shipping the intermediate state (half old, half new): rejected. Finish or revert to the version-control baseline.
- Widening scope beyond the demolition manifest: rejected. Do not widen scope to resolve a finding.

## Inputs

- Old API surface (required): the compat shims, legacy adapters, feature flags, version gates, and backward-compatible interfaces to demolish.
- New API surface (required): the target contract every caller must adopt.
- Scope (optional): file or module boundaries; when omitted, the blast-radius map determines scope.

## Procedure

0. Establish the consumer contract and the required behavior proof. Record the consumer contract the replacement must satisfy and the required behavior proof suited to the actual target; the blocked result names the missing proof. **Done when**: the consumer contract is recorded, and the required behavior proof exists or the block names the missing proof.
1. Map the blast radius. Enumerate every file, module, and caller of the old shape using `ast-grep` or `rg`. This is the demolition manifest. **Done when**: the demolition manifest is complete.
2. Preview and confirm the demolition. Present the demolition manifest and the consequences to the user: every file and caller that will be deleted or rewritten, which tests will change, and which flags or config will be removed. Wait for explicit human confirmation. Do not proceed without it. **Done when**: the user confirms the demolition.
3. Delete the old path as one atomic cutover with step 4. Before destroying anything, confirm no known behavior gap from steps 0-1; if a gap is known, stop before destruction and the blocked result names the consumer and the unreproduced behavior. Otherwise remove compat layers, adapters, legacy branches, and flags used only by the old path. Do not delete a flag that also controls the replacement or another live path. No commenting out. Delete. **Done when**: the old path is deleted from every file in the manifest.
4. Rewrite every caller to the new contract as the second half of the step 3-4 atomic cutover. Migrate all references from step 1. After each batch, run the strongest static enumerator the project has (compiler or typechecker, including opt-in: `mypy`, `pyright`, `tsc --checkJs`, Sorbet). Never sufficient alone: no static pass sees reflective, dynamically dispatched, string-constructed, or generated references, nor code excluded from the build. Enumerate those by hand and name them in the report. The demolition owner migrates every consumer in the same cutover; do not shift migration work to consumers and carry no compatibility path, alias, or shim. If a gap is discovered mid-cutover, finish within the approved scope or restore the whole affected cutover to the pre-change baseline; never leave a half-migrated cutover or report it as success. **Done when**: every caller in the manifest is on the new contract and the static enumerator passes.
5. Rewrite tests to the new truth. Update assertions to the new behavior. Delete tests whose entire purpose was the old behavior. Add tests for the new contract where coverage is now thin. **Done when**: tests assert the new behavior and the old-behavior tests are deleted.
6. Exterminate ghosts. Grep for string references, config keys, env vars, doc links, error messages, and import paths naming the old API. Zero survivors. **Done when**: the grep returns nothing.
7. Strip dead weight. Remove imports, packages, dependencies, types, and dead files that only the old path needed. **Done when**: no dead weight from the old path remains.
8. Verify zero residue. A search for every old symbol, flag, and format name returns nothing. If it returns anything, return to step 4. Where the actual target has metrics, logs, or dependency-analysis channels, corroborate zero active usage through those channels after the cutover; record the commit range that reverts the removal and, only where such channels exist, the post-removal watch set confirming no consumer regressed after removal. **Done when**: the zero-residue search returns nothing, and the report names the revert commit range plus, where applicable, the post-removal watch set.

## Failure and recovery

- Residue remains: old references survive in code, tests, docs, or config after step 8. Report the survivors and stop with exit 1 (residue). Do not widen scope beyond the demolition manifest.
- Build or tests broken: migration incomplete, callers or assertions not yet on the new shape. Fix forward only within the approved scope; otherwise restore the whole affected cutover to the pre-change baseline, report the exact blockers and stop.
- Migration stalled: codebase is half old, half new. Finish within the approved scope or restore the whole affected cutover to the pre-change baseline; never ship the intermediate state.

Partial results are never reported as success. If any failure class triggers, the done predicate does not hold.

## Output
A migration report with blast-radius manifest, deleted artifacts list, caller-migration checklist (naming any pre-destruction blocked consumer and its unreproduced behavior), test-rewrite summary, zero-residue verification result with revert commit range and, where the actual target exposes those channels, post-removal metric/log watch set (otherwise channels reported as not applicable), and final exit code (0 = clean demolition, 1 = residue, 2 = broken build, 3 = stalled migration), ordered as listed.
