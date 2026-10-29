---
name: developer-discovery-surfaces
description: 'Use when auditing GitHub presence or preparing curated directory submission packets for a developer tool. Not for star manipulation, automated PRs, or directory spam.'
---

# Developer discovery surfaces

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User names a repository, tool, or package and asks for discovery review or directory readiness. |
| Authority | Read-only audit in chat, plus submission packets the human submits. GitHub and curated directories are distinct surface profiles. No star or follow manipulation, automated PR submission, listing submission, directory spam, or analytics credential. |
| Side effect | An audit plus per-directory packets in chat. Nothing submitted. |
| Done | Repository facts are accurate, README and topic recommendations trace to observed gaps, each directory packet has unique descriptions and meets current contribution rules, and a maintenance ledger states recheck duties. |

## Not for

- Submitting listings, opening directory PRs, or gaming signals. The human submits; this skill prepares.

## Inputs

- `repo` (required): the repository or package under review with its actual current state.
- `directories` (optional): candidate curated directories or registries. Defaults to proposing candidates from public awesome-lists and registries relevant to the artifact.

## Procedure

1. Audit the repository: README completeness, quickstart that runs, topics, description, license clarity, contributing path, issue and PR responsiveness signs. **Done when:** each item cites the observed state.
2. Recommend GitHub improvements: description, topics, README structure, pinned material, profile placement where relevant. **Done when:** each recommendation names the gap it closes.
3. For each candidate directory, check current contribution rules (cited URL and date): fit, uniqueness requirements, description constraints, maintenance expectations. **Done when:** every candidate has a rules check or an explicit unknown.
4. Write per-directory submission packets with unique descriptions (never the same blurb everywhere), correct category placement, and required metadata. **Done when:** each packet meets its venue rules and differs from the others.
5. Open the maintenance ledger: who rechecks what, on which trigger (release, rule change, quarterly). **Done when:** every packet has a recheck trigger.

## Failure and recovery

- Repository facts unavailable: audit the visible surface and mark the rest unknown.
- Directory rules forbid the listing type: drop the candidate with the reason; do not reframe to evade rules.

## Output

A discovery audit with cited observations, GitHub recommendations, per-directory submission packets with unique descriptions, rules citations, and the maintenance ledger.
