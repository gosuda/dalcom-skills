---
name: architect
description: 'Use when non-trivial code needs a design, codebase architecture needs improving through survey and deepening, or one module needs targeted interface narrowing, seams, or testability. Not for rendered visual artifacts, deploy, or irreversible changes.'
---

# Architect

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Design non-trivial code before implementation (greenfield); survey an existing codebase for shallow modules and deepen the selected candidate (brownfield); locate a seam, harden with guardrails, or make code testable; design one named module interface, seams, and testability (targeted-module) |
| Authority | Reversible local: writes only named local design artifacts and, when the request permits, the selected design in the working tree; rollback is deleting or reverting those writes. No VCS-history rewrite, credential, paid, published, deployed, or remote mutation |
| Side effect | A local design package; in implement mode the accepted refactor, its tests, glossary entries for established domain terms recorded locally, and an optional local ADR the user accepts |
| Done | An explicit design choice with tradeoffs and a coherent implementation plan is recorded. In brownfield implement mode: one chosen deepening candidate is resolved, its shallow path is replaced rather than layered, tests exercise the resulting interface, obsolete shallow tests and code are removed, and established terms and accepted decisions are recorded locally |

## Inputs

- `mode`: `greenfield`, `brownfield`, or `targeted-module`. Infer from the request; confirm when ambiguous.
- Greenfield: the code unit to design, its callers, inputs, and failure paths.
- Brownfield: an optional named direction such as a module, subsystem, pain point, or candidate seam. When absent, recent-change hotspots select the scan scope.
- Targeted-module: exactly one named function, class, package, crate, or tier-spanning slice with readable source and enough callers and tests to judge its interface and depth. Optional: intended adapters, candidate seam locations, target language.
- Optional: an existing design constraint or accepted ADR boundary.

## Vocabulary

Use these terms consistently and do not substitute near-synonyms: no unit, component, or service for module; no API or signature for interface, which name only the type-level surface; no boundary for seam, which is overloaded with bounded context. Say adapter when the seam is the topic and implementation otherwise; a small adapter can hold a large implementation and a large adapter a small one.

- Module: anything with an interface and an implementation, at any scale.
- Interface: every fact a caller must know: types, invariants, ordering, errors, configuration, performance plan.
- Implementation: what the interface hides.
- Depth: behavior hidden per unit of interface learned. A deep module gives high leverage through a small interface.
- Seam: a place where behavior can be substituted or tested in isolation without editing that behavior in place.
- Adapter: a concrete implementation used at a seam.
- Leverage: capability gained per unit of interface learned.
- Locality: concentrating a change, bug, or required knowledge at one maintenance site.

## Greenfield mode

1. Bound scope. Name the code unit, callers, inputs, failure paths, and trust boundary. When the request is trivial or already fully specified, report `no-design-needed`. Done when: the unit and its boundary are stated or the stop is taken.
2. Sketch the usage surface first. Record the public call plan, types, call sites, data shapes, invariants, and observable errors before discussing implementation. Done when: the usage surface is recorded.
3. Produce at least two competing sketches that each satisfy the usage surface and differ in structure or tradeoff. Done when: each sketch is coherent enough to evaluate.
4. Evaluate every sketch against red flags: hidden complexity, leaky interface, unbounded scope, speculative generality, missing error handling, edge handling, seam placement, testability. Done when: each sketch has a red-flag record.
5. Redesign when necessary. When every sketch has a blocking flaw, return to the usage surface and produce a new sketch. Stop once one coherent sketch has no blocking flaw. Done when: at least one coherent unblocked sketch exists.
6. Choose one sketch. State the choice, tradeoffs, and rejected alternatives. Done when: the choice and rejections are recorded.
7. Derive the implementation plan: modules, interfaces, control flow, failure paths, migration steps, proof requirements. Done when: the plan is recorded.
8. Implement only when the request and authority permit; otherwise stop at the design package. Done when: implementation is complete or the package is delivered.

## Brownfield mode

### Survey (read-only)

