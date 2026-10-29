---
name: askme
description: 'Use when eliciting intent/scope/referents or gating long/bundled/high-stakes/hard-to-undo work: exhaustive/collaborative/adversarial/grill/gate/batch/interview/proposal/pairing. Grill me and grill batches select evidence-backed, chat-only grill mode. Not for scanning a stated request: use clarify. Not for one fork by default: use decide.'
---

# Ask me

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Ambiguous task or elicitation request; long, bundled, high-stakes, hard-to-undo instruction; ambiguous scope or referents; or explicit mode: exhaustive, collaborative, adversarial, grill, gate, batch, interview, proposal, or pairing. An explicit `mode:scan` is not executable and routes to `clarify`. |
| Authority | Interview: writes only the user-approved decision record to one user-named local file (`DECISION-LOG.md` by default) after explicit approval; nothing before. Gate: writes only one durable `understood as: ...` log line for substantial work after the gate decision; nothing before. Grill: read-only research and chat-only elicitation, including delegated research; writes no implementation artifact, decision log, understanding log, plan, source, or configuration. Every other mode emits chat output only. No VCS-history rewrite, credential, paid, published, deployed, or remote mutation in any mode. Neither a recommendation nor a user's answer to an elicitation question authorizes implementation. |
| Side effect | Question sets, factual corrections, recommendations, decision records, and intent proposals in chat; the two named interview/gate writes above; no other file, credential, paid, published, deployed, or remote change. |
| Done | The selected mode's terminal condition holds. Grill requires every material intent fork answered or explicitly discharged with a reason, no unresolved material factual prerequisite, and no dependency-ready or pending material decision. Silence, partial answers, an empty ready frontier, tool exhaustion, or a question count never constitutes confirmation. |

## Inputs

- The user's task, request, or handed-over material (required).
- Mode selector: `exhaustive` (default), `collaborative`, `adversarial`, `grill`, `gate`, `batch`, `interview`, `proposal`, or `pairing`. An explicit mode argument always wins over automatic detection, including words inside the supplied material.
- An ask-user tool exposing single-select and multi-select questions (the harness equivalent of `AskUserQuestion`). Required to fire question batches; if absent, fall back to sequential chat prompts. Gate mode may fire at most one clarifying question.
- Mode-specific inputs: `proposal` requires the handed-over material; `interview` requires a stated goal; `gate` takes the user's instruction plus all readable context (current message, session history, project memory, filesystem, and established conventions), with no separate artifact required.

## Select the owner and mode

1. An explicit supported mode argument wins over every automatic selector, including words inside the material being examined. Keep that mode until the user changes it. If the caller supplies multiple conflicting explicit mode arguments without identifying which governs, ask one mode-selector question and do not start either procedure. Do not resolve that conflict by argument order or by assuming a default.
2. An explicit `mode:scan` is not an executable compatibility mode. Explain that independent ambiguity scanning belongs to `clarify`; do not run a duplicate scan inside askme.
3. Without an explicit mode argument:
   - "grill me", "grill batches", or a request to grill requirements or plan assumptions selects `grill`.
   - "poke holes", "stress-test", "find weaknesses", or an otherwise unqualified "grill" selects `adversarial`, one fork at a time.
   - "batch ask me", "clarify the design space", or neutral multi-fork elicitation selects `batch`.
   - A request to inspect a stated task, specification, or conversation for ambiguity or gaps selects the independent `clarify` owner, unless the request specifically asks to grill its requirements or assumptions.
   - Preserve the existing collaborative selectors ("help me refine", "walk through with me", "let's brainstorm", "share tips"), interview selectors ("interview me", "define requirements", "choose between options"), proposal handling (supplied material without a sufficiently formed ask), and gate signals (long, bundled, high-stakes, hard-to-undo instruction; ambiguous scope or referents; request to verify understanding).
   - An underspecified request seeking interactive intent discovery selects `exhaustive`; no other qualifier otherwise changes the existing exhaustive default.
