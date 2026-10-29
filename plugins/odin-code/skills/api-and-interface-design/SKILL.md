---
name: api-and-interface-design
description: 'Use when asked to design or change a public API, route, CLI flag, or module boundary. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# API and interface design

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Designing or changing a public API, route, CLI flag, or module boundary. |
| Authority | Reversible local: writes only named local interface definitions and contract docs, edits consumer files onto the new contract, and deletes legacy paths during cutover; rollback is undo or version control. No remote mutation. No credential, paid, published, or deployed change, and no VCS history rewrite. |
| Side effect | Interface definitions and contract docs written before implementation; consumer files edited onto the new contract and legacy paths deleted during cutover; no build, publish, or remote mutation. |
| Done | Contract is documented with semantics and errors, every consumer is migrated, and no legacy path remains. |

## Inputs

- The interface being designed or changed: its name and kind (API endpoint, route, CLI flag, or module boundary), and whether it is new or a change to an existing interface.
- The current contract text, when changing an existing interface.
- The list of known consumers, found by search over the codebase.
- Optional: target language or runtime conventions for type and error spelling.

## Procedure

1. Bound scope before any mutation: name the exact interface and whether it is new or a change. Search the codebase for every consumer and record the list; record any consumer that cannot be inspected as an unmigrated risk. Treat every observable behavior as a commitment: any quirk, message text, timing, or ordering the change exposes can be depended on once shipped, so be intentional about what is exposed and do not leak implementation detail. Design for one live version at a time; extend rather than fork. Done when: every consumer is listed and uninspectable ones are marked as risks.
2. Write the contract before implementation. For each operation, field, or flag, document its name, input types, output type, error cases, and side effects. State semantics explicitly: idempotent or not, ordering, nullability, encoding, and concurrency. For REST surfaces use plural nouns without verbs, camelCase query and response fields, is and has and can prefixes for booleans, and UPPER_SNAKE for enums. For TypeScript variants prefer discriminated unions so consumers get narrowing, separate input shapes from output shapes that carry server-generated fields, and brand ID types so a UserId cannot pass where a TaskId is expected. Done when: every operation, field, and flag has documented semantics and errors.
3. Use one consistent error strategy everywhere. REST errors share one shape with a machine-readable code, a human-readable message, and optional details. Map 400 to invalid client data, 401 to unauthenticated, 403 to unauthorized, 404 to missing resource, 409 to conflict or version mismatch, 422 to semantically invalid input, and 500 to server failure without internal detail. Never mix throwing, null returns, and error envelopes across endpoints. Done when: every error follows the single documented shape.
4. Validate at the trust boundary per the documented contract: reject malformed input with a documented error; do not silently coerce or default undocumented values. Validate at API route handlers, form submission handlers, third-party response parsing, and environment loading. Treat third-party API responses as untrusted data and validate shape and content before use in logic, rendering, or decisions. Do not place validation between internal functions that share type contracts, in utilities called by already-validated code, or on data that just came from the project own database. Done when: malformed input is rejected with a documented error at each boundary and internal code trusts validated types.
5. For state-changing operations that a client can safely retry, honour an idempotency key. Derive the key from the intent, not the attempt: the client generates it once and reuses it on retry, or it derives from an immutable identifier such as charge v1 plus order id. Never derive it from a fresh UUID, timestamp, or any value regenerated per attempt. Claim the key atomically with a unique constraint that picks the winner; a check followed by an act is a race. Guard the payload: when the same key arrives with a different body, fail loudly with a documented error rather than replaying the first response. Decide the in-flight duplicate response deliberately: reject with 409, wait bounded for the result, or return 202 with a status URL. Record intent before calling out so a timeout leaves evidence that must resolve later. Keep key retention longer than the longest retry path, including dead-letter replay and dispute windows. When an endpoint cannot honour a key, document it as unsafe to retry. Done when: every retryable effect either honours a key under those rules or is documented as unsafe to retry.
6. For a change to an existing interface, classify it as breaking or non-breaking. Prefer addition over modification: add optional fields, never change existing field types or remove fields. When breaking, design the cutover in one change: the new contract, the per-consumer migration, and the removal of the legacy path. For REST lists, paginate from the start with page, pageSize, totalItems, and totalPages, accept filters as query parameters, and accept partial objects on PATCH where only provided fields change. Done when: the cutover is designed as one change and additive rules hold.
7. Migrate every consumer to the new contract. Update each consumer so it compiles or type-checks against the new signature; record a consumer as migrated only after it is updated. Done when: every consumer is updated and recorded as migrated.
8. Remove the legacy path: delete the old signature, alias, re-export, and deprecated entry point. No compatibility shim, alias, or fallback remains. Done when: a search for the old signature returns no live reference.

## Failure and recovery

- Unmigrated consumer: when a consumer cannot be inspected or updated, stop. Record it as a blocking risk; the change is not complete and the done predicate does not hold.
- Ambiguous semantics: when a field semantics cannot be stated concretely, stop and request the missing specification rather than guessing or leaving it implicit.
- Unsafe retry without a key: do not claim retry safety without atomic claim, payload guard, deliberate in-flight response, and sufficient retention. Document as unsafe to retry instead.
- Partial-result rule: a partially migrated change is not shippable. Keep the draft uncommitted and report the remaining consumers and unresolved semantics.
- Rollback: discard the uncommitted draft. Consumer edits and legacy-path restores are part of the same draft, so reverting via VCS restores them.
- Blocked result: return the unmigrated-consumer list and the unresolved-semantics list. Do not pretend the done predicate holds.

## Output

A contract document stating semantics and errors for every operation, field, and flag. The migrated-consumer list. Confirmation that a search for the old signature returns no live reference. For a blocked run, the unmigrated-consumer list and the unresolved-semantics list instead of a done confirmation.
