# Gates and generators

Every file under `scripts/` is either a generator that writes derived files from one authored source, a gate that proves an invariant over the whole tree, or a shared helper module imported by them (`plugin-surfaces.mjs`, `carriers.py`). This document says what each one
reads, what it writes or proves, how to run it, and how to read a failure. It is written against the
scripts as they stand in the tree; when a script and this page disagree, the script is right and this
page has drifted.

`.pre-commit-config.yaml` is the gate list. This page explains the entries; it does not own their
order or their membership, because a second copy of that list drifted twice before it was cut.

## Running the set

| Command | What runs |
|---|---|
| `just render` | `render-skill-manifests.mjs`, then `node scripts/sync-knowledge-copies.mjs`, then `render-plugin-surfaces.mjs`, then `render-skill-index.mjs`, then `python3 scripts/sync-baseline.py`, in that order |
| `just check` | `prek run --all-files`: every hook in `.pre-commit-config.yaml` |
| `just verify` | `just check`, then `gh skill publish --dry-run` |
| `just sync-outline` | `sync-outline-skills.mjs`, writing into the sibling outline checkout |
| `just sync-carriers` | `sync-carriers.py`, rewriting each external carrier's shared sections from the baseline |
| `just sync-carriers-check` | `sync-carriers.py --check`: the planned rewrites plus the `check-carriers` audit |

Every local hook carries `pass_filenames: false` and `always_run: true`, so each gate audits the
whole tree on every commit no matter which files were touched. Expect the full set to take a few
seconds.

The scripts need no package manager. Every `.mjs` imports only `node:` builtins and local project modules (chiefly `./plugin-surfaces.mjs`); every `.py` imports only the standard library and local project modules (chiefly `carriers.py`). There are no external package dependencies, so each one runs directly when `prek` or `just` is absent:

```shell
node scripts/check-plugin-surfaces.mjs
python3 scripts/check-skill-frontmatter.py
```

The hooks run whichever `python3` the machine has, so `check-skill-frontmatter.py --self-test`
proves the gate itself still parses on Python 3.9 before it checks anything else.

One hook writes. `sync-baseline` runs without `--check`, so when an output style has drifted it
rewrites the file, prints `synced <path>`, and exits 1 to fail the commit. Stage the repaired styles
and commit again; the second run is clean. `just check` can therefore leave the tree modified, and
`git status` shows what it repaired.

## Generators

Each generator has a `--check` mode that diffs its output against the tree and exits 1 on drift
instead of writing. The hooks run the check modes of all but `sync-baseline`, which repairs in
place; `just render` runs the write modes of the in-tree generators. `sync-carriers` is
manual: a hook that rewrote home-directory files on every commit would fire on machines with no
carriers to repair. Its `--self-test` is a hook, because the planner has shipped a wrong overlay
rule and the fixtures catch that without touching a live carrier.

### render-skill-manifests.mjs

Derives `plugins/<plugin>/skills/<slug>/agents/openai.yaml` from each `SKILL.md` frontmatter. The
file carries two fields under `interface`:

| Field | Derivation |
|---|---|
| `display_name` | The frontmatter `name`, split on hyphens and title-cased, with an in-script acronym table (`api` to `API`, `mcp` to `MCP`, and so on) and a whole-name literal table (`agents-md` to `AGENTS.md`) |
| `short_description` | The first sentence of `description`, emitted whole. A sentence longer than 1024 characters is cut at its last clause boundary; none in the tree approaches that |

A `short_description` under 25 characters is an error, not a warning: the first sentence is where a
skill states its trigger, and a fragment that short states none.

The 64 character ceiling the generator once imposed was a local choice, not an Agent Plugins requirement. The Codex skill parser in `codex-rs/skills/src/interface.rs` resolves `interface.short_description` against `MAX_DESCRIPTION_LEN = 1024` and only warns above that. The upstream `openai.yaml` reference calls 25 to 64 characters a soft "for quick scanning" guideline, not an enforced limit. Cutting a sentence at 64 characters left dangling conjunctions, articles, prepositions, and mid-clause fragments on the user-facing surface, so the first sentence is now emitted in full. The defensive 1024 cap cuts at the last clause boundary (comma, semicolon, colon, or spaced dash) at or before 1024, strips trailing punctuation, and falls back to the last space. No current first sentence approaches 1024. The longest observed first sentence is 342 characters, so this branch is unreachable on this tree.

