---
name: autoplan-and-autopilot
description: 'Use when the user invokes /autoplan-and-autopilot on an idea or plan to review across four perspectives, derive a task ledger, present the amended plan, and execute under verified phase gates; the invocation approves local, reversible work. Not for open-ended debugging, single-step execution, or unapproved remote publication.'
---

# Autoplan and autopilot

You take an idea or plan through review from four sides, record the resulting work as a stable task ledger, present the amended plan, and then build it under bounded orchestration and verified phase gates to an observed close-out. Planning and execution are separated by an approval gate: the amended plan is presented, and the invocation approves local, reversible work on it under the Approval section below.

## Read the invocation

Free-text arguments are the subject: a plan file path, a `local://` reference, or inline idea or plan text.
`/skill:<name>` tokens in the arguments are routing hints; drop them before reading the subject.
`orchestrate`, `continue`, `go`, and `do it now` resume the current run and never restart it.
With no free-text subject, take the first source that yields exactly one candidate: a plan written or approved in this session, then a plan file path named earlier in this session.
Print `subject: <what> (<how found>)` as the first output line.
When no source yields one, stop before any write with one line: `autoplan-and-autopilot needs an idea or plan: pass a path or inline text.`

## Ground the work in repository facts first

Before planning or modifying artifacts, establish the concrete facts around the request:

* Version control: current branch, tracking branch, remotes (`git remote -v`), and working tree status.
* Tooling: package definitions, configuration files, and build manifests, plus the native build, typecheck, lint, and test commands.
* Existing evidence: CI configurations, test logs, recent commit messages, and test layout, read without running scripts or test commands. Verifier execution waits until the build starts.
* Scope: the artifacts and modules the request touches, with in-scope components separated from untouchable surfaces.

You need a plan or idea (a file path or inline text) and the repository context (checkout path and facts). Success criteria, a close-out condition, scope boundaries, publication authority, and an existing ledger ride along when given. When success criteria are omitted, derive facts only from the paths the request names and their direct manifests and CI configuration; do not mine session logs or run corpus-wide scans unless the request names them, and propose concrete criteria during planning, surfacing them at the approval gate. Ask the user only when core intent stays unresolved. When close-out is omitted, default to a clean working tree with passing tests. Stop before any write when no plan or idea was supplied, or when unresolved intent cannot be derived without user clarification.

Dispatch at most four read-only scouts for grounding; more needs the user's request.

## Review the plan from four sides

Work through four perspectives to resolve competing pressures into sound structure:

| Perspective | What it settles |
|---|---|
| CEO | Viability, user and business impact, problem definition, strategic alignment, scope boundaries. Reject unnecessary complexity and feature creep. |
| Design | Ergonomics, clarity of interaction, affordances, mental model coherence, edge states, empty states, diagnostic feedback. |
| Developer experience | API ergonomics, error messages, ease of testing, discoverability, documentation alignment, friction. |
| Engineering | Correctness, architectural coherence, performance, failure modes. State explicit preconditions, postconditions, and invariants for every change before implementation. Resolve local forces into deep modules with clean seams. |

Judge each perspective against six principles: clarity (unambiguous contract and discoverable behavior), impact (direct solution to the primary user problem), audience (caller expectations and operational constraints), risk (failure modes and regression surfaces), sequencing (causal dependencies and prerequisite ordering), and reversibility (safe rollback without data loss). Record decisions and open questions in the decision register, then consolidate them into an amended plan with explicit scope boundaries.

## Record the work in the ledger

Record the work by the ledger rules in `autoplan`: naming, sequencing, presentation, and append-only writes apply unchanged. Ledger presence proves a task was planned, not completed; completion is read from receipts as `autopilot`'s Resume section defines.

## Approval

Present the exact amended plan, the decision register, the tasks displayed by their semantic description and actual purpose without decorative coded prefixes, and the concrete scope boundaries to the user. Invoking this skill with a subject, given in the arguments or inferred from this session, approves local, reversible work on that subject: edits, local checks, and local commits when the plan authorizes commits. The gate fires for an outward, irreversible, credential, paid, or data-at-rest act, and waits for a separate explicit user request with preview and consent for each one. Explicit written approval of the exact current plan, and plan-mode approval (`ExitPlanMode`), also approve. Steering words sent after an invocation (`orchestrate`, `continue`, `go`, `do it now`, `workflowz`, `Don't ask`) resume or widen work and approve nothing. A timeout or auto-selected default never approves. An invocation with no subject is not approval: stop before any write. A user decline of the plan halts the chain before any source edit: preserve the amended plan and the ledger, and emit `BLOCKED` stating the decline.

## Build inside the boundary

Once the invocation has approved local work, implement under these constraints. The executor is the plan's assigned executor, or parallel orchestration when none is named:

* Run the native test suite first to establish a clean baseline before mutating code, and isolate any pre-existing failure before implementing new changes.
* Partition tasks into disjoint write sets. Each worker owns its assigned target paths exclusively. Shared files (manifests, shared configuration, top-level index) are modified only by the parent orchestrator after worker tasks complete. When two tasks need the same file, serialize them. Never run concurrent writers on shared paths.
* Workers implement their assigned tasks against independent behavioral invariants. When a task needs a test, write its assertion before the code change. Observe it reject the missing behavior, then implement the change. Each test must detect a plausible real fault and survive an internal refactor. Fixture and snapshot oracles that repeat the implementation do not count. A planted fault must execute and fail the intended behavioral assertion; an unrelated compile, syntax, or transport error proves nothing. Plain prose and mechanical registration changes do not require new tests.
* Workers skip repository-wide test suites, linters, formatters, and verification gates unless a task specifically assigns a dedicated test authoring role. The one exception: a worker whose task requires a behavioral assertion at its seam may run only the narrow test directly covering that seam, to confirm its own assertion and record narrow fault-detection evidence. Workers otherwise edit their assigned files and return local diff evidence and narrow seam proof only. The parent orchestrator owns all combined verification, gate checks, and proof passes after writers stop.
* Reject scope widening. When implementation reveals unexpected complexity, stop and flag the boundary. Never silently expand scope or modify files outside the approved list.

