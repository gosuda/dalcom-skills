---
name: pr-impact-quiz
description: 'Use when the user invokes this skill to generate targeted questions proving the author understands the change''s codebase effect. Not for reviewing the change: use review.'
disable-model-invocation: true
---

# PR impact quiz

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants a small set of impact questions proving the author understands how the change affects the existing codebase. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | Chat output of three impact questions. |
| Done | Three impact questions are generated for the author to answer. |

## Inputs

The skill requires:

- PR/MR description: The authored description of the change (GitHub PR or GitLab MR, author-supplied; this skill makes no forge call), including motivation, scope, and expected behavior. Required.
- Diff or change summary: The diff or a structured summary of what changed, from either provider. Required.
- Codebase context: The language, primary modules, and key patterns in the affected area. Required.
- MR context (GitLab only, optional): source and target branch names plus draft state, supplied by the author. When present, one question must probe target-branch compatibility (fork MRs bind source and target projects separately). Provider ambiguity never triggers a remote read, since the author supplies the text.

## Procedure

1. Read the supplied PR/MR description and diff or change summary. Done when: the description and diff are read.
2. Identify the primary modules, interfaces, and data flows the change touches. Done when: the touched modules, interfaces, and data flows are identified.
3. Identify possible effects on callers, downstream consumers, or shared state. Done when: possible effects on callers, consumers, and shared state are identified.
4. Write three impact questions that require the author to confirm how the change affects the existing codebase. Each question must target a specific area of the codebase (not a generic concern), require a concrete answer (not a yes/no or "I checked"), and probe a different impact axis (call-site behavior, data invariants, or backward compatibility). Done when: three concrete, non-generic questions probing distinct impact axes are written.
5. Present the three questions in the chat output. Done when: the three questions are presented in chat.

## Failure and recovery
| Failure class | Condition | Result |
|---|---|---|
| Missing input | PR description or diff is absent or empty | State what is required and do not generate questions. |
| Empty diff | Diff contains no changed lines | State that no changes are present and do not generate questions. |
| Non-converged | Questions are generic, redundant, or require only yes/no answers | Stop; do not present. The done predicate does not hold. |

No rollback is required. No partial result is returned when the done predicate does not hold.

## Output
Three concrete, non-generic impact questions in chat, each addressing a distinct area of potential effect on the existing codebase.
