# Repository contract

## Canonical baseline

Make persona and doctrine changes in `system-prompt-baseline.md`, not in the generated output-style tails. [David Parnas]

Replace the embedded span in each output style by running `python3 scripts/sync-baseline.py`, which replaces each style from its second `<role>` through EOF while preserving the persona preamble above it; stage and commit the canonical file and all six styles together. [Tony Hoare]

Verify alignment with `python3 scripts/sync-baseline.py --check` before committing; exit 0 means all styles match, exit 1 names drifted files, and exit 2 means the canonical file or a required two-`<role>` layout is missing. [Tony Hoare]

Never hand-edit `plugins/odin-core/output-styles/benchmark.md`; changing its runner preamble requires explicit user authorization, and baseline regeneration may change only the embedded cascade below that preamble. [Tony Hoare]

## Submodule publishing

Run git operations in a clone inside `.outline/worktree/<name>` because this checkout's `.git` pointer is unwritable; never put that clone in `/tmp`, where work can be lost. [Tony Hoare]

Never force-push, including any `--force-with-lease` variant; a lease does not protect review history from an intentional rewrite. [Tony Hoare]

After a non-fast-forward rejection, fetch and rebase or ask; do not use a force variant. [Tony Hoare]

## The skill tree

Author each skill once at `plugins/<plugin>/skills/<slug>/SKILL.md`; its directory determines its owner, with no separate membership registry, second tree, or per-plugin copy. [David Parnas]

Each harness reads the immediate children of `skills/`, so keep every skill at `skills/<slug>/`; Cursor additionally walks deeper levels, which would load a nested skill there alone and break cross-harness parity. [Tony Hoare]

Use `retaxonomize-plugins` for batch skill moves or plugin creation, merger, or retirement. [David Parnas]

Promote reusable lessons into the existing owning skill first; add a skill only for a distinct job that warrants a deep procedure. [Dieter Rams]

Keep brainstorming and multiple-agent ideation as distinct jobs; use multiple subagents when ideating skill changes. [David Parnas]

Give iterative review-and-fix orchestration one owner, `review-fix-loop`, rather than duplicating its procedure across skills. [David Parnas]

Balance session-wide essentials and frequently used cross-project workflows in core; keep technology-specific skills in modules. [Christopher Alexander]

Preserve consent and host-policy boundaries when placing remote publishing workflows in core; placement grants no additional authority. [Tony Hoare]

Keep native development and toolchains in `odin-native`, Rust in `odin-rust`, and hardware performance in `odin-performance`; fold singleton systems and Zig skills into `odin-native`. The Apple plugin has no retained skills and is retired. [David Parnas]

Measure explicit user invocation and genuine autonomous task use separately; exclude catalog exposure, inherited replay, and audit-only reads, and leave uncertain intent unresolved. [Richard Feynman]

Use recent cross-project usage alongside lifetime evidence when considering core placement; neither zero observed usage nor a time window authorizes deletion. [Richard Feynman]

Obtain family-level user approval before deleting never-used procedural skills; do not automatically include reference-only teaching in that deletion set. [Tony Hoare]

Keep upstream source checkouts under `.references/<owner>/<repo>` and treat them as read-only sources. [David Parnas]

Adapt upstream procedures and necessary narrow scripts selectively with provenance; propose substantial runtime or service dependencies separately. [Dieter Rams]

Leave managed-source libraries unchanged and promote general lessons into ODIN. [David Parnas]

## Distribution surfaces

Keep distribution limited to Claude Code, Codex, Cursor, Grok, and Kimi; do not add package-registry publication or npm artifacts. A flat Devin mirror of these same skills is exported to the outline repository, which publishes nothing and installs nothing; it is not a sixth distribution surface. [Tony Hoare]

Change plugin identity in `catalog/plugins.json`, not generated manifests or registries. [David Parnas]

Never hand-edit generated plugin and marketplace manifests, plugin `README.md`, `LICENSE`, or `NOTICE` files, skill `agents/openai.yaml` files, or `docs/specs/skill-index.md`. [Tony Hoare]

In the root `README.md`, leave only these spans to the generator: the plugin table under `## Plugins`, the `N skills in M plugins` sentence, and the `The largest plugins are ...` sentence; the rest of that file remains authored. [Tony Hoare]