`--only <slug>[,<slug>...]` limits the run to named skills, which is how a fixture is checked while
the tree is mid-edit. Any other invocation processes every skill the catalog reaches.

### sync-knowledge-copies.mjs

Mirrors authored canonical source files into destination skills as byte-identical copies with executable permissions preserved so standalone and plugin installs keep working without cross-skill path traversal. Covers both knowledge contracts (such as compound schemas and concepts mirrored into autolearn) and runtime review/CI helpers (canonical resolve review scripts and ci-fix inspect_mr_checks.py mirrored into consuming skill bundles across `dstack-core`, `dstack-git`, `dstack-review`, `dstack-run`, and `dstack-infra`).

Direction is strictly one-way: canonical sources are authored and never overwritten; destinations are generated mirrors. Default mode writes missing or drifted destinations with exact source bytes and preserves source permissions (`chmod` matching source mode). `--check` reports missing or drifted files and exits 1 without writing, which is how the pre-commit hook runs it.

| Exit | Meaning |
|---|---|
| 0 | All destinations exist, match canonical source bytes, and match executable mode; or updated in write mode |
| 1 | Drift under `--check` (missing or differing files), or an unreadable file |
| 2 | Invalid command-line arguments |

### render-plugin-surfaces.mjs

Writes every file that `catalog/plugins.json` owns. The renderers live in `plugin-surfaces.mjs`,
which the checks import too, so one module defines both what is generated and what is verified.

| Output | Per | Notes |
|---|---|---|
| `.claude-plugin/marketplace.json` | tree | Codex reads this file too, so each entry carries `policy` |
| `.codex-plugin/marketplace.json` | tree | Forward-compat; Codex's candidate list has no `.codex-plugin/` entry today |
| `.cursor-plugin/marketplace.json` | tree | |
| `.grok-plugin/marketplace.json` | tree | Local source spelled `{"type": "local", "path"}` |
| `.kimi-plugin/marketplace.json` | tree | Sources read `../plugins/<id>`, resolved against `.kimi-plugin/` |
| `.claude-plugin/plugin.json` | plugin | Adds `mcpServers` when `mcp.json` exists and `outputStyles` when `output-styles/` exists |
| `.codex-plugin/plugin.json` | plugin | No `$schema`; adds `mcpServers: "./mcp.json"` when `mcp.json` exists |
| `.cursor-plugin/plugin.json` | plugin | Identity only |
| `.grok-plugin/plugin.json` | plugin | Adds `mcpServers: "./mcp.json"` when `mcp.json` exists |
| `.kimi-plugin/plugin.json` | plugin | Always declares `skills: "./skills"`; inlines the `mcpServers` map from `mcp.json` |
| `plugin.yaml`, `__init__.py` | plugin | Hermes Agent manifest and entry point; `__init__.py` is identical across plugins |
| `README.md`, `LICENSE`, `NOTICE` | plugin | README lists the skills; LICENSE and NOTICE are byte copies of the root `LICENSE` and `licenses/NOTICE` |
| The table under `## Plugins` in the root `README.md` | tree | The only generated region of that file; the prose around it is authored |

The run reports `plugin surfaces match (<files> files, <plugins> plugins)` when clean. On drift it
lists each file and ends with `run: just render`.

Loading the catalog is itself a check. `loadCatalog` throws, and the process exits 1, when the
`schema` is not `odin-plugin-catalog/v1`, when an entry's `index` is out of sequence, when an `id`
repeats, when `directory` is not `plugins/<id>`, or when an `id` falls outside the name grammar
every harness accepts: 1 to 64 characters, lowercase alphanumerics and hyphens, alphanumeric at both
ends, no `--`, no periods.

### render-skill-index.mjs

Writes `docs/specs/skill-index.md`: one row per skill, sorted by slug, naming its plugin and
category. `--check` diffs against the file and exits 1 on drift. The hook runs the check mode; `just
render` writes it.

### sync-baseline.py

