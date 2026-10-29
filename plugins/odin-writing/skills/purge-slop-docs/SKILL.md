---
name: purge-slop-docs
description: 'Use when a human asks to purge stale docs, clean Markdown, or reorder the documentation hierarchy. Not for code debris: use deslop.'
disable-model-invocation: true
---

# Purge slop docs

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A human explicitly asks to purge the docs, clean up stale Markdown, or reorder the documentation hierarchy. |
| Authority | Human-gated: preview every whole-file deletion and its consequence and wait for a separate explicit approval before cutting; one explicit approval may cover an exact previewed whole-document set, and a new approval is required only when the set or its consequences change. Every other write is reversible local, with version control as the rollback, inside the requested documentation tree only. |
| Side effect | Edits, moves, and approved deletions within the bounded Markdown tree; do not alter vendored, dependency, generated, or marked auto-generated content. |
| Done | Report per-class finding counts, edits applied versus findings left untouched, the exact deletion set with its approval, and a passing check for every link or path affected by a move or rewrite. |

## Refusals

- Code debris and dead code: use `deslop`. This skill edits Markdown prose only.
- New strategy documents, channel marketing copy, and outward publication: not this skill. Do not draft, send, post, or publish on the behalf of the user.
- Unbounded or uncertain scope: no changes. Return `BLOCKED` naming the unresolved boundary or authorship question.
- Vendored, dependency, generated, or do-not-modify content is excluded. If authorship, generation status, or scope cannot be established, do not mutate the uncertain target.
- Deletion without separate explicit approval covering that exact set: the file is left unchanged. Never combine approvals across different sets.
- Never touch code blocks, quoted text, frontmatter, link targets, identifiers, or a token the own contract of the caller requires, unless the user names that content as the thing to fix.
- Never state whether text was written by a model.
- Never delete unverified or protected material by assumption. Aggression means investigating uncertain candidates and completing authorized cleanup.

## Inputs

Required: the repository or directory that bounds the Markdown tree and an explicit human cleanup request. Optional: a narrower path or stated exclusions. Determine which Markdown files are project-authored and which entry document anchors the tree. Treat vendored trees, dependency directories, generated API output, and files or regions marked generated or do-not-modify as excluded. If authorship, generation status, or scope cannot be established, do not mutate the uncertain target.

## Procedure

1. Enumerate the Markdown files inside the supplied scope, apply the exclusions, and report the resulting file count before changing anything. Do not widen the scope to resolve a finding. Done when the file list is complete and reported.
2. Inspect the included files and classify each finding by a concrete evidence test: Overstatement (a benchmark lacks a number, a guarantee lacks an enforcing check, a superlative is unproved, or the repository cannot demonstrate the claimed property; rewrite to the supported claim or remove), Jargon (a plainer word preserves the meaning, or a metaphorical noun obscures the mechanism; substitute the plain term, retain established project vocabulary), Outdated (a named path, symbol, flag, command, or version no longer resolves; check the reference or a safe read-only form, update to verified evidence or remove), Redundant (the same meaning has another owner, or prose repeats authoritative configuration; keep one owner, replace the other with a pointer or remove), Empty ceremony (puffery, trailing significance clauses, promotional adjectives, vague attribution, formulaic outlooks, chatbot openers and closers, sycophancy, process narration, manufactured thoroughness; delete the ceremony and keep the fact), Tautology (a heading restated in its first sentence, a bold label restating its line, a summary that repeats the piece; delete the restatement and end on the last concrete point), Stale claim (a guarantee, status, date, or instruction the tree no longer supports; verify against the repository and correct or remove), Duplicated ownership (two documents own the same meaning; keep the authoritative owner and point), Noise (filler, forced triads, synonym cycling, dense sentences, rhythm-crutch dashes, decorative emoji, bullets where two sentences read better, headers over two-sentence sections; rewrite for first-read comprehension). For wording-level checks use `references/slop-patterns.md`. Done when every finding in every included file is classified with its evidence test.
3. Grade certainty independently from severity. Apply an edit only when a deterministic check makes the finding HIGH certainty. Report MEDIUM and LOW findings without changing them. Done when every finding has a certainty grade and only HIGH findings are edited.
4. Treat a whole document as a deletion candidate only when no pointer references it and every section fails at least one evidence test. For each candidate or exact set, preview the exact files, state that no references were found and how that was established, describe the loss including required meaning and links, and request a separate explicit yes. One explicit approval may cover the exact previewed set. A refusal or missing answer leaves those files unchanged. A changed set or changed consequences require a new approval. Done when every deletion candidate has an approval decision recorded against its exact set.
5. Reorder within a file by co-locating the definition, rules, and caveats of each concept under one heading. Inline material every reader path needs; place branch-specific reference detail behind a direct pointer. Done when the definition, rules, and caveats of each concept sit under one heading.
6. Reorder across the tree so the entry document says what the project is and where to start, while detail remains reachable through pointers. Any document with no inbound pointer must be the entry document or an individually reviewed deletion candidate. Done when every non-entry document has an inbound pointer.
7. After each move, deletion, or pointer rewrite, verify every affected Markdown link and repository path resolves. If a pointer breaks, restore the pre-change arrangement for that operation or repair it from verified repository evidence. Done when every affected link and path resolves.
8. Count findings by class, distinguish applied edits from untouched findings, record each deletion and its explicit approval, and record the pointer-check result. Done when the report is complete with all counts and decisions.

## Failure and recovery

- Missing deterministic evidence: leave the candidate unchanged, downgrade to MEDIUM or LOW, include it only in the report.
- Broken pointer or failed verification: restore the affected operation when possible and report `BLOCKED` with the unresolved pointer. Preserve unrelated, already verified edits as an explicit partial result.
- Interrupted mutation: report exactly which files changed, moved, deleted, or remained pending. Never infer approval, hide an error, or claim the done predicate passed.
- Non-convergence: if verified cleanup repeatedly creates new broken references or conflicting ownership, stop, leave the last verified state intact, and return `NON-CONVERGED` with the remaining findings.

## Output

The cleaned documentation tree plus a terminal report with scope, file count, per-class finding counts, applied versus reported-only findings, deletions with approvals, pointer-check results, and `DONE`, `BLOCKED`, or `NON-CONVERGED`.
