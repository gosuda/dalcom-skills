---
name: autoplan-and-autopilot
description: 'Use when the user invokes /autoplan-and-autopilot on an idea or plan to review across four perspectives, derive a task ledger, present for approval, and execute under verified phase gates. Not for open-ended debugging, single-step execution, or unapproved remote publication.'
---

# Autoplan and autopilot

Execute an end-to-end delivery cycle starting from an initial idea or plan: review across four perspectives, record a stable task ledger, present the plan for human approval, and on approval orchestrate bounded implementation through verified phase gates to closeout.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Explicit user invocation of `/autoplan-and-autopilot` with an idea or plan. |
| Authority | Reversible local by default: writes amended plan, appends tasks to `tasks/autoplan-ledger.jsonl`, modifies local source and test files within approved scope, and executes local verifiers; rollback is version control. Committing, pushing, pull request creation, deployment, credentials, paid actions, data-at-rest mutations, or irreversible deletions require separate, explicit user request with preview and consent; never implied by skill invocation or default execution. |
| Side effect | Evaluates plan across four perspectives, appends tasks to `tasks/autoplan-ledger.jsonl`, pauses for human approval, orchestrates disjoint implementation, runs parent-owned verification, enforces review and simplification gates, and verifies closeout. |
| Done | Returns `DONE` only when planning, approval, bounded execution, parent verification of success criteria, review gates, simplification, and authorized closeout are all observed and verified on the final tree, with every post-proof mutation re-verified by a fresh native run. Returns `BLOCKED` with a resumable handoff on any gate stop, withheld approval, or failed proof. |

## Inputs

Required:
- Plan or idea: supplied as a file path or inline text.
- Repository context: current checkout path and repository facts.

Optional:
- Success criteria: explicit acceptance criteria. When omitted, derive discoverable facts and propose concrete criteria during planning, surfacing them at the approval gate. Ask the user only when core intent remains unresolved.
- Closeout condition: definition of final state (clean working tree, test suite green, or explicit commit/push instructions). When omitted, default to clean working tree with passing tests.
- Scope boundaries: explicit list of paths or components permitted to change.
- Publication authority: explicit target remote, branch, and pull request destination; absent means local-only mode.
- Existing ledger: `tasks/autoplan-ledger.jsonl` to extend. If absent, create one.

## Fact discovery and repository reconnaissance

Before planning or modifying artifacts, ground the workflow in concrete repository facts:
1. Inspect version control: check current branch, tracking branch, remotes via `git remote -v`, and status of working tree.
2. Identify tooling: locate package definitions, configuration files, and build manifests. Determine native build, typecheck, lint, and test commands.
3. Inspect existing evidence: read existing CI configurations, test logs, recent commit messages, and test layout through read-only inspection without running scripts or executing test commands. Defer verifier execution until after human approval.
4. Bound scope: identify artifacts and modules related to the request, separating in-scope components from untouchable surfaces.

## Four-perspective review and decision register

Evaluate the plan across four distinct perspectives to resolve competing pressures into sound structure:
1. CEO perspective: evaluate viability, user and business impact, problem definition, strategic alignment, and scope boundaries. Reject unnecessary complexity and feature creep.
2. Design perspective: evaluate ergonomics, clarity of interaction, affordances, mental model coherence, edge states, empty states, and diagnostic feedback.
3. Developer experience (DX) perspective: evaluate API ergonomics, error messages, ease of testing, discoverability, documentation alignment, and friction.
4. Engineering perspective: evaluate correctness, architectural coherence, performance, and failure modes. State explicit preconditions, postconditions, and invariants for every change before implementation. Resolve local forces into deep modules with clean seams.

Evaluate each perspective against a six-principle decision register:
- Clarity: unambiguous contract and discoverable behavior.
- Impact: direct solution to the primary user problem.
- Audience: caller expectations and operational constraints.
- Risk: failure modes and regression surfaces.
- Sequencing: causal dependencies and prerequisite ordering.
- Reversibility: safe rollback without data loss.
Record decisions and open questions in the decision register. Consolidate decisions into an amended plan with explicit scope boundaries.

## Task derivation and ledger destination

1. Destination: `tasks/autoplan-ledger.jsonl`. When absent, create it. When present, append new tasks to the end; never overwrite or truncate existing entries. This guarantees an append-only audit trail across runs.
2. Task ID generation: continue numeric counters from the existing ledger to prevent collisions across runs. For each phase prefix (`CEO-`, `DES-`, `DX-`, `ENG-`), scan the ledger for the highest existing two-digit sequence number and increment from there, starting at `01` when the prefix has no prior entries:
   - CEO review: `CEO-01`, `CEO-02`, ...
   - Design review: `DES-01`, `DES-02`, ...
   - DX review: `DX-01`, `DX-02`, ...
   - Engineering review: `ENG-01`, `ENG-02`, ...
