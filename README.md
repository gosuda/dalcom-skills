# Dalcom Skills

> Formerly the ODIN Claude Plugin. The repository moved to gosuda/dalcom-skills.

Dalcom Skills, built on the DStack methodology, is a highly opinionated code-agent skill library: principles-first
engineering, surgical editing, and workflow automation, published as installable plugins. It gives
you a drop-in skill set with five discipline layers. Skills are authored once in-tree, and every
supported client discovers them from that same layout, so nothing is copied or republished.

Methodology: [outline-driven-development](https://github.com/OutlineDriven/outline-driven-development)
· Site: [outlinedriven.github.io](https://outlinedriven.github.io)

- Five harness surfaces from one tree: Claude Code, Codex, Cursor, Grok, and Kimi
- No package manager for the tooling; every script is dependency-free Node ESM or standard-library Python
- Six output styles in dstack-core, each embedding the canonical doctrine byte-identically
- Pre-commit gates that audit the whole tree on every commit, listed in `.pre-commit-config.yaml`

## Contents

- [What is this](#what-is-this)
- [Install](#install)
- [Choose your plugins](#choose-your-plugins)
- [Using the skills](#using-the-skills)
- [Plugins](#plugins)
- [Core philosophy](#core-philosophy)
- [Output styles](#output-styles)
- [Development](#development)
- [License](#license)

## What is this

304 skills in 22 plugins. A skill is authored once, at
`plugins/<plugin>/skills/<slug>/SKILL.md`, and that path is its only home. The directory states
which plugin owns the skill, so no registry has to answer that question. Every plugin and
marketplace ships at one `releaseVersion`, currently 2.1.9, held in `catalog/plugins.json`.

Each harness resolves components from fixed conventions at the plugin root, so this layout is the
one every supported client already discovers. Nothing is copied at publish time, and nothing is
published to a package registry.

```
plugins/dstack-core/
  .claude-plugin/plugin.json   Claude Code manifest
  .codex-plugin/plugin.json    Codex manifest
  .cursor-plugin/plugin.json   Cursor manifest
  .grok-plugin/plugin.json     Grok manifest
  .kimi-plugin/plugin.json     Kimi manifest
  skills/necessary-work/SKILL.md        authored skill
  skills/necessary-work/agents/openai.yaml   generated from the frontmatter
  mcp.json                     MCP servers, dstack-core only
  output-styles/               Claude output styles, dstack-core only
```

> `dstack-core` carries the six output styles and the core session gates; `dstack-planning` carries the planning skills. `dstack-code` carries the day-to-day engineering skills. Install the rest by working domain.


## Core philosophy

> 1. Investigate before acting. Never speculate about code you have not read.
> 2. Draw the structure before building it.
> 3. Match rigor to risk.
> 4. One logical change per commit.
> 5. Show the code, not a description of the code.

## Install

Six install surfaces are supported; each installs from this repository.

### Claude Code

```shell
claude plugin marketplace add gosuda/dalcom-skills
claude plugin install dstack-core@dstack

# Your selected plugin modules; Keep it lean, only for you.
claude plugin install dstack-code@dstack
claude plugin install dstack-run@dstack
claude plugin install dstack-planning@dstack
claude plugin install dstack-knowledge@dstack

# More ...
```

### Codex

```shell
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-core@dstack

# Your selected plugin modules; Keep it lean, only for you.
codex plugin add dstack-code@dstack
codex plugin add dstack-run@dstack
codex plugin add dstack-planning@dstack
codex plugin add dstack-knowledge@dstack

# More ...
```

### Cursor

Add the marketplace, then `/plugin install dstack-core`. Cursor reads the
`.cursor-plugin/plugin.json` manifest at each plugin root.

```
/plugin install dstack-core

# Your selected plugin modules; Keep it lean, only for you.
/plugin install dstack-code
/plugin install dstack-run
/plugin install dstack-planning
/plugin install dstack-knowledge

# More ...
```

### Individual (gh skill)

`gh skill` installs a single skill for any of its supported agents. Passing the exact path skips a
full tree traversal, which matters at this repository's size.
```shell
gh skill install gosuda/dalcom-skills plugins/dstack-core/skills/askme \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

### Grok

```shell
grok plugin marketplace add gosuda/dalcom-skills
grok plugin install gosuda/dalcom-skills#plugins/dstack-core
```

The `#plugins/<plugin>` suffix selects one plugin subdirectory from the repository.

### Kimi

From a local clone; Kimi cannot install a subdirectory of a GitHub repository.

```shell
/plugins marketplace /path/to/dalcom-skills/.kimi-plugin/marketplace.json
/plugins install /path/to/dalcom-skills/plugins/dstack-core
```

Both paths are absolute: Kimi rejects a relative plugin root.

## Choose your plugins

Nothing here is all-or-nothing. `dstack-core` and `dstack-code` are the base from Install; every
row below is what you add on top for that kind of work, and unselected plugins stay uninstalled.

| Working on | Add |
|---|---|
| Everyday code changes | `dstack-run`, `dstack-git` |
| Tests and verification | `dstack-testing` |
| Large refactors, audits, bounded iteration | `dstack-code`, `dstack-review` |
| A specific language | `dstack-native`, `dstack-typescript`, or `dstack-rust` |
| Web and interface work | `dstack-typescript`, `dstack-design` |
| Security review and hardening | `dstack-security`, `dstack-fuzzing` |
| Research and technical writing | `dstack-research`, `dstack-knowledge`, `dstack-writing` |
| Product, planning, and new artifacts | `dstack-planning`, `dstack-visual` |
| Building agents | `dstack-skills` |
| Infrastructure and data | `dstack-infra` |

Each name installs with the same command:

```shell
/plugin install dstack-security@dstack
```

The largest plugins are `dstack-core` at 83, `dstack-marketing` at 28, and `dstack-run` at 20.
Install one skill instead of a whole plugin with `gh skill install`, shown under Install above.

## Using the skills

You install plugins once and invoke skills every day. Start with the [getting-started guide](docs/guides/getting-started.md) to run your first skill. Read [using the skills](docs/guides/using-skills.md) for the invocation mechanics. Browse [example workflows](docs/guides/workflows.md) for chains mined from real sessions.

## Plugins

| Plugin | Category | Plugin | Category |
|---|---|---|---|
| dstack-core | Coding | dstack-knowledge | Productivity |
| dstack-planning | Productivity | dstack-learn | Productivity |
| dstack-code | Coding | dstack-skills | Productivity |
| dstack-review | Coding | dstack-writing | Writing |
| dstack-testing | Coding | dstack-visual | Design |
| dstack-git | Coding | dstack-design | Design |
| dstack-run | Coding | dstack-typescript | Coding |
| dstack-infra | Infrastructure | dstack-native | Coding |
| dstack-security | Security | dstack-rust | Coding |
| dstack-fuzzing | Security | dstack-performance | Coding |
| dstack-research | Research | dstack-marketing | Marketing |

`catalog/plugins.json` is the identity ledger: it holds each plugin's name, description, category,
and tags, and every manifest and registry is generated from it.

## Output styles

Output styles shape how the agent communicates. Switch through Claude Code's `/config` or by
setting `outputStyle` in `settings.json`. They ship in `dstack-core`.

- `DStack`: default. Skeptic register, scope discipline, no reflexive validation.
- `AxiomMode`: formal-logic English with predicate-form claims and ASCII keywords.
- `Builder`: for non-technical builders. Outcome-first, plain language, progressive disclosure.
- `Duet`: companion to the `duet` skill. Decisions before prose, forks stated loudly.
- `Linus`: Torvalds review discipline. Good taste as special-case elimination.
- `Eval`: benchmark harness register, generated by margin-runner. Do not hand-edit.

Every style embeds a byte-identical copy of `system-prompt-baseline.md`, because the Claude Code
loader does not resolve references. `scripts/sync-baseline.py` owns that copy.

## Development

There is no package manager here. Every script is dependency-free Node ESM or standard-library
Python.

```shell
just              # list tasks
just render       # regenerate skill manifests, plugin manifests, registries, skill index, and the doctrine cascade
just check        # every gate
just verify       # every gate plus Agent Skills validation
```

`.pre-commit-config.yaml` is the gate list. Every gate audits the whole tree and runs
unconditionally, so none of them can be skipped by touching the wrong file. `docs/specs/gates.md`
explains what each generator writes, what each gate proves, and how to read a failure.

## License

See LICENSE. Third-party attribution is in `licenses/NOTICE`.

Issues: https://github.com/gosuda/dalcom-skills/issues