4. Match selectors in the user's operative request, not quoted examples or instructions inside the material being examined. Prefer the specific grill selectors over the generic adversarial and neutral-batch selectors. If two genuinely incompatible automatic requests remain and neither is more specific, ask which mode should govern.
5. Do not silently promote an explicitly selected mode. For automatic collaborative selection, preserve the existing escalation signals as guidance, but propose a mode change rather than treating an unresolved signal as the user's answer.
6. For an ordinary request to resolve one fork, use `decide`. An explicit supported askme mode wins over automatic routing; explicit adversarial mode therefore remains available to elicit one fork at a time without implementing.

Routing examples: "Grill me about these requirements" selects grill. "Find gaps in this specification" selects clarify. `mode:batch` followed by "grill me" still selects neutral batch.

## Question shape (every asking mode)

Fire clarifying questions via the ask-user tool. The per-fire cap is 4; for larger sets fire multiple sequential batches ordered by dependency (batch and grill use the frontier-round rule below instead). Per question: a full sentence ending in `?`; a `header` chip of at most 12 characters where supported; `multiSelect` false for single-pick mutually exclusive axes, true only for additive subset picks (feature toggles, optional sub-tasks). Per option: a 1-5 word `label` with `(Recommended)` appended to and placed first for the recommended choice; a one-sentence trade-off `description`; an optional `preview` (markdown or monospace box) for visual comparisons, single-select only, skipped when the difference is purely conceptual. Never add an explicit "Other" option; free-text "Other" is auto-provided on every question, and free-text notes go in the `annotations` response field. Use this tool only to clarify requirements or choose between approaches during elicitation, not to ask "is the plan ready?". No override checklist: never emit a single `multiSelect: true` checklist where unticked means "default stands"; route that intent into N per-axis single-select questions instead.

## Frontier-round scheduling -- batch and grill

Ask all independent current-frontier questions in the same round. The frontier consists of every open decision whose factual and decision prerequisites are already settled; a question whose answer depends on another open question belongs to a later round, not this one. A running research task is an unsettled prerequisite, so only its downstream questions wait.

- Route at most four questions per tool fire.
- When the frontier exceeds four, send the four highest-impact questions through the tool. Rank by downstream decisions unblocked; break ties toward the least safe default to assume.
- Put every remaining frontier question in that same message as:

  ```markdown
  **Q<n>: <question title>**

  <Question body and choices>

  -> Recommended: <answer>
  ```

- Tool and Markdown answers belong to one answer set. Do not omit overflow questions or split the ready frontier into successive tool-only rounds.
- Preserve stable ids across tool and Markdown forms.
- If the harness only supports single-question interaction, use sequential prompts in dependency order. With no question tool, present the numbered questions in chat and await replies. Missing tool support never supplies an answer.

The three batch-family modes remain distinct:

| Mode | Method retained |
|---|---|
| `adversarial` | Challenge one fork, recommend an answer with a reason, wait, then follow dependencies parents-first. Do not batch it implicitly. |
| `batch` | Neutral design-tree elicitation, retaining weighted intent hypotheses and falsifiers before the first fire. Share frontier scheduling without imposing per-question counterexamples. |
| `grill` | Evidence-backed challenge of requirements and assumptions, concrete counterexamples, recommended verdicts, and independent frontier batches. No mandatory VS block. |

## Mode gate: check, restate, cross-check, decide

1. Recognize when the instruction is long, multi-part, ambiguous in scope or referents, deliberately flexible, high-stakes, or hard to undo enough that a wrong read costs real work. If none of these signals is present, stop without acting.
2. Paraphrase the instruction in the agent's own words. Do not copy the user's wording and treat that as understanding.
3. Compare the restatement against all available context: the current message, session history, project memory, filesystem, and established conventions. Look for contradictions, missing antecedents, or two plausible readings that context cannot choose between.
4. If context resolves every fork, proceed silently without surfacing a question. If a genuine fork survives, surface exactly one specific clarifying question anchored to the restated understanding and name the choice. Perform no file, credential, paid, published, deployed, or remote mutation before this decision; after it passes, substantial work must write one durable `understood as: ...` log line.

## Mode proposal: read, then propose

Read every piece of the handed-over material end to end before proposing anything. State the intent read from the data in one line grounded in what the data actually shows, sketch the next action briefly, and propose only to confirm: right, wrong, or adjust. If two intents are plausible, propose the likelier and name the other in a clause; one intent per turn.

## Mode interview: one assumption at a time