Regenerates the doctrine cascade at the tail of every file in `plugins/dstack-core/output-styles/`.
Each style is a persona preamble followed by a byte-identical copy of `system-prompt-baseline.md`
from its `<role>` line onward. The split point is the style's second whole-line `<role>`: the first
opens the persona voice, the second opens the canonical charter.

| Exit | Meaning |
|---|---|
| 0 | Every style matches |
| 1 | With `--check`, drift was found and named; without it, drifted styles were rewritten |
| 2 | `system-prompt-baseline.md` is missing, or a style has fewer than two `<role>` lines |

A style with one `<role>` line is refused rather than rewritten, because the generator cannot tell
the persona from the charter and would emit a file with no preamble or a doubled one.

File arguments are accepted and filtered to the styles directory, which is how the hook tolerates
being handed every staged path.

A crashed run exits 2. It must not share the rewrite exit 1. The render recipe treats exit
1 as success.

### sync-outline-skills.mjs

Mirrors every skill into `.devin/skills/<slug>/` in the outline repository, the project-scope path
Devin reads. The default target is the sibling checkout `../dstack`; pass
`--target <path>` for a clone elsewhere.

The mirror carries exactly the files `git ls-files` tracks under each skill directory, including the
generated `agents/openai.yaml`, with executable bits preserved. A recursive copy was rejected because
`plugins/.gitignore` excludes eval and workspace directories that exist locally, and re-encoding
those patterns would be a second model of the ignore rules. Beside the slug directories it writes

Devin does not read `agents/openai.yaml`. The mirror keeps it so each skill directory stays
byte identical to its source. An exclusion list drifts when a second per-host manifest
appears. Root files sit beside the slug directories. Agent Skills discovery ignores plain
files there.

`LICENSE`, `NOTICE`, a `README.md` naming the source, and an `index.json` recording which plugin each
slug came from, since flattening drops that.

The run prunes: anything under `.devin/skills/` that the plugin tree no longer carries is deleted.
Deletion never leaves that prefix. Because the run prunes, the target is validated first and must
hold both `manifest.json` and `.git`.

A retired slug must not keep answering `/slug` in Devin. Deletion stays inside
`.devin/skills/`. Every deleted file is generated. Git restore in the outline repository
recovers a committed file. A resync recovers the rest.

| Condition | Result |
|---|---|
| Target absent, `--check` | `outline mirror target absent, skipped`, exit 0, so the hook passes on a machine without the checkout |
| Target absent, write mode | Exit 2 |
| Target present but not the outline checkout | Exit 2 |
| Two plugins claim one slug | Exit 1; the flat mirror needs one directory per slug |
| A skill's `SKILL.md` is untracked | Exit 1; add the file to git first |
| Drift under `--check` | Exit 1, listing up to 20 paths |

Commit the mirror in the outline repository, in its own commit. Never edit it in place; the next run
reverts the edit.

### sync-carriers.py

Rewrites each external harness carrier's shared doctrine sections from `system-prompt-baseline.md`
and leaves the four tool-layer sections alone. The carriers live in the home directory of whoever
runs the harness, so this is a manual command (`just sync-carriers`), never a rewrite hook.

`--check` reports planned inserts and rewrites, then runs the `check-carriers.py` audit on the
would-be result. An unknown section, a missing tool-layer tag, a duplicate shared section, or a
malformed overlay therefore fails even when the shared bodies already match. A missing carrier is
skipped; an existing path that is not a regular file is an error.

The rewriter loads `check-carriers.py` by path. The hyphen in the file name blocks a plain import.

A dangling symlink counts as unusable, not absent. It fails as a symlink instead of skipping as missing.

A carrier may hold one `<role>` overlay above the canonical block. If only the overlay is present,
the planner inserts the canonical block after it rather than rewriting the overlay. `--self-test`
proves that shape, the audit reuse, and the non-file override, using synthetic fixtures so a machine
with no carrier still runs it.

Any other missing section enters at the `<code_tools>` line. Entries at one offset keep baseline order.

## Checks

### check-plugin-surfaces.mjs

The structural gate over the plugin tree. Byte drift belongs to `render-plugin-surfaces --check`;
this script holds the invariants no renderer can restate.

