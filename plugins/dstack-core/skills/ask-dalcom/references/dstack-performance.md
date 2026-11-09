# DStack Performance

DStack workflows for measured performance: hardware kernels, profilers, byte budgets, and optimization proof. Install it with `claude plugin install dstack-performance@dstack` in Claude Code or `codex plugin add dstack-performance@dstack` in Codex; Claude Code invokes its skills as `/dstack-performance:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- One named path and one measured fix: `/skill:optimize`; a whole subsystem driven to a measured floor: `/skill:optimize-extremely`.
- No benchmark yet: `/skill:fastopt` for suspected hot paths, `/skill:fastopt-extreme` to estimate and propose complexity-neutral cuts. Tools: `/skill:heaptrack`, `/skill:simd-intrinsics`, `/skill:cpu-kernel-authoring` (user only), `/skill:decoded-memo-retention`.
