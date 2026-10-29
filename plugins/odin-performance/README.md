# ODIN Performance

ODIN workflows for measured performance: hardware kernels, profilers, byte budgets, and optimization proof.

8 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-performance@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-performance@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-performance/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-performance:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| cpu-kernel-authoring | Use when writing, optimizing, or benchmarking a C++ CPU kernel with AVX2 or AVX512 intrinsics for the Hugging Face kernels ecosystem. |
| decoded-memo-retention | Use when a query-scoped decoded-block cache is bounded only by serialized work bytes, or when fallback paths retain many decoded blocks. |
| fastopt | Use when optimizing suspected hot paths without waiting for benchmarks. |
| fastopt-extreme | Use when estimating hot paths and proposing complexity-neutral cold simplifications while refusing complexity theater. |
| heaptrack | Use when tracking heap allocations on Linux with heaptrack: allocation hotspots, peak heap, temporary allocations, leaks, or a diff of two runs via heaptrack_print. |
| optimize | Use when one named path or performance symptom needs a single measured fix. |
| optimize-extremely | Use when a named subsystem must be made as fast as possible through a measured-floor campaign. |
| simd-intrinsics | Use when reading auto-vectorization reports, writing SSE2, AVX2, or NEON intrinsics, or fixing vectorization failures. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
