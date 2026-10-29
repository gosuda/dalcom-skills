---
name: ground-latest
description: 'Use when starting or scaffolding a codebase or service, migrating, refactoring, or picking language, framework, or dependency, or latest, LTS, or modern way. Not for remote or irreversible changes.'
---

# Ground latest

Pin what is stable and supported today, with dated evidence a later reader can check.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Starting a new codebase or service, scaffolding, migrating or refactoring, picking a language edition, runtime, framework, or dependency, or the user asks for the latest, current, LTS, or modern way |
| Authority | Reversible local: writes only a dated grounded set into the change (plan, ADR, or PR body). Rollback is version control or undo. No remote mutation |
| Side effect | A dated grounded set of pinned versions with release-channel links, LTS-versus-latest decisions, support windows, per-version security applicability, and maintenance context. Pre-release and deprecated choices are dropped with named replacements |
| Done | Every pinned choice carries an exact version, release date, support status, source citation, LTS-versus-latest decision, and exact-version security applicability. Maintenance history is recorded as context. Nothing is pinned from recall |

## Inputs

- The change being grounded (plan, ADR, or PR body) and the list of choices it pins: language edition, runtime, each framework and dependency, build and test tooling, and the platform baseline. That list is the grounding set.
- Existing repo pins and version floors (as available): a floor is a minimum constraint, not a frozen choice; an existing exact pin is a recorded default that can be raised, never a silent freeze.

## Procedure

1. List every choice this change pins: language edition, runtime, each framework and dependency, build and test tooling, and the platform baseline. That list is the grounding set. Nothing is grounded until this list is complete.
2. Look each entry up at its own release channel today: the project release page, changelog, or registry metadata. Recall is not a source. Record the source URL or page for each entry. For support windows and LTS tracks, query the endoflife.date product record at `https://endoflife.date/api/v1/products/<product>/` in addition to the release channel. For security applicability, check the project advisory source for that entry (project security page, GitHub Security Advisories for the repository, OSV, or NVD) and record which advisory source was checked. Recall is not an advisory source.
3. Record per entry the current stable version with its release date, the current LTS version with its release date where the project runs an LTS track, and the end-of-support date for each pinned candidate. Cite the release-channel source and the support-window source separately.
4. Separate floors from pins. A compatibility floor sets the lowest acceptable version: the selected version must satisfy the floor, the floor never freezes the choice at the floor version, and the preferred pick remains the latest stable LTS satisfying the floor, otherwise the latest stable satisfying the floor. An existing exact repo pin is the recorded default, not a freeze: compare the pin against the preferred pick, retain the old pin only when project policy or a verified incompatibility requires it, and otherwise raise to the preferred pick. Name every override: the old pin or floor, the selected version showing the floor is satisfied, and the reason the pin was retained or raised.
5. Read the chosen version current recommended pattern from its release-channel documentation before writing against it. Renamed APIs and replaced defaults are where recalled code breaks. Do not write code against a recalled API.
6. Assess maintenance as context under one rule: record the last 24 months of activity history, the repository archive status, applicable unresolved critical advisories affecting the selected exact version, and evidence of ecosystem adoption and de-facto use such as downstream dependents, distribution packaging, or continued integration references. Archive status is evidence inside this assessment, not an automatic rejection. An archived project with an endorsed successor moves to the successor. An archived project with no successor, and a long-quiet project with no release, stands or falls on advisory applicability and adoption evidence with the reasoning recorded. Never reject a stable project solely because its last commit, release, or security fix is old.
7. Apply advisories at exact-version scope. Check whether each known critical advisory applies to the selected exact version, not merely to the product name. Cite the advisory source, the advisory identifier, and the affected range. When an applicable unresolved critical advisory affects the selected version, do not pin that version silently: select the patched version where one exists, or report the entry as blocked with the advisory identifier and affected range.
8. Drop pre-release choices and deprecated choices, and name the maintained stable replacement pinned instead.
9. Leave the grounded set in the change (plan, ADR, or PR body) as one per-entry table with versions, dates, links, and a grounding date, so the next reader sees when it was grounded. Include per entry the pinned version, stable or LTS status, release date, end-of-support date, release-channel link, support-window source, LTS-versus-latest decision, any repo pin or floor that applied with its disposition, the maintenance context with its sources, the API-pattern change consulted, and the exact-version security applicability with advisory citations.

## Failure and recovery

- No release channel reachable for an entry: mark that entry ungrounded. Do not pin from recall. Report which entry blocked and which channel was tried.
- Support-window source unreachable: record the release-channel facts obtained, mark the support date unconfirmed with the source attempted, and continue the remaining entries. Do not present the support date as confirmed.
- Advisory source unreachable for an entry: record the release facts obtained, mark security applicability unconfirmed with the source attempted, and do not present the version as advisory-clear.
- LTS-versus-latest conflict with no project policy: record both candidates with dates and defer the decision to the human. Do not silently pick.
- A choice is pre-release or deprecated and no maintained replacement exists: mark it dropped-without-replacement and name the gap. Do not retain the dropped version.
- An applicable unresolved critical advisory affects every available stable candidate: mark the entry blocked with the advisory identifier, affected range, and sources attempted. Do not pin the affected version with a disclaimer.
- Partial result: write only entries grounded from a release channel today. List ungrounded entries as blocked, never filled from recall.

## Output

A dated per-entry table written into the change (plan, ADR, or PR body). Per entry: pinned version, stable or LTS status, release date, end-of-support date, release-channel link, support-window source, LTS-versus-latest decision, any repo pin or floor with its retained-or-raised disposition, 24-month maintenance context with archive status and adoption evidence, API-pattern source, and exact-version security applicability with advisory citations. Dropped choices are listed with their named replacement or marked dropped-without-replacement. Blocked entries name the exact missing source, decision, or prerequisite.
