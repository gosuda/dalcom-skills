---
name: ask-dalcom
description: 'Use when the user asks which dstack skill or chain of skills to use for a situation and names no skill, which route to take across skills, or what must exist before a named skill. Recommends one route and runs none of it. Not for a repository orientation or first contribution: use onboard. Not for proving that no skill covers a job: use skill-gap-finder.'
---

# Ask Dalcom

Nobody remembers three hundred skills, so ask. Describe the situation and get one route back: which skills to invoke in which order, what each step does for you, what must exist first, and when you are done.

The summaries below orient you. Before you say what a skill does, or advise skipping a step, read that skill's SKILL.md.

## Answer in five steps

1. Restate the situation in one sentence and place it on the map below: the main flow, an on-ramp, codebase health, writing, or session care. When the situation belongs to another plugin's domain, read that plugin's reference from the table under Other plugins before you answer. This step is done when you can name the one place the situation lands.
2. Give one route, or say plainly that no skill fits and send the user to `/skill:skill-gap-finder`, which names the owning skill or writes the brief that proves the gap. Never stretch a route over a situation it does not fit. Write each step as an invocation the user can paste, with one clause on why it comes next. Name what must exist before the first step (an approved plan, a pull request number, a failing command, an installed plugin) and the check that proves the route done (tests green, pull request opened, report delivered).
3. When two routes fit equally well, ask the one question that separates them, such as "Do you have an approved plan?" or "Is the cause known?". Never list every option.
4. Add a stance from Stances only when the user names one of its pressures (less code, replace instead of patch, correctness by construction, evidence before claims) or the step would otherwise bloat, patch around, or assert without proof. Stack it in the same message as the step it shapes; otherwise leave Stances out.
5. Run nothing yourself. Offer to start the first step, and start it only when the user says so. Steps that commit, push, post, or merge still need the user's explicit words for that act.

Spell each invocation the way the user's harness does: `/dstack-core:<slug>` in Claude Code, `$<slug>` in Codex, `/<slug>` picked by name in Cursor, `<plugin>:<slug>` in Hermes Agent, and `/skill:<slug>` in omp. On Grok, Kimi, or any other harness, use that harness's own invocation form with the same step order. This file writes every step in the harness-neutral form `/skill:<slug>`; translate it before the user types it. In Claude Code a skill from another plugin carries that plugin's name, such as `/dstack-git:resolve-merge-conflicts`. When a step sits in a plugin the user has not installed, add its install line: `claude plugin install <plugin>@dstack` in Claude Code or `codex plugin add <plugin>@dstack` in Codex; give no install spelling for other harnesses. A skill marked (user only) runs only when the user invokes it by name; name it for them to invoke. In any harness, orchestrate and fan out are trigger words for `/skill:parallel-launch` and `/skill:subagent-driven`, workflowz is one for `/skill:workflows-driven`, and orchestrate max asks for the widest safe fan-out for the rest of the session. Inside a running `/skill:autopilot` or `/skill:autoplan-and-autopilot` chain, these words and continue, go, or do it now resume that chain and start no new skill.

## The main flow: from request to shipped change

Most work runs along this line, and the author of these skills runs it as a loop: plan a slice, finish it, ship it, then plan the next slice.

1. Ground the stack when versions or libraries matter. `/skill:ground-latest` picks the current stable or LTS choice before code is written, `/skill:research` reads a named library's documentation, and `/skill:source-driven` keeps framework code tied to that documentation while you write it.
2. Clarify in plan mode. `/skill:askme` interviews you until scope, referents, and acceptance criteria are settled; stack `/skill:exhaustive` in the same message to be asked about every case. `/skill:architect` designs a non-trivial unit or surveys a codebase for its weakest module. `/skill:clarify` lists what is ambiguous in a written request, `/skill:decide` resolves a fork and applies the choice, and `/skill:generalize` states the rule a set of examples implies.
3. Plan. `/skill:plans` writes a plan that keeps every outcome and constraint, `/skill:plans-complete` proves it complete before code starts, and `/skill:autoplan` reviews a plan or idea from four perspectives and stops at an approval gate. Use `/skill:spec-driven` when requirements are unclear or the change crosses modules, and `/skill:wayfinder` when the work cannot fit one session and must be charted as decision tickets first.
4. Turn the approved plan into tasks. `/skill:todos-update` resyncs the task list with the plan and the tree, `/skill:todos-enhance` sharpens tasks that read as headings, and `/skill:todo-add` records one new requirement in the plan and the task list together; a message that starts with `TODO ADD:` fires it.
5. Execute. Every route here except `/skill:autoplan-and-autopilot` needs a plan from step 3 or the task list from step 4 first.
   - `/skill:autopilot` runs execute, simplify, review, finalize, and report under gates. It starts on plan-mode approval, a written approval (including a reply of approved, approve all, run it, or go on after the plan was presented), a plan subject passed in the invocation, or a request whose every item names a location and the expected change.
   - With only an idea and no plan, `/skill:autoplan-and-autopilot` reviews it, presents the amended plan, then runs the same gates. Invoking it with the idea approves local, reversible work; a push or any other outward act still waits for your explicit word.
   - To drive an ordered plan through subagents yourself, use `/skill:subagent-driven`; for independent pieces, `/skill:parallel-launch`, often stacked with it; for audits, migrations, and sweeps that one context cannot hold, `/skill:workflows-driven`. With either of the last two, name a width in the request to set the size of that wave.
   - `/skill:do-it-now` finishes the whole task list with no deferred phase and no follow-up remainder. The author reaches for it after almost every approved plan and after an `/skill:autopilot` halt. Say that the plan is approved in the same message, so nobody asks again.