State that this is a requirements interview and confirm whether the goal is defining requirements, resolving a decision between options, or both; begin no file change, build, or investigation until the decision record is approved. Ask one focused question that exposes the most fundamental unstated assumption in the stated goal; wait for the response; restate what was confirmed or corrected and add it as a row in the running decision log; after each answer ask "What else is unstated or assumed in this goal?" Stop when the user says nothing remains, explicitly declines, or confirms the record is complete. Present the complete log (each assumption, its resolution, and the final agreed scope or decision; no implementation plan), ask the user to approve, amend, or reject any row, and repeat until approved. Write the approved record to a local file named by the user or defaulting to `DECISION-LOG.md` in the current working directory.

## Modes exhaustive, adversarial, and batch: Verbalized Sampling (VS)

Sample multiple intent hypotheses; assign each a probability weight on a 0-1 scale; state the falsifier (the specific observation or scenario that would invalidate it) per hypothesis. Expand hypothesis depth as ambiguity, risk, or architectural surface grows; keep it concise when scope is truly narrow. Render the VS block immediately before the first question fire of the session; subsequent intra-session fires need not repeat it unless the survivor set materially changed. Use this format:

```
1. [Weight: 0.42] hypothesis here
   - Falsifier: [observation or scenario that would invalidate this]

2. [Weight: 0.28] hypothesis here
   - Falsifier: [observation or scenario that would invalidate this]
```

For batch mode, seed the design-tree roots and initial frontier from the surviving hypotheses. Collaborative mode never runs VS. Grill mode has no mandatory VS block; its concrete evidence, counterexamples, and decision ledger provide the required basis.

## Mode exhaustive: exploration

Deliberately seek unconventional, underexplored, and edge-case possibilities relating to the user's objective, drawing on context and plausible but non-obvious requirements. Include at least 3 edge cases (at least 5 if architectural); stop expanding once additional cases no longer change decisions. Broaden sampling if no clear leader emerges. Synthesize surviving hypotheses into one consolidated direction before responding.

## Mode collaborative

Two-way tip-sharing dialogue: surface one of the agent's own observations or tips back to the user as a counter-tip per round; let depth emerge through exchange. Do not run VS. No scoring, no ranked sample. Stop when the user signals convergence.

## Mode adversarial: walk the tree one fork at a time

Per fork: state the question, recommend an answer with a one-sentence rationale, wait for the user, and do not proceed on assumed answers. Resolve dependencies parents-first; do not descend into children while a parent is unresolved.

## Mode batch: frontier rounds

Build a design tree where each node is a decision; the frontier is every decision whose prerequisites are already settled, the questions to ask now without guessing at answers not yet heard. Each round, ask the whole frontier using the shared frontier-round scheduling rule above, each question with a recommended answer. Finding facts is the agent's job, not the user's: when a frontier question needs an environmental fact (filesystem, tools, codebase), dispatch a subagent to find it and never ask the user for something that can be looked up directly. Recompute the frontier once after each full answer set; do not resample VS unless user answers materially change the survivor set. A partially answered batch is not done; re-fire only the unanswered axes, not the whole batch.

## Mode grill: evidence-backed frontier elicitation

Grill authority: read-only research and chat-only elicitation, including delegated research. Write no implementation artifact, decision log, understanding log, plan, source, or configuration. Perform no VCS, credential, paid, published, deployed, or remote mutation. Recommendations, silence, exhausted questions, and completed elicitation do not constitute implementation authorization or automatic user confirmation.

