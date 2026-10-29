---
name: wayfinder
description: 'Use when a greenfield project or large feature build will not fit in a single agent session and the route must be charted as decision tickets first. Not for implementation, remote credential changes, or work that fits in one session.'
---

# Wayfinder

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A greenfield project or a large feature build will not fit in a single agent session. |
| Authority | Human-gated for every outbound write: preview each remote issue creation, remote comment, remote close, remote assignment, and research-subagent dispatch with its exact target and consequence, and proceed only with explicit approval for that write. Local map files under `.outline/wayfinder/` are reversible local writes and need no approval. No remote mutation without approval; no credential use without approval. |
| Side effect | A decision map plus decision tickets stored locally by default, or on the approved remote tracker when the human explicitly chooses it; research findings linked from tickets. |
| Done | The route is clear: no decision remains before someone builds. The map is complete at the handoff edge with decision tickets resolved or front-loaded. |

## Inputs

- Idea or request (required): the loose idea, project brief, or feature request too big for one session, supplied by the human at invocation.
- Existing map reference (optional): a tracker issue URL, issue number, or local `.outline/wayfinder/map.md` path. When present, the skill enters work-through mode instead of charting.
- Storage choice (required before any write): `local` (default, complete path needing no tracker, no credentials, and no cloud service) or a named remote tracker the human explicitly approves.

## Procedure

### Mode selection

1. When an existing map reference is supplied, skip to step 9 (work through the map). Otherwise proceed to step 2 (chart the map). Done when mode is selected.

### Chart the map

2. Name the destination. Conduct an interactive interview with the human to pin down the target spec, decision, or state change that defines completion. Ask one question at a time; prefer single-select for directional choices. Continue until the destination is concrete enough that every subsequent decision tests against it. Done when the destination tests decisions.
3. No-fog early exit. When the interview reveals the route is already clear and the work fits in one session, stop. Ask the user how to proceed instead of creating an unnecessary map. Done when early exit is taken or the map is confirmed necessary.
4. Map the frontier. Conduct a breadth-first interview to surface open decisions and immediate first steps. Record every question phrased precisely now as a candidate ticket. Record questions not yet precisely phrasable as fog items. Done when all currently specifiable questions are candidate tickets and the rest are fog.
5. Preview and approve storage. Present the destination, the candidate tickets with their exact storage targets, and the consequence of each remote write or research dispatch. Obtain explicit approval: local-only proceeds without further gates; each remote write and each research dispatch needs its own approval bound to its exact target. When the human declines remote mutation, use local-only map files. Done when storage is chosen and every approved write is bound to an exact target.
6. Create the map. Local choice creates `.outline/wayfinder/map.md` and never touches a tracker; an approved remote tracker creates exactly one issue labeled `wayfinder:map`. Fill in `Destination`, `Notes` (domain, standing preferences, settled terms), `Decisions so far` (empty), `Not yet specified` (fog), and `Out of scope`. Parse and write local ticket frontmatter with a real safe YAML parser, never a handwritten subset or regex rewrite. Done when the map exists with all sections populated.
7. Create tickets. For each candidate ticket, create one child issue (remote, only when approved for that ticket) or one local file `.outline/wayfinder/tickets/<id>.md` with YAML frontmatter (`type`, `claimed_by: null`, `status: open`), a `Question` section, a `Blocked by` section, and a `wayfinder:<type>` label or local type field (`research`, `prototype`, `grilling`, `task`). Execute remote creations as separate commands and report each outcome; one failure never blocks the rest. Wire blocking edges in a second pass once ticket identifiers exist. Done when every candidate ticket exists with blocking edges wired.
8. Fire approved research dispatches. For each approved `research` ticket, launch one parallel subagent that resolves it and links findings from the ticket without merging anything. Stop; initial charting completes the session. Done when all approved research dispatches are launched and charting is complete.

### Work through the map

