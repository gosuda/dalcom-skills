---
name: setup-repo
description: 'Use when the user asks to set up a repository: deterministic gitignore, repository-native pre-commit hooks, or REVIEW.md and CONTRIBUTE.md rules. This skill supersedes all setup- skills including setup-gitignore and setup-review-rules, and replaces git-guardrails. Not for one-off code reviews, PR feedback, or general documentation.'
---

# Set up a repository natively

Set up the operating repository so it stays clean by construction: ignored paths are deterministic, the commit-time hook runs the repository's own strict gates, and review and contribution rules name only real invariants. Read the repository before choosing anything, reuse what it already declares, and invent nothing.

This skill owns ignore setup, hook setup, and review-rule setup together as one coherent repository setup. It installs no global command interceptor; protection comes from the repository's own hook running its own gates.

## Ground rules before touching anything

Work only inside the repository the user names, resolved via `git rev-parse --show-toplevel`, and make that root the working directory for everything below. When no repository is found, stop and say so with nothing written.

Writes are reversible and local only: the repository `.gitignore`, hook configuration plus whatever manifest, lockfile, or local `.git/hooks/pre-commit` entry the chosen manager needs, and exactly the requested policy files `REVIEW.md` and `CONTRIBUTE.md` under the repository root. Reject any policy target outside that root with no mutation, and never substitute `CONTRIBUTING.md` or any other filename.

Preserve existing configuration and user data. Merge into what is there; never clobber grounded rules, legal notices, AI-contribution policies, or user-owned sections. Preview every genuinely destructive, data-touching, remote, or install consequence with its exact target and proceed only with explicit approval for that write. Never make blanket global changes.

Read representative source before deciding: sample the code the rules will govern, trace at least one consumer path per touched surface, and cover build and test configuration, declared gates and CI checks, architecture and data boundaries, and existing policy. Record every file actually read. Never rest a rule on directory layout alone, never derive a gate command the repository does not declare, and never weaken or disable a check to get green.

## Shape the ignore file deterministically

Detect language template keys from regular files at repository-relative depth 0 through 2, excluding `.git/`, applying every matching row below, deduplicating, and sorting lexicographically. An empty result is valid and means no network template is requested.

| Evidence filename | gitignore.io key(s) |
|---|---|
| `tsconfig.json`, `tsconfig.*.json` | `node,typescript` |
| `package.json` | `node` |
| `pyproject.toml`, `requirements.txt`, `setup.py`, `setup.cfg`, `Pipfile` | `python` |
| `Cargo.toml` | `rust` |
| `go.mod` | `go` |
| `dune-project`, `dune`, `*.opam` | `ocaml` |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | `java` |
| `settings.gradle.kts` with Kotlin source files | `java,kotlin` |
| `CMakeLists.txt` | `cmake,c++` |
| `Gemfile`, `*.gemspec` | `ruby` |
| `composer.json` | `php` |

Capture the current state first: the exact `git status --short --untracked-files=all` entries beginning `?? ` excluding `.gitignore`, with before and after counts reported at the end. When a `.gitignore` already exists, read its exact bytes and copy it to `/tmp/gitignore-snapshot-<UTC-YYYYMMDDTHHMMSSZ>.bak` before modifying it; when that snapshot fails, stop without writing.

Group the untracked paths by top-level directory, grouping root files by lowercase extension with extensionless root files as `(no extension)`, show every path in each group, and ask the user which exact directory (`name/`) or extension (`*.ext`) patterns to add. Normalize confirmed patterns to repository-relative slash form, reject `..`, absolute paths, and patterns matching `.gitignore` itself, then sort and deduplicate. The user declining empirical additions yields an empty empirical block, never cancellation of the rest.

When the key list is non-empty, fetch `https://www.toptal.com/developers/gitignore/api/<comma-separated-keys>` with `curl -sf --max-time 10`, using the response verbatim after normalizing line endings to LF and stripping trailing blank lines. When the request fails, report the keys with the network error and stop leaving `.gitignore` unchanged; there is no silent fallback. An empty key list means an empty language block with no request.

