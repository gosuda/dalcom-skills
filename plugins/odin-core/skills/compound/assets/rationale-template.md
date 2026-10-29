# Rationale template

Copy this template to `docs/solutions/rationale/<slug>.md`, replace every bracketed placeholder, and delete sections with no real content. The template itself is not a record: validate only after all placeholders are replaced.

```markdown
---
schema: odin-learning/v1
record_kind: rationale
date: [YYYY-MM-DD]
type: [pattern | caveat | reference | decision | concept | fix | lesson | workaround | incident | constraint]
confidence: [high | medium | low]
source: [session context, PR, issue, or codebase area]
tags:
  - [keyword-one]
  - [keyword-two]
status: [active]
evidence: [observed | corroborated | single-source | unknown]
retire_when: [condition that should trigger a revisit, or delete this line]
---

# [Short durable claim]

## Context
[What situation, decision, or failure produced this learning]

## Decision
[What was chosen]

## Rationale
[Why this won over the alternatives, grounded in the observed evidence]

## Rejected alternatives
[What was considered and the specific reason each lost; use unknown: when the reason was never established]

## Consequences
[What changes as a result: practice, guardrail, or follow-up]

## Verification
[How the outcome was observed to work]

## Related
[Related records or sources, if any]
```

After assembling, run from the skill directory:

```bash
python3 scripts/validate-record.py docs/solutions/rationale/<slug>.md
```

A non-zero exit blocks publication. `type: caveat` stays `caveat`; never convert it into another type to look more classified.
