---
name: ci-cd
description: 'Use when setting up or modifying CI/CD pipelines, quality gates, test runners, or deployment pipeline configuration through workflow files. Not for triggering a deployment.'
---

# CI/CD and deployment configuration

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Setting up or modifying CI/CD pipelines, quality gates, test runners, deployment strategy, or configuring a deployment pipeline through workflow files. |
| Authority | Reversible local: writes only CI workflow and deployment configuration files in the local repository; rollback is version control. No remote mutation. |
| Side effect | Writes CI workflow and deployment configuration files locally; no deployment, publishing, credential, or remote mutation. |
| Done | Blocking gates in a fixed order, secret references via provider environment variables, a deployment stage with a rollback mechanism, and local schema validation are present. |

## Inputs

- The target repository and its CI provider (e.g., GitHub Actions, GitLab CI). Required; detected from existing configuration (`.github/workflows/` vs `.gitlab-ci.yml`) or from the verified repository remote URL, never assumed. If the provider is ambiguous, stop and ask; never default to GitHub. For GitLab, bind host and project path separately: the host comes from the remote URL or `GITLAB_HOST` (GitLab.com, Dedicated, or self-managed) and the project is the full `GROUP[/SUBGROUP]/PROJECT` path; for forks bind source and target projects separately.
- The quality gates the project requires. Required; defaults to the fixed gate order below.
- The project ecosystem commands that realize each gate (lint, type-check, test, build, integration, security audit, bundle size). Required.
- The deployment target and its rollback strategy. Required when a deployment stage is in scope.
- Any required deployment secrets, environment names, or build commands. Supplied by the user; this skill does not invent credentials.
- An existing pipeline to modify. Optional; supply when modifying rather than creating.

## Procedure

1. Bound scope: confirm the work is authoring or modifying CI workflow and deployment configuration files in the repository. Do not run deployments, publish artifacts, configure branch protection, place secrets in a remote manager, or mutate remote systems. Enumerate the exact files this skill will create or edit and show the set to the user before mutation. Write only those files. Done when: scope is bounded to local config file authoring and the file set is enumerated.
2. Identify the CI provider and target ecosystem. Detect from existing configuration or the verified remote URL; if the provider is ambiguous, stop and ask, never default to GitHub. For GitLab record host plus full project path (both projects for forks) before authoring any file. Done when: the provider and ecosystem are identified from existing config or supplied by the user.
3. Establish the fixed gate order that every PR/MR and push to main must pass, in this sequence: lint, type check, unit tests, build, integration tests, E2E (optional at construction; when included, blocking), security audit, bundle size. The order is fixed across ecosystems; only the commands change (Node: `pnpm exec biome check .`, `pnpm exec tsc --noEmit`, `pnpm exec vitest run`, `pnpm run build`; Python: `uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright`, `uv run pytest`, `uvx pip-audit`; Rust: `cargo clippy`, `cargo test`, `cargo build`, `cargo audit`). On GitLab the same order becomes `stages:` in `.gitlab-ci.yml` (one stage per gate, same sequence); scope merge-request pipelines with `rules: - if: $CI_PIPELINE_SOURCE == 'merge_request_event'` (https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/). Do not add stages the user did not request. Done when: the fixed gate order is established with ecosystem-specific commands.
4. Make every gate blocking. No gate may be skipped. If lint fails, fix lint; if a test fails, fix the code. Do not disable the rule or skip the test. Done when: every gate is configured as blocking with no skip path.
5. Reference secrets via environment variables expected from the provider. Never store secrets in code or in workflow configuration files. The user places secrets in the provider's secret store out of band; this skill only writes the variable references. Done when: secrets are referenced as masked env vars in the workflow file, not stored in any committed file.
6. Author the deployment stage with a rollback mechanism. Configure the deployment pipeline stages (build, test, deploy) using the user-supplied platform, environment, and commands. Include a defined rollback step. Do not add stages the user did not request. Done when: the deployment stage has a rollback mechanism and only user-requested stages.
7. Validate the authored files locally. Run the project's local check set (lint, build, test) against the pipeline definition. If the platform provides a local validation command for the workflow file, run it (`actionlint` for GitHub Actions, `glab ci lint [--dry-run] [--ref <branch>] [--include-jobs]` for GitLab, see https://docs.gitlab.com/cli/ci/lint/). No `glab mr` command has a general dry-run (the dry-run surface is CI-only), so preview MR effects by local computation or JSON reads, never by submitting. Do not trigger a deployment. Done when: every local check and platform validation command is run with pass or fail recorded.
   - Interpret trigger filters using the CI provider's documented grammar, not a generic glob or regex engine. Before changing a filter, state intended included and excluded events and verify representative boundary cases against that grammar; a numeric version triple is not a complete SemVer grammar. On GitLab this is the `rules:if` grammar (`$CI_PIPELINE_SOURCE == 'merge_request_event'`, branch patterns per https://docs.gitlab.com/ci/jobs/job_rules/). For action, tool, image, runner, and toolchain pins, record the primary source and resolved commit or artifact identity. Resolve annotated tags to their commit and verify asset digests through the applicable release source. Treat runner/runtime updates as possible compatibility-floor changes; do not claim a floor violation without target evidence. Distinguish YAML parsing, workflow validation, embedded-shell analysis, and actual job execution; report which occurred and never imply shell checking merely because a workflow linter ran.
