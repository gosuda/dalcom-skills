---
name: developer-video
description: 'Use when preparing a developer video script, storyboard, demo runbook, and accessibility checklist. Not for recording, uploading, or channel management.'
---

# Developer video

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks for a video plan for a technical topic: tutorial, demo, talk recording, or explainer. |
| Authority | Read-only preparation in chat. No recording, upload, channel management, paid promotion, or required vendor dependency. |
| Side effect | A script and production pack the human records. Nothing uploaded. |
| Done | Script or storyboard, chapter and timecode plan, demo runbook with expected outputs, accessibility checklist, title and thumbnail brief, and source backing for every demo claim are present. |

## Not for

- Production, publishing, or promotion. Video artifacts and constraints genuinely differ from text posts, which is why this is a separate owner.

## Inputs

- `topic` (required): the technical subject with supplied material or an explicitly requested read-only research pass.
- `format` (optional): tutorial, demo, talk, or explainer. Defaults to demo when omitted.
- `length` (optional): target duration band. Defaults to the shortest band that fits the runbook.

## Procedure

1. Fix format, audience, and the one viewer outcome. **Done when:** all three are singular and explicit.
2. Write the script or storyboard beat by beat with on-screen content per beat. **Done when:** every beat names what the viewer sees and hears.
3. Build the chapter and timecode plan proportional to the length band. **Done when:** chapters cover the full runtime with no gap.
4. Write the demo runbook: exact commands, inputs, expected outputs, and recovery lines for the likeliest live failures. Mark every claim source-backed or explicitly unverified. **Done when:** each demo step has expected output and a failure line.
5. Complete the accessibility checklist: captions, transcript plan, contrast and font size for on-screen text, audio clarity notes. **Done when:** each checklist item passes or is flagged for production.
6. Draft the title and thumbnail brief from the outcome without clickbait that the video does not deliver. **Done when:** title, thumbnail concept, and outcome agree.

## Failure and recovery

- Demo cannot be verified: mark unverified with what verification needs; do not script an unrun demo as certain.
- Topic too large for the band: split into episodes with per-episode outcomes.

## Output

A video pack: script or storyboard, chapters with timecodes, demo runbook with expected outputs, accessibility checklist, title and thumbnail brief, and the source-backing record.
