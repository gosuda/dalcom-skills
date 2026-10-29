---
name: project-findings-onto-graph
description: 'Use when graph-backed security analysis is needed: project SARIF or reviewer findings onto a program graph; build or query a multi-language graph; summarize Trailmark structure; map smart-contract entry points; compare two refs or snapshots; or hunt confirmed vulnerability variants with pattern or graph seeding. Select findings, build-program-graph, trailmark-structural, entry-point-analyzer, graph-evolution, or variant-hunt mode and supply its required inputs. Not for initial vulnerability discovery: use security-review. Not for verifying one named allegation: use security-finding-verification. Not for security-finding triage: use triage-security-finding. Not for unrelated remote, credential, publish, deploy, or irreversible work.'
---

# Project findings and graph-backed security analysis

Graph-backed analysis gives external findings, source structure, entry points, structural changes, and confirmed root causes a common evidence surface. The default `findings` mode projects SARIF or other supported exports onto an existing graph. The other modes build or query that graph, summarize a Trailmark snapshot, analyze smart-contract entry points, compare two snapshots, or hunt variants of a confirmed root cause. Imported severity remains authoritative, and graph reachability never proves data flow.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A graph-backed security analysis is needed: findings must be projected onto a graph, a multi-language graph must be built or queried, Trailmark structure must be summarized, smart-contract entry points must be mapped, two refs or snapshots must be compared, or variants of a confirmed root cause must be hunted. |
| Authority | Reversible local. Reads the supplied source, graph, refs, snapshots, and finding exports. Depending on mode, writes graph exports, annotations, declared links, structural or variant reports, or temporary snapshot worktrees; `entry-point-analyzer` is read-only and emits only chat output. Temporary worktrees are removed before completion; no remote mutation occurs. |
| Side effect | `findings` writes graph annotations, severity or source subgraphs, and optionally an augmented export; `build-program-graph` writes graph exports, preanalysis annotations, and optional links; `trailmark-structural` emits its summary or full payload; `entry-point-analyzer` emits a structured markdown report as chat output only and writes no file; `graph-evolution` and `variant-hunt` emit their named local reports. Roll back by deleting named artifacts, removing annotations by source tag, and removing any temporary snapshot worktrees. |
| Done | The selected mode's inputs are validated and its evidence is complete: findings are matched or explicitly unmatched with graph context and source severity preserved; `build-program-graph` has parser coverage, preanalysis, bounded queries, and limitations; `trailmark-structural` has its requested summary or full payload; `entry-point-analyzer` accounts for every file and classification; `graph-evolution` classifies every graph change; or `variant-hunt` triages every bounded candidate. |

## Inputs

- `mode` (optional, default `findings`): one of `findings`, `build-program-graph`, `trailmark-structural`, `entry-point-analyzer`, `graph-evolution`, or `variant-hunt`.
- `findings` mode: a program graph already built for the target repository and at least one graph-importable finding export. SARIF 2.1.0 is the standard format; reviewer annotations and other tool exports count when an importer or file-and-line anchors are documented. Optional preanalysis evidence and additional source exports may be supplied.
- `build-program-graph` mode: a target source directory, an optional explicit language list, an existing declared-links file for cross-boundary edges, and an optional external binary-analysis graph export when supported. The installed graph analyzer is required.
- `trailmark-structural` mode: a target directory and `summary` or `full` mode (default `full`). Trailmark must already be available; summary mode returns languages, entrypoints, and dependencies, while full mode returns the version-gated structural payload.
- `entry-point-analyzer` mode: a smart-contract codebase, an optional directory filter, and an optional project name. Supported inputs are Solidity, Vyper, Solana/Rust, Move Sui, Move Aptos, TON, and CosmWasm. The human-invoked `entry-points` command may supply the directory path.
- `graph-evolution` mode: `before_ref` and `after_ref`, each a git ref or an existing directory path; an optional language (`auto`, one language, or a comma-separated list); and installed Trailmark. Refs create temporary worktrees, while directory inputs are used directly.
- `variant-hunt` mode: a confirmed root-cause statement, the original bug location or vulnerable snippet, and the reachable project codebase. Optional inputs select ripgrep, Semgrep, or CodeQL; `pattern-search` or `graph-seeding`; a graph seed node; ranking weights; and an exclusion scope.

## Refusals