1. Scope before scanning. When the user names a direction, scan that scope first. When no direction is named, read recent commit history to find active paths and hotspots and let those paths pull attention first. When changes are scattered with no defensible hotspot, widen the scan and record why. Read the applicable glossary and nearby ADRs before judging module names or responsibilities. Record the chosen scan scope and the evidence that selected it. Done when: scope and its evidence are recorded.
2. Enumerate module surfaces. Within the scope, identify every public module, entry point, package, namespace, or exported surface consumed by another module. Record surface size, internal abstraction, coupling, and responsibility width per surface. See `references/survey-ranking.md`. Done when: every public surface in scope is listed.
3. Assess depth by leverage, not by line ratios. A shallow module exposes a broad surface with little hidden behavior; a deep module hides substantial behavior behind a small interface. Done when: each surface has a depth judgement with leverage evidence.
4. Run the deletion test. For every suspected shallow module, ask whether deleting it would make complexity vanish or spread it across callers. A pass-through verdict is valid and must name the callers that would absorb the complexity. Done when: each suspect has a deletion-test result.
5. Rank candidates by architectural gain and refactoring effort: higher hidden behavior and stronger locality gain rank higher; fewer affected callers and lower migration effort rank higher; a hard invariant or cascade that blocks deepening lowers the recommendation. Done when: a ranked candidate list exists.
6. Return one portable candidate report per candidate using `references/survey-ranking.md`: files and modules, concrete problem, deletion-test result, dependency category, plain-language solution without a premature interface, expected locality, leverage, and testability change, smallest before-and-after visual, recommendation strength (`Strong`, `Worth exploring`, or `Speculative`), and any ADR conflict worth reopening. Return text or Markdown. Do not write a temp HTML file, load a CDN, open a browser, or propose a concrete interface before a candidate is selected. Done when: the report is delivered without mutation.
7. Select the leading candidate with the evidence behind the ranking. When no candidate is defensible, return `no-candidate`. Done when: one candidate is chosen or the stop is reported.

### Deepen (implement)

1. Explore the selected scope read-only. Read the selected files, callers, tests, applicable glossary, and ADRs. Confirm dependencies before proposing a change. Done when: files, coupling, and dependencies are understood.
2. Classify the dependency treatment per `references/deepening.md`: `in-process`, `local-substitutable`, `remote-but-owned`, or `true-external`. When classification is impossible, treat the dependency as `true-external` and require an injected port. Done when: the treatment is named.
3. Apply seam discipline. One adapter is a hypothetical seam; two justified adapters, typically production plus test, make a real one. Do not create an interface for a hypothetical variation. Done when: each seam is justified by variation across it.
4. Present the candidate before mutation: files, problem, deletion-test result, plain-language solution, expected gain, dependency treatment, and bounded changed-file set. Ask the user to select it before editing. Done when: the user selects one candidate.
5. Grill the selected candidate to resolution. Resolve one dependent design decision at a time and recommend one answer per decision. Bound the changed-file set before mutation. Record an established domain term in the local glossary instead of leaving it undefined. Offer an ADR only when the rejection reason is load-bearing for a future explorer, framed as recording it so the same candidate is not re-suggested; skip ephemeral or self-evident reasons. Done when: every design decision is resolved or the blocking decision is named.
6. Design alternatives only when requested, using `references/interface-design.md`: frame constraints and dependency categories, produce at least two radically different interfaces, compare depth, locality, and seam placement, and recommend one, including a hybrid when elements combine well. Done when: designs are compared and one is recommended.
7. Replace rather than layer as the default. State the new interface contract first, then absorb in-scope special cases into it; migrate every scoped caller, delete the replaced shallow path and its obsolete mechanisms, and delete shallow-module tests after equivalent interface tests exist. Preserve essential behavior, validation, and proof on the new contract. Do not keep the old path as a compatibility alias unless the user explicitly includes it in scope. Stop for approval before any live-consumer break, data loss, or non-reversible act. Done when: the shallow path is replaced, not layered.
8. Exercise the changed behavior through the same interface callers use. Confirm invariants, error modes, relevant adapters, and the final changed-file set against the bound scope. Done when: interface-level checks pass and the changed set matches the bound scope.

### Locate seam, testability, guardrails (read-only or implement)

1. Locate the seam: identify points where a caller can substitute an alternate implementation or inject a test double. When none exists, propose the smallest interface introduction that creates one without widening the public surface. Done when: each seam is named or the smallest creating interface is proposed.
2. Make code testable: identify the concrete dependencies that block isolated testing, then propose seams that make those dependencies substitutable. Prefer accepting dependencies over constructing them internally, returning results over mutating hidden state, and keeping the surface small. Done when: each blocking dependency has a proposed seam.
3. Harden with guardrails: recommend only tooling tied to a protected invariant, such as type constraints, boundary checks, lint rules, analysis, or interface-level tests. Name the invariant each guardrail protects. Done when: each guardrail is tied to its invariant.
4. Stop at recommendations when implementation authority is absent. Mark any recommendation not grounded in read code as inference. Done when: recommendations are delivered or implementation is complete.

