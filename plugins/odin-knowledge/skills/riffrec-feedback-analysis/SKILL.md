---
name: riffrec-feedback-analysis
description: 'Use when a Riffrec capture or other screen, voice, or notes artifact needs interpretation into bug or requirements evidence. Not for generic recordings without product feedback, and not for capturing durable learning.'
---

# Riffrec feedback analysis

Standards: raw capture and interpreted evidence are separate artifacts with an explicit boundary. Keep every artifact its consumer needs, nothing it does not.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A Riffrec bundle, recording, or screen/voice/notes artifact arrives needing interpretation, or the user asks how to install, capture, or share Riffrec feedback. |
| Authority | Reads the supplied capture and writes only explicitly requested evidence artifacts. Raw recordings, audio chunks, zip contents, session dumps, and extracted screenshots stay local-only by default and are never committed without explicit privacy-cleared authorization. No publication, remote, credential, paid, or destructive mutation. |
| Side effect | Setup ends with a current capture/share path; quick analysis ends with one evidence-backed bug report; extensive analysis ends with the complete evidence set and, unless extraction-only was asked, a framing handoff. |
| Done | The route complete result or an actionable blocker is returned; partial interpretation is never claimed as complete evidence. |

## Inputs

- The input artifact or the setup question. Required.
- The desired route when ambiguous: setup, quick bug report, or extensive analysis. Ask when length and event content do not decide it.

Route from the input. Setup is no recording yet with install/capture/share questions. Quick is a short capture (about a minute or less), a single specific issue, or an explicit quick/transcribe request. Extensive is longer, multi-issue, requirements-bearing, or workflow-walkthrough material, or an explicit requirements request. A Riffrec bundle means the synchronized screen, voice, and event capture from the Riffrec tool, not a generic video file. Generic recordings without product feedback are out of scope: return the boundary rather than analyzing them as product evidence.

## Procedure

1. Route first and load only that route. When the input is ambiguous, inspect recording length and event count before choosing; when still unclear, ask which route applies before running anything heavy.
2. Setup route: report the current supported capture/share path from presently readable project or vendor guidance. Invent no install commands, flags, or endpoints. When guidance is unavailable or stale, return that as the blocker with what would unblock it.
3. Quick route: interpret the single issue into one evidence-backed bug report with reproduction, observed behavior, expected behavior, and cited capture moments. Create no durable artifact unless requested.
4. Extensive route: build the complete evidence set (problem analyses, requirements kickoff material, source manifest with repo-relative screenshot paths and no absolute local paths). Keep text artifacts committable only when needed for traceability and free of sensitive data. Unless the user asked for extraction only, hand the evidence to product framing as the next owner without executing it here.
5. Close each route explicitly: setup with the path, quick with the report, extensive with the evidence set plus framing handoff or extraction-only delivery. Analyzer or input failure ends as a blocker with recovery, never a partial success claim.

## Failure and recovery

- No input and no setup question: ask for the artifact or question; analyze nothing.
- Analyzer capability missing: blocked with the exact missing capability and recovery.
- Ambiguous route: ask before heavy work; do not default to extensive.
- Privacy-sensitive raw: keep local-only; commit only cleared text artifacts on explicit authorization.

## Output

Return the route taken, the setup path or bug report or evidence set with manifest paths, the framing handoff when one applies, and any blocker with recovery. Raw stays local; evidence carries repo-relative references later agents can open.
