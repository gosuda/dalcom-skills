---
name: supply-chain-risk-auditor
description: 'Use when assessing npm, PyPI, or Go dependency supply-chain risk, with lockfile-absent paths marked unassessable. Not for remote or irreversible changes.'
disable-model-invocation: true
---

# Supply chain risk auditor

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user asks to assess third-party package or dependency supply-chain risk for a project using npm, PyPI, or Go manifests, with lockfile-wide advisory coverage where supported. |
| Authority | Reversible local: writes only the named local artifacts (`findings.json`, `report.md`) outside the audited repository; rollback is deleting both files. No remote mutation. |
| Side effect | Never installs, builds, imports, or executes the audited project or dependencies and never reads dependency source. Performs network metadata queries and writes deterministic findings.json plus report.md outside the audited repository. |
| Done | The report contains direct-dependency risk findings, supported lockfile-wide version-matched advisories, three-state assessed-clean/assessed-flagged/unassessable coverage, exact measured data, and clearly separated remediation judgment without treating unavailable data as risk or absence as safety. |

## Inputs

1. **Project path** (required): directory containing a manifest file (`package.json`, `requirements.txt` / `pyproject.toml`, or `go.mod`).
2. **Lockfile** (optional): if present (`package-lock.json`, `poetry.lock`, `Pipfile.lock`, `go.sum`), the auditor resolves transitive dependencies and matches advisories to exact resolved versions. If absent, direct dependencies are assessed against declared version constraints and all transitive dependencies are marked unassessable.
3. **severity_floor** (optional): the minimum advisory severity shown as an actionable finding. Default: `medium`. This is the only severity floor for this skill and applies after the existing three-state coverage calculation; it never changes a dependency's state.
4. **Output directory** (required): directory where `findings.json` and `report.md` are written. Defaults to a directory adjacent to the audited project.

## Refusal

- Missing manifest: return `findings.json` with an empty dependencies array and all counts zero; `report.md` states no recognized manifest was found.
- Network failure or rate limit: mark affected queries as unassessable; return partial results for completed queries. Never retry with widened scope.
- Malformed advisory response: mark the affected dependency as unassessable; do not guess vulnerability status.
- Any step would require execution: stop and mark the dependency as unassessable. The procedure never installs, builds, imports, or executes the audited project or its dependencies. It never reads dependency source code.

## Procedure

1. **Identify the ecosystem** from the manifest file type. If no recognized manifest exists, mark all dependencies as unassessable and proceed to step 5. Done when: the ecosystem is identified or all dependencies are marked unassessable.

2. **Parse the manifest** to extract direct dependencies with their declared version constraints. For npm: parse `package.json` `dependencies` and `devDependencies`. For PyPI: parse `requirements.txt` lines or `pyproject.toml` `[project.dependencies]` and `[tool.poetry.dependencies]`. For Go: parse `go.mod` `require` blocks, distinguishing direct (`// indirect` absent) from indirect. Done when: direct dependencies are enumerated with version constraints.

3. **Resolve exact versions.** If a lockfile is present, parse it to resolve exact versions and enumerate transitive dependencies. For npm: parse `package-lock.json` `packages` for resolved versions. For PyPI: parse `poetry.lock` or `Pipfile.lock` for pinned versions. For Go: parse `go.sum` for module hashes and `go.mod` for versions; `go.sum` confirms module integrity but `go.mod` carries the version. If no lockfile is present, use declared version constraints from the manifest for direct dependencies and mark all transitive dependencies as unassessable with reason `no-lockfile`. Done when: exact versions are resolved for direct dependencies, and transitive dependencies are enumerated or marked unassessable.

4. **Query the ecosystem advisory source** for each dependency. Load `references/ecosystem-queries.md` and apply the query method for the detected ecosystem. The existing ecosystem query owner remains authoritative: npm uses the existing `npm audit --json` path; PyPI uses the existing OSV query path; Go uses the existing `vuln.go.dev` path. Do not invoke a second scanner for an ecosystem already handled by `references/ecosystem-queries.md`. Record advisory ID, severity, affected version ranges, and fixed version for each match; each recorded advisory carries `advisory_id`, `affected_range`, `severity` (when the source supplies it or it is derivable from the advisory), `fixed_versions` (when supplied), and `patchable`. Classify each direct dependency into one of three states:
   - assessed-clean: advisory query succeeded and returned no matching vulnerabilities for the resolved version.
   - assessed-flagged: advisory query returned one or more matching vulnerabilities.
   - unassessable: advisory source was unreachable, rate-limited, returned malformed data, the dependency has no resolved version, or the dependency is transitive with no lockfile.
   Apply `severity_floor` only after this classification: below-floor advisories stay assessed-flagged and are counted as suppressed-by-floor rather than relabeled clean; advisories with missing severity are never suppressed and never treated as safe.
   Done when: every direct dependency has a state and every query is attempted.

5. **Compile `findings.json`** with the structure: `{ dependencies: [{ name, version, ecosystem, direct, state, reason, advisories: [{ advisory_id, affected_range, severity, fixed_versions, patchable }] }], summary: { total, assessed_clean, assessed_flagged, unassessable, severity_floor, suppressed_by_floor, patchable, unpatchable } }`, where `reason` is present when `state` is unassessable and `patchable` / `unpatchable` count advisories with and without a supplied fix, derived from the per-advisory `patchable` flags. Done when: `findings.json` is written.

6. **Generate `report.md`** containing: direct-dependency risk findings with per-dependency state and advisory detail (advisory IDs, affected ranges, fixed versions when the source supplies them, and patchable versus unpatchable status), lockfile-wide version-matched advisories for transitive dependencies (if the lockfile was available), the applied severity floor with the suppressed-by-floor count shown separately, patchable versus unpatchable counts derived from the per-advisory `patchable` flags, coverage summary with counts for each of the three states computed before severity filtering, unassessable dependencies with their reason, and remediation recommendations prioritized by severity and clearly separated from measured findings. A clean conclusion is permitted only for the portion whose advisory queries completed and whose exact-version coverage is assessed-clean; unassessable dependencies remain visible in the coverage section. Done when: `report.md` is written.

## Failure modes

- Rollback: delete `findings.json` and `report.md` from the output directory.
- Unrecognized manifest: write `findings.json` with empty dependencies and zero counts; `report.md` states no recognized manifest was found.
- Network failure: mark affected dependencies unassessable with reason `network-failure`; continue with completed queries.
- Malformed advisory response: mark the affected dependency unassessable with reason `malformed-response`; do not guess vulnerability status.

## Output

`findings.json` (structured JSON with per-dependency risk assessment, advisory matches, coverage summary, and unassessable reasons) and `report.md` (human-readable report with direct-dependency findings, lockfile-wide advisories, three-state coverage, unassessable dependencies with reasons, and separated remediation guidance).