- In `findings` mode, will not build a missing graph as part of augmentation; switch to `build-program-graph` mode first.
- Will not install or upgrade the graph analyzer, or install Trailmark into the project; only `trailmark-structural` may use an ephemeral `uv run --with trailmark` probe, and that probe must not modify the project.
- Will not present call-graph reachability or taint-subgraph membership as attacker-controlled data-flow or vulnerability proof.
- Will not promote imported findings beyond their source severity or status.
- Will not widen a matching heuristic to force unmatched findings or variant candidates into the graph.
- Will not classify uncertain smart-contract access as confident; ambiguous restrictions remain `Restricted (Review Required)`.
- Will not generate an evolution report from one healthy snapshot, a malformed ref, or a language-mismatched empty graph.
- Will not perform file, VCS, credential, paid, published, deployed, or remote mutation in `entry-point-analyzer` mode.

## Procedure

1. **Select and validate the mode.** Use `findings` when no mode is named. Validate every required path, ref, export, root-cause statement, or graph seed at its trust boundary before running a mode. Reject an unknown mode or a missing required input with its exact name; never widen scope by guessing. **Done when:** one named mode has a validated input set.

2. **Mode `findings`: project exports onto an existing graph.**
   1. Verify the graph exists by loading it with the graph tool's API. If loading fails, return `blocked: no-graph` and direct the invoker to `build-program-graph` mode; do not build it in this mode. **Done when:** the graph is confirmed.
   2. Reuse preanalysis if present; otherwise run blast-radius, entry-point, privilege-boundary, and taint passes on the loaded graph. If preanalysis cannot be made available, continue only with that absence recorded and omit cross-reference claims. **Done when:** preanalysis evidence is available or its absence is explicit.
   3. Locate every supplied finding export and record its path and format. **Done when:** every input is recorded.
   4. Probe optional importers on the loaded graph object before using them. Skip an input that requires an unavailable importer and name the requirement; never invent a CLI flag or API. **Done when:** every importer is gated.
   5. Project each input with its native importer. If no importer exists, resolve each file-and-line finding to the graph node whose span contains the normalized location and record that the match was manual. Record matched findings, unmatched findings, and created subgraphs per source. **Done when:** every input has a projection result.
   6. Report matched and unmatched counts per source. Investigate path alignment or scope when unmatched counts are high, but do not widen the heuristic. Enumerate annotated nodes and subgraphs; SARIF severity subgraphs use `sarif:error`, `sarif:warning`, and `sarif:note`, while source subgraphs retain tags such as `sarif:<tool>`, `weaudit:<author>`, or `binary:<artifact>`. **Done when:** counts, nodes, and subgraphs are listed.
   7. Overlap severity subgraphs with `tainted`, `high_blast_radius`, and `privilege_boundary` sets. Attach the result as prioritization context without reclassifying the imported finding. **Done when:** graph context is recorded and source severity is unchanged.
   8. Emit an augmentation report ordered by source path and format, matched and unmatched counts, subgraphs, cross-reference highlights, skipped inputs, and reasons. **Done when:** the augmentation report is complete.

