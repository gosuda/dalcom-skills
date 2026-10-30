# Workflows

Most campaigns below share one shape: open by clarifying or planning (*explicitly* in **plan mode** with `/askme` or `/architect` or *implicitly* with `/wayfinder` or `/autoplan`), steer with short corrections rather than restated requirements, and close with a pass over what was left behind before you call anything done. The mined work spans a Rust Bitcoin node, two greenfield Rust ports, a harness port, and this marketplace itself; map your own work onto the closest shape.

Chains are written in the harness-neutral form `/skill:<slug>`. Type each step as your harness spells it: `/<plugin>:<slug>` in Claude Code, `$<slug>` in Codex, or `/` and the skill name in Cursor; [using-skills.md](using-skills.md) has the table.

| Workflow | Chain | When not to use it |
|---|---|---|
| Clarify an ambiguous request, then plan (usually inside harness plan mode) | `/skill:askme` → `/skill:plan` or `/skill:autoplan` → `/skill:todo-add` → `/skill:todos-enhance` | The request already states sharp acceptance criteria and fits one session. |
| Plan a build that outgrows one session (usually when working without plan mode) | `/skill:wayfinder` → `/skill:todo-add` → `/skill:todos-update` | One agent finishes the work in one session with no handoff. |
| Execute the plans or tasks with subagents (daily execution driver after the planning phases) | `/skill:subagent-driven` → `/skill:verification-before-completion` | The plan fits one agent, and delegation costs more than it saves. |
| Fan out independent work | `/skill:parallel-launch` → `/skill:do-it-now`, or `/skill:diamond-task` when one change is too large to split by worker | The tasks share mutable state or must run in a strict order. |
| Re-derive a bloated module from scratch | `/skill:minimalism-driven` ↔ `/skill:breaking-driven` → `/skill:refactor-break-compat` → `/skill:architect` | A focused patch fixes the defect without touching the structure. |
| Ground an unfamiliar or outdated stack knowledge (from LLM itself) to latest solid ground before writing code | `/skill:research` → `/skill:ground-latest` → `/skill:source-driven` | You already know the stack and its current version. |
| Use when agents **should** do same as user's intent, make the result match to every shape in user's directed specifications | `/skill:exhaustive` → `/skill:validation-first-driven` → `/skill:tests-purge-unneeded` | No contract exists yet, as in an early exploratory spike. |
| Run a clean **documentation** pass | `/skill:good-readme` → `/skill:docs-writing` → `/skill:sync-docs` → `/skill:unslop` → `/skill:purge-slop-docs` | One file changed and no index or guide points at it. |
| Author a new **skill** | `/skill:skill-gap-finder` → `/skill:writing-for-agents` → `/skill:unslop` → `/skill:humanizer-simple-english-asd-ste100` → `/skill:taste` | The skill index already holds a skill that covers the job. |

## Example workflow invocations
Install the plugins for these workflows from the `dstack` marketplace added from `gosuda/dalcom-skills`:

```shell
claude plugin marketplace add gosuda/dalcom-skills
claude plugin install dstack-core@dstack
claude plugin install dstack-planning@dstack
claude plugin install dstack-code@dstack
claude plugin install dstack-run@dstack
claude plugin install dstack-knowledge@dstack
```

In Claude Code, invoke workflow steps using each plugin's verified namespace:

- Clarify, plan, and refine: `/dstack-core:askme` → `/dstack-core:plan` → `/dstack-core:todo-add` → `/dstack-core:todos-enhance`
- Map structure and options: `/dstack-planning:minimap`
- Structural AST edits: `/dstack-code:ast-grep`
- Execute with subagents: `/dstack-core:subagent-driven` → `/dstack-core:verification-before-completion`
- Partition large issues: `/dstack-run:diamond-task`
- Sync mental models: `/dstack-knowledge:mutual-sync`
