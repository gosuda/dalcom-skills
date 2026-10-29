# Solution doc templates

Pick the template for the `problem_type` track (see `references/schema.md`). Each doc records one generalized, well-abstracted invariant: a reusable mechanism (never an incident, project name, command, version, or path) with stated supported scope, actual enforcement or proof, and a material consequence (prevents a plausible significant failure or improves a recurring decision). Tiny one-off fixes, trivia, and session history never qualify; no non-trivial-fix shortcut; no speculative universal truths. Replace every bracketed placeholder. Delete sections with no real content instead of leaving placeholders. Never add, rename, or drop frontmatter fields: the stored `odin-learning/v1` shape is fixed. The template itself is not a record: run the validator only after all placeholders are replaced.

## Bug track

For: `build_error`, `test_failure`, `runtime_error`, `performance_issue`, `database_issue`, `security_issue`, `ui_bug`, `integration_issue`, `logic_error`

```markdown
---
schema: odin-learning/v1
record_kind: solution
date: [YYYY-MM-DD]
title: [Clear problem title]
category: [directory basename from the schema category map]
module: [Module or area]
problem_type: [schema enum]
component: [component or subsystem]
severity: [critical | high | medium | low]
symptoms:
  - [Observable symptom 1]
root_cause: [schema enum]
resolution_type: [schema enum]
tags:
  - [keyword-one]
---

# [Clear problem title]

## Problem
[1-2 sentences: the issue and its user-visible impact]

## Symptoms
- [Observable symptom or error]

## What Didn't Work
- [Attempted fix and why it failed]

## Solution
[The fix that worked, with code snippets when they carry weight. State the generalized mechanism with its supported scope, never the incident retelling and never broader than the evidence.]

## Why This Works
[The mechanism, its enforcement or proof, and the material fault consequence if violated. The WHY, not a restatement of the diff and not a fixture snapshot.]

## Prevention
- [Concrete reusable guardrail, check, or test that enforces the invariant and stops a recurrence]

## Related
- [Related docs or issues, if any]
```

## Knowledge track

For: `best_practice`, `documentation_gap`, `workflow_issue`, `developer_experience`, `architecture_pattern`, `design_pattern`, `tooling_decision`, `convention`

```markdown
---
schema: odin-learning/v1
record_kind: solution
date: [YYYY-MM-DD]
title: [Clear, descriptive title]
category: [directory basename from the schema category map]
module: [Module or area]
problem_type: [schema enum]
component: [component or subsystem]
severity: [critical | high | medium | low]
applies_when:
  - [Condition where this applies]
tags:
  - [keyword-one]
---

# [Clear, descriptive title]

## Context
[What situation, gap, or friction prompted this guidance]

## Guidance
[The invariant mechanism as a reusable practice, with code examples when useful. Never an incident, project name, command, version, or path.]

## Why This Matters
[Material rationale: the plausible significant failure prevented or the recurring decision improved by following this]

## When to Apply
- [Supported scope where this applies, no broader than the evidence]

## Examples
[Concrete reusable input or setup showing the practice in action, not a session log]

## Related
[Related docs or issues, if any]
```

After assembling, run from the skill directory:

```bash
python3 scripts/validate-record.py docs/solutions/<category>/<slug>.md
```

A non-zero exit blocks publication. Quote any value containing `: ` or starting with a reserved indicator, then re-run until exit 0.