3. **Mode `build-program-graph`: build and query a full multi-language program graph.**
   1. Verify the installed graph analyzer is on PATH and importable from scripts. Record its version; if unavailable, report the installation gap and stop without installing or manually replacing the analysis. **Done when:** tool availability or the gap is recorded.
   2. Ask the installed build which languages it supports and detect which languages exist under the target. Treat documentation as non-authoritative; use the installed build's answers. Stop if nothing is parseable. **Done when:** supported and detected languages are recorded.
   3. Build the full graph for the selected languages, using auto-detection unless the invoker supplied an explicit list. Never sample the tree. When supplied and supported, incorporate an external binary-analysis graph export as an augmentation and record its provenance; otherwise report that augmentation is unavailable. **Done when:** the full graph is built and any binary augmentation is incorporated or its limitation is recorded.
   4. Run all preanalysis passes before dependent queries: blast-radius estimation with downstream and upstream annotations and `high_blast_radius`; entry-point enumeration with `entrypoints`, `entrypoint_reachable`, `untrusted_external`, `semi_trusted_external`, and `trusted_internal`; privilege-boundary detection with `privilege_boundary`; and taint propagation from untrusted and semi-trusted entry points into `tainted`, with trusted entry points generating none. **Done when:** all four passes complete.
   5. Execute requested queries with the version-safe vocabulary: direct callers and callees; paths between functions or from entry points to targets; transitive ancestor and descendant slices; `complexity_hotspots(threshold=N)`; `attack_surface()` (passing through newer `attributes` objects unchanged); summary and JSON export; named subgraphs; and structured annotations (`ASSUMPTION`, `PRECONDITION`, `POSTCONDITION`, `INVARIANT`) with a source convention of `llm`, `docstring`, `manual`, or `preanalysis`. **Done when:** every requested query returns evidence or a named version limitation.
   6. Probe method or attribute presence before every version-specific feature. On older builds, use the documented baseline or compute from the export, such as selecting edges whose endpoints are both in a named subgraph. **Done when:** every versioned feature is safely used or reported unavailable.
   7. Declare parser-invisible FFI, RPC, IPC, or contract edges in the analysis-root links file when needed. Use TOML `[[link]]` blocks with `source`, `target`, `kind`, `confidence`, and optional `description` or `target_external = true`; reject ambiguous endpoints, unknown internal endpoints, invalid enums, and malformed TOML. Record `configured_by` on declared edges and treat `proxy.external:<symbol>` nodes as system boundaries, not source functions. **Done when:** each required boundary link validates or no declaration is needed.
   8. Record the model emitted by the installed build: node kinds such as `function`, `method`, `class`, `module`, `struct`, `interface`, `trait`, `enum`, `namespace`, `contract`, `library`, `template`, and newer `proxy`, `schema`, `table`, `view`, or `procedure`; origins such as `source`, `proxy`, `binary`, or `synthetic`; edge kinds and confidence; and per-unit parameters, return and exception types, cyclomatic complexity, and branch metadata. **Done when:** metadata describes the installed build rather than documentation.
   9. Bound every security claim. Paths are call-graph reachability; `tainted` is reachability from an untrusted entry point, not interprocedural data flow. Verify data flow by hand, account for `uncertain` dynamic-dispatch edges, and do not treat proxy or binary nodes as source functions. **Done when:** claims use only the strength of their evidence.
   10. Write the requested JSON export containing summary, nodes, edges, and subgraphs, and record emitted proxy nodes, external endpoints, and origins. **Done when:** the export exists, or no export was requested.

4. **Mode `trailmark-structural`: summarize one target with Trailmark.**
   1. Confirm the supplied target exists and is a readable directory. **Done when:** the target boundary is validated.
   2. Check the `trailmark` command or Python module, with `uv run trailmark analyze --help` as an acceptable probe fallback. Record a version when available. An ephemeral `uv run --with trailmark` retry is allowed only to test the import and must not install into the project. If all checks fail, report `trailmark is not installed` and return. **Done when:** availability or the installation gap is recorded.
   3. Detect languages through `trailmark.parse.detect_languages`, falling back to `trailmark.query.api.detect_languages` for pre-0.3 builds. If the result is empty, report `Trailmark found no supported languages under target` and return. **Done when:** supported languages or the language gap is recorded.
   4. For `summary`, run only `trailmark analyze --language auto --summary <target>` (or its `uv run` fallback), and verify the detected languages, `Entrypoints:`, and `Dependencies:` are present. For `full`, construct `QueryEngine.from_directory(target, language="auto")`, run `preanalysis()`, and assemble version-gated `languages`, `summary`, `preanalysis`, `attack_surface`, `hotspots`, `proxy_nodes`, and every named subgraph with counts and sample IDs. Probe `subgraph_edges`, `type_references`, and other newer methods with `hasattr()`; preserve `attack_surface` attributes and explicit empty sections. **Done when:** the selected payload is assembled without a widened analysis.
   5. Verify and return the complete summary or full payload, including the version when captured, or the exact missing-field/import gap. **Done when:** every field required by the selected mode is present or its gap is named.

