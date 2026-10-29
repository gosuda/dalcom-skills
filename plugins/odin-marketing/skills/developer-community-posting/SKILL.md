---
name: developer-community-posting
description: 'Use when preparing a Hacker News or Reddit post package with eligibility, disclosure, and do-not-post conditions. Not for posting, replying, voting, or account activity.'
disable-model-invocation: true
---

# Developer community posting

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User names the target venue (Hacker News or a specific subreddit) and the technical material to prepare. |
| Authority | Read-only preparation. HN and Reddit are separate internal profiles with genuinely different rules that are never flattened. No post, reply, vote, upvote request, account creation, alternate account, ring, astroturf, or moderator circumvention. Drafts never leave chat without explicit target and content consent, and consent to draft is never consent to post. |
| Side effect | A venue-specific preparation package in chat. Nothing posted or voted. |
| Done | Eligibility and risk check, title, body, first-comment guidance, response guidance, disclosure line, and do-not-post conditions are present; every conduct rule below is honored; no posting action was taken. |

## Not for

- Posting, replying, voting, or managing accounts. The human posts; this skill prepares.

## Inputs

- `venue` (required): `hacker-news` or `reddit:<subreddit>`.
- `material` (required): the technical substance (launch, Show-style demo, question, or technical writeup) with sources.
- `standing` (optional): the poster account history the user discloses (age, prior participation). Used only for eligibility risk, never improved by automation.

## Procedure

1. Run the eligibility and risk check against current venue rules (cited URLs, observation dates): account standing, venue fit, prior-post history, duplicate or merge-bait risk, moderator-edit expectations. State do-not-post conditions plainly. **Done when:** the check cites current rules and ends in proceed-with-risk or do-not-post.
2. Apply the venue profile. Shared: human voice, technical specifics, affiliation disclosure, no duplicate posts, creator available to answer as a human task. HN profile: no upvote asks, no voting rings, no multiple-account voting, no astroturf, title states the technical substance, first comment adds substance the page lacks. Reddit profile: subreddit rules read and cited, comment-first history honored, disclosure in post or flair as the rules require, no vote manipulation, no alternate accounts, cross-posts tailored per community with separate risk notes. **Done when:** the draft follows the selected profile and the other profile rules are not mixed in.
3. Draft title, body, and first-comment substance (what to add beyond the link, not a verbatim script to paste blindly). **Done when:** each part exists and matches venue shape and length norms with reasons.
4. Write response guidance: which questions the human answers, which to decline, how to handle corrections and moderator edits. **Done when:** guidance covers corrections, hostile threads, and moderator actions.
5. Write the disclosure line the human uses. **Done when:** affiliation is disclosed in the venue-required place.
6. Close with the human-action checklist: who posts, from which standing account, when the human decides, and the explicit reminder that no agent action posts. **Done when:** every outward step names a human actor.

## Failure and recovery

- Do-not-post conditions met (duplicate, rule mismatch, standing risk, astroturf pressure): stop with the reasons; do not reframe the package to evade rules.
- Venue rules unavailable: mark unknown, do not proceed on lore, timing myths, karma ladders, or algorithm claims.

## Output

A preparation package: eligibility verdict with cited rules, title, body, first-comment guidance, response guidance, disclosure line, do-not-post conditions, and the human-action checklist.
