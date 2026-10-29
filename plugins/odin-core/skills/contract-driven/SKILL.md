---
name: contract-driven
description: 'Use when crossing a public API boundary, guarding complex invariants, or hardening untrusted input or integration seams. Not for remote or irreversible changes.'
---

# Contract-driven

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Crossing a public API boundary, guarding complex invariants, or hardening untrusted input or integration seams. |
| Authority | Reversible local: writes only named local types, assertions, validators, and tests at contract boundaries; rollback is undo (delete the added code or revert the boundary change). No remote mutation. |
| Side effect | Adds or refines local types, assertions, validators, and tests at contract boundaries. |
| Done | Every planned contract is implemented at the appropriate static/test/debug/runtime layer and violations fail explicitly at the boundary. |

## Inputs

Required:

- The requirements or specification for the operation whose contract is being designed.
- The target source file or module containing the public API boundary, invariant, or untrusted seam.

Optional:

- Existing tests that must continue to pass.

## Procedure

1. Plan: extract PRE/POST/INV from the requirements. Give each contract an ID and a one-line description (e.g. PRE-1: amount > 0; POST-1: balance == old(balance) - amount; INV-1: balance >= 0). Do not begin implementation until every planned contract has an ID. Done when: every planned contract has an ID and a one-line description.

When an enforcement point moves, enumerate every entry that reached the protected region through the old point, including callbacks, retries, forks, resume/replay paths, and test entries. Record coverage or a justified exemption for each and exercise newly covered entries directly. When an adapter narrows arguments, inventory every source field and state whether it is carried, explicitly refused, or genuinely irrelevant; a handwritten list is not automatic coverage for future fields. When validation moves earlier, preserve its applicability conditions, observable check order, and established error contract; leave a check at the later boundary when the required early state is unavailable. When registry keys or path representations change, use one explicit identity contract across registration, lookup, move, deletion, and busy checks while preserving public representations unless their change is authorized. For Windows paths, distinguish operational namespace paths from comparison representations and establish drive, UNC, symlink, case, and filesystem-identity semantics before normalizing; do not use naive prefix containment or universal lowercasing. For provider/model migrations, separate stable identifiers, display labels, credential scope, and actual request fields. Trace rejected fields through the current schema and request builder and prove the intended request difference offline before proposing any live call. These checks do not authorize credential changes, retries, uploads, or paid services.

2. Select verification level: choose the strongest layer that can enforce each contract, preferring static over runtime:
   - Static type system or static_assert for type size, alignment, null/type safety, and exhaustiveness.
   - Test assertions for expensive O(n)+ properties.
   - Debug-only invariants for internal invariants.
   - Runtime guards for public API input, and always for external or untrusted input.
   If a property can be verified statically, do not add a runtime contract.
   Done when: every contract has a selected verification level, static preferred over runtime.
3. Create: implement every PRE, POST, INV at its chosen level in the target local code. Runtime contracts, where used, must be active and not compiled out or disabled. When the surface is an HTTP API that returns errors, use one error shape everywhere: a machine-readable code, a human-readable message, and optional details. Map invalid client data to 400, unauthenticated to 401, unauthorized to 403, missing resource to 404, conflict or version mismatch to 409, semantically invalid input to 422, and server failure without internal detail to 500. Never mix throwing, null returns, and error envelopes on one surface. Done when: every contract is implemented at its chosen level and runtime contracts are active.
4. Verify: run the type checker, static analysis, and build. Contracts must compile and lint. Done when: the type checker, static analysis, and build pass with all contracts.
5. Test: write one violation test per PRE/POST/INV proving the contract catches bad input or bad state. Static contracts are verified by the type checker; runtime contracts by violation tests that assert the boundary fails explicitly. Done when: one violation test per contract passes, proving the boundary fails on bad input or state.

## Failure and recovery
- Contract lint or build fails: fix the contract or implementation; do not disable or compile out the runtime contract to make it pass.
- A violation test does not fire: the contract is not enforced at the chosen layer; re-select the layer or strengthen the check; never delete the test to make it pass.
- A contract restates the implementation trivially (e.g. ensures(result == x - y) for subtract(x, y)): delete that contract; it is contract fatigue, not a boundary guarantee.
- Partial result: if some contracts cannot be implemented because a requirement is missing, stop and report the missing requirement; do not invent contracts or widen scope.
- Rollback: delete the added local types, assertions, validators, or tests, or revert the boundary change; no remote, credential, published, or deployed artifact is touched.

## Output
Local code with every planned PRE/POST/INV contract implemented at its verification layer, plus one violation test per contract. Violations fail explicitly at the boundary. Each contract traces to a requirement by ID.