3. Ledger schema: preserve the standard autoplan ledger contract where each line is a JSON object with exact keys:
   - `id`: string (for example, `ENG-01` or `ENG-03`)
   - `description`: string stating the concrete task and contracted invariant
   - `phase`: string (`CEO`, `DES`, `DX`, or `ENG`)
4. Aggregation: update local task tracking to reflect the newly appended task list.

## Human approval gate

1. Presentation: present the exact amended plan, the decision register, the task ledger entries, and the concrete scope boundaries to the user.
2. Approval evaluation: check whether the exact current plan has explicit written approval in the session. If not, stop immediately and request explicit approval.
3. Gate rule: no source code file, configuration file, or script may be edited or executed until explicit human approval is received.
4. Withheld or missing approval: if approval is withheld, declined, or unanswered, halt the chain. Preserve the amended plan and task ledger at `tasks/autoplan-ledger.jsonl`. Emit a `BLOCKED` status stating that human approval is required to proceed.

## Bounded orchestration and implementation

When human approval is confirmed, transition into execution under bounded orchestration:
1. Baseline verification: run the native test suite to establish clean baseline status before mutating code. Isolate any pre-existing failure before implementing new changes.
2. Disjoint work partitioning: partition tasks into disjoint write sets. Each worker owns its assigned target paths exclusively. Shared files (manifests, shared configuration, top-level index) are modified only by the parent orchestrator after worker tasks complete. If two tasks require editing the same file, serialize them; never run concurrent writers on shared paths.
3. Implementation discipline: workers implement assigned tasks adhering to the engineering invariants. Follow test-driven discipline where the task requires behavioral assertions: write behavioral assertions or failing tests at named seams before making code changes, and implement the minimal logic to satisfy the contract.
4. Worker gate exemption: workers explicitly skip repository-wide test suites, linters, formatters, and verification gates unless a task specifically assigns a dedicated test authoring role. A worker whose task requires a behavioral assertion or failing test at its seam may execute only the narrow test directly covering that seam to confirm its own assertion. Workers default to editing assigned files and returning local diff evidence only. The parent orchestrator owns all combined verification, gate checks, and proof passes after workers stop writing.
5. Scope boundary enforcement: reject scope widening. If an implementation step reveals unexpected complexity, stop and flag the boundary; do not silently expand scope or modify files outside the approved list.

## Parent-owned verification and phase gates

After worker implementation completes and writers stop, the parent orchestrator takes exclusive control of verification:
1. Proof-invalidation rule (no post-proof unverified fixes): EVERY repair, review-autofix, or simplification mutation to source, test, or configuration files invalidates the relevant prior proof. The gate that owned the mutation AND every earlier gate whose evidence the mutation could disturb (at minimum the G1 native suite) must rerun on the final post-mutation tree before completion. DONE requires fresh verification evidence collected on the final diff; evidence collected on a pre-mutation tree never closes a mutated tree. No post-proof unverified fix can close.
2. State machine: each gate follows the autofix-then-halt state machine:
   - RUN: evaluate the gate condition.
   - Pass: advance to the next phase.
   - Fail: if autofix arm is available and has not run for this phase, invoke autofix exactly once, then recheck (the recheck includes the native verification rerun required by the proof-invalidation rule whenever autofix mutated files).
   - Recheck fail: halt immediately. Never loop autofix a second time.
3. Gate G1 (Execute): parent executes the repository's native verification suite (build, typecheck, unit tests) and verifies every success criterion.
   - Pass: verifier exits clean with zero errors and every contracted success criterion is verified with evidence.
   - Autofix: one targeted root-cause repair pass addressing the specific failure, followed by recheck.
   - Halt: if verifier fails or success criteria remain unsatisfied after autofix, halt the pipeline and record verifier output, unmet criteria, and diff.

## Simplification and review gates

Ordering (preserved): gates run G1 then G2 then G3 (simplify-then-review) unless the exact user requirement specifies a different order. The review-autofix proof gap is closed by explicit recheck, not by reordering gates.

1. Gate G2 (Simplify): aggressive simplification within approved scope.
   - Simplify dead branches, duplicated logic, temporary scaffolding, and single-use wrappers introduced or exposed during changes.
   - Structure-preserving rule: preserve all observable behavior and contractual invariants.
   - Proof invalidation and verifier recheck: every simplification edit is a mutation that invalidates the prior G1 proof. Rerun the native verification suite on the final simplified tree; G2 passes only on a fresh native PASS with behavior preservation confirmed. If any regression occurs, revert the simplification increment and rerun the native suite again to re-establish proof on the reverted tree.
