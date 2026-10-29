---
name: marketing-behavior-audit
description: 'Use when diagnosing observed buyer or market behavior with evidence before changing copy, offer, or interface. Not for running experiments or claiming uplift.'
---

# Marketing behavior audit

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User supplies an observed behavior, test result, interface change, or proposed behavioral intervention. |
| Authority | Read-only. Chat diagnosis only. Peer-reviewed or user-selected sources. No social scraping, no experiment execution, no product changes. |
| Side effect | A diagnosis with hypotheses, alternatives, and reversible test designs in chat. Nothing else changes. |
| Done | Observations, interpretations, and unknowns are separated; the smallest defensible hypothesis set is stated with case-specific confidence; every test design carries a rejection rule; deceptive patterns get a plain-language warning plus a truthful alternative. |

## Not for

- Running experiments, changing product behavior, or promising conversion uplift.
- Catalog-scale psychology surveys; the vocabulary below is the whole operational set.

## Inputs

- `observation` (required): what happened, with the actual interface, copy, or change details.
- `evidence` (required): test results, analytics excerpts, or peer-reviewed sources the user supplies or selects.
- `proposal` (optional): the intervention being considered.

## Procedure

1. Separate observed facts, interpretations, and unknowns into three labeled lists. **Done when:** no interpretation or unknown appears as fact.
2. Choose the smallest defensible hypothesis set that explains the facts. Keep a leading hypothesis only when the case favors it over alternatives. State the nearest alternative and the scientific limitation. **Done when:** hypotheses, alternatives, and limits are all explicit.
3. Keep confidence case-specific: state what this case supports, not what the literature claims in general. **Done when:** every confidence claim cites this case plus its source.
4. Recommend only what the supplied evidence supports. **Done when:** each recommendation traces to a named observation.
5. Place all tests in one verification section. Each test names: uncertainty resolved, smallest reversible change or observation, prediction, primary metric, countermetrics, backfire condition, and rejection rule. **Done when:** every test has all seven fields.
6. Warn in plain language about autonomy and truthfulness risks touched by the case: deceptive scarcity, fabricated popularity, hidden terms, coercive exit paths, vulnerable targeting. Offer a transparent alternative for each warning rather than a blanket refusal. **Done when:** each flagged risk carries a concrete truthful alternative.

## Failure and recovery

- Observation too thin to support any hypothesis: say so, list what evidence would change that, stop.
- Sources insufficient: mark claims provisional with the missing source named.
- Proposed intervention is deceptive on its face: name the deception, offer the truthful alternative, do not design the deceptive variant.

## Output

A behavior audit: fact/interpretation/unknown lists, hypothesis set with alternatives and limits, evidence-backed recommendations, a verification section with fully specified reversible tests, and ethics warnings each paired with a truthful alternative.
