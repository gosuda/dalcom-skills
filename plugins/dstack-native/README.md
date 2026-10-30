# DStack Native

DStack workflows for native systems, toolchains, and performance.

18 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-native@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-native@dstack

# Hermes Agent
hermes plugins install gosuda/dalcom-skills/plugins/dstack-native --enable
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-native/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-native:<name>` in Claude Code, `$<name>` in Codex, `dstack-native:<name>` in Hermes Agent, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| abi-and-calling-conventions | Use when explaining System V AMD64, ARM AAPCS, RISC-V psABI, stack frames, variadic calls, or FFI register rules. |
| assembly-arm | Use when reading or writing AArch64 or AArch32 Thumb assembly, inline asm in C, AAPCS64 register roles, or NEON and SVE vector code. |
| assembly-x86 | Use when reading GCC or Clang x86-64 assembly, writing inline asm, decoding AT&T syntax, or applying System V AMD64 register rules. |
| c-hardening-baseline | Use when C code is written or audited and needs a pure-C baseline: standard, undefined behavior, integer and buffer safety, sanitizers, fuzzing, build flags. |
| code-generation-and-backends | Use when reading llc output, tracing IR through legalization and instruction selection, or scoping a new LLVM target. |
| compiler-frontend | Use when building a lexer, Pratt or recursive-descent parser, AST, symbol table, type checker, or LLVM IR emitter for a language or DSL. |
| concurrency-debugging | Use when reading TSan race reports, debugging deadlocks with GDB thread inspection, analyzing Helgrind lock-order violations, or reviewing std::atomic and happens-before usage. |
| dynamic-linking | Use when debugging shared library load failures, setting RPATH or RUNPATH, applying soname versioning, writing dlopen plugins, or intercepting with LD_PRELOAD. |
| elf-inspection | Use when examining ELF binaries with readelf, objdump, nm, or ldd: dependencies, symbols, sections, relocations, build IDs, or hardening, or when enabling RELRO, PIE, stack canaries, FORTIFY_SOURCE, CET, CFI, or seccomp filters, or checking a binary with checksec. |
| gdb | Use when running GDB: breakpoints, watchpoints, segfault or hang debugging, reverse debugging, remote gdbserver, core dumps, pretty-printers, Python scripting, or multi-threaded debugging. |
| kernel-internals | Use when diagnosing scheduler latency, kmalloc vs vmalloc, page cache, meminfo under pressure, or OOM victim choice, or when reading kernel/sched, mm, or fs source. |
| make | Use when writing or debugging Makefiles, understanding pattern rules and automatic dependency generation, managing CFLAGS/LDFLAGS, or diagnosing incremental build, phony targets, or recursive make. |
| memory-model | Use when choosing memory orderings for C++ or Rust atomics, reasoning about happens-before, writing lock-free patterns, or diagnosing data races. |
| production-go | Use when writing, reviewing, debugging, or architecting Go code. |
| reverse-engineering | Use when triaging an unknown binary, decompiling with Ghidra, scripting radare2, or diffing two builds for patched functions. |
| sanitizers | Use when building, running, or interpreting ASan, UBSan, TSan, MSan, LSan, HWASan, or Miri for native or Rust code, including memory-corruption debugging, unsafe-code validation, and sanitizer CI wiring. |
| strace-ltrace | Use when a binary misbehaves without crashing and the question is which file, socket, syscall, or library call fails: strace for syscalls, ltrace for library calls. |
| zig-cross | Use when building Zig or C for another platform with Zig: target triples, -mcpu features, zig cc cross-compiles, multi-target build.zig, bare-metal Cortex-M, or WebAssembly. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
