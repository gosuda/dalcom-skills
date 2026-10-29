---
name: wizard
description: 'Use when a human must perform steps only they can, such as provisioning infrastructure, entering credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Not for steps the agent can perform itself.'
---

# Wizard

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Provisioning, credential or secret setup, dashboard walkthrough, migration, or cutover where a human drives the browser and only the human can act. |
| Authority | Reversible local: writes only the wizard script to the named target path; deleting the file rolls back. Human-only execution: the skill never runs the wizard end to end, never enters credentials, and never performs the manual steps. |
| Side effect | One executable bash wizard at the target path. Static verification only. |
| Done | The script exists, is executable, passes static verification, and every collected value traces to its declared destination. |

## Inputs

1. **Procedure description** (required): what the wizard must accomplish.
2. **Target path** (optional): where to write the script; default `scripts/setup-<topic>.sh`.
3. **Repository context** (read, never asked cold): `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework configuration, `.github/workflows/*`.

## Procedure

### 1. Scope the procedure

Read the repository context first. Treat every `secrets.*` and `vars.*` reference in a workflow as a value the wizard must produce. For a migration, read the current state, the target state, and every irreversible action between them. Show the ordered stage list with the values each stage produces and confirm it with the user. Done when every stage is named in order and every captured value has a known source, a destination (`.env`, a CI secret, both, or nowhere for a pure-action stage), and a secret or public classification.

### 2. Map the human journey

Write stranger-followable instructions per stage: which URL to open, what to click, where the value appears, and which variable it fills. Where the current UI or exact command is unknown, say so and check the official docs or ask the user. Never invent steps that may not exist. Done when every stage traces to concrete instructions a stranger can follow.

### 3. Author the script

Fail if a file already exists at the target path; never overwrite. Copy `scripts/wizard-template.sh` to the target path and replace only the example stage with one `stage` per step in dependency order. Set `TOTAL_STAGES` and `TOTAL_MINUTES` to honest values. Use the library helpers only by the contract in `references/library-helpers.md`: open the URL before asking for its value, `ask_secret` for secrets, `write_env` for every persisted value, `set_secret` only for values CI needs, `confirm` before any irreversible action. Keep each stage to one focused task. Never hand-edit the library above the stages marker. Done when the script holds one stage per step with honest totals and every helper used by contract.

### 4. Verify and hand off

Run `bash -n <script>`, run `shellcheck <script>` when available, and run `chmod +x <script>`. Never execute the wizard: it opens browsers and blocks on human input. Trace statically instead: every value from step 1 is captured and lands where step 1 declared, and every `set_secret` name exactly matches a `secrets.*` workflow reference. Tell the user how to run the script. Commit it only when the user wants a repeatable setup path that lives in the repo and is linked from the README; otherwise treat it as ephemeral and delete it when the job is done.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| `scope-unconfirmed` | Stop before authoring. Re-present the stage list and wait. |
| `path-collision` | Fail before write. Report the existing path. Never overwrite. |
| `unknown-step` | Stop. Report what is unknown and how to resolve it. Never invent UI steps or commands. |
| `value-untraced` | Stop. Report which value has no capture or no destination. Never hand off. |
| `secret-mismatch` | Stop. Report the secret name and the workflow reference. Reconcile before handoff. |
| `syntax-failed` | Stop. Report the `bash -n` or `shellcheck` error. Fix before handoff. |
| `gh-unready` | Record in `SKIPPED`. The script warns at runtime and the human sets the secret by hand. |

Partial-result rule: a partially authored script is never handed off. Rollback is deleting the script file while it is still uncommitted.

## Output

A self-contained executable bash wizard at the target path with honest totals and every scoped value captured and routed to its declared destination, plus the run instruction and the ephemeral or repeatable disposition.
