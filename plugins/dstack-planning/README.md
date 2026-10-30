# DStack Planning

DStack workflows for shaping intent into approved plans, specs, and task lists.

19 skills, category Productivity. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-planning@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-planning@dstack
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-planning/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-planning:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| automatic-freeform-graphs-design | Use when a user wants a looser conceptual graph for exploratory work. |
| bakeoff | Use when choosing well needs developing competing solutions to a defined brief beyond their current form. |
| council | Use when the user asks for a council, second opinions, or parallel investigation. |
| cross-critique | Use when independent proposals on a contested decision need cross-critique before choosing, reusing the original authors. |
| cross-lens-converge | Use when one reviewer is not enough because failure modes are heterogeneous, or a claim needs cross-lens pressure before it ships. |
| decision-rationale-gaps | Use when a current decision needs pressure-testing until the rationale is clear to a skeptic. |
| define-goalstate | Use when the user wants the finished-system contract for a piece of work: behavior, protocols, allowed, forbidden, and impossible states with a state-space proof. |
| frame | Use when a vague or ambitious product idea needs framing into a right-sized requirements-only plan before implementation. |
| from-perspective | Use when an answer is wanted from one named seat only: breaking, business, career, codebase, human, impact, innovation, moat, rent-seeking, skeptic, or stability. |
| graph-backbone | Use when defining, revising, or gate-replanning the project structural backbone in project-root graph.yaml. |
| gut-check | Use when a user asks for a gut-check on a decision or action, or asks whether enough is known to proceed. |
| ideate-multiple-agents | Use when the user wants divergent ideas or an independently generated candidate pool grounded in the working repository. |
| influence-and-negotiation | Use when an agreement-seeking interaction arises, including mid-conversation moments the model detects. |
| minimap | Use when the user needs a compact read-only current-work view from Git state, recorded test evidence, and optional graph.yaml. |
| possible-worlds | Use when a design dispute has at least two live interpretations and the caller wants worlds made explicit or a plain-language recommendation. |
| prism | Use when one reviewer angle is insufficient or the user suspects a direction is tunnel-visioned or inherited its framing. |
| punishing-practices | Use when a workflow, plan, diff, or completed work cycle must be checked for practices that punish the project later. |
| state-machine-workflow | Use when work has distinct modes and the user wants states, events, guards, outcomes, illegal transitions, not a prose todo list. |
| taste | Use when asking "overkill?", "elegant?", "audit", or "taste-test this", or setting a taste register. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