1. Bind the scope. Identify the requirements, plan assumptions, or intent being examined. Read the supplied material and relevant settled conversation answers. Stay inside the requested surface; do not expand a requirements interview into an architecture replacement or implementation task.
2. Verify facts before building questions. Resolve claims about existing files, APIs, callers, configurations, tool capabilities, and established behavior through relevant read-only evidence. Cite the inspected source for each material correction. If a premise is wrong, correct it before asking a question built on it. Remove forks that exist only because of the false premise. When a fact remains inaccessible after relevant reachable research, record the missing fact, attempted sources, and affected decisions. It remains a factual prerequisite, not a disguised preference question. Continue independent reachable work.
3. Track decisions and dependencies in chat. Give each material fork a stable id, its prerequisites, and one state: open, answered, or discharged. Record answers with their substance and discharges with their reason. Separately track factual prerequisites as resolved or unresolved. Preserve prior settled answers. Reopen one only when the user changes it or new evidence exposes a concrete conflict; name the old answer and the reason before reopening it.
4. Challenge each current fork concretely. Identify the assumption or choice, show a concrete counterexample or failure scenario, and explain which requirement or invariant it threatens. Label hypothetical scenarios as hypothetical. Do not present them as observed defects. Recommend a verdict and an answer with a concise reason. Distinguish an evidence-resolved factual conclusion from a user-owned trade-off. If the evidence already disposes of the issue, record the conclusion and basis without asking the user to confirm a fact. If genuine intent remains open, ask the decision question. A recommendation never settles that question.
5. Ask the independent current frontier together. The frontier consists of all open intent decisions whose factual and decision prerequisites are settled. Use the shared frontier-round scheduling rule and shared question format. Do not ask a child decision while its parent is unresolved. A running research task remains an unresolved factual prerequisite. Include each question's concrete scenario and recommended verdict in its body; do not create a second duplicate questionnaire for the challenge.
6. Incorporate the answer set without losing state. Settle only the axes the user actually answered. A free-text answer may settle several ids when its meaning is unambiguous; record that mapping. Preserve unanswered ids and their dependencies. For partial answers, ask only the remaining unanswered axes from the current round; do not re-fire settled questions or advance their dependent children while the round remains incomplete. An explicit "skip" leaves an axis open unless the user explicitly discharges it. A discharge records why the decision no longer needs resolving and its consequences. After the current answer set is complete, recompute the frontier. If the user changes a parent answer, revisit only the affected descendants and preserve unrelated settlements.
7. Close by decision state, not question count. Finish only when every material fork is answered or explicitly discharged, required facts are resolved, and no material pending dependency remains. An empty ready frontier with pending blocked nodes is incomplete. Report the exact blockers and continue other reachable work. When the whole material frontier is exhausted, emit the agreed scope, answers, discharges, factual corrections, and remaining nonblocking caveats in chat. Do not manufacture another question or ask "is the plan ready?" merely to prolong the session. Do not claim user confirmation beyond the answers actually given. Do not implement or write an artifact.

A recommended verdict means a concrete disposition such as "Reject silent data loss; recommend reporting an explicit failure" or "Keep the requirement, but narrow it to authenticated users." It is not a numerical severity score or an unsupported claim that a defect occurred.

## Mode pairing: persistent elicitation posture

Explicitly selected persistent pairing posture only (never auto-detected). While active: meaningful forks return to elicitation until the user disengages (`go ahead on your own`, `full autonomy`, `you drive`, `/duet off`, or similar). Settled picks survive disengagement as load-bearing decisions. On rubber-stamping (two consecutive unengaged accepts) or answer fatigue, coarsen: ask fewer, bigger-stakes questions and raise the fork threshold. Elicitation only — this mode executes no changes and authorizes no irreversible action. Reuse the batch frontier, preview, dependency, and harness-mapping rules above.

## Escalation (collaborative to adversarial)

Promote mid-session when any of these fire: (a) ambiguity cardinality of at least 2 valid architectural decisions surfaces from a single user message; (b) the user references "the function" or "that file" without a concrete path; (c) the user describes a goal without a verifiable done signal. These signal patterns are guidance, not a hard rule; the user can always override mode via argument.

## Harness mapping

If the harness exposes only single-question prompts, fire them sequentially in dependency order; the shape (clarifying questions with one Recommended each) is what matters, and batching is an optimization. Map `(Recommended)` to whatever default-marker convention the harness uses; the rationale belongs in the description body either way. If no multi-pick mechanism exists, decompose additive picks into N independent single-selects.

## Stop

Terminate when the mode's terminal holds: exhaustive: every clarifying question answered or discharged and intent confirmed; collaborative: the user signals convergence; adversarial: every fork resolved; grill: every material fork answered or explicitly discharged, required facts resolved, and no material pending dependency remains; batch: frontier empty and shared understanding confirmed; interview: record approved and written; proposal: the user replied yes, correction, or adjust; gate: no read signal and the gate stopped, or the restatement was paraphrased and context-checked, every fork was resolved or its one question answered, and no action started prematurely; pairing: disengagement with the retained pick set recorded, or a blocking unknown reported. Do not proceed on non-trivial changes without visible VS (exhaustive, batch), completed fork resolution (adversarial, batch, grill), or a passed gate (gate).

