# DStack Infra

DStack workflows for CI, deployment, observability, cost, and infrastructure tooling. Install it with `claude plugin install dstack-infra@dstack` in Claude Code or `codex plugin add dstack-infra@dstack` in Codex; Claude Code invokes its skills as `/dstack-infra:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- Red CI is core `/skill:ci-fix`; building or changing pipelines and quality gates is `/skill:ci-cd`.
- Environment-dependent code or missing runtime configuration: `/skill:environment-contract-audit`. Telemetry, alerts, and production diagnosis: `/skill:observability`. Terraform: `/skill:terraform-style-check` (user only). CI capacity and required-check safety: `/skill:workflow-capacity-audit` (user only).
