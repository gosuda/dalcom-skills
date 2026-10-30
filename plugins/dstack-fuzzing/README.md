# DStack Fuzzing

DStack workflows for fuzz harnesses, fuzzer setup, sanitizers, and coverage analysis.

4 skills, category Security. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-fuzzing@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-fuzzing@dstack
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-fuzzing/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-fuzzing:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| fuzzing | Use when planning an end-to-end fuzzing program for a project: engine and target selection, corpus management, and CI or nightly wiring. |
| fuzzing-dictionary | Use when a parser, protocol, or file format fuzzer stalls at fixed-token validation gates and needs a coverage dictionary. |
| fuzzing-obstacles | Use when asked to identify and bypass checksums, nondeterminism, or validation barriers that block fuzzing coverage. |
| libfuzzer | Use when asked to build, run, or triage a coverage-guided C/C++ fuzz campaign on the libFuzzer or AFL++ engine. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
