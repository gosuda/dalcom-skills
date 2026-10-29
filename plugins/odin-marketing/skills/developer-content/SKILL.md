---
name: developer-content
description: 'Use when preparing an evidence-backed developer content package with runnable examples and accuracy checks. Not for publishing, fabricating results, or unverified performance claims.'
disable-model-invocation: true
---

# Developer content

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks for a tutorial, guide, comparison walkthrough, troubleshooting piece, or technical announcement package. |
| Authority | Read-only preparation. Tutorials, guides, comparisons, troubleshooting, and announcements are modes of this one owner, not separate channel wrappers. No publication, no execution implied by drafting. |
| Side effect | A content package in chat the user can hand to `technical-article-writer`. Nothing published. |
| Done | Audience, goal, format, prerequisites, outline, runnable examples with expected output, error handling, tradeoffs, sources, and next steps are present; every code block is marked verified or unverified; no fabricated result, fictional case study, or unverified speedup claim remains. |

## Not for

- Publishing, distribution, or vendor-required production. Formatting and design tools are optional references, never required dependencies.

## Inputs

- `audience` (required): who the piece serves and their starting point.
- `goal` (required): the one thing the reader can do afterward.
- `material` (required): supplied code, docs, or an explicitly requested read-only research pass.
- `mode` (optional): tutorial, guide, comparison, troubleshooting, or announcement. Defaults to guide when omitted.

## Procedure

1. Fix audience, goal, and mode. State prerequisites including imports, versions, and setup. **Done when:** a reader matching the prerequisites can start.
2. Build the outline with progressive complexity: concept, minimal working example, real variation, errors, tradeoffs, next steps. **Done when:** each section names what the reader can do after it.
3. Prepare runnable examples with exact inputs, expected output, and error handling plus troubleshooting for the likeliest failures. **Done when:** every example has inputs, expected output, and at least one failure path.
4. Mark every code block verified (ran against the stated versions) or unverified (not run, with what would verify it). **Done when:** no block lacks a mark.
5. Attach sources for every factual claim and forbid fictional case studies and unverified multiplier claims. **Done when:** each claim traces to a source and no multiplier lacks measurement.
6. Submit the package to technical-accuracy review as a checklist the author runs: versions, imports, outputs, errors, links. **Done when:** the checklist is complete with pass or flagged items.

## Failure and recovery

- Example cannot be verified: mark unverified, state what verification needs, keep it only if the unverified status is visible beside it.
- Material too thin for the goal: narrow the goal or name the missing material.

## Output

A content package: audience and goal, prerequisites, outline, runnable examples with expected output and error paths, tradeoff notes, source list, next steps, verification marks, and the accuracy checklist result.
