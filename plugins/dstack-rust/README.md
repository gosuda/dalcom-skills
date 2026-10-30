# DStack Rust

DStack workflows for Rust development: cargo, async, FFI, cross-compilation, debugging, and unsafe review.

10 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-rust@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-rust@dstack

# Hermes Agent
hermes plugins install gosuda/dalcom-skills/plugins/dstack-rust --enable --force
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-rust/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-rust:<name>` in Claude Code or Hermes Agent, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| cargo-workflows | Use when managing Cargo workspaces, feature flags, build scripts, CI caching, dependency auditing, or Cargo.lock with Rust. |
| idiomatic-rust | Use when writing, reviewing, or refactoring Rust code. |
| rust-async-internals | Use when understanding the Rust Future poll model, Pin and Unpin, tokio scheduling, async stack traces, waker leaks, or select!/join! behavior. |
| rust-build-times | Use when profiling slow Rust builds with cargo --timings, configuring sccache, selecting the Cranelift dev backend, splitting a workspace for parallelism, or tuning LTO and the linker. |
| rust-cross | Use when building Rust binaries for a different target architecture or OS, using cross or cargo-zigbuild, configuring .cargo/config.toml, or targeting embedded bare-metal. |
| rust-debugging | Use when debugging Rust binaries with GDB or LLDB, enabling pretty-printers, interpreting panics and backtraces, debugging async with tokio-console, or stepping through no_std code. |
| rust-ffi | Use when calling C libraries from Rust, generating bindings with bindgen, exporting Rust functions to C with cbindgen, writing safe wrappers over unsafe FFI, or linking system libraries. |
| rust-security | Use when auditing Rust dependencies for vulnerabilities, enforcing license and source policies with cargo-deny, reviewing RUSTSEC advisories, or fuzzing and testing unsafe code for security. |
| rust-unsafe | Use when writing, reviewing, or auditing unsafe Rust, or understanding raw pointers, transmute, UnsafeCell, and safe abstractions over unsafe code. |
| rustc-basics | Use when selecting RUSTFLAGS, configuring Cargo profiles, tuning release builds, reading assembly or MIR output, understanding monomorphization, or diagnosing compilation errors. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
