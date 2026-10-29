---
name: ideate-multiple-agents
description: 'Use when the user wants divergent ideas or an independently generated candidate pool grounded in the working repository. Requires at least two successful independent generation workers, a full-pool critic, and a separate reviewer. Not for refining one supplied idea: use brainstorm.'
---

# Ideate with independent agents

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user asks for divergent ideas, asks what to build, or requests independent candidate generation on an identifiable subject. |
| Inputs | Subject, working repository, optional constraints, and optional leading `format:html`. |
| Authority | Research, generators, critic, and reviewer are read-only. The coordinator may write only `docs/ideation/<slug>.md` and, when requested, `docs/ideation/<slug>.html`. No implementation, VCS, credential, paid, published, deployed, or remote mutation. |
| Observable done | At least two distinct independent generation workers returned usable grounded work under distinct assignments; every raw candidate received a critic verdict and an independent reviewer verdict; the written output accounts for the entire pool; every survivor carries a complete direction card; the result stops at intent clarification. |

## Inputs and preconditions

Parse the subject and optional `format:html`; reject unsupported flags. Derive `<slug>` by lowercasing the subject, replacing runs of non-alphanumeric characters with one hyphen, and trimming leading and trailing hyphens.

Reject an empty subject, empty slug, or target escaping `docs/ideation/`. Fix the output set before writing. If either requested target exists, report `blocked: target-exists`; do not overwrite it.

Require a real subagent facility that can run separate workers and return their outputs. Coordinator roleplay, sequential self-prompts, explorers, critics, and reviewers do not count as generation workers. Without that facility, report `blocked: independent-generation-unavailable`; do not substitute single-agent ideation.

## Problem frame

Before generating candidates, write a solution-neutral frame:

- Frame the problem as a "How might we..." question without embedding a proposed implementation.
- Name the target user or actor whose job or constraint is being addressed.
- State the observable result that would show the idea is useful.
- State the binding constraints that materially shape the idea.

If the target user or observable success cannot be established from the supplied context or repository evidence, stop with `blocked: intent-underdefined`. Ask only for the missing intent input. Do not generate candidates against an invented audience or success criterion.

Done when: the problem frame names the user, desired outcome, and material constraints, or the run stops with `blocked: intent-underdefined`.

## Independent generation requirement

Ideation MUST obtain usable contributions from at least two independent generation subagents with different assignments. The assignments MUST differ by frame, such as user value, workflow, architecture, reliability, constraint removal, or simplification. A critic or reviewer does not count as a generator. One agent role-playing multiple seats does not count.

Each generator returns candidates that include the idea itself, why the idea exists, its evidence basis, its user-facing value, its hardest feasibility risk, and its differentiating decision or capability.

Done when: at least two independent generators have returned usable, evidence-backed contributions, or each failed generator and its failure is recorded without pretending that a single generator satisfied the requirement.

## Candidate evaluation

For every candidate, record the user-facing value, the concrete pain or job relieved, the hardest feasibility dependency, and the differentiating decision or capability.

Reject a candidate that cannot name a user-facing value or that is only a restatement of an existing survivor. Preserve a high-value but difficult candidate only when the feasibility risk is explicit and the reviewer can state why it is worth that risk.

Done when: every candidate has an evidence-backed value, feasibility, and differentiation assessment, or has been rejected with a reason.

## Survivor direction card

Every surviving candidate receives a direction card containing:

- Problem statement.
- Recommended direction.
- User value.
- Feasibility and hardest risk.
- Differentiation.
- Key assumptions to validate.
- MVP scope limited to one user job and the riskiest assumption.
- Not doing, with a reason for every excluded item.
- Open questions.

A survivor without a complete direction card is not ready for intent clarification.

Done when: every candidate is either rejected with a reason and evidence or survives with a complete direction card, and no candidate disappears between generation, critique, and adjudication.

## Procedure

1. Write the problem frame first per the section above. Then ground the subject. Read the smallest relevant repository surfaces. Record existing architecture, patterns, and constraints with `file:line` citations.
   - For one known concern, use one read-only explorer.
   - For multiple or uncertain concerns, use three parallel explorers.
   - For a cross-module or architectural subject, use five parallel explorers.
   Explorer work supplies evidence, not the required generation count. If evidence cannot identify the subject, report `blocked: subject-unidentified`.