5. **Mode `entry-point-analyzer`: analyze state-changing smart-contract entry points.**

   1. Resolve the codebase or `entry-points` command directory to an absolute
      readable path. Detect languages from extensions and manifests:

      - Solidity;
      - Vyper;
      - Solana/Rust with `solana-program` or an equivalent program entrypoint;
      - Move Sui with `Move.toml` Sui/edition metadata;
      - Move Aptos with `Move.toml` Aptos metadata;
      - TON (`.fc`, `.func`, `.tact`);
      - CosmWasm with `cosmwasm-std`.

      If none is supported, report the unsupported codebase and stop.

      **Done when:** languages and scope are confirmed.

   2. Apply the optional directory filter and locate every contract or module
      file in scope. Do not sample the tree. Record generated, inherited,
      vendored, and unreadable paths separately.

      **Done when:** every in-scope file is located or explicitly recorded as
      unreadable.

   3. Use source inspection as the authoritative foundation. A locally available
      Solidity analyzer may be read as supplementary evidence, but it is never
      required, never installed, and never authoritative for access
      classification. If an analyzer is absent or fails, continue with manual
      source analysis and record the fallback. Do not invent a replacement
      command.

      **Done when:** the foundation method and any analyzer limitation are
      recorded.

   4. Retain every externally callable, state-changing function and exclude only
      forms that are read-only or not externally reachable in the target
      language:

      - Solidity: exclude `view` and `pure`; include state-changing `external`
        and `public` functions, `receive`, `fallback`, and state-changing
        callbacks.
      - Vyper: exclude `@view` and `@pure`; include state-changing `@external`
        functions and the state-changing default handler.
      - Solana/Rust: include the native program entrypoint, instruction
        handlers, and Anchor program functions that can mutate accounts; exclude
        helpers and handlers whose accounts are not mutable.
      - Move/Aptos: include `public entry fun`, `entry fun`, and `public fun`
        when the body changes state or accesses mutable resources. Exclude
        private, `public(package)`, and `public(friend)` functions as
        independent transaction entry points.
      - Move/Sui: include `public entry fun`, `entry fun`, and transaction-
        reachable `public fun` when they mutate an owned or shared object.
        Exclude private `fun` and `public(package) fun`.
      - TON: include state-changing `recv_internal`, `recv_external`, tick-tock
        handlers, Tact `receive`, `external`, and `bounced` handlers; exclude
        getters and read-only receivers.
      - CosmWasm: include `instantiate`, `execute`, `migrate`, `reply`, `sudo`,
        IBC, and other state-changing callback entry points; exclude `query`.

      Do not decide whether a Move function is an entry point from the presence
      or absence of `entry` alone. Determine state effects and transaction
      reachability according to the target Move dialect.

      **Done when:** state-changing scope is complete for each detected
      language, and every excluded form has a recorded reason.

   5. Classify each retained function as exactly one of:

      - `Public (Unrestricted)`;
      - `Role-Restricted`;
      - `Restricted (Review Required)`;
      - `Contract-Only (Internal Integration Point)`.

      Trace actual restrictions, including owner/admin/governance/guardian/
      operator/minter/pauser/keeper/relayer checks, role predicates,
      capability objects, ownership constraints, signer checks, sender equality,
      and inherited modifiers or decorators.

      Read every modifier, helper, parent definition, handler, and constraint
      that establishes the restriction. Names are search hints, not proof.

      **Done when:** every retained entry point has one conservative class.

   6. Apply these adversarial classification checks before preparing the report:

      - An unguarded callback is Public, regardless of its name.
      - A configured caller address whose identity is not established remains
        Restricted (Review Required), not Contract-Only.
      - Aptos public non-entry functions that mutate state are included.
      - Sui public non-entry transaction-reachable mutating functions are
        included.
      - Read-only Solidity, Vyper, Move, TON, and CosmWasm forms remain
        excluded from the recurring state-changing inventory.
      - CosmWasm `execute` message variants are classified at their handlers,
        not only at the dispatcher.
      - Constructors, initializers, upgrade functions, and proxy dispatchers
        are listed separately when they are not recurring entry points.
      - A signer argument alone is not an administrator role.
      - `msg.sender != tx.origin` is a call-path condition, not authentication.
      - An inherited, generated, or unresolved restriction remains a warning or
        Review Required classification.

      **Done when:** every callback, caller check, read-only exclusion, and
      framework-specific visibility rule has a source-backed classification or
      an explicit warning.

   7. Record for every entry point:

      - signature or message variant;
      - file and line;
      - state-changing operation;
      - access class;
      - exact restriction evidence;
      - inherited or delegated restriction implementation;
      - callback or integration role;
      - expected caller and how that identity is established;
      - unresolved assumptions.

      **Done when:** every entry point has source-backed evidence.

   8. Emit the markdown report with:

      - project and optional project name;
      - timestamp;
      - scope and directory filter;
      - detected languages;
      - state-changing-only focus;
      - summary counts for Public, Role-Restricted, Restricted (Review
        Required), Contract-Only, deployment-only, and recurring total;
      - per-category entry-point tables;
      - read-only exclusions;
      - per-file accounting;
      - Analysis Warnings.

      The report MUST contain an explicit recurring state-changing entry-point
      count and an explicit Analysis Warnings section, even when the warning set
      is empty.

      Entry-point mode is inventory only. It does not report vulnerabilities,
      assign exploitability or severity, generate exploits, recommend fixes, or
      invoke `security-review` automatically.

      **Done when:** every file and classification is accounted for and the
      final report is emitted.

