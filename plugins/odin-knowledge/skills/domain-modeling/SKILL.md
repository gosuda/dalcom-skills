---
name: domain-modeling
description: 'Use when pinning down domain terminology, maintaining the domain model, or recording a glossary term or ADR. Not for reading a glossary to pick a name: just read it. Not for code changes.'
---

# Domain modeling

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Domain terminology is disputed, vague, or missing; a relationship boundary needs sharpening; a glossary term or ADR needs recording during design |
| Authority | Reversible local: writes only the glossary artifacts below and ADR files inside the working tree; rollback is version control or undo. No remote mutation. |
| Side effect | Lazily creates or updates root `GLOSSARY.md`, `GLOSSARY-MAP.md` plus context-local `GLOSSARY.md` files, and ADR files in the detected ADR directory; no source-code, VCS, credential, or remote change beyond those files. |
| Done | Every resolved term is recorded once with canonical name, definition, and rejected synonyms; every qualifying decision has a local ADR or a named skip reason; unresolved terms are reported with reasons. |

## Inputs

Required: the term, conflict, or boundary question from the current design conversation, plus the human ruling when a conflict needs one. Optional: an existing `GLOSSARY.md`, `GLOSSARY-MAP.md`, or context-local `GLOSSARY.md` files (absence is normal; files are created lazily), the implementation source behind a term (when absent or unreadable, skip the code cross-check and report it), and the existing ADR directory. Scope is terms in the current design work unless the request asks for a repository-wide glossary sweep. Entry shape follows `references/GLOSSARY-FORMAT.md`; ADR shape follows `references/ADR-FORMAT.md`.

## Procedure

1. **Detect the glossary layout.** Check the repository root for `GLOSSARY.md` and `GLOSSARY-MAP.md`, and beside each bounded-context source for a context-local `GLOSSARY.md`. A lone root `GLOSSARY.md` means one shared glossary. A root `GLOSSARY-MAP.md` means bounded contexts, each with its glossary beside its source and the map relating them. A project that already keeps a `GLOSSARY.md` beside a context source keeps that file; do not relocate it. Read the applicable glossary before judging any term. If none exists, create nothing yet. Done when: the layout is determined and the applicable glossary is read or confirmed absent.
2. **Migrate legacy names once.** If only legacy `CONTEXT.md` or `CONTEXT-MAP.md` files exist and no `GLOSSARY.md` names exist, read the legacy files once and write their entries forward into the `GLOSSARY.md` layout at the first resolution. Report the migration with file paths. Never write new entries under `CONTEXT` names after migration. Done when: legacy content is carried forward or confirmed absent.
3. **Challenge conflicting terms.** Compare each term used in the current design work against the glossary. The moment a use contradicts a glossary entry, state both meanings and ask which one is correct before continuing, for example, a glossary that defines cancellation as ending an Order versus a use that changes one Line Item. Done when: every conflicting term is surfaced with both meanings and the ruling is requested.
4. **Sharpen fuzzy terms.** When a name is vague or overloaded, pick the single domain term that owns the rule; every other name becomes a rejected synonym. Done when: each fuzzy term has one canonical owner and its rejected synonyms are named.
5. **Stress-test relationships.** Construct an edge case that exposes a relationship boundary. For example, if one Order is split across two shipments, when may Billing issue the invoice? Resolve which term owns each side of the boundary. Done when: each relationship boundary is resolved with an edge case that exposes it.
6. **Check claims against code.** Read the implementation behind each term under resolution. Surface any contradiction between the model and the code, then rule which is authoritative. When the code wins, correct the model term. This skill never edits code. If the implementation is unreadable or absent, skip the cross-check and mark it not performed. Done when: each term is cross-checked or marked not performed, with contradictions surfaced and ruled.
7. **Record each resolution immediately.** The moment a term resolves, write it to the applicable glossary file per `references/GLOSSARY-FORMAT.md`: canonical term, one or two sentence definition of what it is, and rejected synonyms on the `_Avoid_` line. Create the glossary or map file lazily at this first write, never before there is something to record. Done when: each resolved term has exactly one entry with all three parts.
8. **Keep the glossary pure.** Entries contain definitions and rejected synonyms only. Refuse implementation details, specification content, and scratch notes in glossary files; put them in their own artifacts or drop them. Exclude general programming concepts even when the project uses them heavily; only project-domain terms belong. Done when: every touched entry contains only definitions and rejected synonyms.
9. **Record qualifying ADRs locally.** Offer an ADR only when all three hold: the decision is hard to reverse, a future reader would find it surprising without context, and it was the result of a real tradeoff with genuine alternatives. When any one is missing, skip the ADR and say why. Detect the project ADR path and template first: keep the existing directory, filename scheme, numbering, and headings, and continue its sequence. When none exists, use `references/ADR-FORMAT.md` defaults. Write the full local ADR file at decision time; never delete an ADR file. When a later decision reverses an earlier one, write a new ADR that supersedes the old and mark the old accordingly. Done when: each qualifying decision has a local ADR file, and each skip has a named reason.

## Failure and recovery

- Unresolvable conflict. Neither the conversation, the human ruling, nor the code settles which meaning owns the rule: record nothing, leave the glossary unchanged, and report the term as unresolved. Do not pick a winner to force closure.
- Implementation unavailable. The cross-check cannot run: record the term only when the design conversation resolved it, mark the cross-check not performed, and say so in the report. Never claim code agreement that was not observed.
- Purity pressure. A resolution only makes sense together with implementation detail or specification content: write the glossary entry without that content and route the remainder to its own artifact.
- Partial results. Resolved terms are written; unresolved terms stay out of the files.
- Rollback. Revert the glossary edit; delete a lazily created glossary file that ends the session with no surviving entry. Never delete an ADR file; correct a wrong ADR with a superseding ADR.
- Blocked result. The terminal report names each unresolved or unrecorded term and each missing ADR fact with its reason. Never present Done while a resolved term lacks its entry or a qualifying decision lacks its ADR or skip reason.

## Output

Updated or newly created `GLOSSARY.md` or `GLOSSARY-MAP.md` plus context-local glossaries, new local ADR files where qualifying, and a terminal report listing terms resolved and recorded, conflicts surfaced, model-versus-code contradictions with rulings, entries whose cross-check was not performed, ADRs written with paths, ADR skips with reasons, legacy migrations performed, and terms left unresolved with reasons.
