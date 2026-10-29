---
name: offensive-driven
description: 'Use when the user explicitly asks for a replacement-first pass such as "rebuild it clean", "replace-first", or "offensive pass on <target>" spanning code, docs, plans, or research. Not for code-only restructuring (existing code skills already own that and stay offensive by default); not for root-cause repair or thin-slice additions.'
---

# Offensive driven

Replacement-first operation across code, docs, plans, or research, invoked by explicit user request only. State the contract, expose the broken assumption, re-derive the simplest valid replacement from contract and evidence, preserve what works, remove the obsolete structure, migrate every dependent in scope, and prove the delta with a domain-appropriate check. Offense is a posture toward the broken structure, never permission to rewrite correct structure, erase needed validation, or widen authority.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User explicitly requests a replacement-first pass on a named target (e.g. "rebuild it clean", "replace-first", "offensive pass on <target>"). Never self-initiated; never inferred from bloat, duplication, or trigger phrasing alone. |
| Authority | Reversible local: writes only the explicitly invoked scope (exact disclosed path or artifact set). No remote, credential, paid, or deployed mutation. No commit, push, or publication unless the user explicitly asks for it in this invocation. Human approval is required before removing a live or consumer-facing surface, discarding stored data or history, or taking any irreversible, remote, or paid action. |
| Side effect | Replaces the broken structure with the re-derived form inside the invoked scope; migrates every dependent in scope in the same change; leaves no half-migrated reference the skill itself introduced. |
| Done | Contract stated, broken assumption exposed with evidence, simplest valid replacement derived from contract and evidence, useful behavior and detail preserved, obsolete structure removed, every in-scope dependent migrated, domain-appropriate proof exercised, and actual delta compared. |

## Boundary

- Code-only or architecture-only restructuring already has owners that stay fully offensive by default; this skill does not replace, gate, or require opt-in to them. Invoke this skill for a cross-domain replacement-first pass, or when the user names it explicitly.
- Offense never authorizes rewriting a structure that meets its contract, deleting validation that still guards a named invariant, or exceeding the disclosed scope. If the structure is correct, say so and stop.
- This skill is self-contained. It names no peer skill as a runtime dependency and delegates no step to one.

## Inputs

Supply the named target, the domain it lives in (code/architecture, plan/workflow, prose/docs, or research), the desired outcome with its consumers, the invariants or obligations that must survive, and the exact surface or path set in scope. Supply the contract source when one exists (signatures plus call-site usage, schema plus stored data, approved plan plus approval boundaries, claims plus cited evidence); otherwise the skill derives the contract from that evidence during the procedure. Name the proving check when the repository or artifact type does not define one. When any required element cannot be established from the request plus local evidence, stop rather than invent it.

## Procedure

1. **State the contract and bound the surface.** Write the desired outcome, its consumers, the invariants or obligations that must survive, and the exact surface in scope (paths, artifacts, interfaces, or claim set). Name every dependent in scope and every live, persisted, or consumer-facing surface whose removal needs human approval. Done when: outcome, consumers, invariants, exact surface, in-scope dependents, and approval-gated surfaces are all written.
2. **Expose the broken assumption with evidence.** Identify the failing assumption or structure and the evidence that breaks it (failing check, contradictory usage, violated invariant, unsupported frame). If the evidence shows the structure meets its contract, report that and stop; offense does not apply. Done when: the broken assumption is named with its evidence, or the target is declared sound with reasons.
3. **Re-derive the simplest valid replacement.** Build the replacement from the contract and supporting evidence alone, in the smallest form that satisfies it: code from signatures plus call-site usage with caller, format, and stored-data safety; prose or docs preserving every obligation and citation; research rejecting the unsupported frame without altering facts; plans or workflows preserving approval boundaries. Carry forward only behavior or detail with evidence behind it. Done when: the replacement traces to the contract with each preserved element cited.
4. **Cut the obsolete structure and migrate dependents.** Remove the broken structure within the disclosed scope; migrate every in-scope dependent in the same change so no caller, link, plan step, or claim references a removed surface. Stop and ask when a dependent falls outside the disclosed scope, when removal needs the human-approval gate, or when stored data or history would be discarded. Done when: obsolete structure is gone from scope, every in-scope dependent resolves to the replacement, and each approval-gated removal carries an explicit yes.
5. **Prove the delta in the domain's own terms.** Exercise the narrowest check that covers the change (code: compile plus behavioral checks over changed contract; docs/prose: obligation and citation review plus any applicable render or lint check; research: claim-to-evidence recheck confirming no fact changed; plans/workflows: approval-boundary and handoff check, dry run where the repo defines one). Compare actual before/after delta against the stated contract and report preserved, removed, and migrated items. Done when: the check result is recorded, the delta matches the contract, and any gap is named rather than rounded up.

## Failure and recovery

- Missing contract or evidence: make no replacement edit and return `blocked` with the exact missing outcome, invariant, surface, or evidence.
- Approval withheld or scope exceeded: make no further change and return `blocked` with the gated surface or exact additional path; never cut on silence and never widen scope implicitly.
- Verification failure: stop; restore the current increment to the last green state while preserving earlier green work. Return `non-converged` with the failed check and observed result.
- Non-convergence: when repeated attempts preserve neither the contract nor the done predicate, return `non-converged` with the last green state, the failed increment, and the evidence. Never report success from a partial replacement or leave a half-migrated dependent behind.

## Output

Return the stated contract (outcome, consumers, invariants, exact surface), the broken assumption with its evidence, the replacement with per-item preservation citations, the removed surfaces with approvals obtained, every migrated dependent, the domain check run with observed result, and the before/after delta. Terminal classification: `complete`, `blocked`, or `non-converged`; `complete` requires the bound done predicate.