6. Clean before shipping. The author's most repeated chain is `/skill:purge-slop-docs`, `/skill:tests-purge-unneeded`, then `/skill:code-simplification`: stale docs, tests that prove nothing, and dead code go in that order. `/skill:sync-docs` then updates docs a behavior change left stale; it does not steer a document toward a target state you name.
7. Verify and ship. `/skill:verification-before-completion` checks a claim of done against fresh evidence; the push skills run it before every push unless fresh evidence for the same tree exists. Name the publish target before you push: `/skill:commit` makes local atomic commits, `/skill:commit-push-pr` pushes a feature branch and opens or updates the pull request (it needs a configured remote and base branch), and dstack-git's user-only skills push to the current branch or to main. `/skill:code-review` reviews a named diff or pull request. `/skill:autowatch` takes one request all the way to an open pull request, then watches checks, reviews, comments, and conflicts until the change is decided. It also watches an open pull request you name.
8. Close the loop. `/skill:retro` looks back on a finished session or cycle with evidence. When it finds a lesson worth keeping, `/skill:autolearn` captures it from a verified fix you name, and `/skill:compound` from a closed knowledge-work session.

### At a phase boundary

A phase ends when you think "that part is done". Decide what happens to the context there, never in the middle of a phase.

- Continue in the same session when the next phase needs this one's reasoning word for word, such as going from planning to execution.
- Delegate a tightly scoped piece with `/skill:subagent-driven` or `/skill:parallel-launch` when it can run without you.
- Use `/skill:handoff` only when the work travels: to another harness, another directory, or a colleague.
- In a fresh session after a break, `/skill:recall` recovers the prior work and its status, and `/skill:catchup` explains what happened while you were away.

## On-ramps

Situations that create work and then join the main flow.

- Something broke and the cause is unknown, or the same fault keeps coming back: `/skill:grill-core` reproduces it and removes the fault class. A known local defect or a failing verifier: `/skill:fix`. A pasted `FIX:` block, traceback, or compiler output is input for one of those two, not a request to stack more skills. CI is red: `/skill:ci-fix`, which handles CI only; let its sweep mode or `/skill:autowatch` keep watching rather than invoking it again by hand.
- Review feedback arrived. For the comment batch on one pull request or merge request, `/skill:resolve-pr-comments`. For local findings, a pasted report, or an explicit mode choice, `/skill:resolve`. To repeat review and repair until clean, across one or more pull requests, `/skill:review-fix-loop`. Merge conflicts belong to `/skill:resolve-merge-conflicts` in dstack-git.
- You want an audit rather than a fix: `/skill:audit-project` for bugs, `/skill:security-review` for security.
- A repository is new to you or to the agent: `/skill:explore` maps it, `/skill:inits` records its costly conventions in AGENTS.md, `/skill:setup-repo` adds gitignore rules, hooks, and review rules, and `/skill:strict-validation-setup` sets up strict gates.
- You are rebuilding or porting a codebase: `/skill:breaking-driven` with `/skill:refactor-break-compat`, then `/skill:wayfinder` when the rebuild cannot fit one session. `/skill:fromzero` replaces an attempt from a clean pad and needs that attempt committed first.
- A dependency or version problem: `/skill:ground-latest` with `/skill:deps-upgrade` from dstack-code.

## Stances

A stance changes how a step is done, not what it does. Stack it in the same message as the step, the way the author writes `/skill:architect /skill:abstract-well` or `/skill:minimalism-driven /skill:breaking-driven`.

