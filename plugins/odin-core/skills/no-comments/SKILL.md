---
name: no-comments
description: 'Use when asked to remove source comments by replacing them with clear code or accessible documentation. Not for deleting legal notices, required tool directives, or public documentation contracts without an equivalent home.'
---

# No comments

Remove the dependence on comments, then remove the comments. Preserve the knowledge and behavior that still matter.

Anchors: Dieter Rams (nothing left that the code or its documentation does not already carry), David Parnas (a comment describing a hidden decision moves into the module, its contract, its test, or its design record, never into the void).

## Scope and authority

Required input: the target files, directory, or code surface.

An implementation request authorizes reversible local changes to the target code and to the callers, tests, and documentation needed to preserve its contracts. An audit-only or plan-only request authorizes findings and proposed edits, not source changes.

Preserve explicit user exclusions. Do not edit generated or managed sources; identify their authoring source instead. Do not publish, change credentials, delete user data, or cross a public compatibility boundary without explicit authorization for that action and its consequence.

## Procedure

1. **Establish the complete target set.** Read repository instructions and the relevant code, including surrounding control flow and consumers. Discover languages, documentation conventions, and documentation consumers from the repository itself. Record unreadable files, generated sources, and uncertain spans as coverage gaps, never as silent exclusions. Done when: every target is covered or gapped by name.

2. **Inventory comments with a language-aware method that preserves comment tokens and source spans.** An AST alone may discard comments. Use lexical state to distinguish comments from strings, regular expressions, raw literals, template contents, and embedded languages. A textual search may locate candidates; it never decides what to delete. Record each comment's location, attached code, and purpose, including documentation comments and commented-out code. Treat docstrings and other runtime-visible documentation according to their actual language semantics (including introspection surfaces such as `__doc__`), not as disposable comment tokens. If no reliable tool exists for a language, read and account for its lexical forms manually. If classification remains uncertain, leave the span unchanged and report the exact gap. Never apply a naive strip. Done when: every real comment in reachable scope is inventoried and every uncertain span is gapped.

3. **Protect comments with legal or mechanical meaning.** Preserve license, copyright, attribution, and required legal notices. Preserve directives consumed by compilers, interpreters, build tools, formatters, linters, coverage tools, documentation generators, and code generators, including placement-sensitive annotations and delimiters. Identify the consumer before deciding that a directive is obsolete. An ordinary explanation of a business rule is not automatically a legal notice; preserve the rule's meaning through the implementation, invariants, tests, or documentation. Done when: every legal and mechanical comment is identified with its consumer and excluded from removal.

4. **Read what each remaining comment compensates for, then take the smallest complete action.** The no-information exception: a comment that carries zero information beyond its attached code (empty comment, repeated punctuation or whitespace ornament, narration that restates the code token-for-token with no reason, constraint, history, or contract, genuinely dead commented-out code with no design knowledge worth keeping) is deleted without a destination; record it as no-information with its one-line justification. Every other removable comment requires a destination before its source comment is removed: make intent visible through precise names, direct control flow, existing domain types, or a named constant, extracting a function only when it gives a real operation a useful boundary; express a required invariant in the code when doing so preserves the contract, or add or update a focused test when the constraint is behavioral, without introducing runtime assertions, allocations, or abstractions merely to replace prose; move irreducible design rationale, specification references, and incident knowledge into the repository's existing design-record or technical-documentation home, preserving the decision, its reason, and its connection to the affected code; resolve an actionable TODO within the authorized scope, otherwise preserve its useful obligation in the existing issue or task record before removing the marker, and never create a remote issue without approval; never silently erase unfinished work. Correct a misleading comment by establishing the actual behavior and intended contract first; never change working behavior to agree with an unsupported comment. A comment's category, length, or non-obviousness alone is never a reason to retain it. Done when: every removable comment is either deleted under the no-information exception with its justification or relocated to its destination and then removed.

5. **Handle public documentation as a consumer contract.** Before relocating API documentation, identify the documentation generator, packaged output, symbol association, examples, links, and any runtime documentation consumers. Relocate the content only when those consumers can still discover and use equivalent documentation. Update navigation, cross-references, generation inputs, and affected examples together. Preserve a mechanically required attachment comment when the established documentation system needs it. If equivalent discoverability or compatibility cannot be maintained, retain the affected documentation and name the exact constraint. Never turn comment removal into an unapproved documentation-system migration. Done when: relocated documentation is discoverable through its established consumers, or the blocking constraint is named and the comment retained.

6. **Remove every remaining removable comment in scope.** Retain only explicit user exclusions, legal or mechanical necessities, and comments whose useful contract cannot yet be preserved safely. Give each retained exception a specific reason tied to a consumer, invariant, compatibility mechanism, or approval; "helpful" and "design decision" alone are not sufficient. No-information deletions from step 4 stand as completed removals with their justifications; they are not retroactively required to name a destination. Done when: every target comment is removed, relocated with its content preserved, removed under the no-information exception with justification, or retained with a specific reason.

7. **Verify the actual change within the assignment's permissions.** Re-inventory the final source with the same language-aware method; check affected behavior, directive consumers, and documentation discovery where changed. Use the repository's existing checks rather than inventing a parallel verification system. A lower comment count alone proves nothing about correctness. If verification is prohibited or unavailable, state the unproved claims and the precise restriction instead of labeling them verified. Done when: the final inventory, behavior evidence, and documentation evidence support the reported result.

## Failures and recovery

- Unreadable target or uncertain syntax: finish independent reachable files, preserve uncertain spans, and report the uncovered scope. Do not claim complete removal.
- Unknown directive consumer: investigate its configuration and use before deleting the directive. Preserve it if its necessity cannot be established safely.
- Knowledge has no safe replacement: retain the comment and identify the missing invariant, documentation home, compatibility mechanism, or approval.
- Failed edit or verification: repair the source. If recovery requires undoing an owned edit, preserve unrelated and intervening user changes; never restore an entire stale file over them.
- Public contract change required: request approval for the exact change before crossing that boundary.
- Verification prohibited or unavailable: state the unproved claims and the precise restriction. Do not label them verified.

## Output

Return the implemented change, or the requested read-only proposal, with the target coverage and any uncovered files or spans, the structural changes and destinations of useful knowledge, the no-information deletions with their one-line justifications, the retained comments with their legal, mechanical, contractual, or explicit-exclusion reasons, and the evidence obtained with any remaining blocker. Completion means every target comment is accounted for, every removable comment is removed or relocated, useful contracts are preserved, and the evidence supports the reported result. No persistent ledger and no per-comment approval round is required for authorized local implementation; audit-only scope, explicit exclusions, and compatibility boundaries keep their approval gates.