2. Fix distinct generation assignments. Create at least two assignments crossing repository-relevant topic axes with different frames, such as user workflow, architecture, reliability, small changes with large effect, or constraint removal. Record each worker's id, axis, frame, scope, and expected return. Give every worker the same grounding summary and constraints, but a distinct assignment. Do not pass another generator's candidates, the coordinator's preferred answer, or an emerging shortlist. Assignments must differ in the work they ask for, not merely in persona names.
3. Dispatch independent generation. Launch the generation workers together. Request roughly six to eight concise candidates per worker, each containing an idea, rationale, and basis. A basis is a repository `file:line` anchor or `external:<source>` for a source actually inspected. Distinguish the existing fact from the proposed change; evidence for an opportunity is not proof of future results. Assign stable candidate ids using worker id and local sequence. Preserve every returned candidate, including unsupported, duplicate, or malformed proposals, in the raw pool. Each candidate must include its idea, why it exists, evidence basis, user-facing value, hardest feasibility risk, and differentiating decision or capability.
4. Establish the generation precondition. A successful generation worker is a distinct worker that completed its assignment and returned at least one usable candidate with an idea, rationale, and inspected supporting basis. Require at least two successful workers with distinct assignments. A worker returning only criticism, an empty response, or ungrounded suggestions does not qualify. Wait for every assigned worker to return or reach an explicit failed state. Record failures and partial outputs. If an assignment needs replacement, give a separate generator the same uncovered axis without exposing the pool. Continue only after the successful-worker minimum and assigned-axis coverage hold. If they cannot be achieved, report `incomplete: independent-generation`, the successful count, failed assignments, and partial pool. Do not produce a success artifact or silently narrow the assignment set.
5. Critique the full raw pool. Give one separate read-only critic the grounding summary, assignment inventory, complete raw pool, and worker outcomes. Require `survive` or `reject` and a reason for every candidate id. Apply the Candidate evaluation section: a candidate survives only when its cited basis supports the opportunity, it names a user-facing value, it is feasible in this repository, it changes a meaningful decision, and it is not a restatement of another survivor. Unsupported candidates remain visible as rejections. Duplicate rejections name the retained candidate id. Do not filter the pool before the critic sees it.
6. Adjudicate independently. Give a separate read-only reviewer the same grounding and raw pool, every critic verdict, and the generation inventory. The reviewer must be neither a generator nor the critic. Require an audit of generation independence, assignment coverage, citation accuracy, scope, consistency, and candidate accounting. Require one final `survive` or `reject` verdict with a reason for every raw candidate id. The reviewer may correct the critic and must state why. Use the reviewer's survivor set. Do not rescue a rejection or remove a survivor by coordinator preference. A missing, invented, or repeated candidate id, missing reason, or unsupported survivor is `non-converged: incomplete-adjudication`. Return it for correction; if correction is unavailable, stop before writing a success artifact.
7. Assemble the result. Write the canonical Markdown with these sections: subject; problem frame; grounding context and citations; topic axes, generation frames, and worker identities and outcomes; survivors, each with candidate id, direction card per the Survivor direction card section, rationale, evidence, and final verdict reason; rejected candidates, each with candidate id, proposal, available evidence or explicit evidence absence, and final rejection reason; next step: clarify the user's intent among the survivors. Every raw candidate must appear exactly once in the survivor or rejection sections. Preserve the full critic and reviewer verdicts in an accounting table keyed by candidate id; this table may reference the candidate sections rather than repeat their prose. Require `raw count = survivor count + rejection count`. Zero survivors is a valid adjudicated result, not permission to invent a winner. Ask whether to revise the subject or constraints rather than asking the user to select a nonexistent survivor.
8. Write the fixed output set. Create `docs/ideation/` if needed, write only the fixed targets, and read the result back for candidate accounting and evidence completeness. When `format:html` was requested, render one self-contained HTML view of the canonical Markdown without adding or omitting substantive content. Check parity for headings, problem frame, worker outcomes, ids, survivors, direction cards, rejections, reasons, citations, and next step. Markdown remains canonical.
9. Stop at intent clarification. Report the exact output set, successful generation-worker count, raw candidate count, survivor count, and rejection count, and any recorded worker failures. Ask which surviving direction best matches the user's intent, or whether to revise the subject when none survived. Do not plan, implement, stage, or commit a survivor.

## Failure and recovery

- Missing or unidentified subject, or missing user or observable success for the problem frame: report the missing input or `blocked: intent-underdefined` and write nothing.
- Existing target: report `blocked: target-exists`; do not overwrite or select another output path silently.
- Independent workers unavailable, fewer than two successful generators, or uncovered assignments: return the explicit incomplete result. A critic or reviewer never supplies the missing generator count.
- A worker fails after returning candidates: retain those candidates in the raw pool and record the worker failure. Its partial result does not count as successful completion.
- Citation missing or unsupported: retain the candidate and require an explained rejection; never invent a citation.
- Critic or reviewer unavailable: return the pool and missing role as incomplete; the coordinator does not impersonate that role.
- Incomplete adjudication: name the affected candidate ids and stop before a success artifact.
- Survivor without a complete direction card: not ready for intent clarification; complete the card or reject the candidate with a reason.
- HTML mismatch: report `non-converged: html-parity`; do not claim the requested output set is complete.
- Write or read-back failure: report exact created paths and the failure. Remove only newly created incomplete output files owned by this run after preserving any user-requested diagnostics. Never delete pre-existing files.
- No justified survivors: preserve the reviewed rejection record and state that no candidate survived.

## Output

Canonical `docs/ideation/<slug>.md`, optional equivalent HTML, generation assignment and outcome inventory, complete candidate accounting, direction cards for every survivor, counts, and an intent-clarification prompt.

An incomplete result names the unmet precondition, affected workers or candidate ids, available partial evidence, and what would unblock it. It never claims successful independent ideation.
