# DStack Learn

DStack workflows for teaching, explaining, drilling, and onboarding. Install it with `claude plugin install dstack-learn@dstack` in Claude Code or `codex plugin add dstack-learn@dstack` in Codex; Claude Code invokes its skills as `/dstack-learn:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- A new repository: `/skill:onboard` for orientation and where to start.
- A concept: `/skill:explain-concept` explains one concept in one reply. It needs only the concept; the angle is optional, and it cites a `CORPUS.md` from `/skill:map-corpus` when one exists, otherwise it asks once which source to ground in. `/skill:wait-what` restates the last answer in plain words.
- A course from study material: `/skill:map-corpus` makes a folder teachable, `/skill:teach` (user only) runs the sessions, `/skill:capstone` (user only) applies cleared concepts in a project, `/skill:learning-retrospective` reviews progress, and `/skill:explainer-artifact` (user only) writes an explainer document.