6. **Mode `graph-evolution`: compare graph structure across two refs or snapshots.**
   1. Confirm both refs resolve or both directories exist. Run `trailmark --help`; if absent, report the installation gap and stop. **Done when:** inputs and Trailmark are valid.
   2. For git refs, create temporary `mktemp -d` worktrees with `git worktree add`; for directory inputs, use them directly. Confirm both snapshots are non-empty. **Done when:** two snapshot directories exist.
   3. Build a Trailmark graph and run preanalysis for each snapshot, export both JSON graphs, and verify non-zero, plausible node counts. **Done when:** both healthy exports exist.
   4. Run `trailmark diff --json --language {language}` with the same explicit language used to build the graphs. Never accept the default `python`; distinguish a healthy empty diff from a language-missed near-empty graph using the summaries. **Done when:** native diff JSON is captured and interpreted against healthy counts.
   5. Compute membership changes for `tainted`, `high_blast_radius`, `privilege_boundary`, and related subgraphs from the exports, using `graph_diff.py` when available or direct set differences otherwise. **Done when:** every changed set has added and removed members.
   6. Classify every change in priority order: new tainted paths; privilege-boundary changes; attack-surface growth, especially `untrusted_external`; high-blast-radius additions; cyclomatic-complexity increases greater than 3 on tainted or entry-point-reachable nodes; structural additions; and structural removals checked for replacement rather than silent deletion. **Done when:** every change has node or edge evidence and one category.
   7. Assign severity to every finding, including removals: CRITICAL for a new tainted path to a sensitive function or removed auth boundary; HIGH for a new high-blast-radius entry point or large tainted-node complexity increase; MEDIUM for new trust-boundary edges or moderate complexity increase; LOW for additions without entry-point reachability; and INFO for dead-code removal or complexity reduction. **Done when:** every classification has a severity.
   8. For refs, capture `git diff {before_ref}..{after_ref}` and attach source context to findings naming nodes or edges. For directory inputs, state that source-level VCS context is unavailable. **Done when:** source context is attached or its absence is explicit.
   9. Write `GRAPH_EVOLUTION_{project}_{before_ref}_{after_ref}.md` with summary metrics, critical changes and recommendations, attack surface, complexity, taint, blast radius, privilege boundaries, added and removed nodes and edges, methodology, preanalysis, refs, and honest limitations. **Done when:** every required section exists.
   10. Remove temporary worktrees after writing the report and record their removal. **Done when:** no temporary worktree remains.