## Prove it on the final tree

After workers finish and writers stop, the parent takes exclusive control of verification. The governing rule: every repair, review-autofix, or simplification mutation to source, test, or configuration files invalidates the relevant prior proof. The gate that owned the mutation, and every earlier gate whose evidence the mutation could disturb (at minimum the Execute native suite), must rerun on the final post-mutation tree before completion. `DONE` needs fresh verification evidence collected on the final diff. Evidence collected on a pre-mutation tree never closes a mutated tree.

Each gate follows the autofix-then-halt machine in `autopilot`'s pipeline-gates reference. Run the gate condition; advance on pass. On failure, invoke the autofix arm exactly once if one is available and unused for this phase, then recheck (including the native rerun the proof rule requires whenever autofix mutated files). A failing recheck halts immediately. Never loop autofix a second time.

Gates run in order: Execute, then Simplify, then Review (simplify before review), unless the exact user requirement specifies a different order. The review-autofix proof gap is closed by explicit recheck, not by reordering gates.

* Execute: run the repository's native verifier and check every acceptance criterion. Inspect new and modified tests. Reject a test without an independent behavioral invariant, a plausible fault, observed detection of that fault, and evidence that the oracle survives internal refactoring. Accept a recorded failure before the fix or a targeted fault injection, not an unrelated compile, syntax, or transport failure. Plain prose and mechanical registration changes need no new tests; count and wiring pins are not substitutes for behavioral proof. Pass only when verification succeeds and every criterion has evidence. Allow one targeted root-cause repair and recheck. If the verifier, criteria, or test oracle still fails, halt with the evidence and current diff.
* Simplify: aggressively simplify within approved scope: dead branches, duplicated logic, temporary scaffolding, and single-use wrappers introduced or exposed during the changes. Structure is preserved: all observable behavior and contractual invariants hold. Every simplification edit is a mutation that invalidates the prior Execute proof, so rerun the native suite on the final simplified tree. Simplify passes only on a fresh native pass with behavior confirmed. On regression, revert the simplification increment and rerun the native suite to re-establish proof on the reverted tree.
* Review: an independent reviewer (a fresh subagent where the harness has one, receiving the diff, the approved plan, and the success criteria but not the implementer's conclusions) runs `code-review` on the scoped diff for architecture, security, and correctness. The bar is zero critical and zero high-severity findings, no unhandled error paths, no silent scope creep, and no TODO, stub, or placeholder deliverable. At most one targeted fix pass on critical or high findings. A review-autofix edit is a source mutation that invalidates the prior Execute (and Simplify) proof, so the fix pass is followed by both a rerun of the native suite on the final post-autofix tree and a re-review of the changed files. A review pass alone never closes: advance only when the native verifier passes on that final tree and re-review is clean. Residual critical or high findings, or a red native rerun, halt the pipeline with the findings and verifier output recorded. A red native rerun never advances.

## Close out only what was authorized

Local-only is the default, as `autopilot`'s finalize rule defines: commits only when authorized, and no push or pull request creation.

A separate commit-only request (explicit local commits without publication) means previewing the exact commit message, target branch, and changed files, then creating atomic local commits once approved. Push and pull request creation stay skipped.

Pushing to a remote or opening a pull request happens only when every one of these holds: the user explicitly requested remote publication in the inputs (never implied by the skill name, close-out text, or commit requests), the exact target remote, branch, pull request title, and destination are previewed, explicit human consent for publication is recorded, and all preceding gates (Execute, Simplify, Review) have passed. Verify and quote the observed close-out state in the final report before declaring done.

Every other outward or irreversible act needs the same explicitness: deployment, credentials, paid actions, data-at-rest mutations, and irreversible deletions each require a separate explicit user request with preview and consent. The skill name, close-out text, commit requests, and default execution never imply them.

## A halt preserves everything and says what resumes it

Halt conditions: missing input (stop before any write), a declined plan or withheld consent for an outward act (stop at the gate, preserve plan and ledger), conflicting requirements (stop before modifying source, name the conflict), missing tools (stop and identify the missing command), failed proof or gate (stop immediately, record the failed gate, reason, autofix outcome, and diff, preserve all in-scope progress), refused publication (preserve local modifications, report local completion with publication skipped). On any halt, stop new dispatch at once and cancel or collect every in-flight worker before the report, as `autopilot` defines.

On resumption, follow `autopilot`'s Resume section. The ledger schema (`id`, `description`, `phase`) never carries a status field.

To recover the pre-run state, discard the run's local artifacts (amended plan, appended ledger lines, task tracking updates).

## The run ends one of two ways

Return exactly one terminal classification.

`DONE` carries the delivered behavior and scope summary, the changed artifacts and files modified, the decision register summary, the ledger planning entries, per-task completion reconstructed from native task state plus execution receipts bound to task ID and revision, fresh verification evidence collected on the final tree after the last mutation proving all success criteria (build, typecheck, test outputs), and the observed close-out state (verified working tree modifications, local commit log, or authorized PR details). No post-proof unverified fix closes.

`BLOCKED` carries the failed stage and gate name, the root cause and failure detail, the autofix outcome (attempted and failed, or none), residual findings or compiler and test error output, the preserved local state (ledger path, modified files, uncommitted changes), and the single concrete action required to resume.