| Invariant | Failure text |
|---|---|
| No retired surface exists: `package.json`, `catalog/skill-membership.json`, `plugins/<id>/plugin.json`, the retired package and distribution generators under `scripts/`, a root `skills/` or `packages/` directory, and `.agents/` | `retired surface present: <path>` |
| Every `plugins/` directory is a catalog entry and every entry has a directory | `catalog entries without a directory` or `plugin directories without a catalog entry` |
| Every plugin has at least one skill | `<id>: no skills` |
| All five dotdir manifests exist, parse, and carry `name` equal to the catalog `id` | `<id>: missing <dotdir>/plugin.json` or `name is X, catalog id is Y` |
| `.codex-plugin/plugin.json` declares no `$schema` | `must not declare $schema` |
| `.kimi-plugin/plugin.json` declares `skills` | `must declare skills` |
| A plugin shipping `mcp.json` declares `mcpServers: "./mcp.json"` in its Codex and Grok manifests | `must declare mcpServers "./mcp.json"` |
| Every plugin carries the Hermes `plugin.yaml` and `__init__.py`, and `plugin.yaml` names the catalog `id` | `<id>: missing Hermes <file>` or `plugin.yaml name does not match the catalog id` |
| Every skill directory holds `SKILL.md` and no nested `SKILL.md` one level down | `missing SKILL.md` or `nested SKILL.md at <dir>/ never loads` |
| All five registries exist, list exactly as many plugins as the catalog, and every source starts with `./plugins/` (`../plugins/` for Kimi) | `missing registry`, `N plugins, catalog has M`, or `source is not a repository path` |

The name-parity rule exists because Codex resolves a plugin's namespace from the dotdir manifest list
alone. Five manifests with different names load one plugin's components under another's namespace,
and nothing else reports it.

Retired surfaces stay listed because each one regrew at least once from a generator that outlived its purpose.

Passing output: `plugin surfaces ok: 22 plugins, 305 skills`.

### check-skill-routes.mjs

Proves each skill resolves on both install routes, `gh skill install <repo> plugins/<plugin>/skills/<slug>`
and `plugin install <plugin>@dstack`. Both read `<dir>/SKILL.md` and expect the frontmatter
`name` to equal the directory, so a mismatch drops the skill from one route while the other keeps
working.

| Check | Rule |
|---|---|
| Frontmatter | Present, terminated, and carrying `name` |
| Name | Equals the directory slug |
| Quoting | Any value containing `: ` is single-quoted; double quotes fail with their own message; strict YAML parsers reject an unquoted colon-space |
| Description | Present, at most 1024 characters (the Agent Skills limit), and stating a trigger unless `disable-model-invocation: true` |
| Display name | Unique across every generated `agents/openai.yaml`, so no two skills share a label in a harness picker |
| Pointer | Every `Not for <x>: use <slug>` pointer names an existing skill, directly or through a slug glob such as `from-*-perspective`; an article after `use`, as in `use the mewt CLI`, is prose, not a pointer |

A trigger is one of these phrases, case-insensitive, with the trailing space load-bearing: `use when `,
`use this `, `use for `, `use to `, `use after `, `use on `, `use during `, `runs /`, `invoked `,
`invoke `, `asks to `, `asks for `, `says `. Without the space, a "not for X, use ..." pointer
such as "use to-greenfield" would match `use to` and pass a description that never states its own
trigger. A bare imperative such as "Design non-trivial code" says what the skill does and never
when to reach for it, so it fails.

The display-name check reads the generated `agents/openai.yaml`, so a freshly added skill fails this
gate with `missing display_name` until `just render` has run.

Each failure class reports its first five instances and a total.

`--self-test` runs the pointer check against planted descriptions and exits non-zero unless it catches the
dangling pointers and passes the valid ones. A built-in structural parser reads the frontmatter: flat keys
and one level of nesting, hyphenated keys such as `disable-model-invocation` included. Flow styles,
multi-line scalars, and sequences are outside its scope; strict YAML parsing belongs to
`check-skill-frontmatter.py`.

### check-skill-frontmatter.py

Proves each frontmatter parses under a strict YAML parser, using the standard library only. The
manifest generator brackets single-quoted scalars with `lastIndexOf("'")`, so an unescaped
apostrophe passes it silently and then fails `gh skill publish` with `yaml: did not find expected
key`. This gate closes that hole.

