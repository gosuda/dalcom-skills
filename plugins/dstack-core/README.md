# DStack Core

Cross-project workflows for planning, implementation, review, verification, and delivery.

83 skills, category Coding. Install the whole plugin below, or take a single skill with `gh skill install`.

## Install

```bash
# Claude Code
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-core@dstack

# Codex
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-core@dstack
```

### Individual (gh skill)

```shell
gh skill install gosuda/dalcom-skills plugins/dstack-core/skills/<skill> \
  --agent <agent> --scope user
```

`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.

Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.

## Skills

Each row states when to reach for the skill. Invoke one as `/dstack-core:<name>` in Claude Code, `$<name>` in Codex, or type `/` and pick it in Cursor.

| Skill | Trigger |
|---|---|
| abstract-well | Use when the user wants to classify abstractions as useful, bad, or busy and keep one shallow level. |
| architect | Use when non-trivial code needs a design, codebase architecture needs improving through survey and deepening, or one module needs targeted interface narrowing, seams, or testability. |
| architecture-simplification | Use when the user explicitly asks to simplify an architecture, collapse modules or crates, or cut a dependency graph within approved boundaries. |
| askme | Use when eliciting intent/scope/referents or gating long/bundled/high-stakes/hard-to-undo work: exhaustive/collaborative/adversarial/grill/gate/batch/interview/proposal/pairing. |
| audit-project | Use when the user says "audit my code", "find all the bugs", "review until clean", or "grill my changes". |
| autolearn | Use when a verified fix yields a generalized well-abstracted invariant with enforcement or proof, or existing solution docs need bounded refresh. |
| autopilot | Use when a human has an approved delivery plan and wants the full chain run under phase gates. |
| autoplan | Use when the user runs /autoplan on a plan or idea. |
| autoplan-and-autopilot | Use when the user invokes /autoplan-and-autopilot on an idea or plan to review across four perspectives, derive a task ledger, present for approval, and execute under verified phase gates. |
| autowatch | Use when the user explicitly asks for autonomous end-to-end work from request to open pull request or merge request with CI watched to decided. |
| brainstorm | Use when capturing or refining notes, a transcript, a brain dump, or an existing idea, or when a concrete visual question is clearer shown in a local browser. |
| breaking-driven | Use when bloated code needs clean re-derivation, or the user says "this module is bloated" or "break it and rebuild". |
| catchup | Use when the human returns after a gap, cannot follow the project, asks what happened, or wants a visual HTML recap page. |
| ci-fix | Use when "CI is red", "fix the checks", or "make CI green", one check needs classifying, or a bounded sweep runs. |
| clarify | Use when the user says "clarify", "what is ambiguous here", or when a prompt or spec reads as under-specified before planning. |
| code-review | Use when a named diff or pull request needs review for bugs, regressions, tests, and standards. |
| code-simplification | Use when a named module, file set, or dependency slice needs less code and structure without losing required behavior. |
| commit | Use when asked to commit working-tree changes as typed atomic local commits. |
| commit-push-pr | Use when asked to commit and push a feature branch, with or without a pull request or merge request. |
| complexity-grill | Use when a user wants to identify the true sources of complexity qualitatively before counting metrics. |
| compound | Use when the user explicitly asks to save a generalized invariant from a closed knowledge-work session. |
| contract-driven | Use when crossing a public API boundary, guarding complex invariants, or hardening untrusted input or integration seams. |
| contraint-driven | Use when no quality bar is written down, when setting up constraints, or when implementing under non-negotiable budgets, limits, or API rules. |
| decide | Use when the user has a fork and wants it resolved and applied, not explored: "decide this", "choose the path", or "decide and fix it". |
| do-it-now | Use when the user asks to finish the whole task now, clear active todos, or unblock undone implementation without deferred phases or follow-up remainders. |
| docs-practices | Use when deciding whether a durable document, ADR, plan, or spec is needed, or when checking its invariant quality, scope, and naming. |
| doubt-driven | Use when a non-trivial decision sits under uncertainty and correctness matters more than speed. |
| enforce-workflow-constraints | Use when any bounded workflow starts or reaches an action, path, proposal, or merge boundary. |
| exhaustive | Use when asked to prove coverage, find missing cases, or enumerate state, decision, requirement, or behavior space. |
| explore | Use when asked to explore the codebase to map structure, symbols, and dependencies. |
| fix | Use when the user asks to fix a local bug, make a verifier pass, or implement an already-adjudicated repair. |
| from-first-principle | Use when a user wants to rebuild a design, organization, or API from primitives. |
| fromzero | Use when replacing a greenfield attempt with a clean pad of verified requirements. |
| generalize | Use when asked to derive the general rule a request carries as examples instead of a stated rule, then bound it. |
| grill-core | Use when the cause is unknown, the fault recurs as a class, or a review comment needs a root-design repair rather than a patch. |
| ground-latest | Use when starting or scaffolding a codebase or service, migrating, refactoring, or picking language, framework, or dependency, or latest, LTS, or modern way. |
| guillotine | Use when dead, duplicate, superseded, or generated residue must leave more than one artifact class of a repo or subsystem, preserving behavior. |
| handoff | Use when work reaches a session boundary or the user asks to hand off, delegate, or get a clipboard-ready prompt. |
| inits | Use when onboarding to a repository, capturing costly conventions, constraints, or rationale, or improving AGENTS.md. |
| leave-only-first-principle | Use when asked to prune a design or codebase until only primitives remain, producing a first-principles map. |
| let-fate-decide | Use when the user says let fate decide, YOLO, dealer choice, surprise me, whatever, or delegates a vague choice in a casual or playful tone, or when you are about to pick arbitrarily between valid options. |
| minimalism-driven | Use when writing or restructuring code, before adding a helper, wrapper, config key, or dependency, or when the user asks for minimal or DRY code. |
| necessary-work | Use when work is about to grow past the ask, the task may already be done, or the user requests only the minimum. |
| no-comments | Use when asked to remove source comments by replacing them with clear code or accessible documentation. |
| no-excuses | Use when a material claim rests on missing proof, an untested assumption, or unresolved counterevidence that investigation can still settle. |
| offensive-driven | Use when the user explicitly asks for a replacement-first pass such as "rebuild it clean", "replace-first", or "offensive pass on <target>" spanning code, docs, plans, or research. |
| parallel-launch | Use when work splits into independent sub-tasks or cross-domain research. |
| plan | Use when multi-step work needs a structured implementation plan that preserves outcomes and constraints. |
| plan-complete | Use when a plan must be proven complete before implementation begins. |
| proof-driven | Use when property-based testing, theorem proving, or formal proof tactics require zero unproven properties. |
| purge-slop-docs | Use when a human asks to purge stale docs, clean Markdown, or reorder the documentation hierarchy. |
| recall | Use when asked to recover prior work and current status before resuming. |
| refactor-break-compat | Use when modernizing APIs, removing compat shims, killing feature flags, or rewriting a subsystem cleanly. |
| research | Use when researching a named library, framework, SDK, API, or service, or finding a migration guide. |
| resolve | Use when local feedback needs adjudication, or the user explicitly chooses analyze, reception, summary, interactive, or autonomous mode for one feedback batch. |
| resolve-pr-comments | Use when handling GitHub PR or GitLab MR review threads, top-level comments, or review bodies on one named PR/MR in a single batch: enumerate completely, judge against current code, repair valid findings at the root, and post only explicitly approved replies and resolutions. |
| retro | Use when a finished session, period, milestone, or cycle needs an evidence-backed look-back, or an existing system needs its unexplained rationale recovered. |
| retune | Use when a skill corpus degrades on a new model and needs measurement-first retuning against a registered bar. |
| review-fix-loop | Use when review and repair must repeat to an evidenced end state, locally or across one or more GitHub PRs or GitLab MRs. |
| security-review | Use when changes touch auth, parsing, dependencies, network, or pre-release, or a diff or baseline needs regression review, or the user asks for a security review, vulnerability audit, or OWASP review of a supplied file, diff, or component, covering injection, XSS, auth, or crypto, with high-confidence findings only (mode: confirmed), or an API, configuration schema, cryptographic interface, authentication surface, or library design is audited for misuse resistance or footguns at a caller-named target (mode: edges, inline or delegated specialist). |
| setup-repo | Use when the user asks to set up a repository: deterministic gitignore, repository-native pre-commit hooks, or REVIEW.md and CONTRIBUTE.md rules that enforce anti-slop, anti-spaghetti, and offensive-minimalism defaults. |
| show-me | Use when asked to show/diagram: comparison table, data record, metric card, stepper, mockup, numeric chart, interactive explainer. |
| simplify | Use when the user asks to simplify a change-set, diff, branch, or module and the right level is not yet decided; routes each cut to the simplification skill that owns it. |
| source-driven | Use when writing or verifying framework-specific code, boilerplate, or a documented, correct implementation. |
| spec-driven | Use when starting a project or feature, requirements are unclear, or a change crosses modules. |
| strict-validation-setup | Use when a user invokes a strict-mode validation or verifiable-goals loop setup. |
| subagent-driven | Use when a user says execute with subagents or hands over an ordered multi-task plan. |
| sync-docs | Use when a behavioral diff may have left docs or CHANGELOG stale, or when tidy targets stale code comments. |
| tasty-abstraction | Use when a user wants to design an abstraction boundary that collapses a complex implementation into a simpler interface without leaking internal state. |
| tests-adversarial | Use when hardening error handling, validating boundary behavior, or hunting silent failures. |
| tests-practices | Use when developing a fix or feature test-first, plan a TDD build, or work red-to-green in slices. |
| tests-purge-unneeded | Use when a legacy, slow, or duplicate test suite needs purging, a post-refactor sweep is due, or types cover a contract. |
| to-greenfield | Use when the user says greenfield this or rescue this codebase, names a field (dark, red, blue, or brown), or diagnoses a subsystem. |
| todo-add | Use when a message contains `TODO ADD: <requirement>`. |
| todos-enhance | Use when tasks are too vague, read as headings, or the user asks to sophisticate the todos. |
| todos-update | Use when user asks to update todos, resync the task list, say what to do next, or plan and tree have drifted apart. |
| type-driven | Use when modeling a domain, encoding a state machine, hardening APIs, making invalid states unrepresentable, or parsing instead of validating. |
| unslop | Use when prose is drafted or edited, reviewed for AI tells, or the user asks to remove AI patterns, humanize, or add voice. |
| validation-first-driven | Use when protocols, workflows, concurrency, or lifecycle state need states, transitions, and temporal properties. |
| verification-before-completion | Use when a task, feature, or fix is called done, complete, finished, or fixed, or before a commit, PR, or next task. |
| wayfinder | Use when a greenfield project or large feature build will not fit in a single agent session and the route must be charted as decision tickets first. |
| workflows-driven | Use when work decomposes across subagents or phases: audits, migrations, research sweeps, or scale one context cannot hold. |
| writing-for-agents | Use when authoring or restructuring an agent-consumed document, a SKILL.md or skill directory, writing skills, or deciding a skill split-or-monolith disclosure question. |

## Workflows

[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.