9. Load the map. Read the map body for destination, notes, and decisions so far. Query open tickets dynamically; open tickets never live in the map body. Done when the map is loaded and open tickets are known.
10. Work the frontier with accounting. Take the human-named ticket or the first frontier ticket (open, unblocked, unclaimed) in order. Claim it before any work by assigning the remote issue to the driver or setting the local `claimed_by` field. Resolve it, record it per step 12, graduate its fog per step 13, then continue to the next frontier ticket while session capacity holds and the frontier advances; research tickets may resolve in parallel. Stop and hand off with the map current when the session is full, the frontier is empty, or a blocker remains, and state which stop reason applies. Never leave a claimed ticket unrecorded. Done when every worked ticket is claimed, resolved, and recorded, and the stop reason is stated.
11. Resolve the decision. Read related or closed tickets on demand. For `research`, surface facts from docs, APIs, or local knowledge bases. For `prototype`, build a cheap concrete artifact and link it. For `grilling`, run batched single-select interview rounds and sharpen domain terms, recording settled terms in the map notes. For `task`, complete only the manual prerequisite that unblocks a decision; never build the destination. Done when the decision is resolved with evidence or a linked artifact.
12. Record and close. Post the resolution as a remote comment (only when that write was approved) or a local closing entry, linking created assets. Close the remote issue or set local `status: closed` and clear `claimed_by`. Append a one-line gist with link to `Decisions so far`. Done when the resolution is recorded and the ticket is closed.
13. Graduate fog. Move newly specifiable items from `Not yet specified` into new tickets (each remote creation approved as in step 7). Move invalidated or out-of-scope items to `Out of scope`; out-of-scope items never graduate. Close mis-scoped live tickets and record the one-line reason with link. Done when fog is graduated and invalidated items are moved out.

### Rules

- Refer by name. In all user-facing prose, refer to tickets by title, never by bare issue numbers, IDs, or slugs. The link wraps the name.
- Planning by default. Each ticket resolves a decision. The map is done when nothing remains to decide before someone builds. The pull to implement signals the map edge and time to hand off. An effort `Notes` section can explicitly carry execution into the map; without that instruction, produce decisions, never deliverables.
- Fog of war. The map stays deliberately incomplete: never pre-slice fog into ticket-sized pieces. Ticket when the question is sharp now; fog when it cannot yet be phrased sharply. One fog patch can graduate into several tickets, one, or none.
- Frontier accounting. The frontier decides what is worked and session capacity decides when to hand off. No fixed per-session ticket count defines completion; the run continues while frontier tickets resolve with verified progress and stops at a real boundary with the map current.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| `no-storage` | No writable local filesystem and no approved remote tracker. Stop and report the blocker. Never create a partial map. |
| `no-destination` | The human cannot name a destination after the interview. Stop. Never proceed with an ambiguous map. |
| `map-exists` | A `wayfinder:map` issue or `.outline/wayfinder/map.md` already covers this effort. Load it and enter work-through mode. Never duplicate the map. |
| `write-declined` | The human declines a remote write or dispatch. Keep the local equivalent and record the declined write. Never treat invocation as approval. |
| `write-failed` | Report the failed write with its target. Continue past it to the remaining approved writes. Never claim an unmade write. |
| `needs-build` | Resolving the decision requires building the destination. Stop at the decision boundary and hand off, unless `Notes` explicitly overrides. |
| `research-failed` | Mark the ticket blocked with the failure reason. Never invent evidence. |
| `out-of-scope` | Close the ticket, record the one-line reason in `Out of scope`, and keep it out of `Decisions so far`. |

Partial-result rule: the map and completed tickets are kept on failure. Never claim the route is clear while open decisions remain.

## Output

A map (local `.outline/wayfinder/map.md` by default, or the approved `wayfinder:map` tracker issue) with destination, notes, decisions so far, fog, and out-of-scope sections; decision tickets with type, question, blocking edges, claim state, and resolution; research findings linked from tickets; the frontier stop reason; and a handoff artifact when the route is clear.