It does so without reimplementing YAML, because the frontmatter shape is closed: one flat mapping,
keys from a fixed set, each value a plain or quoted scalar on one line. Anything outside that shape
fails and names what it saw, so an author introducing a new value form is told to extend the checker
rather than passing unnoticed.

| Rule | Detail |
|---|---|
| Keys | Only `name`, `description`, `disable-model-invocation`, `argument-hint`, `allowed-tools`; `name` and `description` required; no duplicates |
| Shape | No indented continuation lines; `key:value` without a space after the colon is one plain scalar, not an entry |
| Single-quoted | `''` is one apostrophe; anything else after a lone `'` is content after the closing quote |
| Double-quoted | Only the YAML 1.2 escapes; `\x`, `\u`, `\U` take exactly 2, 4, 8 hex digits |
| Plain | May not start with an indicator character, contain `: ` or ` #`, or end with `:` |

The `metadata` key the Agent Skills specification allows is rejected here, so a skill that needs it
has to widen `ALLOWED_KEYS` first.

The gate parses on Python 3.9, the oldest interpreter a contributor may carry. A backslash in an f-string field is a SyntaxError below 3.12, and this exact form shipped here once. `ast.parse(feature_version=...)` misses it, because the flag does not downgrade the f-string tokenizer. The self-test therefore checks both halves: grammar newer than 3.9, and backslashes in f-string fields.

`--self-test` runs the inline fixtures for the scalar rules and the compatibility rules, then exits
before the tree scan. Fixtures are string literals rather than files because every tracked markdown
file is gated by `check-voice`, and a fixture carrying a defect by design would need an ignored
directory the gates can see.

The f-string check is measured on Python 3.9 and 3.14, thirteen cases on each, with zero wrong verdicts. It does not slice the field by node position, because positions are unreliable below 3.12 and the slice catches legal backslashes in the literal part. It does not unparse the field, because unparsing drops a line continuation and reports a false pass.

### check-voice.py

Enforces the measurable half of `docs/specs/voice.md`: five density-based formatting tells. Fenced
blocks and inline code spans are stripped first, so a shell flag or a sample never trips a gate,
and hiding prose in backticks to silence a finding is gaming the gate.

| Gate | Trips at |
|---|---|
| Bold run | Consecutive lines opening with a bold span: 2 when at least two are colon-bearing labels, 5 otherwise |
| Dash run | 5 em or en dashes inside 600 characters |
| Title-case heading | A minor word capitalized past the first position and followed by another capitalized word |
| Banned words | The filler senses of `delve`, `leverage`, `seamless`, `underscore`, plus `holistic` and `synergy` |
| Curly quotes | Any of the four |

Scope is every markdown file the git index tracks, generated files included, minus the
pinned verbatim-upstream inventory `VENDORED_UPSTREAM`, plus two external carriers named
in `carriers.py`: `~/.codex/AGENTS.md` and `~/.omp/agent/AGENTS.md`. An absent
carrier is skipped with a notice. A carrier that exists but cannot be written is still gated and
fails the run if it carries findings, because they cannot be repaired from here. Passing file
arguments gates only those files, including a vendored path named explicitly.

Scope comes from the index on purpose; `docs/specs/voice.md` (Scope) records the untracked-tree
incident that motivates this rule.
When `git` is missing or the path is not a work tree, the gate exits 1 rather than falling back to a
walk that would change its scope silently.

The inventory is the 92 byte-identical fate assets (78 cards, 12 houses,
`INTERPRETATION_GUIDE.md`, `TECHNICAL_CONTEXT_LENSES.md`) pinned in
`plugins/dstack-core/skills/let-fate-decide/references/SOURCE-MAP.md` ("Files to copy
byte-identically") from `trailofbits/skills` at `2be6433b39e009cd2b6fd3be1895f6b1faa5af9a`,
loaded via standard library `runpy` from the skill's public `expected_asset_files()`
(`scripts/draw.py`). It is an exact path set, not a directory or suffix exclusion, so a new
file under the fate skill stays gated. The skill's authored files (`SKILL.md`, `agents/draw.md`,
`SOURCE-MAP.md` itself) stay gated, and byte preservation remains the draw script's `--verify`
proof, not this gate.

