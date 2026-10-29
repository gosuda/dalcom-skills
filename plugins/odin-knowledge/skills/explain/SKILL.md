---
name: explain
description: 'Use when a scoped question about how or why something has its current shape, or what happened over a work window, needs an evidence-grounded answer. Not for judging adoption, capturing durable learning, or diagnosing a failure to fix.'
---

# Explain

Anchors: David Parnas (an explanation hides nothing its consumer needs: evidence, limits, and unknowns are the interface), Dieter Rams (no filler around the answer).

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A person or calling workflow asks what something is, why it is shaped this way, or what happened over a bounded window, with an identifiable subject and intended use. |
| Authority | Read-only research and composition. Writes a standalone artifact only when the intended use needs one. No implementation, diagnosis-to-fix, durable memory maintenance, judgment of adoption, or publication. Publication needs separate explicit confirmation. |
| Side effect | An answer with supporting evidence, preserved constraints, and material unanswered questions; optionally one artifact at its path. |
| Done | The scoped question is answered with evidence and limits, or the specific blocker is returned. A verified behavior may be reported while its historical rationale stays explicitly unknown. |

## Inputs

- The subject: question, concept, change, or work window from the request and available context. Required.
- The intended reader and use (working answer vs teaching artifact, inline return vs file). Required; depth follows it, not the caller identity.

Resolve discoverable facts before asking. Ask only when missing information materially changes the answer and cannot be resolved from the request or evidence. A bare invocation with no recoverable subject needs clarification, not an invented topic.

## Procedure

1. Establish the question and use. Explain only the requested subject. An empty diff range or empty work window ends in an explicit no-activity result, not a substitute subject, unless the request permits a substitution and the substitution is named in the result and artifact.
2. Gather scoped evidence from the repository and current sources first. Use existing adequate evidence when it is current; check claims whose support is missing, disputed, or affected by source changes. A function call never establishes guarantees about its uninspected implementation. Keep attribution accurate when work spans multiple authors.
3. Compose the answer from the evidence. State the mechanism and its consequential constraints. Before delivery, check every factual claim against its source; remove unsupported claims or mark their uncertainty where they appear, including in diagrams and examples. Disclose selection when the requested scope cannot hold the full evidence; never present a partial account as exhaustive. Distinguish documented rationale from inference and from unknown.
4. Deliver at the intended shape. For a workflow return, deliver the content directly with the evidence, constraints, and unanswered questions it needs, and leave continuation to its owner with no destination menus. For a standalone artifact, write the selected format and return an inline summary plus the file path. Public publishing never runs headless and never follows from naming a host; without confirmation after the publishing warning, preserve the local artifact and report its path.

## Failure and recovery

- No recoverable subject: ask for it once; stop without an artifact when none arrives.
- Evidence missing or contradictory: report the gap and its consequence; do not wait silently or invent the answer.
- Historical rationale unknown: state it as unknown in the body, not as a guessed explanation.
- Request is actually a judgment, new alternative, implementation scope, or fix request: route to the owning job instead of answering here.
- Publication requested without confirmation: do not publish; report the local path.

## Output

Return the answer with cited evidence, preserved constraints, unanswered questions, and, when requested, the artifact path. No follow-on work, destination choice, or memory write follows from an explanation alone.