7. **Mode `variant-hunt`: search variants of a confirmed root cause.**

   1. Require a confirmed root-cause statement and either the original
      location or a vulnerable snippet. Validate the location in the codebase
      when supplied; otherwise preserve and validate the supplied snippet before
      proceeding.

      If neither is present, return:

      `blocked: root cause and original location or snippet required`

      This mode is not initial vulnerability discovery. Route initial discovery
      to `security-review`. It is also not verification of one allegation; route
      that work to `security-finding-verification`.

      **Done when:** the root cause and one concrete source anchor are
      validated.

   2. State the root cause precisely.

      For taint-like defects:

      > `[data or state] reaches [dangerous operation or decision] without
      > [required protection] under [enabling context].`

      For logic, ordering, or concurrency defects without a taint flow:

      > `[invariant] must hold across [operation], but [ordering or state
      > transition] allows it to fail.`

      A check/use separation such as TOCTOU MUST be described as a changing
      checked state, a check/use gap, or a missing atomicity guarantee. Do not
      reduce it to generic "untrusted input reaches a sink" language.

      **Done when:** the root-cause statement distinguishes the known defect
      from nearby safe code.

   3. Enumerate grounded expansion axes:

      - dangerous operation;
      - dangerous data or state;
      - missing protection;
      - enabling context;
      - semantically related identifiers;
      - sibling APIs and callbacks;
      - alternate entry points;
      - copied implementations;
      - alternate manifestations of the same invariant failure;
      - null, empty, zero, negative, maximum, repeated, and nested values;
      - success, error, cancellation, teardown, and cleanup paths.

      Search for evidence that each proposed identifier or axis exists in the
      codebase. Do not invent a family from names alone.

      **Done when:** every independent axis is grounded or explicitly rejected.

   4. Calibrate with an exact pattern that matches only the known bug.

      Use the strongest available local mechanism: repository-native structural
      search, Semgrep, CodeQL, or a simpler textual search when the stronger
      tool is unavailable. Do not install a tool or fabricate a command.

      The exact pattern must match the original location or supplied vulnerable
      snippet. A zero-hit calibration is:

      `blocked: pattern does not match known bug`

      It is not evidence that no variants exist. Record the tool actually used
      and any precision loss caused by fallback.

      **Done when:** exact calibration is proven or the tool limitation is
      explicit.

   5. Generalize one element at a time.

      For each axis:

      - change exactly one name, literal, structural relation, source/sink, or
        graph expansion parameter;
      - search the complete declared source scope;
      - record all matches;
      - read every new match;
      - record confirmed variants, safe matches, unreadable matches, and noise;
      - stop that axis when more than half of its matches are noise.

      Do not jump from the seed directly to a maximally broad semantic pattern.
      A pattern change that exceeds the noise threshold is rejected or narrowed;
      it is not hidden.

      **Done when:** each completed axis has a methodology record.

   6. In graph-seeding mode, load an existing graph and resolve the seed.

      If no graph artifact exists, return:

      `blocked: missing-graph-artifact`

      and direct the invoker to `build-program-graph`.

      Malformed or missing nodes return:

      - `blocked: invalid node object`; or
      - `blocked: node-not-found`.

      Compute at most three hops, exclude the seed, confirmed vulnerabilities,
      out-of-scope nodes, and nodes without textual or symbol content. Bound
      the candidate set to 50 and rank by at least three of degree centrality,
      clustering coefficient, path length, and structural similarity. Record
      weights, truncation, and the fact that every result is only a review
      target.

      **Done when:** the bounded ranked candidate set is ready for triage.

   7. Triage every pattern or graph candidate.

      Read the surrounding function, relevant callers and callees, types,
      guards, sanitizers, validation, ownership, and entry-point reachability.

      Assign exactly one status:

      - `confirmed-variant`: the same root cause is present;
      - `safe-look-alike`: the shape resembles the seed but an actual guard,
        sanitizer, type constraint, or different sink prevents the seed defect;
      - `unreachable-unprotected`: the protection is absent but current
        reachability is not established; retain it at lower confidence and state
        what would make it reachable;
      - `unreadable`: required source or callee evidence could not be read;
      - `out-of-scope`: the match is outside the declared scope.

      A candidate is not safe merely because it currently has no callers. A
      candidate is not confirmed merely because it resembles the seed.

      Record severity and confidence separately. For every ruled-out candidate,
      record why it was safe. For every confirmed candidate, quote the relevant
      code and identify the violated invariant or source-to-sink path.

      **Done when:** every candidate has a status, severity where applicable,
      confidence, and evidence.

   8. Write the variant report with:

      - root cause;
      - original location;
      - analyzed scope and coverage;
      - methodology table;
      - exact and generalized patterns;
      - confirmed findings with quoted code;
      - grouped safe look-alikes;
      - unreachable, unreadable, and out-of-scope candidates;
      - graph seed, hop bound, ranking dimensions, weights, and truncation when
        graph seeding is selected;
      - a CI-ready regression-rule recommendation from the strongest pattern.

      The report MUST end with an explicit conclusion:

      - `variants found: N`; or
      - `no confirmed variants found in the analyzed scope`.

      A per-candidate "not a variant" list without an overall conclusion is
      incomplete. A negative conclusion MUST name the analyzed scope and any
      unreadable remainder.

      The report MUST state that graph reachability is not data-flow proof.

      **Done when:** the complete report and explicit conclusion are written.

   9. Variant-hunt mode is read/search/report work. It does not edit source,
      tests, CI, or graph data to make a candidate pass. Its CI-ready rule is
      a recommendation only.

      **Done when:** no repair or review-loop mutation occurs.

