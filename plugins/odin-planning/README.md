# ODIN Planning

ODIN workflows for shaping intent into approved plans, specs, and task lists.

39 skills, category Productivity. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add OutlineDriven/odin-claude-plugin
/plugin install odin-planning@odin-marketplace

# Codex
codex plugin marketplace add OutlineDriven/odin-claude-plugin
codex plugin add odin-planning@odin-marketplace
```

### Individual (gh skill)

```shell
gh skill install OutlineDriven/odin-claude-plugin plugins/odin-planning/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/odin-planning:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| abstract-well | Use when the user wants to classify abstractions as useful, bad, or busy and keep one shallow level. |
| attack-shape | Use when the user wants adversarial stress-testing of a proposed architecture, structure, or shape. |
| bakeoff | Use when choosing well needs developing competing solutions to a defined brief beyond their current form. |
| brainstorm | Use when capturing or refining notes, a transcript, a brain dump, or an existing idea, or when a concrete visual question is clearer shown in a local browser. |
| council | Use when the user asks for a council, second opinions, or parallel investigation. |
| cross-critique | Use when independent proposals on a contested decision need cross-critique before choosing, reusing the original authors. |
| cross-lens-converge | Use when one reviewer is not enough because failure modes are heterogeneous, or a claim needs cross-lens pressure before it ships. |
| decide | Use when the user has a fork and wants it resolved and applied, not explored: "decide this", "choose the path", or "decide and fix it". |
| decision-rationale-gaps | Use when a current decision needs pressure-testing until the rationale is clear to a skeptic. |
| define-goalstate | Use when the user wants the finished-system contract for a piece of work: behavior, protocols, allowed, forbidden, and impossible states with a state-space proof. |
| doubt-driven | Use when a non-trivial decision sits under uncertainty and correctness matters more than speed. |
| frame | Use when a vague or ambitious product idea needs framing into a right-sized requirements-only plan before implementation. |
| from-first-principle | Use when a user wants to rebuild a design, organization, or API from primitives. |
| from-perspective | Use when an answer is wanted from one named seat only: breaking, business, career, codebase, human, impact, innovation, moat, rent-seeking, skeptic, or stability. |
| generalize | Use when asked to derive the general rule a request carries as examples instead of a stated rule, then bound it. |
| graph-backbone | Use when defining, revising, or gate-replanning the project structural backbone in project-root graph.yaml. |
| ideate-multiple-agents | Use when the user wants divergent ideas or an independently generated candidate pool grounded in the working repository. |
| influence-and-negotiation | Use when an agreement-seeking interaction arises, including mid-conversation moments the model detects. |
| leave-only-first-principle | Use when asked to prune a design or codebase until only primitives remain, producing a first-principles map. |
| let-fate-decide | Use when the user says let fate decide, YOLO, dealer choice, surprise me, whatever, or delegates a vague choice in a casual or playful tone, or when you are about to pick arbitrarily between valid options. |
| load-bearing-assumption-test | Use when the user asks why a plan is wrong or says "poke holes in this". |
| loop-me | Use when the user says "loop me" or asks to design a recurring workflow. |
| minimap | Use when the user needs a compact read-only current-work view from Git state, recorded test evidence, and optional graph.yaml. |
| plan | Use when multi-step work needs a structured implementation plan that preserves outcomes and constraints. |
| possible-worlds | Use when a design dispute has at least two live interpretations and the caller wants worlds made explicit or a plain-language recommendation. |
| pov | Use when a supplied question, document, or approach set needs a project-grounded judgment with attribution. |
| prism | Use when one reviewer angle is insufficient or the user suspects a direction is tunnel-visioned or inherited its framing. |
| punishing-practices | Use when a workflow, plan, diff, or completed work cycle must be checked for practices that punish the project later. |
| readiness-assessment | Use when a user asks for a gut-check on a decision or action, or asks whether enough is known to proceed. |
| spec-driven | Use when starting a project or feature, requirements are unclear, or a change crosses modules. |
| state-machine-workflow | Use when work has distinct modes and the user wants states, events, guards, outcomes, illegal transitions, not a prose todo list. |
| taste | Use when asking "overkill?", "elegant?", "audit", or "taste-test this", or setting a taste register. |
| tasty-abstraction | Use when a user wants to design an abstraction boundary that collapses a complex implementation into a simpler interface without leaking internal state. |
| to-spec | Use when settled conversation decisions need synthesis into an agent-ready implementation spec, stopping before publication. |
| to-tickets | Use when a settled plan needs implementation tickets published as blocker-linked slices, tracer bullets, or expand-contract sequencing. |
| todo-add | Use when a message contains `TODO ADD: <requirement>`. |
| todos-enhance | Use when tasks are too vague, read as headings, or the user asks to sophisticate the todos. |
| todos-update | Use when user asks to update todos, resync the task list, say what to do next, or plan and tree have drifted apart. |
| wayfinder | Use when a greenfield project or large feature build will not fit in a single agent session and the route must be charted as decision tickets first. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
