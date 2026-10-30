# DStack Learn

DStack workflows for teaching, explaining, drilling, and onboarding.

8 skills, category Productivity. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-learn@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-learn@dstack
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-learn/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-learn:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| capstone | Use when the learner is ready to apply cleared concepts in a real project. |
| explain-concept | Use when a concept needs making clear rather than practising: explain simply, why does this exist, draw it, or simplify for a beginner. |
| explainer-artifact | Use when asked to create an explainer document for a concept, diff, idea, or work recap. |
| learning-retrospective | Use when asked to review learning progress after a milestone. |
| map-corpus | Use when the user points to a study-material folder and asks to make it teachable. |
| onboard | Use when the user asks for onboarding, orientation, a repository tour, or where to start. |
| teach | Use when the user wants a course, a learning workspace, or ongoing teaching across sessions, with cited lessons and retention-gated advancement. |
| wait-what | Use when the user says "wait, what", "the explanation is unclear", "say that again", or asks to restate the last response in plain language. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
