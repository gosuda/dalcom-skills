# DStack Run

DStack workflows for executing plans, orchestrating subagents, and bounded autonomous loops.

20 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-run@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-run@dstack

# Hermes Agent
hermes plugins install gosuda/dalcom-skills/plugins/dstack-run --enable --force
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-run/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-run:<name>` in Claude Code or Hermes Agent, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| append-run-log | Use when a completed agent run must be recorded as durable, queryable evidence. |
| artifact-arena | Use when asked to run /artifact-arena to generate and judge competing artifact implementations. |
| cybernetic-loop | Use when the caller supplies a falsifiable out-of-happy-path invariant and a finite budget. |
| diagnose-loop-health | Use when a configured loop misbehaves, produces unexpected results, or its setup soundness is questioned. |
| diamond-task | Use when one issue or PR is too large for a worker and partitions into disjoint write sets. |
| feedback-sweep | Use when asked to /feedback-sweep [setup\|reconfigure] [mode:non-interactive]. |
| figure-it-out | Use when non-trivial work should run a matched playbook to verified real-surface completion, or a bespoke workflow when none fits. |
| goal-prompt-drafting | Use when asked to draft copy-ready /goal objectives for long-running agents. |
| guardrail-carve-run | Use when guardrail-adjacent material (stealth, scraping, privacy, IP, policy, security) or mixed reversible/irreversible, sensitive work, or the user says "autobahn this". |
| implement-spec | Use when a ticket DAG from a complete specification needs parallel execution into a verified integration branch, with an optional green draft pull request or merge request on explicit approval. |
| orchestration-patterns | Use when work decomposes across subagents or role panels and needs coupling-based orchestration. |
| partition-scopes-to-subagents | Use when asked to partition non-overlapping scopes across subagents and drive each to completion. |
| schedule-dependency-waves | Use when work units carrying declared dependencies must be ordered into execution waves before any dispatch, including detecting a dependency cycle. |
| scheduler | Use when asked to set, list, pause, update, or delete a reminder or local task that fires at a confirmed time or interval. |
| show-me-your-work | Use when the user invokes it to append a structured decision record to an append-only TSV log, ending with an Attention section for reviewers. |
| size-the-run | Use when a run could be over- or under-powered, before dispatching a subagent, or the user asks how hard to think about a task. |
| watch-for | Use when monitoring a file, log, endpoint, or artifact for drift or errors, or polling a target until a predicate holds. |
| watch-for-harness-mode | Use when a proven watch pattern should become a reusable harness artifact with configurable inputs. |
| watch-for-structured | Use when the user wants to classify a surface state and page an on-call API when triggered. |
| wizard | Use when a human must perform steps only they can, such as provisioning infrastructure, entering credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