Assemble four managed sections in this exact order, each opened by its exact anchor line followed by its normalized body and one blank line except the final block: `# === LANGUAGE TEMPLATES ===` with the fetched body or empty, `# === AI TOOLING ===` with `.claude/settings.local.json`, `.cursor/`, `.windsurf/`, `.aider.chat.history.md`, `.aider.input.history`, `# === IDE / EDITOR ===` with `.idea/`, `.vscode/*` plus the four `!.vscode/extensions.json`, `settings.json`, `tasks.json`, `launch.json` keeps, `*.swp`, `*.swo`, `*~`, `.DS_Store`, `Thumbs.db`, and `# === EMPIRICAL ===` with the confirmed patterns one per line. A non-comment, non-blank pattern line duplicates when its exact trimmed text already appeared in preserved user content or an earlier managed section; first occurrence wins, and API-supplied comment lines are preserved.

Merge without touching user content: with no existing file the candidate is the four sections; otherwise require each of the four exact anchor lines to occur zero or one time, replace each existing managed block from its anchor through the line before the next managed anchor, append missing blocks in canonical order, preserve all other bytes exactly, normalize only generated blocks to LF, and end with exactly one terminal newline.

Show the complete before/candidate diff with any available local renderer and write the candidate atomically to the repository-root `.gitignore` only on approval; on decline leave the file unchanged. Then re-run detection, fetch, build, and merge in memory against the new bytes with the same confirmed empirical inputs and require a byte-identical second candidate, otherwise restore the snapshot (or remove a newly created file) and report the second-pass diff. Recount untracked entries with the same command and report both counts plus every remaining path.

## Wire one hook manager to the repository's own gates

Inventory the repository's manifests, lockfiles, declared gate scripts, hook configuration, and `.git/hooks/pre-commit`, noting `pnpm-lock.yaml`, `bun.lock`, legacy `bun.lockb`, `uv.lock`, `go.mod`, `Cargo.toml`, and `dune-project`. When one hook manager already exists, extend it; when several managers could fire on the same commit, stop and report every firing path with the smallest clean cutover, removing nothing observable without the user's approval.

When none exists, pick from repository evidence: Lefthook for a pnpm, Bun, or Go repository, prek for Python, Rust, or OCaml, and in a mixed repository the manager already represented by its lockfile or task runner, asking the user only when two choices remain equally supported. Install through the current project toolchain only: `pnpm add -D lefthook @biomejs/biome && pnpm exec lefthook install` for JavaScript or TypeScript, `go install github.com/evilmartians/lefthook@latest && lefthook install` for Go, `uv tool install prek && prek install` for Python, Rust, or OCaml. Never introduce ESLint, Prettier, Black, isort, mypy, a second package manager, or any formatter, linter, or type checker the repository did not already declare; duplicate policy stacks are a defect.

