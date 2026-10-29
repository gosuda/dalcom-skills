---
name: frame
description: 'Use when a vague or ambitious product idea needs framing into a right-sized requirements-only plan before implementation. Not for executing specified work, judging an external candidate, or refining supplied notes without product decisions.'
---

# Frame a product idea

Anchors: David Parnas (WHAT the product must do is a separate contract from HOW it is built), Dieter Rams (the smallest plan that prevents invention downstream wins).

This is the product-WHAT owner sourced from ce-brainstorm. The `brainstorm` slug stays with knowledge capture and refinement; this skill owns vague-to-requirements framing. Verdict questions about a named external candidate route to pov.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user wants to explore or scope what to build from a vague or ambitious idea, and the result must be sized so planning can build on it without inventing product behavior, scope boundaries, or success criteria. |
| Authority | Read-only research plus one requirements-only plan artifact when one is earned. No implementation, no test execution, no VCS, credential, paid, published, deployed, remote, or destructive mutation. |
| Side effect | A chat paragraph for lightweight work or a requirements-only plan file for durable work, plus an explicit handoff. No requirements, plans, or code beyond that. |
| Done | The artifact or chat result is written and passes the ready check, or no file was earned and none was requested, and the handoff was presented. |

## Inputs

- The feature idea or problem from the invocation or conversation. Required; when absent, ask for it and wait.
- Output preference when supplied (markdown default, HTML only on explicit request). Exclusive: one format per run.

Lightweight work (small, well-bounded, low ambiguity) ends in chat with no file, no grounding dispatch, and no approach generation. Heavier work earns a file only through a decision a later reader needs recorded under a stable ID, or through an explicit user file request.

## Procedure

1. Classify before dispatching. Decide lightweight vs heavier from the request and bounded inline reads; when uncertain, take the heavier path. Route out explicitly: non-software work follows a different method; a verdict question about a named external candidate is offered as a pov handoff; quick help, factual questions, and single-step tasks are answered directly with no plan artifact.
2. Understand the idea through dialogue. Ask one question at a time and only decisions the environment cannot settle. Preserve settled decisions; never re-ask them without new conflicting evidence. Scan current context and the smallest relevant repository surfaces for constraints and conflicts with existing concepts and verified code. Record scope as one coherent piece of work; split or stop when it is not.
3. Generate approaches only for heavier work, then synthesize and verify claims against sources before writing. A function call never proves its uninspected guarantees; drop or qualify unsupported claims where they appear.
4. Write the requirements-only plan when earned: goal capsule plus product contract with scope boundaries and success criteria, artifact identity fixed before writing, no implementation design. Run the ready check: every later-reader decision has a stable ID, scope and criteria are explicit, and no implementation choice is smuggled in. A failing check blocks the handoff claim.
5. Hand off explicitly. Present the next action with its exact input (the plan path or the session as seed) without invoking it. Pipeline or headless runs return the plan state and handoff instead of a menu.

## Failure and recovery

- No idea supplied: ask and wait; invent no topic.
- Incoherent scope: split or stop with the reason rather than planning across unrelated work.
- Evidence contradicts a settled choice: reopen that choice and dependents; never leave contradictions labeled settled.
- Ready check fails: repair the plan or return explicitly incomplete.
- Explicit user limit reached: stop incomplete with evidence and remaining questions.

## Output

Return the chat paragraph or the plan path with its ready-check state, the decisions recorded, open questions with why they stay open, and the explicit handoff. No implementation follows from framing alone.
