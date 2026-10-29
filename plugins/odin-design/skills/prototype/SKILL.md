---
name: prototype
description: 'Use when committing the wrong product answer would be expensive to unwind and a cheap sketch cannot settle how it should work, feel, or read. Not for visual probes during framing, deciding what to build, polishing a working feature, or shipping the real thing.'
---

# Prototype

Anchors: David Parnas (a throwaway hides the product behind one tested question; nothing about it is load-bearing), Dieter Rams (fidelity follows the question, never habit).

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A product question needs a runnable or viewable artifact to settle it, and the user is available to experience the result and decide. |
| Authority | Builds a throwaway in scratch or an explicitly authorized isolated path; may touch the product tree only as a reversible throwaway overlay that is restored afterwards. Writes a short decisions note for continuity. No implementation commitment, polish pass, publication, remote, credential, paid, or destructive mutation. Never ships the prototype as the product. |
| Side effect | A settled user decision on the tested questions, or a faithful recap when no decision transfers. |
| Done | The user decided how the product should work or feel against a prototype that did not fake the tested dimension, or the run returned why it could not proceed. Their choice settles the matter, never the agent judgment of the artifact. |

## Inputs

- The product question and what judgment settles it: seeing the rendered result (layout, density, finish) or driving it (flow, state model, control response). Required.
- Authorization to build, plus the related plan or contract path when the result must write back. Required before building.

Do not build until authorized. A request that names the thing to prototype is that authorization after scoping. If no person can experience the prototype in this run (headless, pipeline, or caller reports no human present), stop and return that this skill needs a human instead of previewing or inventing how it should feel.

## Procedure

1. Scope the question. Read only the repository surfaces the question touches; do not scan the tree. Decide narrow vs wide, seeing vs driving, and which follow-up questions remain after each decision. Do not fake the tested dimension: a driving question needs behavior, a seeing question needs real finish at the judged surface.
2. Build at the fidelity the question needs. Default to an isolated web artifact whatever the product is written in; touch the existing app only when the question is density or chrome on an existing page that an isolated page would hide. When touching the tree, record every changed file and restore each one when the try ends; when restoration is not clean, name the files left modified rather than handing off a dirty tree. Never commit the overlay and never delete a kept prototype as cleanup: throwaway describes the code, not a removal request.
3. Keep a short decisions note with the run: what was settled, the adjustments attached, and the prototype path when one survives. Point at the prototype; do not reproduce it. Include only what changes later planning. Update it only when confident a choice settled through user judgment of the artifact.
4. Apply or recap. When the user applies and a directly related plan or contract was passed or named in-session, write the settled decisions back to that artifact only; never mint an unrelated plan. Otherwise recap from the decisions note with the choices and, when one survives, the prototype path (an undone overlay has none; say so). Then recommend the next owner by name (framing when product questions remain, planning when the session is enough to plan) without invoking it.

## Failure and recovery

- No human present: stop with that blocker. Do not invent how it should feel.
- Question answerable by a cheap sketch or already settled: stop and say so; do not build.
- Request is polish of a working feature or a build decision: route to the owning job.
- Overlay cannot be restored cleanly: report the modified files explicitly and stop.
- User moves the goal instead of answering: stop building for the old question and hand back what was learned.

## Output

Return the tested questions, the settled decisions with user adjustments, the prototype or overlay path when one survives, the decisions-note path, and the recommended next owner or the explicit blocker. Prototype evidence informs a later decision; it never counts as shipped behavior.