Configure only commands the repository can execute, with `pass_filenames: false` on whole-repository commands and parallel independent read-only checks only where their tools do not edit the same files: JavaScript or TypeScript Lefthook runs `pnpm exec biome check --write --no-errors-on-unmatched .` plus the declared type-check and targeted-test scripts; Python prek local hooks run `uv run ruff check --fix .`, `uv run ruff format --check .`, `uv run pyright`, and the declared targeted pytest command; Go Lefthook fails when `gofmt -l .` returns a path, then runs `go vet ./...` and `go test ./...`; Rust prek local hooks run `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and the repository test command preferring `cargo nextest run` when configured; OCaml prek local hooks run `dune fmt`, `dune build @runtest`, and any stricter repository alias already declared. Include the declared strict checks, complexity limits, and dependency boundaries the repository already states; never invent pins or thresholds.

Run the manager's all-files entry point (`pnpm exec lefthook run pre-commit` or `prek run --all-files`); when a formatter changes files, inspect the diff and repeat until the non-mutating gate passes. Then prove the hook is load-bearing without creating history: introduce one temporary reversible formatting violation inside an owned scratch file the hook includes, run the hook requiring non-zero or an automatic repair plus a dirty diff, restore the scratch file, rerun requiring zero. When the hook includes no formatter, stage a trivial change such as a blank line in a tracked file, run the hook requiring every configured check to pass, then revert the staged change. Never weaken a command to make a probe pass. Confirm exactly one executable `.git/hooks/pre-commit` entry remains delegating to the chosen manager, confirm the worktree matches the pre-probe baseline, and do not commit unless the user separately asks.

## Write review and contribution rules from evidence

Read the existing `REVIEW.md` and `CONTRIBUTE.md` when present alongside the source, consumer, configuration, gate, boundary, and policy evidence above. Admit a candidate rule only when it states a material repository-specific invariant a future reader must obey, grounded in a file actually read or explicitly tagged human-supplied; reject templates, universal stack claims, and anything derivable by reading the repository. Write a file only when admitted invariants justify it; when none exist, write neither file and say so.

Merge admitted rules into each existing target without clobbering: keep grounded rules, legal notices, and AI-contribution policies intact, flag direct conflicts to the user instead of overwriting, and create no unrequested third policy file.

Hold `REVIEW.md` to evidence-backed, firm review. Every finding names the actual bug or invariant violation, the affected consumer and its consequence, the code path, quoted evidence, and severity in plain semantic words. Proof is a powerful test that fails on the fault, with reusable inputs allowed and saved-output pins and source-text assertions rejected. No fabricated findings, no unearned approval, no filler. The tone is direct and firm, attacking defects and never people.

Hold `CONTRIBUTE.md` to clean contract-first contributions that keep the repository natively anti-slop, anti-spaghetti, and minimal by replacement rather than accretion. Every change migrates all its callers and leaves no obsolete path, shim, or alias. Code reads through names, types, and control flow with no comment crutches and no commented-out code. Tests are invariant or adversarial oracles each detecting a distinct plausible fault, never weak coverage padding. No unnecessary docs, plans, specs, or ADRs accompany a change. Names are semantic; opaque codes, numbers, and sequence prefixes are rejected. No defers, stubs, placeholders, or excuses ship. Stated authority, security, and data boundaries stand, with no implicit publish or deploy step.

Re-read each written file and verify every rule against all of the above, removing any rule that lacks grounding, restates repository-derivable fact, or depends on a private anchor list or peer runtime. Write no generated manifests, registries, or YAML.

## When to stop instead

Stop with nothing further mutated and a plain `blocked` report naming the exact cause and what was left untouched or restored: an unresolvable repository root or an out-of-repository target; no grounded repository-specific invariants; a conflicting existing rule, leaving the conflicted region unchanged; a failed snapshot, unreachable template source, rejected empirical pattern, duplicated or out-of-order managed anchors, declined write, failed write with the snapshot restored or partial file removed, or a non-identical second candidate; missing repository-native gates; competing hook managers; an install failure with manifest, lockfile, hook config, and hook entry restored from baseline; a probe that does not trip, meaning the hook is not load-bearing and a green normal run alone never counts; leftover probe residue, restoring the scratch path first; or a write or verification failure with pre-write contents restored where possible. When a probe fails, tell hook-wiring faults (the hook did not fire, fired the wrong command, or missed the file, fixed here) apart from check-content faults (the check reported a real issue, reported to the user without editing check logic). Never swallow an error and never claim completion while any check failed.

## What you hand back

The written `.gitignore` with before/after untracked counts, remaining paths, and the snapshot path when an existing file was merged; the selected hook manager with changed config and manifest paths, the installed hook path, the passing all-files command and output with no formatter residue, the failing-probe evidence showing a block and the passing-probe evidence showing zero (or the trivial-commit probe equivalents), and the rollback command; the written `REVIEW.md` and `CONTRIBUTE.md`; and a report listing every file actually read, the human-supplied rules as tagged, applied merges, flagged conflicts, and the rollback path. Otherwise hand back the exact `blocked` classification with partial-state or rollback detail.