2. Gate G3 (Review): examine the scoped diff against architecture, security, and correctness criteria.
   - Criteria: zero critical and zero high-severity findings; no unhandled error paths; no silent scope creep; no TODO, stub, or placeholder deliverable.
   - Autofix with proof revalidation: at most one targeted fix pass on critical or high findings. A review-autofix edit is a source mutation that invalidates the prior G1 (and G2) proof, so the fix pass is followed by BOTH a rerun of the native verification suite on the final post-autofix tree AND re-review of the changed files. A review pass alone never closes: advance only when the native verifier passes on that final tree AND re-review is clean.
   - Halt: if critical or high findings persist after the single fix pass, or the native verifier fails on the post-autofix tree, halt the pipeline and record the residual review findings plus verifier output. A red native rerun never advances.

## Authorized closeout and publication safety

1. Local-only by default: when neither commit nor remote publication is requested, leave verified changes in the working tree. No commit, push, or pull request creation occurs.
2. Separate commit-only request: when the user explicitly requests committing locally without publication, preview the exact commit message, target branch, and changed files. Once approved, create atomic local commits without requiring a remote or pull request target. Push and pull request creation remain skipped.
3. Explicit publication gate: pushing to a remote or opening a pull request occurs only when all of the following hold:
   - The user explicitly requested remote publication in the inputs (never implied by skill name, closeout text, or commit requests).
   - The exact target remote, branch, and pull request title and destination are previewed.
   - Explicit human consent for publication is recorded.
   - All preceding gates (G1, G2, G3) have passed.
4. Observation: verify and quote the observed closeout state in the final report before declaring done.

## Failure, blocked states, and resumption

Halt conditions and blocked states:
- Missing input: stop before any write; report when no plan or idea was supplied, or when unresolved intent cannot be derived without user clarification.
- Withheld approval: stop immediately at the approval gate; preserve plan and ledger; report blocked waiting for approval.
- Conflicting requirements: stop before modifying source files; name the conflicting requirements.
- Missing tools: stop and identify the missing tool or command.
- Failed proof or gate: stop immediately; record the failed gate, reason, autofix outcome, and diff; preserve all in-scope progress.
- Refused publication: if committing or publication is unrequested or refused, preserve local working tree modifications; report local completion with publication skipped.

Resumption protocol:
- Ledger is planning-only and append-only: the ledger schema (`id`/`description`/`phase`) is unchanged and carries no status field. Ledger presence proves a task was planned, never that it completed. Never infer success from ledger presence.
- State inspection: upon restart or resumption, inspect `tasks/autoplan-ledger.jsonl`, git status, commit log, and per-task execution receipts/report evidence where present (existing run record or structured worker return; no new persistence framework is invented).
- Source of truth and resume from actual state: reconstruct completed versus pending by binding each ledger task ID to its own task revision: the execution receipt/report evidence recorded for that taskID plus the contracted tree state that task produced. A task counts completed only when its receipt/report evidence exists for its taskID AND its contracted code and behavior still hold in the tree (not clobbered by later work); otherwise it is pending. Revisions are per-task, never one global HEAD: later tasks mutating the tree do not retroactively un-complete earlier tasks whose contracted state still holds. Do not re-run tasks whose contracted state still holds with matching receipt, do not overwrite existing ledger entries, and resume from the first pending task without duplicating completed actions.
- Zero silent caps: never truncate the task list or silently declare completion when tasks remain undone.
- Zero stubs: reject stubs, mocks, fake fallbacks, or `TODO: implement` deliverables. All deliverables must be genuine, working code.

## Output

Return exactly one terminal classification:

### DONE
- Delivered behavior and scope summary.
- Changed artifacts and files modified.
- Decision register summary, ledger planning entries, and per-task completion reconstructed from native task state plus execution receipts bound to taskID and revision.
- Fresh verification evidence collected on the final tree after the last mutation, proving all success criteria (build, typecheck, test outputs); no post-proof unverified fix closes.
- Closeout state (verified working tree modifications, local commit log, or authorized PR details).

### BLOCKED
- Failed stage and gate name.
- Root cause and failure detail.
- Autofix outcome (attempted and failed, or none).
- Residual findings or compiler/test error output.
- Preserved local state (ledger path, modified files, uncommitted changes).
- Single concrete action required to resume.
