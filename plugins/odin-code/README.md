# ODIN Code

ODIN workflows for writing, changing, and simplifying code.

26 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-code@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-code@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-code/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-code:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| api-and-interface-design | Use when asked to design or change a public API, route, CLI flag, or module boundary. |
| architecture-simplification | Use when the user explicitly asks to simplify an architecture, collapse modules or crates, or cut a dependency graph within approved boundaries. |
| ast-grep | Use when asked to run AST-based structural search, lint, or rewrite of code when regex is too fragile. |
| breaking-driven | Use when bloated code needs clean re-derivation, or the user says "this module is bloated" or "break it and rebuild". |
| clean-clean-cut | Use when asked to run /clean-clean-cut to cut accumulated records and residue. |
| code-review | Use when a named diff or pull request needs review for bugs, regressions, tests, and standards. |
| constraint-driven-development | Use when no quality bar is written down, when setting up constraints, or when implementing under non-negotiable budgets, limits, or API rules. |
| contract-driven | Use when crossing a public API boundary, guarding complex invariants, or hardening untrusted input or integration seams. |
| deprecate-and-migrate | Use when asked to remove old code, migrate consumers, or decide whether to maintain or sunset a system. |
| deps-upgrade | Use when dependency upgrades need batching for CVEs, a major release, forced compatibility, a scheduled or vulnerability-triggered sweep. |
| deslop | Use when the user says deslop, debloat, tidy, clean a diff, cleanup codebase, or deslop branch diff, or remove dead code or config. |
| dimensional-analysis | Use when code mixes units, fixed-point precisions, scaling factors, rates, prices, shares, or conversions. |
| explore | Use when asked to explore the codebase to map structure, symbols, and dependencies. |
| first-load-byte-reduction | Use when a first screen needs lower transfer bytes without visual or behavioral change. |
| fromzero | Use when replacing a greenfield attempt with a clean pad of verified requirements. |
| guillotine | Use when dead, duplicate, superseded, or generated residue must leave more than one artifact class of a repo or subsystem, preserving behavior. |
| incremental-implementation | Use when implementing a multi-file change, building a feature from a breakdown, or writing a large amount of code. |
| minimalism-driven | Use when writing or restructuring code, before adding a helper, wrapper, config key, or dependency, or when the user asks for minimal or DRY code. |
| offense | Use when a human says "overhaul", "rebuild this subsystem", or "rewrite it from scratch". |
| polish | Use when a working feature needs user-directed UX refinement before shipping. |
| refactor-break-compat | Use when modernizing APIs, removing compat shims, killing feature flags, or rewriting a subsystem cleanly. |
| restart-keeping-lessons | Use when an implementation has more workarounds than structure and another patch will not pay. |
| slicing-code-context | Use when an exact symbol, path, entrypoint, or line range can bound a focused code question or patch proposal under a fixed source budget. |
| source-driven | Use when writing or verifying framework-specific code, boilerplate, or a documented, correct implementation. |
| to-greenfield | Use when the user says greenfield this or rescue this codebase, names a field (dark, red, blue, or brown), or diagnoses a subsystem. |
| type-driven | Use when modeling a domain, encoding a state machine, hardening APIs, making invalid states unrepresentable, or parsing instead of validating. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
