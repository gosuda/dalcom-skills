---
name: code-simplification
description: 'Use when the user names a module, file set, or dependency slice and wants it structurally smaller with its consumer contract preserved. Not for diff-only polish: use simplify. Not for architecture layout re-derivation: use architecture-simplification. Not for test-only purges: use tests-purge-unneeded. Not for cutting a consumer-facing surface without an explicit yes: use refactor-break-compat.'
---

# Code simplification (offensive structural default)

Standards: every remaining element earns its place. A module hides decisions behind its contract, migrating affected callers is part of the cut.

Aggressive by default. The scope is the complete authorized module or dependency surface: every module, file, and edge in scope is classified and challenged, not only lines recently touched. Shallow layers (forwarding tiers, single-use layers, pass-through modules, depth without a decision boundary) are challenged first and collapsed into their surviving owners; all in-scope callers are migrated in the same change. Real invariants (protocol, error, security, persistence, and compatibility contracts) are retained, and boundary cuts need an explicit recorded yes.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User names a code scope (file, module, directory, crate or package set, dependency slice) and asks for structural reduction: simplify, cut bloat, collapse special cases, remove indirection or dead state, reorganize a module. |
| Authority | Reversible local: writes only VCS-tracked paths inside the named scope plus proven internal callers, their test references, and their doc pointers when migration requires it; rollback is version control through atomic commits. Scope expansion beyond the named scope plus proven callers needs a new explicit scope. No remote mutation. |
| Side effect | Residue deleted, special cases collapsed into the general case, shallow layers collapsed into their surviving owners, single-use indirection inlined and deleted, all in-scope callers migrated in the same change, no shim, alias, tombstone, or deprecated path left behind. |
| Done | Scoped consumer contract holds, every divergence is classified essential or residue, residue resolves to nothing under search, all in-scope callers and pointers are migrated, the narrowest applicable verifier is green, and no shim, alias, tombstone, or deprecated path survives. Line delta is reported evidence only, never the predicate; no percentage or count target is accepted. |

Two modes share this contract. `module` takes one named scope and reduces its interior. `dependency` takes one named slice plus its dependency edges and reduces both the slice and the edges it forces. Both preserve the consumer contract and real invariants; both stop at the boundary gate.

## Inputs

- Target (required): the file, module, function, directory, or slice to simplify, named by the user. The working surface is the complete authorized surface, never a touched-lines subset. For `dependency` mode, the dependency edges in play (imports, re-exports, feature flags, build edges) as observed in the tree.
- Consumer contract and invariant sources (derived, not guessed): call-site usage, existing tests, public signatures, wire or on-disk shapes, configuration surfaces, plugin points, plus the real invariants the scope must preserve (protocol, error, security, persistence, and compatibility contracts).
- Verifier (derived): the compiler or typechecker first, then the repository's own test command.

## Procedure

1. **Bound the scope and state the consumer contract and invariants.** List the exact paths in scope plus the observable surfaces they expose, covering the complete authorized surface rather than recently touched lines. Derive the contract from call-site usage, existing tests, and public signatures, never from the target's internals. Name the real invariants that must survive (protocol, error, security, persistence, compatibility), and how each will be checked. For `dependency` mode also list every dependency edge entering or leaving the slice with its owning file and line. Done when: the path set, the edge set where applicable, the exposed surfaces, the contract, and the invariants with their checks are written down.

2. **Classify every divergence, challenging shallow layers first.** Walk the old shape function by function and branch by branch: essential (fold into the general case, one-line reason) or residue (cut, one-line reason). Challenge shallow layers first: forwarding tiers, single-use layers, pass-through modules, and depth without a decision boundary are residue unless a named invariant requires them, and collapse into their surviving owners. Further residue covers dead state, forwarding-only wrappers, single-use generics with one concrete use, factories with one real implementation, always-on or always-off flags whose losing branch is deletable, and redundant nesting with no behavioral cause. A swappable-implementation contract counts only when more than one real implementation ships today; single use or zero branching alone never proves a wrapper is unnecessary. A live invariant never counts as residue even when it looks like ceremony. Done when: nothing reachable in scope is unclassified, and every shallow layer has a keep-with-invariant-reason or a collapse target.

3. **Gate the boundary before cutting.** Interior (every caller in-tree, nothing persisted, shipped, configured in someone else's deployment, or promised against a version) is demolished without asking once the scope is named. Boundary (public API, wire or on-disk format, configuration running in someone else's deployment, plugin point, documented example consumers import, anything a version was promised against) needs a recorded yes before cutting; on silence or no, keep it permanently as contract and hand the compat cut to `refactor-break-compat` with file, line, contract evidence, and reason. Never cut a boundary surface on silence, and never cut a real invariant to make the structure smaller. Done when: every boundary surface has a yes or a no, every invariant has its check, and nothing protected is cut on silence.

