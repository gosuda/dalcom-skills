---
name: polish
description: 'Use when a working feature needs user-directed UX refinement before shipping. Not for throwaway prototypes, deciding what to build, general QA sweeps, or publishing the change.'
---

# Polish

Anchors: Dieter Rams (refinement stops when nothing else can be removed without harming use), David Parnas (working behavior is the contract; polish never renegotiates it).

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A functional feature needs focused UX refinement driven by live observation of the running page before shipping. |
| Authority | Edits and locally commits only the requested in-scope surface. Never works on the default branch, never pushes, never opens PRs, never runs general QA or autonomous checklists. A voice-interviewed live session with screen observation runs only on explicit user request with disclosed requirements and consent. |
| Side effect | Requested fixes reflected in the live feature and saved in local commits, with residual items and blockers explicitly reported. |
| Done | The user ends the loop, every requested fix is reflected or reported blocked with evidence to resume, and in-scope changes are in local commits. A live session additionally ends with the residual unit list and session-log path. |

## Inputs

- The target: PR number, branch name, or blank for the current branch. Required to resolve before serving.
- Traditional vs live observation. Required to ask once before any server starts, with disclosure when live is offered. Traditional is typed user observations. Live is talk-and-draw with a voice interviewer that hears the user, sees pointed-at screen content on request, and streams the session locally.

The user drives what to inspect and change. Do not invent an autonomous checklist or expand into general QA.

## Procedure

1. Ask traditional or live once, with live disclosure (what hears, sees, streams, and what setup change it needs, including any dependency or provider mount that would stay on the branch). Traditional proceeds below. Live proceeds only on explicit user choice with the disclosed prerequisites present; otherwise fall back to traditional and record why.
2. Get the page ready safely. Resolve the requested ref without switching branches implicitly and without touching unrelated worktrees. Start only the repository own dev server through its documented command; invent no server, script, or flag. Confirm reachability and hand the URL to the user. When no browser capability exists in the harness, ask the user to describe what they see.
3. Wait for observations. Tell the user where the server runs and ask what could be better. Do not start a review pass while they browse.
4. Iterate the requested scope. For each requested change, inspect only as needed, edit the in-scope surface, and let hot reload update the page. When asked to verify visually, use an available browser capability or ask the user to describe the result.
5. Close locally. When the user says they are done, commit the polish changes locally and report the commits, the still-running server URL, and any residual blocker. Push and PR creation wait for a separate explicit shipping request.

## Failure and recovery

- Target unresolvable or server unreachable: blocked with evidence needed to resume.
- Live prerequisites missing or declined: run traditional; do not add the live setup commit.
- Request expands beyond the in-scope surface: record it as residual rather than widening silently.
- Checkout is the default branch: do not edit there; resolve an authorized working branch first.

## Output

Return the commits, server URL, applied fixes, residual items with reasons, and any blocker with resume evidence. For a live session also return the residual unit list and session-log path.