## Failure and recovery

- Gate sees no read signal or context resolves every fork: pass silently; do not surface a question.
- Gate restatement does not match the instruction: surface the mismatch as the first finding and stop until it is resolved.
- Gate finds multiple genuine forks: surface the highest-stakes one first and hold the rest pending resolution.
- A gate question is later resolved by context: retract the question and pass silently.
- A genuine gate fork survives: ask exactly one specific question anchored to the restated understanding, then hold substantial work until it is answered.
- Unresolved fork or blocking unknown (adversarial, batch, grill): stop; report the blocking unknown and the unresolved fork. Do not assume an answer or descend into children.
- Grill ready frontier is empty because remaining nodes depend on an unanswered parent or unavailable fact: report incomplete with the exact pending ids and prerequisites. Do not announce successful completion.
- Grill user says "skip this" or a question times out: the axis remains open unless explicitly discharged with a recorded reason. No default acceptance.
- Grill user gives an explicit resource limit before closure: stop at that boundary with an incomplete outcome and preserved decision state; do not claim success.
- Grill participant asks to save a record or implement: grill itself writes nothing and implements nothing. Return the current decision state in chat; saving or implementation requires a distinct authorized task rather than an automatic transition.
- User answer contradicts a falsifier (batch): update the survivor set, adjust the design-tree roots, and recompute the frontier. Do not discard already-settled answers.
- No clear leader after broadened sampling (exhaustive): broaden sampling further or surface the decision point with concrete options and trade-offs. Do not silently pick.
- Fact lookup fails or is inconclusive (batch, grill): record the prerequisite as unresolved with attempted sources, block dependent decisions, and continue independent reachable work. Never ask the user for a fact that can be looked up, and never guess a fact to avoid asking.
- Empty goal (interview): ask for the goal before proceeding; stop if the user declines to supply one.
- User abandons or asks to implement mid-interview (interview): end the interview with no file written and report "no decision recorded", or decline and redirect back to the interview until the record is approved. Preserve the existing approved decision-log write; grill adds no change to it.
- Decision log written before approval (interview): delete the file. The log is written only after explicit user approval.
- Data too thin to propose from (proposal): say so and stop. Do not fall back to asking.
- User composes the ask from scratch (proposal): the proposal was wrong or a question in disguise; redo the proposal grounded in the data.
- User refuses to answer or signals non-convergence: record the discharged questions and the open ambiguity. Do not pretend intent is confirmed, and do not act on a partial understanding.
- Ask-user tool unavailable: fall back to sequential single-question chat prompts in dependency order; if no question tool exists at all, emit the question set as chat text and await replies.
- Partial-result rule: for a multi-step instruction, verify the read for the whole before beginning any part; a partial misread blocks action. For batch and grill modes, a partially answered batch is not done; re-fire only the unanswered axes, not the whole batch.
- Non-mutation rule: before a gate passes, make no file, credential, paid, published, deployed, or remote mutation. After a passed gate, substantial work must write one durable "understood as: ..." log line; interview mode may write only its approved decision log; grill and every other mode write no files. The blocked or non-converged result is an explicit list of open ambiguities and discharged questions, not a fabricated confirmation.

## Output

Per mode, chat output only except where named. Exhaustive, adversarial, and batch emit the VS block (once, before the first fire), the batched question sets, and a terminal intent summary stating the consolidated direction, assumptions, and discharged questions; batch additionally ends on the user's confirmation of shared understanding. Grill emits the decision ledger (ids, prerequisites, states), concrete counterexamples with recommended verdicts, the frontier question sets, and a terminal summary of agreed scope, answers, discharges, factual corrections, and nonblocking caveats; it writes no files and implements nothing. Interview emits the presented decision log, then writes the approved record to `DECISION-LOG.md` or a user-named file. Proposal emits the one-line intent proposal, the next-step sketch, and the confirm/correct/adjust prompt. Gate emits nothing when no read signal is present or context resolves every fork; when a genuine fork survives, it emits exactly one specific clarifying question anchored to the restated understanding.