A finding in a generated file, such as a plugin README, names the generator as the defect site.

Passing output: `voice ok <N> files`. `--self-test` runs the inline classification and scope
fixtures, including the 92-path inventory count, repository target scope parity, controlled
carrier present/absent checks without touching real user carriers, authored-sibling negative
controls, and the explicit-argument pin.

Ignored files are never targets, and untracked files are never targets. The self-test proves both with a live witness. It checks that the index returns nothing for an existing ignored path. It checks that an untracked markdown file stays out of the target set even when the file carries findings.

### check-carriers.py

Proves the two external harness carriers hold the canonical shared doctrine. Sections are the
whole-line `<tag>` to `</tag>` blocks of `system-prompt-baseline.md`, compared byte for byte, with
line endings preserved so a CRLF carrier cannot pass an LF baseline.

Tags match on whole lines only. A substring match starts on a tag name inside prose and reports drift that is not there. A style-clean carrier can still carry wrong doctrine, so the voice gate cannot stand in for this check. A green run does not assert whether a carrier may hold rules the baseline lacks.

Four sections are the harness tool layer and are exempt from comparison but required to be present:
`git`, `directives`, `code_tools`, `thinking`. The gate prints this bound on every run, because
doctrine written inside those four is outside what a green run asserts.

AGENTS.md orders this split. It tells each carrier to keep its harness-specific tool layer and tool names. Codex shells out through rtk, while omp and Claude Code use native file tools.

| Carrier shape | Verdict |
|---|---|
| A shared section matches | Counted |
| A shared section is absent or differs | Failure |
| A shared section appears twice, even with identical copies | Failure; a consumer has no rule for which copy wins |
| A section the baseline does not define | Failure |
| A tool-layer section is absent | Failure |
| One extra `<role>` block above the canonical one | Allowed; the omp carrier prepends a persona overlay this way |
| A `<role>` below the canonical one, or two overlays | Failure |

The overlay sits above the charter role and states that it overrules the cascade on identity conflict. Only one overlay is allowed, because any extra block still steers behavior.

When neither carrier is installed the gate prints a notice and exits 0, so a contributor who uses
neither harness is not blocked. `--self-test` builds every drift shape synthetically from the
baseline and proves each is caught, so it runs identically on a machine with no carrier.

The carriers are edited in place and never committed from this repository. The baseline generator
does not update them. A doctrine change means editing `system-prompt-baseline.md`, running
`sync-baseline.py`, then `just sync-carriers` so the two external carriers pick up the shared
sections. `check-carriers.py` and `just sync-carriers-check` both have to be green.

### check-skill-scripts.py
Compile-, syntax-, and self-checks shipped skill executables before commit. This gates shipped executables; it is not a test suite. `--self-test` flags planted defects, and the hook pair runs the gate plus its fixtures.

It compiles every tracked Python file under `plugins/` and `scripts/`. It runs `bash -n`
on every tracked shell script under `plugins/`. A file counts as shell when it carries a shell
shebang or a `.sh` suffix. It runs each shipped `--self-check`. A missing heavyweight
import prints a skip, not a failure. The torch self-check is
`plugins/dstack-performance/skills/cpu-kernel-authoring/scripts/benchmark_cpu.py` with skip
exit 2. It holds the E4M3 to BF16 conversion against an independent float oracle. Both
reference snippets must carry each constant in `FP8_CONSTANTS`. The pinned pairs come from
the hardware verified run: zero, one flushed subnormal, one, two, and both NaN signs. E4M3
subnormals are representable in BF16. The taught kernels flush them by design. The oracle
checks every other encoding with independent float packing. `--self-test` plants one broken
file of each kind and proves each detector fires.

## Shared modules

### plugin-surfaces.mjs

`plugin-surfaces.mjs` renders every distribution surface from `catalog/plugins.json`.
The catalog is the only identity ledger.
No source is published to a package registry.
Every source is a repository-relative path.

Five harness lanes share one catalog entry.
Each lane owns one root registry and one manifest per plugin.
Hermes owns no registry file.
Install one Hermes plugin with `hermes plugins install <repo>/plugins/<id>`.