### Targeted module (read-only or implement)

1. Bound one module. Name exactly one target, confirm its source is readable, and read its interface surface, implementation, and crossing callers and tests. When depth cannot be judged inside this scope, stop and name the missing evidence. Done when: one module is named and surveyed.
2. Classify depth by leverage, not line ratio. Internal parts, including internal seams used only by the own tests, are not interface; one module has exactly one interface. Done when: a deep or shallow verdict is stated with leverage evidence.
3. Run the deletion test and name the callers that would absorb the complexity when the verdict is pass-through. Done when: the verdict is recorded.
4. Narrow the interface in order: reduce methods, simplify parameters, hide more complexity inside. Prefer the form that gives callers leverage and maintainers locality. Done when: the interface is at its narrowest form that preserves caller-visible behavior.
5. Place seams by variation. The external seam carries the interface; internal seams stay private to the implementation and its tests. Done when: every seam sits where something varies across it.
5a. **Seal versus deliberately expose.** State the intent explicitly: seal (make the dependency explicit and controlled behind the seam) or deliberately expose (name it as a configuration key, module seam, or override hook). Choose by caller knowledge, locality, variation, and deletion-test evidence — not by a line/branch ratio. Migrate every in-scope caller to the chosen seam, record exact pre-change text for rollback, and re-verify callers and tests still cross the same seam.
6. Check the test surface. Callers and tests cross the same seam; a test that must reach past the interface means the module is the wrong shape. Done when: callers and tests cross the same interface without reaching past it.
7. Reject the framings wherever they appear: depth as a line-count ratio, which rewards padding the implementation; and interface as a language keyword or public method list, which omits invariants, ordering, errors, configuration, and performance facts. Done when: both framings are checked and absent from the analysis.
8. Anchor terms in the target language per `references/language-anchors.md`; infer the language from the source when not stated. Done when: vocabulary is anchored in the target constructs.
9. Deliver, then edit. Emit the recommendation in the fixed vocabulary; when restructuring is in scope, keep edits inside the bounded module while every caller and test keeps crossing the same seam. Done when: the recommendation is delivered and any local edits stay bounded.

## Failure and recovery

- `no-design-needed`: the request is trivial or fully specified; mutate nothing.
- `no-candidate`: the survey finds no defensible deepening candidate; make no changes.
- `blocked`: code, callers, tests, glossary, ADR, or required behavioral evidence cannot be read; report what is missing and stop.
- `blocked-by-decision`: an ADR, user decision, or scope boundary conflicts with the candidate and no reopening reason is accepted; preserve the ADR and stop.
- `scope-drift`: the request widens beyond the named module, candidate, or changed-file set; stop and report the widening; mutate nothing outside the named artifacts.
- `ambiguous-mode`: the request does not distinguish greenfield, brownfield, or targeted-module; ask which branch applies before proceeding.
- `unbounded-target`: targeted-module mode cannot isolate one module or needs evidence outside the scope; stop before any edit and name the missing evidence.
- `pass-through`: the deletion test shows the module hides no useful complexity; report it as shallow with absorbing callers; do not silently rewrite it.
- `non-converged-interface`: the interface cannot narrow without changing caller-visible behavior beyond the bound; report the conflict and stop.
- `failed-edit`: restore every modified named file to its captured pre-edit contents and report the failure; when exact restoration cannot be proved, stop with `recovery-required` and list each affected file with its pre-change source.
- `missing-proof`: the design cannot name interface-level checks for its invariants, errors, or relevant adapters; stop before claiming done.
- `missing-dependency-treatment`: an external dependency cannot be classified; treat it as `true-external` and require an injected port.
- `incomplete-survey`: the scan scope or recent-change evidence is insufficient; report the missing evidence rather than a whole-codebase conclusion.
- `partial-result`: return the completed survey or analysis, list unresolved decisions, and do not claim implementation or proof is complete.

## Output

A design package containing the bounded scope; the usage surface or brownfield candidate report with the smallest visual; competing sketches or the targeted-module recommendation; depth, deletion-test, seam, adapter, dependency, and testability findings; the chosen design and rejected alternatives; implementation sequence, failure paths, migration, and proof requirements; changed-file bounds and rollback; and a terminal classification: `done`, `no-design-needed`, `no-candidate`, `blocked`, `blocked-by-decision`, `failed-edit`, `non-converged-interface`, or `partial-result`.
