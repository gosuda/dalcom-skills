---
name: developer-release-communication
description: 'Use when writing factual release notes or upgrade notices from a release diff or changelog. Not for promotional copy, commits, releases, or publishing.'
---

# Developer release communication

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User supplies a release diff, changelog, or explicit change list and asks for notes. |
| Authority | Read-only drafting in chat. No commit, release, publish, send, or invented performance result. |
| Side effect | Factual notes the user can hand to `release-promotion` for optional channel-shaped copy. Nothing shipped. |
| Done | Notes use Added, Changed, Deprecated, Removed, Fixed, Security sections; breaking changes carry impact and migration action; every claim traces to the diff or a supplied source with links. |

## Not for

- Promotional channel copy; that is `release-promotion`. This skill owns the factual record that promotion must stay consistent with.

## Inputs

- `changes` (required): release diff, changelog entry, or supplied change list with source links.
- `audience` (optional): operators, integrators, or end developers affected. Defaults to integrators when omitted.

## Procedure

1. Extract changes from the supplied diff or changelog only. **Done when:** every note item traces to a supplied line or link.
2. Sort into Added, Changed, Deprecated, Removed, Fixed, Security. Omit empty sections. **Done when:** no item sits in the wrong section.
3. For breaking changes, state impact (who breaks, how) and the migration action with commands or config where applicable. **Done when:** each breaking change has impact plus action.
4. Record deprecations with timeline and replacement, removals with last-supported version, security fixes with severity and upgrade urgency. **Done when:** each carries its required field or an explicit unknown.
5. Verify against invention: no performance result, adoption claim, or cause that the diff does not show. **Done when:** every claim has a trace and every gap is marked.

## Failure and recovery

- Diff ambiguous: present both readings with the question for the author; do not pick one silently.
- No supplied source: stop and ask; do not reconstruct changes from memory.

## Output

Factual release notes with the six sections, breaking-change impacts and migration actions, source links per claim, and the verification note.
