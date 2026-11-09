# DStack Review

DStack workflows for reviewing diffs, branches, and implementations against their specs. Install it with `claude plugin install dstack-review@dstack` in Claude Code or `codex plugin add dstack-review@dstack` in Codex; Claude Code invokes its skills as `/dstack-review:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- Everyday diff review is core `/skill:code-review`. A deeper pull request or merge request review with standard and depth modes: `/skill:review`.
- To see the findings: `/skill:show-review` walks through them one by one; `/skill:visual-diff-review` builds a seven-section visual page.
- Adversarial passes: `/skill:interrogate` (user only) across models, `/skill:perspective-complete-review` (user only) for one viewpoint until a fresh reviewer finds nothing, `/skill:no-hide` for clever concealment. `/skill:pr-impact-quiz` (user only) checks that the author understands the change.
