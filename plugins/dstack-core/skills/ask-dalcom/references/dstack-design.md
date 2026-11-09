# DStack Design

DStack workflows for interface design, prototypes, and visual fidelity. Install it with `claude plugin install dstack-design@dstack` in Claude Code or `codex plugin add dstack-design@dstack` in Codex; Claude Code invokes its skills as `/dstack-design:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- Starting UI work or a design system: `/skill:design`; a raw idea that needs an approved design first: `/skill:design-gate-brainstorming`; a cheap sketch to settle a costly question: `/skill:prototype`.
- Building: `/skill:frontend-ui-engineering`; rebuilding to match a reference: `/skill:frontend-fidelity-rebuild`. Polish and proof: `/skill:final-grain` (user only), `/skill:ui-animation` (user only), `/skill:fixed-view-visual-benchmark` (user only), `/skill:thumbnail-accuracy-scorecard` (user only).
