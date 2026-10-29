# Solution doc templates

Pick the template for the `problem_type` track (see `references/schema.md`). Replace every bracketed placeholder. Delete sections with no real content instead of leaving placeholders. The template itself is not a record: run the validator only after all placeholders are replaced.

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
[The fix that worked, with code snippets when they carry weight]

## Why This Works
[Root cause, and why the fix addresses it, the WHY, not a restatement of the diff]

## Prevention
- [Concrete practice, test, or guardrail that stops a recurrence]

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
[The practice or recommendation, with code examples when useful]

## Why This Matters
[Rationale and impact of following, or not following, this]

## When to Apply
- [Conditions or situations where this applies]

## Examples
[Concrete before/after or usage example showing the practice in action]

## Related
[Related docs or issues, if any]
```

After assembling, run from the skill directory:

```bash
python3 scripts/validate-record.py docs/solutions/<category>/<slug>.md
```

A non-zero exit blocks publication. Quote any value containing `: ` or starting with a reserved indicator, then re-run until exit 0.
