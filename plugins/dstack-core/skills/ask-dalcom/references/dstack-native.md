# DStack Native

DStack workflows for native systems, toolchains, and performance. Install it with `claude plugin install dstack-native@dstack` in Claude Code or `codex plugin add dstack-native@dstack` in Codex; Claude Code invokes its skills as `/dstack-native:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- Debugging: `/skill:gdb`, `/skill:strace-ltrace`, `/skill:sanitizers`, `/skill:concurrency-debugging`, `/skill:memory-model`, `/skill:kernel-internals`.
- Binaries and linking: `/skill:elf-inspection`, `/skill:dynamic-linking`, `/skill:abi-and-calling-conventions`, `/skill:assembly-x86`, `/skill:assembly-arm`. Building: `/skill:make`, `/skill:zig-cross`. Compilers: `/skill:compiler-frontend`, `/skill:code-generation-and-backends`.
- Hardening and languages: `/skill:c-hardening-baseline` (user only), `/skill:production-go` (user only). Unknown binaries: `/skill:reverse-engineering`.
