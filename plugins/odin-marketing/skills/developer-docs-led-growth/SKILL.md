---
name: developer-docs-led-growth
description: 'Use when auditing docs or planning quickstart and API-reference improvements that drive acquisition and activation. Not for deploying docs or changing product code.'
---

# Developer docs-led growth

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks how docs should acquire, activate, retain, or refer developers. |
| Authority | Read-only audit and plan. Actual docs paths and observed steps only. No docs deployment, CMS integration, or product-code changes. |
| Side effect | A docs audit or quickstart and API-reference plan in chat. Nothing deployed. |
| Done | Pages map to acquisition, activation, retention, and referral jobs; every finding points to an actual docs path with observed steps, missing examples, error coverage, or navigation defects; no universal time-to-first-call benchmark is asserted. |

## Not for

- Product onboarding implementation, auth and sandbox builds, or SDK design. Those stay with product and DX owners; this skill consumes them as inputs and reports docs gaps only.

## Inputs

- `docs` (required): the docs tree or the explicit page set under review.
- `jobs` (optional): which of acquisition, activation, retention, referral to emphasize. Defaults to all four.

## Procedure

1. Walk the actual paths a new developer takes: landing to quickstart to first call to next step. Record observed steps with paths. **Done when:** the walk names real paths and real outcomes.
2. Map each page to its jobs: which pages acquire, which activate, which retain, which refer. Mark pages serving no job. **Done when:** every reviewed page has a job mapping or an explicit none.
3. Check quickstart completeness: prerequisites, copy-paste commands, expected output, error coverage, next step. **Done when:** each quickstart has a completeness verdict per item.
4. Check API-reference completeness for the paths developers actually reach: parameters, errors, examples, links back to guides. **Done when:** gaps name the exact reference page and missing item.
5. Check information architecture: search intent coverage, cross-links, version clarity, stale pages. **Done when:** each IA finding names the defect and the affected paths.
6. Forbid universal benchmarks: report observed friction only, never a fixed conversion threshold. **Done when:** no threshold appears without a supplied measured baseline.

## Failure and recovery

- Docs paths inaccessible: audit the reachable set and name the blocked paths as gaps.
- Product friction found that docs cannot fix: route it as a product finding with evidence; do not disguise it as a docs edit.

## Output

A docs audit or improvement plan: journey walk with paths, per-page job map, quickstart and reference completeness verdicts, IA defects, routed product findings, and prioritized next edits by developer impact.