Change generated output through its generator or catalog input, regenerate with `just render`, and commit input and output together. [David Parnas]

Declare only harness components that defaults do not resolve: Kimi needs `skills`, and Codex and Grok need `mcpServers` where a plugin ships dotless `mcp.json`. [Dieter Rams]

Keep every plugin and marketplace version aligned with `releaseVersion`, currently `2.1.6`. [Tony Hoare]

Bump `releaseVersion` by one patch when shipping a skill, output style, manifest, or attribution change; bump the minor version only on explicit request. [Tony Hoare]

Update the authored version literals in `catalog/plugins.json`, this file, and the release-version sentence in the root `README.md` together, then regenerate and commit the catalog with its generated output. [Tony Hoare]

Do not bump for tooling-only changes or edits to this file alone. [Tony Hoare]

Do not add or backfill changelog entries for routine version work; give a bump shipping a skill or behavior change one entry. [Dieter Rams]

Name plugins for a job or stack, not a tier such as `-advanced` or a miscellaneous collection. [David Parnas]

## Devin skill mirror

Never hand-edit the outline repository's `.devin/skills/<slug>/` mirror; edit the owning ODIN skill and regenerate the export. [David Parnas]

From a clone under `.outline/worktree/`, give the mirror script an explicit `--target` pointing to the real outline checkout; its default sibling path is not that checkout. [Tony Hoare]

Track a new `SKILL.md` before syncing; an untracked skill is a sync error, not an omission to accept. [Tony Hoare]

Commit mirror changes separately in the outline repository, never from this repository. [David Parnas]

## Skill metadata

Keep frontmatter to `name`, `description`, and little else; make `name` match the directory and begin `description` with a routable trigger. [Dieter Rams]

Single-quote frontmatter values containing `: `; strict YAML parsers reject unquoted colon-space even when Claude Code accepts it. [Tony Hoare]

Do not add a `license` field to a skill. [Tony Hoare]

Maintain attribution in `licenses/NOTICE` rather than representing mixed provenance with a uniform skill license. [Tony Hoare]

## Verification

Run `just check` before committing and inspect resulting changes because the cascade hook can repair files. [Tony Hoare]

Accept `recommended field missing: license` advisories from `just verify` skill validation rather than adding misleading license metadata. [Tony Hoare]

Do not invent language test commands or add CI without an explicit request. [Tony Hoare]

Test persona and doctrine changes in a fresh Claude Code session; the current session has already loaded its baseline and output style. [John Carmack]

## External harness carriers

Propagate shared doctrine changes to `~/.codex/AGENTS.md` and `~/.omp/agent/AGENTS.md` with `just sync-carriers`, then prove alignment with `just sync-carriers-check`; baseline generation does not update them. [Tony Hoare]

Keep shared carrier sections byte-identical to `system-prompt-baseline.md`, including `<change_discipline>`; preserve the intentional tool-layer differences in `<git>`, `<directives>`, `<code_tools>`, and `<thinking>`, which are compared for presence only. Reference the omp-authoritative doctrine choice when selecting future shared wording and move it into the baseline rather than authorizing a second variant. [Tony Hoare]

Edit carriers in place under their owning repositories; never commit them from this submodule or stage `~/.codex/config.toml`. [David Parnas]

## Writing style

Make each section independently actionable, with needed conditions and rules stated where the reader uses them. [Italo Calvino]

Prefer a short necessary repetition to a decorative pointer; cross-reference when the target itself is required for correct behavior. [Dieter Rams]

When auditing authored Markdown, distinguish generated regions, verbatim upstream material, and historical records before proposing edits; exclude generated output from the authored-prose audit. [Tony Hoare]

Preserve behavior and structure in wording-only edits and obtain file-specific approval before deleting a whole document. [Tony Hoare]

## Voice

Follow `docs/specs/voice.md` and the baseline's authoring register. [Otl Aicher]

Read the private spine when authoring, but never edit it from this repository or vendor its contents here. [David Parnas]

Judge the prose itself rather than treating a passing voice gate as proof of quality. [Richard Feynman]

Give every prescriptive rule in this file exactly one full-name spine anchor and re-check its fit when the rule changes. [Tony Hoare]
