---
name: marketing-assumption-grill
description: 'Use when pressure-testing one marketing decision, idea, or plan before committing. Not for executing the decision or asking the user for facts the environment already holds.'
---

# Marketing assumption grill

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User explicitly asks to grill, challenge, or pressure-test one marketing idea, decision, or plan. |
| Authority | Read-only. Chat questions, answers, and recommendations only. Optional public factual research. No writes, publication, outreach, or remote mutation. |
| Side effect | Interview transcript and recommendation set in chat. No external state changes. |
| Done | The answerable frontier is empty or the user stops; every asked question carried a recommendation beside it; no decision was executed. |

## Not for

- Executing the grilled decision, writing the plan into files, or running research as a substitute for judgment.
- General critique of non-marketing work; that belongs with general review owners.

## Inputs

- `target` (required): one marketing idea, decision, or plan under test.
- `answers` (ongoing): user responses to frontier questions.
- `sources` (optional): user-selected public sources for fact-finding.

## Procedure

1. Build a dependency-aware question tree for the target: which questions must settle before downstream ones are answerable. **Done when:** the tree names prerequisites per question.
2. Ask the whole currently answerable frontier, not downstream questions whose prerequisites are open. **Done when:** every asked question has its prerequisites settled.
3. Find discoverable facts through read-only research from supplied or public sources instead of asking the user for them. **Done when:** no asked question could have been answered from the available environment.
4. Give a recommendation beside each question while preserving the decision for the user. Separate facts found, recommendations made, and decisions the user owns. **Done when:** each question carries a recommendation and the user decision slot stays explicit.
5. Recompute the frontier after each answer. **Done when:** answered questions leave the frontier and newly answerable ones enter it.
6. Stop when the frontier is empty or the user stops. Do not execute the resulting decision. **Done when:** the run ends with understanding confirmed and nothing executed.

## Failure and recovery

- User stops early: keep answered ground, mark the remaining frontier explicitly.
- Fact unavailable from any authorized source: mark it unknown, do not ask twice, do not invent it.
- Target too broad for one grill: name the split and grill the first branch only.

## Output

Frontier transcript: questions asked with prerequisites, facts found with sources, recommendations per question, user decisions recorded verbatim, and the remaining frontier or confirmation that it is empty.