| Lane | Registry | Per-plugin manifest |
|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` | `plugins/<id>/.claude-plugin/plugin.json` |
| Codex | `.codex-plugin/marketplace.json` | `plugins/<id>/.codex-plugin/plugin.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `plugins/<id>/.cursor-plugin/plugin.json` |
| Grok | `.grok-plugin/marketplace.json` | `plugins/<id>/.grok-plugin/plugin.json` |
| Kimi | `.kimi-plugin/marketplace.json` | `plugins/<id>/.kimi-plugin/plugin.json` |
| Hermes | none | `plugins/<id>/plugin.yaml` plus `plugins/<id>/__init__.py` |

A dotdir manifest declares only what the harness default does not resolve.
Kimi defaults to a root `SKILL.md` fallback, so `skills` is mandatory there.
Codex and Grok default to the dotted `.mcp.json`, so `mcpServers` is explicit there.
Claude Code defaults to `skills/`, Codex defaults to `./skills`, and Grok defaults
to `skills/`.
Cursor discovers `skills/` and the dotless `mcp.json` by default.

Codex reads `.claude-plugin/marketplace.json` today.
`MARKETPLACE_MANIFEST_RELATIVE_PATHS` in `codex-rs/core-plugins/src/marketplace.rs`
holds no `.codex-plugin/` entry, so the Codex registry here is forward-compat and
inert today.

`loadCatalog` accepts an `id` of 1 to 64 characters.
Use lowercase alphanumerics and hyphens, with alphanumerics at both ends.
Use no `--` and no period.
Grok and Kimi reject periods, so the shared grammar excludes them.

Every harness dotdir manifest carries the same `name`.
Codex resolves the plugin namespace from the dotdir list only
(`plugin_namespace_for_root_uri` in
`codex-rs/utils/plugins/src/plugin_namespace.rs`) and never from a root file.
Diverged names load one plugin's components under another plugin's namespace.
`check-plugin-surfaces.mjs` asserts the parity.

| Manifest | Rule | Reason |
|---|---|---|
| Claude Code | Omit `skills`. Point `mcpServers` at `./mcp.json` and `outputStyles` at `./output-styles` where each exists. | `skills` defaults to `skills/`. |
| Codex Legacy (`RawPluginManifest` in `codex-rs/core-plugins/src/manifest.rs`) | Omit `skills`. Omit `$schema`. Set `mcpServers` to `./mcp.json` where `mcp.json` exists. | The Legacy default is the dotted `.mcp.json`. `resolve_manifest_path` drops a value without the leading `./`. The published schemastore schema is closed and rejects `$schema`, while the Rust deserializer ignores it. |
| Cursor | Carry identity only. | Cursor discovers `skills/` and the dotless `mcp.json` by default. |
| Grok | Omit `skills`. Set `mcpServers` to `./mcp.json` where `mcp.json` exists. | Grok defaults to the dotted `.mcp.json`. |
| Kimi | Always declare `skills: "./skills"`. Inline the `mcpServers` map from `mcp.json`. Carry name only in `author`. | Without `skills` Kimi loads zero skills from `skills/`. Kimi's schema strips the non-standard `alwaysLoad` key instead of erroring. Kimi's `readAuthor` accepts no `url` field. |
| Hermes `plugin.yaml` | Skip the harness dotdirs. Express every scalar as a JSON string. | A root Agent Plugins `plugin.json` flips Codex and Cursor into the retired portable format. YAML reads a JSON string as a double-quoted scalar. |

The Hermes entry point is identical in every plugin.
`register()` hands each `skills/<slug>/SKILL.md` to `ctx.register_skill`, which
namespaces it as `<plugin>:<slug>`.
It reads `description` with the same closed scalar grammar
`check-skill-frontmatter.py` enforces, so the skill index carries the routing
trigger without importing Hermes internals.

Each Claude marketplace entry carries `policy.authentication: "ON_USE"`.
Codex parses this registry too with a path-agnostic entry parser and would
otherwise default authentication to `ON_INSTALL`.

