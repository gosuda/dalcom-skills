---
name: developer-social-drafts
description: 'Use when drafting evergreen technical X and LinkedIn posts from the same evidence with distinct shapes. Not for scheduling, automation, DMs, or follower manipulation.'
disable-model-invocation: true
---

# Developer social drafts

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User supplies technical evidence and asks for social drafts for X, LinkedIn, or both. Scope is evergreen technical explainers; shipped-feature announcements belong to `release-promotion` and founder stories belong to `linkedin-ghostwriting`. |
| Authority | Read-only drafting in chat. X and LinkedIn are separate internal profiles. No DMs, scheduling, automation, follower buying, engagement pods, follow or unfollow campaigns, or unsourced reach or algorithm claims. |
| Side effect | Separately labeled drafts plus a claim and source ledger in chat. Nothing posted or scheduled. |
| Done | Each draft honors its profile, carries disclosure where required, includes at most one CTA where the venue supports it, is never a verbatim cross-post, and every technical claim traces to the ledger. |

## Not for

- Posting, scheduling, outreach, or growth hacking. The human ships; this skill drafts.

## Inputs

- `evidence` (required): the technical substance with sources (diff, docs, benchmark with method, or supplied writeup).
- `venues` (required): `x`, `linkedin`, or both.
- `angle` (optional): the one idea per post when the user wants a series. Defaults to one post per venue.

## Procedure

1. Fix one idea per post. Split multi-idea requests into a series. **Done when:** each draft has one idea.
2. Apply the venue profile. X: hook first, short technical thread only when more than one beat earns its line, visual code where it helps, plain language, 0 to 2 hashtags only where expected, no engagement automation. LinkedIn: professional context, engineering-manager relevance, personal framing without founder-story appropriation, warmer paragraph shape. **Done when:** each draft matches its profile and the two are not verbatim copies.
3. Lead with the reader outcome, not the build story. Cut throat-clearing, AI tells, and hype adjectives. **Done when:** the first line earns the next line on each venue.
4. Build the claim and source ledger: every technical claim beside its source. Mark unverified claims and either verify or remove them. **Done when:** no claim lacks a source or an explicit unverified flag resolved by removal.
5. Add disclosure where affiliation or sponsorship rules require it, and one CTA at most where the venue supports it. **Done when:** disclosure and CTA match venue norms with reasons.
6. Present drafts as labeled copy-pasteable blocks with a revision offer. **Done when:** each block is labeled, self-contained, and the revision offer is stated.

## Failure and recovery

- Evidence too thin for the claimed outcome: narrow the claim or name the missing proof; do not post-shape an unverified claim.
- Request is actually a shipped-feature announcement or founder story: route to `release-promotion` or `linkedin-ghostwriting` by name instead of drafting here.

## Output

Labeled X and LinkedIn drafts from the same evidence with distinct shapes, the claim and source ledger, disclosure and CTA notes, and a revision offer.
