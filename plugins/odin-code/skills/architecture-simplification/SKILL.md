---
name: architecture-simplification
description: 'Use when the user explicitly asks to simplify an architecture, collapse modules or crates, or cut a dependency graph within approved boundaries. Not for single-module cleanup: use code-simplification. Not for full rebuild with contract changes: use offense. Not for blind re-derivation: use breaking-driven.'
disable-model-invocation: true
---

# Architecture simplification (very-offensive layout reduction)

Anchors: Dieter Rams (every remaining module and edge earns its place), David Parnas (each surviving module hides exactly one family of decisions behind a contract its callers can rely on).

Human invocation only: the model never auto-fires this skill. An explicit human request or an explicit `architecture-simplify` ask is required every time.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Human explicitly asks for architecture simplification: collapse crates, layers, or modules; re-derive a subsystem layout; cut a dependency graph; remove architectural edges or tiers. Human-invoked or an explicit `architecture-simplify` ask only; never self-initiated from a smaller cleanup. |
| Authority | Reversible local over the human-scoped path set only: re-derive layout, move or merge modules, collapse edges, migrate every affected caller, test reference, and doc pointer in atomic commits; rollback is version control. No remote mutation. Any path outside the approved set needs a new explicit scope; any product-boundary or consumer-contract change needs a recorded yes. |
| Side effect | Layout re-derived with fewer modules, crates, or edges; every affected caller migrated; no shim, alias, tombstone, re-export stub, or deprecated path left behind. |
| Done | Every in-scope module and edge classified, interior layout re-derived and migrated, boundary decisions recorded, residue search empty, the narrowest verifier plus the applicable end-to-end check green, and no shim, alias, tombstone, or deprecated path surviving. Crate, module, and edge deltas are reported evidence only, never targets. |

## Inputs

- Scope (required): the explicit human-approved path set (subsystem, crate set, layer set) plus the dependency edges under review, observed in the tree with owning files and lines.
- Contracts (derived): the consumer-visible surfaces of the subsystem (public APIs, re-exports, wire or on-disk shapes, configuration keys, plugin points, documented examples) and the end-to-end behavior the layout must preserve.
- Plan anchor (derived): the approved layout direction, whether from the user directly or from `architect`; this skill executes the cut, it does not substitute its own plan for an approved one.

## Procedure

1. **Record scope, contracts, and the dependency graph.** List every in-scope path, every exposed surface, and every dependency edge entering, leaving, or crossing the scope with its owner and line. Derive the preserved contracts from call sites, tests, signatures, wire shapes, and configuration consumers, never from the layout's own aspirations. Done when: the path set, surface list, edge table, and preserved contracts are written and the approval covering them is recorded.

2. **Classify every module and edge.** For each module: essential owner (hides one decision family, keep or merge as the surviving owner, one-line reason) or residue (forwarding tier, single-use layer, duplicated owner, dead branch of the graph, cut with reason). For each edge: load-bearing (real consumer need with evidence) or removable (forwarding, speculative, or superseded). Competing canonical owners are not unified here on judgment alone: the surviving owner needs consumer-need evidence and the losing import path migrates fully. Done when: no in-scope module or edge is unclassified.

3. **Gate the boundary.** Interior layout (every caller in-tree, nothing persisted, shipped, externally configured, or version-promised) is re-derived without further asking. Boundary surfaces (public API, crate-root re-export an external example or downstream crate imports, wire or on-disk format, live configuration, plugin point, version promise) need a recorded yes before removal or relocation; on silence or no, keep the surface permanently as contract and hand the compat cut to `refactor-break-compat` or `deprecate-and-migrate` with file, line, evidence, and reason. Done when: every boundary surface carries a yes or a no; nothing structural crosses on silence.

4. **Re-derive and migrate in the same series.** Collapse the condemned modules and edges into their surviving owners; move code to its justified owner; update every affected internal caller, test reference, example, and doc pointer in the same commit series, one slice per atomic commit. Never leave a caller on a removed module or edge; never leave a shim, alias, tombstone, re-export stub, dual path, or deprecated wrapper as a convenience. Config-selected, environment-selected, and build-variant-selected references are enumerated by exact token search, not assumed absent. Done when: the new layout is in place, every affected reference resolves to a surviving owner, and exact-token search for every removed module, edge, and re-export returns nothing.

5. **Prove the new layout.** After each atomic commit run the narrowest verifier (compiler or typechecker, then the repository's own test command); finish with the applicable end-to-end check for the subsystem. A red baseline stops all cutting and is reported first. A regression reverts that slice with its failing check recorded. Permitted test edits are mechanical migration to the new layout (imports, paths, fixture wiring, renamed symbols) plus assertion updates strictly required by an approved contract change, each with a recorded reason. Forbidden: deleting, suppressing, skipping, or weakening tests to force green. Test shrinkage belongs to `tests-purge-unneeded` under mutation proof; doc-only purges belong to `purge-slop-docs`. Done when: verifier and end-to-end are green on the migrated tree with no forbidden edit.

6. **Ghost sweep across surfaces.** Grep code, tests, docs, configs, registries and overrides, error messages, log lines, and navigation for every removed module, edge, configuration key, and re-export. Done when: zero survivors, or the hit is reclassified not-dead with its consumer evidence.

## Owner limits (stop here, hand off with file, line, evidence, reason)

| Owner | When it owns the job, not this skill |
|---|---|
| This skill | Fewer modules, crates, or edges with the product boundary preserved; interior re-derivation plus full caller migration; boundary cuts only on recorded yes. |
| `architect` | Layout planning itself. This skill executes an approved direction slice by slice; it does not plan the target layout from nothing. |
| `code-simplification` | One named module or dependency slice whose interior shrinks without re-deriving the surrounding layout. Route single-scope work down, not up. |
| `breaking-driven` | Blind re-derivation from call-site evidence alone. This skill reuses the interior-versus-boundary gate without copying that method. |
| `offense` | Explicit human overhaul or rebuild where product contracts themselves may change with approval. Never self-escalate here to rewrite contracts. |
| `guillotine` | Multi-artifact-class residue requiring a candidate ledger and bidirectional consumer proof. Route when the cut's residue spans code plus docs, tests, config, workflows, or generated sources under one unchanged boundary. |
| `refactor-break-compat` / `deprecate-and-migrate` | Any consumer-facing removal or relocation. Recorded yes only; silence keeps the surface. |

## Failure and recovery

- Missing or vague scope: stop and ask for the exact path set. Do not infer the subsystem from a symptom.
- Red baseline: stop before cutting; report the failing tests and the end-to-end state. Never cut on unproven ground.
- Regression in a slice: revert that slice; record the failing check; keep prior green slices.
- Boundary cut on silence: restore from version control; record the surface, the missing yes, and the handoff.
- Hidden consumer found (config, environment, build variant, downstream example): stop cutting that surface; enumerate the exact tokens; migrate or record no before proceeding.
- Ghost references remain: incomplete; remove survivors or roll back the slice that left them.
- No verifier or no end-to-end available: state exactly which claims are unproved; do not claim done.
- Partial result: keep green slices; report rejected slices with reasons; never claim the layout done while callers dangle or residue resolves.

## Output

The re-derived layout plus a report: approved scope and plan anchor, module and edge classifications with reasons, applied slices with atomic commits and migrated callers, boundary decisions with yes or no evidence, ghost-sweep result, verifier and end-to-end results, and reported structural deltas. Terminal classification: simplified, already-at-floor, or blocked with the exact missing scope, yes, prerequisite, or hidden consumer.
