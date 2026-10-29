---
name: competitive-intelligence
description: 'Use when mapping the competitive landscape and battlecards for a developer product from authoritative sources. Not for per-feature changelog research or unsourced market predictions.'
---

# Competitive intelligence

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User names a product and asks for a landscape, competitor map, or battlecard. |
| Authority | Read-only. Public and supplied sources only. No credentials, outreach, or remote mutation. |
| Side effect | A dated landscape matrix and battlecard set in chat. Nothing else changes. |
| Done | Direct, indirect, DIY, and platform alternatives are covered; every fact links to an authoritative source with an observation date; win and lose conditions and unknowns are explicit; no unsourced trajectory claim remains. |

## Not for

- Per-feature or changelog research; that stays with `competitor-feature-research`. This skill owns the broader landscape and battlecard context and hands off to it for depth.

## Inputs

- `product` (required): the product being positioned.
- `scope` (required): which alternative classes to cover and which competitors are in scope.
- `sources` (optional): user-selected authoritative sources; otherwise public docs, pricing pages, and reputable coverage.

## Procedure

1. Fix scope: list in-scope competitors across direct, indirect, DIY, and platform classes, plus explicit exclusions. **Done when:** scope and exclusions are written.
2. Build the landscape matrix: features that matter, pricing model, positioning, content strength, community signals, with one source link and observation date per cell. **Done when:** every cell traces to a source or is marked unknown.
3. Write battlecards: when the alternative wins, when this product wins, the decisive conditions, and the proof behind each. **Done when:** each card states win and lose conditions with evidence.
4. Record unknowns and freshness triggers (what would change the map, and what to recheck). **Done when:** unknowns and recheck triggers are explicit.
5. Purge unsourced trajectory claims (market size futures, share predictions) unless the user supplies an authoritative source, which is then cited verbatim. **Done when:** no prediction lacks a cited source.

## Failure and recovery

- Authoritative source missing for a material cell: mark unknown with the needed source named; do not fill from model knowledge.
- Scope too wide: map the top tier fully and list the remainder as deferred scope.

## Output

A dated landscape matrix with per-cell sources and dates, battlecards with win and lose conditions, unknown list, and recheck triggers.
