# DStack Security

DStack workflows for security review, vulnerability triage, and defensive implementation. Install it with `claude plugin install dstack-security@dstack` in Claude Code or `codex plugin add dstack-security@dstack` in Codex; Claude Code invokes its skills as `/dstack-security:<slug>`. Read a skill's SKILL.md before you recommend it.

## Routes

- Start from core `/skill:security-review` for a diff or a component.
- One concrete finding: `/skill:triage-security-finding`; a named allegation that needs a verdict: `/skill:security-finding-verification`; a report, CVE, or bounty submission: `/skill:vulnerability-triage-brocards` (user only).
- Analysis: `/skill:codeql-security-analysis`, `/skill:project-findings-onto-graph`, `/skill:function-audit-context-analyzer` (user only). By domain: `/skill:c-security-review` (user only), `/skill:zeroize-audit`, `/skill:vector-forge`, `/skill:mermaid-to-proverif` (user only), `/skill:supply-chain-risk-auditor` (user only), `/skill:yara-rule-authoring` (user only).
- Smart contracts: `/skill:smart-contract-guidelines-advisor`, `/skill:smart-contract-secure-workflow`, `/skill:chain-vulnerability-scanner` (user only), `/skill:token-integration-analyzer` (user only).
