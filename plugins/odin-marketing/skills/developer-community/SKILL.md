---
name: developer-community
description: 'Use when designing developer community operations including platform choice, moderation, and health metrics. Not for creating servers, inviting members, or automated outreach.'
---

# Developer community

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks for a community plan, channel map, moderation model, or health review. |
| Authority | Read-only planning in chat. Platform profiles may cover Discord, Slack, GitHub Discussions, and Discourse without becoming separate skills. No server creation, invites, bot setup, member pinging, or automated outreach. |
| Side effect | A community operating brief in chat. No community state changes. |
| Done | Platform decision with reasons, channel map, onboarding path, code of conduct, moderation matrix, escalation path, and health metrics are present; no creation, invitation, or automation step is included. |

## Not for

- Running the community, moderating members, or contacting anyone. Operations stay human; this skill designs the operating brief.

## Inputs

- `purpose` (required): what the community exists to do for developers.
- `scale` (optional): current size and moderation capacity. Defaults to a small volunteer-run group when omitted.
- `constraints` (optional): platform limits, brand rules, or staffing the user names.

## Procedure

1. Decide platform from purpose and capacity, comparing the candidate surfaces on threading, search, discoverability, and moderation cost. **Done when:** the choice names its reasons and the rejected options with reasons.
2. Draw the channel map: purpose per channel, what belongs where, archive policy. **Done when:** each channel has a purpose and a misplacement rule.
3. Write the onboarding path: first visit to first contribution, with the exact links and docs a newcomer needs. **Done when:** the path is walkable from the stated entry point.
4. Set the code of conduct, moderation matrix (violation classes with responses), and escalation path (moderator to maintainer to legal where relevant). **Done when:** each violation class has a response and an escalation endpoint.
5. Define health metrics from observable behavior (response time the team can already measure, repeat contributors, resolved-question rate). **Done when:** each metric names its existing measurement source; no metric needs a new credential.
6. Purge automation: bots, scheduled prompts, and outreach sequences appear only as explicitly human-approved future options, never as embedded steps. **Done when:** no automated action is prescribed.

## Failure and recovery

- Capacity insufficient for the ambition: cut scope to what the stated moderators can run, and name the cut.
- Platform decision blocked on unknown policy: mark it unknown with the policy question, do not guess.

## Output

A community operating brief: platform decision, channel map, onboarding path, code of conduct, moderation matrix, escalation path, health metrics, and staffing assumptions.
