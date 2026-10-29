---
name: docs-practices
description: 'Use when deciding whether a durable document, ADR, plan, or spec is needed, or when checking its invariant quality, scope, and naming. Not for drafting prose or restructuring agent-consumed documents.'
---

# Docs practices

Decide whether a durable record is warranted, then hold it to invariant quality. Default answer is no new document.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A durable document, ADR, plan, or spec is proposed, drafted, or under review for scope, naming, or lasting value. |
| Authority | Reversible local: writes only the document under review inside the requested tree; rollback is version control or undo; never publishes, installs, or commits. Whole-document deletion needs separate explicit approval for that exact set. |
| Side effect | The reviewed document is kept, narrowed, renamed, or removed; existing sources gain a pointer when they already cover the need. No new file unless the need test passes. |
| Done | Every proposed record has a keep-or-reject verdict with evidence, every kept record carries scope, enforcement, and proof, and every affected name and link resolves. |

## Refusals

- Drafting, ghostwriting, or restructuring prose on request is out of scope. Judge need, scope, and naming only.
- Activity records, decision diaries, meeting notes, status logs, mini-learnings, and jargon stay out of durable records. Do not preserve them as history.
- Code comments never substitute for a missing durable record. Fix the record or leave the gap explicit.
- Placeholders, deferred sections, follow-up promises, and excuses never ship as content. Missing authority or prerequisites stay reported as blocked.
- Legal notices, license text, required attribution, and quoted evidence stay intact. Never generalize a time-bound fact into a timeless rule.
- Opaque labels are rejected: bare numbers, coded prefixes, random letters, hashes, date prefixes, and Roman numerals never name files, headings, phases, or tasks.

## Inputs

- Required: the proposed or existing document path, or the claim that needs a durable home.
- Required: the invariant the record would protect, stated in one sentence.
- Optional: the existing sources already covering the topic; the enforcement and proof each source provides.

## Procedure

1. State the need test first. Keep a durable record only when it protects a material generalized invariant that future readers must obey or rely on. Reject notes about what happened, what was decided when, and what was learned once. Done when: the invariant sentence exists or the proposal is rejected.
2. Search for a sufficient existing home. Read the candidate sources before writing. Reuse the sufficient source and add a pointer when it covers the invariant. Done when: every proposal maps to an existing home or proves none suffices.
3. Check scope and enforcement on kept records. Each record states its scope of application, what enforces it, and what proof shows a violation. Remove material that applies once, applied in the past, or restates configuration the source of truth already owns. Done when: scope, enforcement, and proof are explicit and single-owned.
4. Check naming end to end. Give files, titles, headings, phases, and task labels concise semantic words a stranger understands. Replace each opaque label with a meaningful name and update every link, pointer, and reference to the renamed target. Keep useful ordered steps, quoted historical evidence, legal notices, and externally fixed machine or standard identifiers unchanged. Done when: no opaque label remains and every affected link resolves.
5. Check proof quality. Accept only independent or adversarial evidence that detects a plausible material fault and survives equivalent refactors. Fixture inputs and setup are permitted; saved-output pins, literal snapshots, mock echoes, and source-text assertions are rejected. Done when: each proof detects a distinct fault or is removed.
6. Handle the negative verdict honestly. When authority or a prerequisite is missing and unreachable, finish reachable narrowing and renaming, then report blocked with the exact missing item. Never invent coverage for the gap. Done when: the report states kept, rejected, or blocked with evidence.

## Failure and recovery

- No material invariant: reject the record, point to the sufficient existing source or to no record, and stop.
- Uncertain ownership or scope: change nothing in the uncertain region; report the boundary question as blocked.
- Broken link after rename: restore the prior arrangement for that operation or repair the pointer from verified evidence, then re-verify every affected link.
- Non-convergence: repeated narrowing creates new broken references or ownership conflicts; stop, keep the last verified state, and return the remaining findings.

## Output

- The verdict per record: kept with its invariant, scope, enforcement, and proof; or rejected with the sufficient existing source or the reason no record applies.
- The narrowed or renamed document tree, plus a terminal report with kept, rejected, and blocked counts, every rename with its updated links, and the link-check result.
