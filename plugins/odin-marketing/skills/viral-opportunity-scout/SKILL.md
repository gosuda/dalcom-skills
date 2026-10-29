---
name: viral-opportunity-scout
description: 'Use when asked to find distribution opportunities for a template, tool, or artifact. Not for content creation, campaign management, or paid placement.'
disable-model-invocation: true
---

# Viral opportunity scout

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to find where a template, tool, or artifact can be distributed through niche or high-impact channels. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, submitted, posted, or remote mutation. Public official documentation reads and web search only; no social-post scraping. |
| Side effect | Emits a chat report. No external state, credential use, or artifact mutation. |
| Done | A ranked report of distribution opportunities with fit, entry barrier, submission rationale, cited reach or explicit unknown, evidence-backed fit, entry policy, unresolved evidence, and the user decision, for each channel. |

## Not for

- Content creation, campaign management, posting, submission, or paid placement execution.

## Inputs

- `artifact` (required): the template, tool, or artifact to scout, as text description or verbatim content.
- `target_audience` (optional): comma-separated audience descriptors. Narrows channel mapping.
- `channels` (optional): restrict scouting to `community`, `platform`, `editorial`, `aggregator`, `offline`, or `social`. Scouts all families when omitted.

## Procedure

1. Classify the artifact. If the user supplied a type, use it. Otherwise infer: executable code, CLI, or API is `tool`; fill-in fields or placeholders is `template`; short copy-pasteable code is `snippet`; packaged code with imports and public API is `library`; prose or structured documentation is `article`; slide format is `deck`; audio or video content is `video`; tabular or structured data is `dataset`; agent workflow, harness, or scaffold is `agent-harness`; none of the above is `unknown`. **Done when:** the artifact type is determined.
2. Query known directories and aggregator platforms per in-scope family. Verify each platform is live and public through official docs or current search results. Social-platform research uses official public policy or metadata pages or user-supplied evidence, never scraped feeds. **Done when:** every in-scope family is queried and each candidate is confirmed live or skipped with a reason.
3. Filter for active communities. Confirm recent activity (posts or submissions within the last 90 days) and public submission access (no invite-only or closed communities). Skip failures with named reasons. **Done when:** every candidate is validated or skipped with a named reason.
4. Score each validated channel: `reach` (1 to 5) with a cited current authorized source for the band, or `unknown` when no such source exists; `fit` (1 to 5) with the evidence behind it; `priority = reach * fit` only when reach is cited, otherwise rank by fit and mark priority provisional; `entry_barrier` (low, medium, high) with the entry policy cited. Write a one-sentence submission rationale. **Done when:** every validated channel has reach (cited or unknown), evidence-backed fit, barrier with policy, and rationale.
5. Compile the ranked report. Separate evidence-backed fit, entry policy, estimated reach, unresolved evidence, and the user decision. Present recommendations first, then secondary opportunities, then skipped families with reasons. **Done when:** the report distinguishes what is proven, what is unknown, and what the user must decide.

## Failure and recovery

- No artifact supplied: stop. Report the failure and do not produce a partial report.
- No viable channels found: return a non-converged result with the artifact classification and a statement that no matching channels were validated. The done predicate is not satisfied.
- Partial validation: include only validated channels. Do not infer or fabricate unvalidated opportunities. Flag any family where validation was skipped.

## Output

A structured scout report with artifact summary, channel opportunities grouped by family (each with reach cited or unknown, evidence-backed fit, priority, entry barrier with policy citation, submission rationale), recommendations, secondary opportunities, unresolved evidence, and notes on skipped families.