## Failure and recovery

| Case | Handling |
|---|---|
| Findings | missing graph returns `blocked: no-graph`; missing preanalysis produces an explicitly unprioritized report; an absent importer skips only the affected input; malformed inputs report their path and continue; high unmatched counts trigger path-root review without heuristic widening; interruption returns collected sources and their completion states; rollback deletes the augmented export or removes source-tagged annotations. |
| Build-program-graph | a missing tool, import error, language detection failure, or unrun preanalysis stops the affected analysis and reports the gap; version-gated methods fall back to the baseline or export computation; rollback deletes exports and declared links, while in-memory annotations vanish with the engine. |
| Trailmark-structural | invalid target, missing Trailmark, no supported languages, import failure, missing summary field, or failed feature probe is reported without fabricated sections; empty pass outputs are valid and returned explicitly; partial output is labeled partial. |
| Entry-point-analyzer | an unsupported codebase returns no invented entry points; unparsable files remain in Analysis Warnings; Slither failures fall back to manual analysis; ambiguous access remains Restricted (Review Required); no source or repository mutation is attempted. |
| Graph-evolution | Trailmark absence, failed diff, a single failed snapshot, skipped preanalysis, or a language-mismatched empty diff stops report generation. Healthy non-zero summaries plus empty arrays mean structural stability. If cleanup is interrupted, remove temporary worktrees before retrying and report the incomplete state. |
| Variant-hunt | missing root cause, missing original location or snippet, zero exact matches, excessive false positives, missing graph artifacts, missing or malformed seed nodes, zero candidates, unsupported initial-discovery request, one-finding-verification request, and write failures return their named blocked result. If more than 200 candidates exist before triage, triage the first 200 and document the remainder; if the graph-seeded 50-candidate bound is exceeded, truncate by the documented ranking and record the truncation. Delete partial reports after a failed write. |
| Rollback | remove every named local artifact and temporary worktree created by the selected mode; no remote state is changed. |

## Output

- `findings`: an augmentation report ordered by source path and format, with matched and unmatched counts, annotated nodes, created subgraphs, tainted/high-blast-radius/privilege-boundary overlaps, skipped inputs, and source severity preserved.
- `build-program-graph`: an evidence report ordered by installed version and parser coverage, languages, graph summary, preanalysis, requested queries, model metadata, exports, and limitations; it states that reachability is not data-flow proof.
- `trailmark-structural`: the requested Trailmark summary with language, `Entrypoints:`, `Dependencies:`, and version, or the full JSON payload ordered as languages, summary, preanalysis, attack surface, hotspots, proxy nodes, subgraphs, and optional type-reference samples.
- `entry-point-analyzer`: the scoped markdown entry-point report with summary and per-category tables, file accounting, restriction evidence, callbacks, and warnings.
- `graph-evolution`: `GRAPH_EVOLUTION_{project}_{before_ref}_{after_ref}.md`, including metrics, all structural and security-relevant changes, severity, source context, and cleanup methodology.
- `variant-hunt`: a local variant report with root cause, original location, analyzed scope and coverage, methodology table, exact and generalized patterns, confirmed findings with quoted code, grouped safe look-alikes, unreachable/unreadable/out-of-scope candidates, graph-seeding details when selected, an explicit `variants found: N` or `no confirmed variants found in the analyzed scope` conclusion naming scope and unreadable remainder, and a CI-ready regression-rule recommendation; states that reachability is not data-flow proof.

## Provenance

This skill contains substantially rewritten adaptations of material from:

- `trailofbits/skills`
- revision `2be6433b39e009cd2b6fd3be1895f6b1faa5af9a`
- source paths:
  - `plugins/entry-point-analyzer/skills/entry-point-analyzer/SKILL.md`
  - `plugins/variant-analysis/skills/variant-analysis/SKILL.md`

Copyright: Made by Trail of Bits.

The adapted entry-point and variant-hunt procedures are modified for ODIN's
existing graph-backed security owner, tool boundaries, report formats, and
failure semantics. They are distributed under CC-BY-SA-4.0:
https://creativecommons.org/licenses/by-sa/4.0/legalcode

The surrounding ODIN-authored material remains covered by the repository's
existing license and notice structure. This provenance does not imply Trail of
Bits sponsorship, endorsement, or official status. No Trail of Bits logo,
mark, brand color, or marketplace metadata is included.
