# DStack Fuzzing

DStack workflows for fuzz harnesses, fuzzer setup, sanitizers, and coverage analysis. Install it with `claude plugin install dstack-fuzzing@dstack` in Claude Code or `codex plugin add dstack-fuzzing@dstack` in Codex; Claude Code invokes its skills as `/dstack-fuzzing:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- `/skill:fuzzing` plans the program (engine, targets, corpus, CI), `/skill:libfuzzer` runs and triages a C or C++ campaign, `/skill:fuzzing-dictionary` helps when coverage stalls at fixed tokens, and `/skill:fuzzing-obstacles` when it stalls at checksums, nondeterminism, or validation gates.
