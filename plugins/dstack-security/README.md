# DStack Security

DStack workflows for security review, vulnerability triage, and defensive implementation.

16 skills, category Security. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-security@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-security@dstack

# Hermes Agent
hermes plugins install gosuda/dalcom-skills/plugins/dstack-security --enable --force
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-security/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-security:<name>` in Claude Code or Hermes Agent, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| c-security-review | Use when the user requests a userspace C or C++ security review with a threat model and severity filter and wants validated findings. |
| chain-vulnerability-scanner | Use when an Algorand, Cairo, Cosmos SDK, Solana, Substrate, or TON codebase needs vulnerability scanning with reachability-backed findings. |
| codeql-security-analysis | Use when building or reusing a CodeQL database, running CodeQL security analysis, or modeling project-specific sources and sinks. |
| function-audit-context-analyzer | Use when asked for audit-context analysis of one function, or to build audit context across codebase before vulnerability hunting. |
| mermaid-to-proverif | Use when a crypto Mermaid sequenceDiagram needs a ProVerif model for secrecy, authentication, replay, or forward-secrecy checks. |
| project-findings-onto-graph | Use when graph-backed security analysis is needed: project SARIF or reviewer findings onto a program graph; build or query a multi-language graph; summarize Trailmark structure; map smart-contract entry points; compare two refs or snapshots; or hunt confirmed vulnerability variants with pattern or graph seeding. |
| security-finding-verification | Use when a named security allegation needs a true-positive or false-positive verdict. |
| smart-contract-guidelines-advisor | Use when a smart-contract project needs architecture, testing, or a maturity scorecard. |
| smart-contract-secure-workflow | Use when a smart-contract team invokes this before check-in or deployment. |
| supply-chain-risk-auditor | Use when assessing npm, PyPI, or Go dependency supply-chain risk, with lockfile-absent paths marked unassessable. |
| token-integration-analyzer | Use when a token implementation or integration needs standards, privilege, nonstandard-behavior, and defensive-integration analysis. |
| triage-security-finding | Use when exactly one concrete security finding with a source anchor needs a verdict before PoC work. |
| vector-forge | Use when crypto implementations and a vector harness need mutation-driven cross-implementation test vector expansion. |
| vulnerability-triage-brocards | Use when a vulnerability report, CVE, bug-bounty submission, or automated finding needs triage before deep verification. |
| yara-rule-authoring | Use when writing, reviewing, optimizing, validating, or migrating YARA or YARA-X malware-detection rules, including CRX or DEX rules. |
| zeroize-audit | Use when auditing C, C++, or Rust secret-handling code to verify zeroization survives compiler optimization. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
