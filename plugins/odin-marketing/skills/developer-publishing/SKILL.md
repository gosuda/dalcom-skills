---
name: developer-publishing
description: 'Use when adapting a finished technical draft for Dev.to or Hashnode with correct canonical and metadata handling. Not for account creation, publication, or scheduling.'
disable-model-invocation: true
---

# Developer publishing

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User supplies a finished draft and names Dev.to, Hashnode, or both as adaptation targets. |
| Authority | Read-only adaptation pack in chat. Dev.to and Hashnode are separate internal profiles. No account creation, publication, scheduling, follower manipulation, or canonical-URL change. |
| Side effect | An adaptation pack the human applies. Nothing published. |
| Done | Canonical ownership is stated, per-platform metadata agrees with content, series placement and content differences are explicit, and no factual drift between versions remains. |

## Not for

- Publishing, distributing, or managing publications. The human publishes; this skill prepares the pack.

## Inputs

- `draft` (required): the finished technical draft with its canonical home URL.
- `targets` (required): `dev-to`, `hashnode`, or both.
- `metadata` (optional): existing tags, series, or custom-domain facts the user supplies.

## Procedure

1. Fix canonical ownership: state the canonical URL and require it recorded on every syndicated copy. Never change canonical as part of adaptation. **Done when:** canonical is stated and every target pack references it.
2. Apply the Dev.to profile: frontmatter fields, tag selection within venue limits, series placement, cover and description rules per current venue docs. **Done when:** each Dev.to field is filled or marked venue-default with the doc cited.
3. Apply the Hashnode profile: article settings, tags, series, custom-domain behavior per current venue docs. **Done when:** each Hashnode setting is filled or marked venue-default with the doc cited.
4. State content differences honestly: what is trimmed, expanded, or reformatted per venue and why, with no factual drift between versions. **Done when:** every difference names its reason and factual parity is confirmed.
5. Verify metadata and content agreement: titles, descriptions, tags, and code match the draft or the difference is named. **Done when:** no silent drift remains.

## Failure and recovery

- Canonical home missing: stop and ask; do not syndicate an orphan.
- Venue docs unavailable for a setting: mark venue-default-unknown with the question, do not guess.

## Output

An adaptation pack per target: canonical statement, metadata fields with cited venue docs, series placement, content differences with reasons, and the parity verification note.