4. **Cut and migrate in the same change.** Delete residue; collapse special cases into the general case; collapse condemned shallow layers into their surviving owners; inline single-use indirection at every call site, then delete the wrapper. Migrate all in-scope callers, test references, and doc pointers in the same change: imports, call sites, fixture wiring, renamed symbols, module doc pointers, navigation entries. Never leave a caller on a removed surface; never leave a shim, alias, tombstone, dual path, or deprecated wrapper. Done when: residue search returns nothing and no reference to a removed surface remains.

5. **Prove behavior and invariants.** Run the narrowest applicable verifier after each atomic commit (compiler or typechecker first, then the repository's own test command), plus every invariant check named in step 1. If the suite is red at baseline, stop before cutting and report the failing tests; never cut on unproven ground. If an edit regresses, revert that edit and record the failing check. Permitted test edits: mechanical migration to the new internal contract and assertion updates strictly where an approved contract change requires them, each with a recorded reason. Forbidden: deleting tests (route to `tests-purge-unneeded` with mutation proof), suppressing, skipping, or weakening assertions to force green, and adding parser exceptions or duplicate-resolution logic to fit the cut. Done when: the verifier and all invariant checks are green on the migrated tree with no forbidden edit.

6. **Ghost sweep.** Grep code, tests, docs, configs, error messages, and log lines for string references to every removed concept. Done when: zero survivors, or the candidate is reclassified not-dead with its reason.

## Owner limits (stop here, hand off with file, line, evidence, reason)

| Owner | When it owns the job, not this skill |
|---|---|
| This skill | One named scope, consumer contract and real invariants preserved. Aggressive reduction of the complete authorized surface with all in-scope caller migration in the same change. No blind re-derivation, no contract rewrite. |
| `breaking-driven` | The module is bloated enough to derive blind from call-site evidence and audit every old behavior as essential-or-residue. Replacement derived from the stated contract alone. Route when the divergence walk shows the old structure reproduces itself under fresh names. Human-explicit overhaul, rebuild, or rewrite-from-scratch intent is handled here through the same contract-first replacement with boundary approval, never self-initiated from this skill. |
| `guillotine` | Residue spans more than one artifact class (code plus docs, tests, config, workflows, or generated sources) with the observable boundary unchanged. Requires a candidate ledger plus bidirectional consumer proof. Route when the cut crosses artifact classes. |
| `architect` | Crate, module, or dependency-graph layout planning across scopes. This skill executes an approved slice at a time; `architect` owns the plan. |
| `deps-upgrade` | Drop or upgrade of a third-party dependency for semantic, version, or policy reasons. |
| `tests-purge-unneeded` | Any test deletion. Only owner with a mutation-proof contract. |
| `purge-slop-docs` | Doc-only purges, hierarchy reorders, whole-doc deletion (separate yes per file). |
| `refactor-break-compat` | Any consumer-facing surface cut. Explicit recorded yes only. |

This skill never renames itself into a rebuild to avoid a handoff.

## Failure and recovery

- Red baseline: stop before cutting; report the failing tests. Never cut on unproven ground.
- Regression after an edit: revert that edit immediately; record the edit and the failing check; continue with other candidates only while the baseline stays green.
- Already at floor: every module, file, and edge in the complete authorized surface is classified essential with invariant reasons, and no residue remains that preserves behavior and invariants; report the floor with the classified list and invariant checks. Do not force cosmetic or taste-only edits past clear and maintainable, and do not claim the floor from a touched-lines subset.
- Boundary cut attempted on silence: restore from version control; record the surface, the missing yes, and the handoff.
- Invariant violation: revert the edit that broke it; record the invariant and the failing check; continue only with invariant-preserving candidates.
- Ghost references remain: incomplete; remove the survivors or roll back the cut that left them.
- No verifier available: every fix is unverified, the limitation is stated, and the done predicate is not claimed.
- Partial result: keep applied changes that preserve behavior and invariants; report rejected changes with reasons; never claim done while behavior or invariants are unverified or callers dangle.

## Output

The simplified scope plus a report: mode (`module` or `dependency`), the stated consumer contract and invariants with their checks, the essential-or-residue classification with one-line reasons (shallow layers first), applied cuts with their atomic commits, all migrated in-scope callers and pointers, reverted edits with failing checks, boundary decisions (every yes or no with its evidence), ghost-sweep result, final verifier and invariant results, and the reported line delta. Terminal classification: simplified, already-at-floor, or blocked with the exact missing scope, yes, invariant check, or prerequisite.
