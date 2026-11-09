# DStack Planning

DStack workflows for shaping intent into approved plans, specs, and task lists. Install it with `claude plugin install dstack-planning@dstack` in Claude Code or `codex plugin add dstack-planning@dstack` in Codex; Claude Code invokes its skills as `/dstack-planning:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- A vague or ambitious product idea: `/skill:frame` sizes it into a requirements-only plan, then core `/skill:askme` takes over.
- A finished-system contract of allowed, forbidden, and impossible states: `/skill:define-goalstate`. Work with distinct modes and illegal transitions: `/skill:state-machine-workflow`.
- Choosing between options: `/skill:gut-check` when you only need to know whether enough is known, `/skill:possible-worlds` when a dispute has two live readings, `/skill:bakeoff` to build competing solutions to one brief, `/skill:ideate-multiple-agents` for a divergent candidate pool, `/skill:council` for second opinions, `/skill:cross-critique` to let independent proposals critique each other, `/skill:cross-lens-converge` (user only) when failure modes differ by lens, `/skill:prism` when one angle feels tunnel-visioned, and `/skill:from-perspective` for one named seat.
- Pressure on a decision already made: `/skill:decision-rationale-gaps`; on a plan's long-term cost: `/skill:punishing-practices`; on overkill: `/skill:taste`.
- Maps of the work: `/skill:minimap` for a compact current-work view from Git state, `/skill:graph-backbone` for the project graph, `/skill:automatic-freeform-graphs-design` for a looser exploratory graph. `/skill:influence-and-negotiation` (user only) handles agreement-seeking conversations.
