# DStack Marketing

DStack workflows for marketing and viral growth, from audience research to opportunity scouting.

28 skills, category Marketing. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-marketing@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-marketing@dstack

# Hermes Agent
hermes plugins install gosuda/dalcom-skills/plugins/dstack-marketing --enable
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-marketing/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-marketing:<name>` in Claude Code, `$<name>` in Codex, `dstack-marketing:<name>` in Hermes Agent, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| buzzword-hijack | Use when a user wants to choose and execute a bounded positioning move that rides a jargon wave. |
| competitive-content | Use when preparing an honest alternative or comparison page brief or draft from source-backed claims. |
| competitive-intelligence | Use when mapping the competitive landscape and battlecards for a developer product from authoritative sources. |
| content-evidence-brief | Use when designing a long-form marketing or developer content piece from a source pack before drafting. |
| developer-advocacy | Use when preparing a conference talk, workshop, demo, podcast appearance, or building-in-public brief. |
| developer-audience-context | Use when grounding developer marketing in a confirmed audience profile of persona, pains, alternatives, and trust signals. |
| developer-champion-programs | Use when designing a consent-aware advocate or champion program with qualification, benefits, and opt-in records. |
| developer-community | Use when designing developer community operations including platform choice, moderation, and health metrics. |
| developer-community-posting | Use when preparing a Hacker News or Reddit post package with eligibility, disclosure, and do-not-post conditions. |
| developer-content | Use when preparing an evidence-backed developer content package with runnable examples and accuracy checks. |
| developer-discovery-surfaces | Use when auditing GitHub presence or preparing curated directory submission packets for a developer tool. |
| developer-docs-led-growth | Use when auditing docs or planning quickstart and API-reference improvements that drive acquisition and activation. |
| developer-lifecycle-messaging | Use when drafting consent-segmented newsletter, onboarding, activation, or re-engagement messages from real product behavior. |
| developer-listening | Use when collecting dated per-conversation evidence from public developer discussions to triage opportunities. |
| developer-publishing | Use when adapting a finished technical draft for Dev.to or Hashnode with correct canonical and metadata handling. |
| developer-release-communication | Use when writing factual release notes or upgrade notices from a release diff or changelog. |
| developer-search | Use when mapping technical search opportunities by exact query, intent, and source evidence. |
| developer-social-drafts | Use when drafting evergreen technical X and LinkedIn posts from the same evidence with distinct shapes. |
| developer-utility-growth | Use when designing a free tool or ungated resource brief for developer acquisition. |
| developer-video | Use when preparing a developer video script, storyboard, demo runbook, and accessibility checklist. |
| marketing-assumption-grill | Use when pressure-testing one marketing decision, idea, or plan before committing. |
| marketing-behavior-audit | Use when diagnosing observed buyer or market behavior with evidence before changing copy, offer, or interface. |
| marketing-decision-map | Use when a marketing initiative is too broad for a brief and needs its decisions charted before action. |
| offer-page-brief | Use when designing an evidence-led offer or comparison page from confirmed facts before writing final copy. |
| open-source-adoption | Use when planning open-source adoption through README quality, contributor funnel, and sustainable maintenance. |
| release-promotion | Use when asked to draft launch or promotion copy for a shipped feature across channels via /release-promotion. |
| social-sentiment | Use when the user asks for a weekly sentiment report, weekly social summary, or how mentions looked this week. |
| viral-opportunity-scout | Use when asked to find distribution opportunities for a template, tool, or artifact. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
