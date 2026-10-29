---
name: minimalism-driven
description: 'Use when writing or restructuring code, before adding a helper, wrapper, config key, or dependency, or when the user asks for minimal or DRY code. Not for performance tuning: use optimize.'
---

# Minimalism driven

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Writing or restructuring code; considering a helper, wrapper, config key, or dependency; or an explicit request for minimal code, DRY code, or no gold-plating. |
| Authority | Reversible local: writes only reversible local edits needed by the ask; rollback is version control or undo. No remote mutation. Human approval is required before removing a live or consumer-facing surface, discarding stored data or history, or taking any irreversible, remote, or paid action. |
| Side effect | Edit code within the requested scope; replace broken structure with its clean re-derived form, absorb special cases, delete obsolete mechanisms, and migrate every in-scope dependent in the same change; do not implement adjacent improvements. |
| Done | Every addition has a concrete reason, intent and failure behavior are obvious, broken structure is replaced rather than patched around, every in-scope dependent resolves to the replacement, and the resulting scope exactly matches the ask. |

## Inputs

Supply the requested behavior and the local code surface to change. Supply explicit constraints or acceptance criteria when they exist. Existing nearby implementations and call sites are required evidence for reuse decisions; no additional input is optional if its absence would require guessing behavior.

## Procedure

1. Bound the requested behavior, affected files, and acceptance criteria before editing. If any required behavior cannot be determined from the request or local code, stop rather than invent it. Done when: the behavior, files, and criteria are stated and no unknown remains.
2. Inspect the affected code and its relevant call sites for an existing implementation or convention that can satisfy the ask; reuse that before creating a second form. Done when: every reuse candidate is identified and the reuse-or-create decision is recorded.
3. Try deletion first, then clean replacement of the broken structure. Add new code only when neither can produce the required behavior. When the structure in scope is broken, replace it by default: absorb special cases into the replacement, delete the obsolete mechanism, and migrate every in-scope consumer in the same change; patch around it only when replacement would exceed the disclosed scope or need withheld approval. Leave a structure that meets its contract as it is. Done when: the smallest-form approach is selected and justified, and any replacement traces to the contract with each preserved element cited.
4. Before adding a helper, wrapper, config key, dependency, branch, or other surface, state its concrete necessity in one sentence. Omit it if removing it would leave the requested outcome unchanged. Done when: every retained addition has a stated necessity and every rejected addition is omitted.
5. Keep each retained addition sufficient rather than merely short: use clear names, handle required error paths, and encode or state assumptions where the code otherwise permits a silent gap. Done when: every addition handles its required error paths and states its assumptions.
6. Make only the bounded local edits. Do not build an adjacent improvement; report it separately only when it materially affects the requested work. Done when: the change set contains only bounded edits, no adjacent improvement, and no caller references a removed surface.
7. Verify the changed behavior using the narrowest available check that exercises it, then inspect the final change set. Done when: the check passes, every addition retains concrete necessity, intent and failure behavior remain obvious, and no change lies outside the ask.

## Failure and recovery

- Missing contract: if required behavior or acceptance criteria remain unknowable from the request and local evidence, make no speculative edit and return `blocked: missing contract` with the exact missing fact.
- No safe minimal form: if deletion, reuse, or modification cannot satisfy the ask without breaking required behavior, retain the smallest necessary addition and identify the constraint that requires it; if that constraint cannot be established, return `blocked: necessity unproven`.
- Verification failure: if the changed behavior fails its narrow check, restore the files changed by this procedure to their pre-edit contents or leave the failing edits clearly identified as a partial result, and return `non-converged: verification failed` with the failed check and observed result.
- Scope expansion: if completion would require unrelated files, remote mutation, credentials, publishing, deployment, or a dependency not authorized by the ask, do not perform that work and return `blocked: scope expansion required` with the exact boundary.
- Approval withheld or scope exceeded: make no further change and return `blocked` with the gated surface or exact additional path; never cut on silence and never widen scope implicitly.

Never report the done predicate while a required check fails or evidence is missing.

## Output

Return the completed local code change and a concise report naming the behavior implemented, the files changed, the necessity of each new surface, the verification performed and its observed result, and any blocked adjacent work. On failure, return the exact blocked or non-converged classification defined above and preserve or restore the pre-edit state as specified.