| Stance | Skills |
|---|---|
| Less code | `/skill:minimalism-driven`, `/skill:necessary-work`, `/skill:no-comments` |
| Replace instead of patch | `/skill:offensive-driven`, `/skill:breaking-driven` with `/skill:refactor-break-compat`, `/skill:fromzero`, `/skill:to-greenfield` |
| Rebuild from primitives | `/skill:from-first-principle`, `/skill:leave-only-first-principle` |
| Correct by construction | `/skill:type-driven`, `/skill:contract-driven`, `/skill:proof-driven`, `/skill:validation-first-driven`, `/skill:contraint-driven` |
| Tests | `/skill:tests-practices`, `/skill:tests-adversarial`, `/skill:exhaustive` |
| Evidence before claims | `/skill:no-excuses`, `/skill:doubt-driven`, `/skill:source-driven` |
| Abstraction shape | `/skill:tasty-abstraction`, `/skill:abstract-well`, `/skill:complexity-grill` |

## Codebase health

Upkeep, not feature work. `/skill:simplify` decides which level owns a cut and routes it: `/skill:code-simplification` for one module's interior, `/skill:architecture-simplification` for layout (explicit request only), `/skill:guillotine` for residue spread across code, docs, tests, and config, and `/skill:refactor-break-compat` for removing a consumer-facing surface. `/skill:docs-practices` decides whether a document should exist at all.

## Writing and visuals

`/skill:unslop` removes AI tells from prose. `/skill:writing-for-agents` shapes AGENTS.md files and other documents agents read. `/skill:show-me` turns an explanation into a table, chart, diagram, or mockup. `/skill:brainstorm` refines notes or a brain dump into an idea.

## Skills themselves

Before you write a skill, `/skill:skill-gap-finder` proves that no installed skill already owns the job. `/skill:writing-for-agents` then shapes the skill directory and its SKILL.md. Before you install or ship a skill, `/skill:skill-scanner` audits it for security risk. Deduplication, model retuning, and marketplace review live in dstack-skills.

## Session care

`/skill:enforce-workflow-constraints` holds a bounded workflow to its boundaries. `/skill:retune` remeasures a skill corpus on a new model. `/skill:let-fate-decide` picks among valid options when the user hands over the choice.

## Other plugins

Each plugin outside dstack-core has a reference beside this file. Read the one whose domain the situation names; its routes name every skill in that plugin.

| Reference | Read it when the situation involves |
|---|---|
| `references/dstack-planning.md` | framing a vague product idea, comparing options or viewpoints, a second opinion on a decision, an overbuilt plan that needs cutting, state machines, goal-state contracts |
| `references/dstack-code.md` | structural search and rewrite, dependency upgrades, unit mixing, a first screen that ships too many bytes, a question about one symbol or file |
| `references/dstack-review.md` | deep pull request review, visual or per-finding walkthroughs, adversarial interrogation, concealment patterns |
| `references/dstack-testing.md` | browser or Electron testing, CLI and TUI verification, smoke tests, TLA+ specs, verification loops that repeat |
| `references/dstack-git.md` | pushing straight to a branch or to main, atomic pull request series, merge conflicts, worktrees, stacked commits, gating and merging pull request queues, issue triage |
| `references/dstack-run.md` | splitting work across subagents, tasks that must run in order, sizing a run, watching a target, a loop that misbehaves, steps only a human can take, a long autonomous run |
| `references/dstack-infra.md` | CI/CD pipelines, deployment configuration, observability, Terraform, workflow capacity |
| `references/dstack-security.md` | security findings and triage, CodeQL, smart contracts, supply chain, crypto and zeroization audits |
| `references/dstack-fuzzing.md` | fuzz campaigns, harnesses, dictionaries, fuzzing blockers |
| `references/dstack-research.md` | sourced research reports, drift between docs and code, GitHub solution search, how a code path works |
| `references/dstack-knowledge.md` | saving and cleaning memory files, syncing after a gap, weekly reviews, summarizing past work, turning chat history into reusable steps |
| `references/dstack-learn.md` | learning a concept, onboarding to a repository, courses and capstones, restating an unclear answer |
| `references/dstack-skills.md` | deduplicating skills or shared doctrine, retuning skills for a new model, marketplace review, a personal taste skill |
| `references/dstack-writing.md` | documentation, READMEs, copywriting, plain-language and STE rewrites in English, Korean, or French |
| `references/dstack-visual.md` | a 3D workflow, a visual review of a pull request, a zoomable map of a pull request |
| `references/dstack-design.md` | UI design systems, prototypes, frontend fidelity, animation, visual benchmarks |
| `references/dstack-typescript.md` | TypeScript types, Node.js services, graceful shutdown, Node internals |
| `references/dstack-native.md` | C, C++, assembly, ABI, linking, ELF, GDB, sanitizers, kernels, Go, Zig cross-builds, reverse engineering |
| `references/dstack-rust.md` | Cargo, idiomatic Rust, async internals, FFI, unsafe, cross-compilation, Rust debugging and build times |
| `references/dstack-performance.md` | measured optimization, hot paths, heap profiling, SIMD, CPU kernels |
| `references/dstack-marketing.md` | developer marketing, launches, communities, content, search, competitive research |
