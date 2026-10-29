---
name: retro
description: 'Use when a finished session, period, milestone, or cycle needs an evidence-backed look-back, or an existing system needs its unexplained rationale recovered. Not for saving learnings into docs: use compound or autolearn.'
---

# Retro

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks for a look-back on a finished session, period, milestone, or cycle, or for recovery of rationale an existing system cannot explain. |
| Authority | Read-only, except one file write when the user explicitly asks for a file report; rollback is deleting that file. No VCS, credential, paid, published, deployed, or remote mutation. Never writes docs/solutions/, CONCEPTS.md, or rationale topic files; capture belongs to compound and autolearn. |
| Side effect | Chat report; optionally one report file at a user-named path (default reports/retro-<mode>-<slug>.md). |
| Done | Every finding cites traceable evidence with an honest standing; recommendations are ranked; unavailable sources and unverified items are named as gaps, never filled by invention. |

## Principles

- Less but better: one mode per run, merged findings, no padding. A recommendation stays only if a reader can act on it.
- Do not fool yourself: observation stays separate from inference, unknowns are recorded as unknowns, and every citation must survive a reader who checks it.

## Modes

One run uses exactly one mode. Never run several modes as a routine; a request naming no mode gets one clarifying question, not five reports.

- environment: a completed session assessed for agent-environment friction. Needs the session transcript or state record.
- engineering: a named period assessed from repository and tracker telemetry. Needs the period, resolved to explicit start and end dates.
- learning: a milestone assessed from progress evidence. Needs the milestone definition and at least one progress artifact.
- next-cycle: a finished cycle distilled into lessons, anti-patterns, gates, and a keep, iterate, or restart decision. Needs the cycle objective and the final artifact.
- rationale: an existing system assessed for unexplained why-knowledge. Needs the target path and a fixed pass scope (the whole system or one named subsystem).

Mode evidence paths, source precedence, and prioritization live in references/mode-evidence.md.

## Inputs

- Scope (required): the session artifact, period, milestone, cycle objective plus final artifact, or target path plus fixed pass scope, per the mode.
- Evidence (per mode): telemetry, artifacts, QA output, complaints, diffs, transcripts, planning notes, or for rationale: history, tracker threads, existing docs, and maintainer statements. Each consulted source is cited; each unavailable source is recorded as a gap.
- Report path (optional): where to write the file report. Without one, the report stays in chat.

## Procedure

1. Route exactly one mode from the request. Ambiguous scope gets one question naming the five modes and what each needs; do not start gathering until the mode is settled. Done when: one mode is routed with its required scope present, or the run stops to ask.
2. Confirm authority: read-only unless the user asked for a file report. Done when: no mutation occurs without an explicit file request.
3. Gather only the routed mode's evidence per references/mode-evidence.md. Missing required scope stops the run before any finding is drafted. Unavailable optional sources become named gaps. Never infer an environment, invent telemetry, or treat code as proof of motive. Done when: every available source is gathered or the run stops for missing scope, with gaps recorded.
4. Draft findings where each finding carries evidence, standing, and severity. Standing is confirmed (stated by the evidence), inferred (reasonably derived, labeled as such), or unverified (no traceable support). Severity is high (blocks progress), medium (degrades efficiency or correctness), or low (minor friction). Merge duplicates; drop findings with no traceable evidence, or keep them under Gaps as unverified with downgraded priority. No numeric scores or invented metrics. Done when: every finding has evidence, standing, and severity, and nothing unevidenced poses as confirmed.
5. Generalize before recommending. Cluster specific complaints or incidents upward into the shared pattern; record the pattern as the finding and keep specifics as evidence. A recommendation that fixes only the reported case is rework waiting to happen: escalate it to the class or drop it. Done when: each recommendation addresses a pattern, not a single reported case.
6. Rank recommendations. Order by severity, then by evidence strength. Each recommendation names the concrete change, the cost or friction it removes, and the evidence behind it. Findings that merit durable capture become pointers: learnings to compound or autolearn, rationale topic records to compound, never writes by this skill. Done when: recommendations are ordered and capture pointers name the owning skill.
7. Mode verdicts: engineering names team or contributor breakdowns with per-source attribution and separates evidenced habits from inferences; next-cycle separates working assets from misleading progress, names each anti-pattern as a concrete failure mode with the gate that catches it, prefers hard gates over advice, and ends with an explicit keep, iterate, or restart decision; rationale enumerates every in-scope gap with Evidence and Status, marks unrecoverable items unknown with needs-maintainer notes, flags conflicts open with both sides recorded, and organizes entries by topic. Done when: mode verdicts are present, every gate traces to observed evidence, and no rationale entry poses a guess as confirmed.
8. Emit the report in chat per templates/retro-report.md, keeping only the routed mode's section and deleting the other four. Write the file only when asked. A fresh reader can tell what to preserve, discard, and check first without reading the source session. Done when: the report is emitted with the mode's required sections, ranked recommendations, gaps, and capture pointers, and any file write matches the chat report.

## Failure and recovery

- Missing required scope: stop before gathering; state what is missing. Nothing is written.
- Source unavailable: record the gap with its reason and continue on what is evidenced. Never fabricate activity, issues, or rationale.
- Ambiguous or conflicting evidence: mark the finding unverified or record both sides; ask for the specific missing fact, never a generic explanation.
- Scope widens mid-run: stop and report the widening; recommend a separate retro for the added scope.
- A guessed entry is detected: demote it to unverified and correct the report before finishing.
- Rollback: the single written file, if any, is deleted. Nothing else was mutated.

## Cutover

Retro is the only surviving retrospective entry point. No alias is kept for any name below.

- plugins/odin-agent/skills/agent-environment-retrospective: friction taxonomy, severity ranking, and evidence validation become environment mode. Directory closes.
- plugins/odin-knowledge/skills/engineering-retrospective: period telemetry, source precedence, breakdowns, and gap accounting become engineering mode. Directory closes.
- plugins/odin-learn/skills/learning-retrospective: criterion classification, strategy assessment, adjusted plan, and measurable next milestone become learning mode. Directory closes.
- plugins/odin-agent/skills/skill-doctor retrospective surface: its decode-the-transcript plus evidence-cited per-turn findings discipline is carried by the shared evidence rules. Its numeric scores and scratch HTML report are grading, not retrospective analysis, and are not carried; retro uses ranked findings, never numeric scores. The skill-doctor directory itself is outside this cutover.
- plugins/odin-run/skills/cycle-memo: lesson extraction, asset separation, pattern escalation, and anti-pattern plus gate discipline become next-cycle mode. Directory closes.
- plugins/odin-run/skills/cross-run-playbook: cycle memo and the explicit keep, iterate, or restart decision become next-cycle mode. Its build, real-surface drive, and versioning machinery stays with the work owners; retro assesses finished cycles, it does not run them. Directory closes.
- plugins/odin-knowledge/skills/keep-why-retrospective: gap scanning, evidence search and trust order, Evidence and Status classification, conflict flagging, and the unknown discipline become rationale mode. Its topic-file capture moves to compound under the keep-why fold; retro analyzes and recommends, it never writes topic files. Directory retires.

Preserved, never absorbed:

- compound and autolearn keep the capture jobs; compound additionally receives the keep-why topic-file capture under the separate fold. Retro recommends capture; it never writes their surfaces.

## Output

A report with scope, sources consulted, sources unavailable, the routed mode's required sections, ranked recommendations, explicit gaps, and capture pointers. File form goes to the user-named path only.