8. When a CI run has already failed, route the failure back to the agent that owns the change: copy the failing job name, the error text, and the repo state at failure, so the root cause is fixed rather than re-run. For a GitLab MR read the head pipeline with `glab ci get --merge-request <iid> -F json` (explicit host from the remote URL or `GITLAB_HOST`, project via `-R GROUP/PROJECT`; forks need source/target projects bound separately; note `-p` on this command selects a pipeline ID, it is not a page flag), enumerate every page on list reads (`glab ci list -P/--per-page` with `-p`, or `glab api --paginate` for REST reads), and pull logs with `glab ci trace <job>`; the ci-fix helper `../../../odin-core/skills/ci-fix/scripts/inspect_mr_checks.py --host HOST --project GROUP/PROJECT --mr IID --json` is the scripted equivalent. Match the pipeline `sha` against the MR head SHA, since a missing, skipped, or unrelated-successful pipeline is not proof. Skip this step when setting up a new pipeline that has no failure yet. Done when: the failure is routed to the owning agent with job name, error text, and repo state, or the step is skipped for a new pipeline.
9. Verify all gates are present, the pipeline runs on every PR/MR and push to main, secrets are referenced via env vars, deployment has a rollback mechanism, and local schema validation passes. Done when: every done-predicate element is verified present.

## Failure and recovery

- Unsupported CI provider: stop and report; do not guess a provider-specific schema.
- Missing required ecosystem commands: stop and ask the user; do not invent commands.
- Gate failure: fix the code or configuration that caused the failure. Never disable the gate, skip the test, or re-run a flaky test; fix the flakiness.
- Secret leak in a config or code file: remove the secret from the file, rotate it, and re-reference it as an env var before proceeding.
- Missing rollback: do not mark deployment configuration done; add the rollback mechanism first.
- Validation fails: report the failing check with its file and line; do not mark the pipeline verified. Leave the edited files in place for the user to correct, or revert them to their prior state on user request.
- Partial result: keep all completed gate configuration, but do not commit a pipeline that is missing a blocking gate, a secret boundary, or a rollback. The blocked result is a report listing exactly which done-predicate element is missing and what was tried.
- Rollback: the edited CI or workflow files are version-controlled; restore them from VCS to the pre-edit state.
- MR head moved during review: prior pipeline and approval evidence is invalid; re-read the MR head SHA and its pipeline before reporting gates green.
- Platform-side merge gates (required approvals, unresolved discussions, draft state, project merge policy) are enforced by the forge, not authored here; never treat CI green as merge approval and never bypass these gates from pipeline configuration.

## Output

`.github/workflows/*.yml` or `.gitlab-ci.yml` (per the detected provider) plus deployment configuration files in the repository implementing the fixed gate order, blocking gates, secret references via environment variables, a deployment rollback mechanism, and local schema validation, plus a report listing files written and per-check pass or fail status. No deployment triggered.
