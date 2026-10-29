# ADR format

## Location and numbering

- Keep the project existing ADR directory, filename scheme, numbering, and headings. Continue its sequence.
- When no ADR convention exists, store ADRs in `docs/decisions/` as `ADR-NNNN-short-slug.md`, starting at `ADR-0001`, with the title `# ADR-NNNN: Short title` inside.
- Create the directory lazily at the first qualifying ADR. Never delete or renumber an ADR file.

## Gate

Write an ADR only when all three hold:

1. **Hard to reverse.** The cost of changing course later is meaningful.
2. **Surprising without context.** A future reader will wonder why it was done this way.
3. **The result of a real tradeoff.** Genuine alternatives existed, and one was picked for specific reasons.

If any condition is missing, skip the ADR and record the reason.

## Template

```markdown
# ADR-NNNN: Short title of the decision

## Status
Accepted

## Date
YYYY-MM-DD

## Context
What problem or force makes this decision necessary. Key requirements and constraints.

## Decision
What was decided, stated plainly.

## Alternatives Considered

### Option name
- Pros: why it was attractive.
- Cons: why it was rejected.

## Consequences
Non-obvious downstream effects: what this enables, what it forecloses, what the team must now know or operate.
```

Status, Alternatives Considered, and Consequences are optional per record: include them only when they add value, but Context and Decision are always present. A short ADR may be a single paragraph of context, decision, and reason; the value is recording that a decision was made and why, not filling out sections.

## Decisions that usually qualify

- Architectural shape, such as monorepo layout or an event-sourced write model with a projected read model.
- Integration patterns between contexts, such as domain events instead of synchronous calls.
- Technology choices that carry lock-in: database, message bus, auth provider, deployment target. Not every library, only swaps that take sustained effort.
- Boundary and scope decisions, including explicit no-statements about which context owns what.
- Deliberate deviations from the obvious path, such as manual SQL instead of an ORM for stated reasons.
- Constraints not visible in the code, such as compliance or latency contracts.
- Rejected alternatives whose rejection is non-obvious and will otherwise be re-proposed.

## Lifecycle

```
PROPOSED -> ACCEPTED -> (SUPERSEDED or DEPRECATED)
```

- Keep old ADRs; they capture historical context.
- When a decision changes, write a new ADR that references and supersedes the old one, and mark the old Status accordingly.