`source.path` in the Codex marketplace resolves against the marketplace root.
Start it with `./` and keep it inside the repository.
The Grok marketplace spells the local source as `{"type": "local", "path"}`.
Codex uses `source` for the same role.
`path` resolves against the marketplace root and rejects `..` and absolute paths.
Grok `owner` carries name only because `IndexOwner` has no `url` field.
Kimi resolves a relative source against the registry directory, so the source
climbs one level to `../plugins/<id>`.
Kimi entries key by `id`; the other lanes key by `name`.
Consume it from a local clone with `/plugins marketplace <clone>/.kimi-plugin/marketplace.json`.
Kimi cannot install a GitHub repository subdirectory, so its lane is the local clone.

`parseScalar` parses one single-line YAML scalar after `key:`.
`firstSentence` takes text up to the first period plus whitespace, else the whole value.
`tableCell` escapes backslashes and pipes and folds newlines to spaces, so a pipe
or newline in a trigger cannot split the row.
`skillTrigger` is the description first sentence, the trigger a human or a model routes on.
`repoSlug` derives the `gh skill install` owner and repo slug from the catalog
`repository` URL rather than a second literal that can drift.

Only the plugin table is generated in the root `README.md`.
The prose around it is authored.
`renderRootReadme` replaces that one region in the current file.
A hand-kept copy drifted: a category flip in `catalog/plugins.json` left the table
stale with every gate green.

### carriers.py

Names the two external harness carriers. Both live in the home directory of the user who
runs the harness. Git cannot list them, so each gate that touches them imports this list.
The entries are `~/.codex/AGENTS.md` and `~/.omp/agent/AGENTS.md`. `check-voice.py` holds
them to the voice contract. `check-carriers.py` holds them to the canonical doctrine. The
list uses `Path.home()`. A hardcoded absolute path once carried a username. It resolved to
nothing on other machines. The gate then skipped both carriers without a word. A gate that
needs another location takes it as an argument. It must not add a third copy of this list.

## Exit codes

| Script | 0 | 1 | 2 |
|---|---|---|---|
| `render-skill-manifests.mjs` | Written, or matched under `--check` | Generation error or drift | `--only` given no slug list |
| `sync-knowledge-copies.mjs` | Written, or matched under `--check` | Drift under `--check`, or an unreadable file | Bad arguments |
| `render-plugin-surfaces.mjs` | Written, or matched | Drift under `--check`; catalog failed to load | |
| `sync-baseline.py` | Clean | Drift; also after repairing in write mode | Canonical file or two-`<role>` layout missing |
| `sync-outline-skills.mjs` | Written, or matched, or target absent under `--check` | Slug collision, untracked `SKILL.md`, or drift | Bad arguments or an unusable target |
| `render-skill-index.mjs` | Written, or matched under `--check` | Drift | |
| `sync-carriers.py` | Written, in sync, skipped missing, or self-test passed | Would change, audit failure, not a file, or self-test failure | Bad arguments |
| `check-plugin-surfaces.mjs` | Clean | Any invariant broken | |
| `check-skill-routes.mjs` | Clean | Any check failed | |
| `check-skill-frontmatter.py` | Clean, or self-test passed | Any failure, or a self-test fixture failed | |
| `check-voice.py` | Clean, or self-test passed | Findings, self-test failure, or git unavailable | |
| `check-carriers.py` | Clean or no carrier installed | Failures, missing baseline, or self-test failure | |

## Workflows

Adding a skill: create `plugins/<plugin>/skills/<slug>/SKILL.md` with `name` equal to `<slug>` and a
`description` whose first sentence states a trigger, run `just render` to generate its
`agents/openai.yaml`, refresh the plugin README, and refresh the skill index, then `just check`.
Nothing else records membership; the directory is the registry.

Adding a plugin: append an entry to `catalog/plugins.json` with the next `index`, an `id` in the
shared name grammar, and `directory` equal to `plugins/<id>`. Create at least one skill under it, run
`just render` to write its five manifests, README, LICENSE, and NOTICE and to extend every registry
and the root README table, then `just check`.

Changing doctrine: edit `system-prompt-baseline.md`, run `python3 scripts/sync-baseline.py`, confirm
with `--check`, and commit the canonical file with all six styles. Then run `just sync-carriers` and
confirm with `just sync-carriers-check` and `check-carriers.py`.

Reading a failure: each gate names the file and the rule in its stderr lines and ends with a count.
A generator's drift message ends with the command that repairs it. A `retired surface present`
finding means a generator that should be dead has run again; delete the file and find what wrote it.
