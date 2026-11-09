---
name: autoplan
description: 'Use when the user runs /autoplan on a plan or idea. Reviews, amends, and derives purpose-named tasks with a final human approval gate. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Autoplan

An idea or plan goes in; an amended plan and an appended task ledger come out, presented at a final approval gate where you stop for the human decision. Nothing here executes, publishes, or reaches the network. All effects are reversible local artifacts, discarded to recover the pre-run state.

## Read the invocation

Free-text arguments are the subject: a plan file path or inline idea.
`/skill:<name>` tokens in the arguments are routing hints; drop them before reading the subject.
`orchestrate`, `continue`, `go`, and `do it now` resume the current run and never restart it.
With no free-text subject, take the first source that yields exactly one candidate: a plan document written or approved in this session, then a plan file path named earlier in this session.
Print `subject: <what> (<how found>)` as the first output line.
When no source yields one, stop before any write with one line: `autoplan needs a plan or idea: pass a path or inline text.`

## The ledger and task naming

The ledger file carries the task list. Resolve its path once per run and use the first rule that applies: a path the invocation names; a directory for plans, tasks, or working documents that the project instruction file (`AGENTS.md` or `CLAUDE.md`) names, holding `autoplan-ledger.jsonl`; an existing `autoplan-ledger.jsonl` anywhere in the repository; otherwise `tasks/autoplan-ledger.jsonl`. State the resolved path at the approval gate. Create the file when missing. Otherwise append new tasks to the end, never overwriting or truncating existing entries. Each run appends only the tasks it produces.

Internally, preserve existing stored ledger `id`, `description`, and `phase` fields and values, and never migrate user records. Each ledger line is a JSON object with `id`, `description`, and `phase` keys. For internal sequencing and tracking, each task ID joins its reviewing phase prefix (`CEO`, `DES`, `DX`, `ENG`) to a zero-padded sequence number within that phase:

| Phase prefix | Internal ledger IDs |
|---|---|
| CEO review | `CEO-01`, `CEO-02`, and so on |
| Design review | `DES-01`, `DES-02`, and so on |
| DX review | `DX-01`, `DX-02`, and so on |
| Engineering review | `ENG-01`, `ENG-02`, and so on |

Sequence numbers continue from the existing ledger. For each phase prefix, scan the file for the highest existing sequence number and increment from there, starting at `01` when the prefix has no prior entries. Tasks increment in the order identified. The same plan evaluated the same way against the same ledger produces the same internal IDs. A phase with no tasks leaves its prefix unused.

For human presentation, plans, tasks, headings, and TODOs must use the actual purpose, never phase+counter labels (`CEO-01`, `DES-01`, `DX-01`, `ENG-01`), parenthesized opaque IDs, or decorative coded task prefixes. Always display the semantic description of what the task accomplishes. Genuine fixed external metadata IDs (such as internal ledger fields) remain intact internally, but human labels name the concrete work directly.

## Plan mode

Plan mode makes the repository read-only and leaves the plan file writable. Write the amended plan to the plan file for this session: the path the user named, or a new `local://<slug>-plan.md` where `<slug>` is a short semantic name. End the plan file with the ledger lines this run produces, one per line, inside one fenced `jsonl` block. On the first turn that is not in plan mode, re-scan the ledger, renumber the block's IDs for any phase prefix whose highest sequence moved, skip any `id` already present in the ledger, append the rest to the resolved ledger path, and report the count appended. Ledger presence proves a task was planned, not completed.

## How the review runs

Read the subject as the Read the invocation section defines. Ground only in the paths the subject names. A file subject is read in full, every line, and the report states the line count. Then run the four review phases: CEO, design, DX, and engineering. Each phase judges the idea against clarity, impact, audience, risk, sequencing, and reversibility, recording its decisions in the register. A phase that cannot reach a decision records the open question and the remaining phases continue. If subagents are unavailable or a phase has not settled after one health check, run that phase inline and record `coverage: inline` in the register. The plan is amended with the consolidated decisions from all four phases.

From the four phases come implementation tasks. Assign internal deterministic IDs per the rules above, append one JSON line per task to the ledger, and update TODOs to reflect the aggregated tasks using their actual purpose and semantic description.

Present the amended plan and aggregated tasks at a final approval gate, naming tasks and headings by their actual purpose without opaque coded labels. Quote the plan file path at the gate. Autoplan records no approval and never executes. End the report with one line: `Run: /autopilot <plan path>`. Invoking autopilot with that path approves its local work, and its gate still fires for outward, irreversible, credential, paid, and data-at-rest acts.

## Requirements added later

When the user adds requirements to a plan already in this conversation, amend the plan file in place and append tasks with the next sequence numbers. Re-run a review phase only where a decision that phase recorded is invalidated.

## When the run stops instead

A missing subject stops everything before any write. An undecided phase never blocks the others: its open question lands in the register, the rest continue, and the question surfaces at the approval gate. A ledger write failure discards the partial append, and the result is reported as blocked with the phase reached rather than done. Until the approval gate is reached and presented, the outcome is blocked, never done.
