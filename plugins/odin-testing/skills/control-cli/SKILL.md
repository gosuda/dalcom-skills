---
name: control-cli
description: 'Use when asked to reproduce, profile, or verify CLI/TUI behavior. Produces a deterministic transcript or profile proof with session cleanup. Not for CLI design advice, use cli-for-agents.'
---

# Control CLI

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Reproduce, profile, or verify CLI/TUI behavior. |
| Authority | Reversible local: writes only temporary transcript or profile artifacts under a system temp directory and may spawn local PTY sessions; rollback is terminating the PTY process and removing its runtime scratch. No remote mutation. No source or VCS mutation. No credential or paid mutation. |
| Side effect | Runs temporary terminal sessions and captures evidence. |
| Done | A deterministic transcript or profile proof artifact exists and the live PTY session is terminated with its runtime scratch removed. |

## Inputs

- The CLI/TUI binary or command to exercise (must be supplied).
- The exact reproduction steps, profile target, or verification scenario (must be supplied).
- Optional: expected output, timeout, and environment variables.

## Procedure

1. Create a fresh session directory under the system temp path for the captured artifact and PTY/tmux runtime scratch. Record the directory for cleanup. Done when: the session directory is created and recorded.
2. Spawn the target CLI/TUI under a PTY, or a tmux session attached to a PTY, so interactive behavior is observable. Apply one action per observation: send one input, then capture the full terminal render before sending the next. Done when: the PTY or tmux session is spawned and interactive behavior is observable.
3. For reproduction: drive the supplied steps in order, appending the terminal state after each action to the transcript artifact. Done when: every step is driven in order and the transcript artifact captures the terminal state after each action.
4. For profiling: run the target under the chosen profiler, capturing timing or allocation output into the profile artifact. Done when: the profile artifact captures timing or allocation output.
5. For verification: exercise the scenario, compare the observed output against the expected output when supplied, and record the pass or fail classification in the transcript artifact. Done when: the pass or fail classification is recorded in the transcript artifact.
6. Terminate the PTY process, or detach and kill the tmux session. Done when: the PTY process or tmux session is terminated.
7. Remove the PTY/tmux runtime scratch (pipes and sockets); the captured transcript or profile artifact file remains as the retained proof. Done when: runtime scratch is removed and the artifact file remains.

## Failure and recovery
- PTY spawn failure or binary not found: record the error in the transcript, do not invent output, and return blocked with the spawn error.
- Timeout: terminate the PTY process, append the partial transcript up to the timeout, and return blocked with the timeout boundary.
- Non-deterministic output: run a second capture, record the observed variance, mark the proof non-deterministic, and return blocked rather than asserting a false pass.
- Any failure: terminate the PTY or tmux process and remove its runtime scratch before returning; if no artifact was captured, delete the whole temp session directory. Never swallow errors or claim the done predicate holds when the proof is missing or inconclusive.

Use temporary credential-free HOME, configuration, data, and session roots when the application supports them. Record the executable, arguments, environment relevant to the scenario, terminal geometry, and launch identity. If concurrent rebuilding could replace the executable, launch a permission-preserving snapshot under the existing temporary-artifact authority. Do not modify source, initialize a repository, repair an installation, enable paid calls, or alter the user's session store.

Declare the terminal capability profile. Answer only the queries appropriate to that profile and record the replies; a copied capability table can invalidate a legacy-terminal test. Wait for the actual painted input surface, send one contract-correct input, drain output, and capture the settled rendered state before the next action.

Retain raw bytes and rendered frames with input and byte-offset attribution. Use raw-stream assertions for byte claims and terminal-emulated rows and cursor state for paint claims. Redraw fragmentation can defeat a phrase search without proving absent paint. A distinctive token may locate a frame but does not replace the scenario's complete rendered predicate.

For synthetic approval fixtures, interact only with the currently visible permitted question and answer row. Do not infer real user consent or disable production approval policy. Derive idle predicates from state-bearing output and test them against a known busy frame. Exercise resize after startup when making a resize claim.

When the claim is normal exit, invoke the application's exit action and observe and reap its child status before cleanup termination. Terminate only still-live processes owned by this session in cleanup. Retain failed captures and remove runtime scratch without deleting unrelated processes or user data.

## Output
Transcript or profile artifact containing captured terminal evidence, plus final classification: reproduced, profiled, verified-pass, verified-fail, blocked, or non-deterministic. Live PTY session terminated and runtime scratch removed before return.

When the requested evidence is a terminal animation, retain a deterministic input script or transcript and record the actual terminal geometry. Inspect representative rendered frames, including a post-paint frame, before claiming that the animation shows the intended behavior. Record blank startup frames or nondeterminism honestly. Keep the recording local; commits, orphan asset branches, uploads, and hosted URLs require a separate publication owner and grant.
