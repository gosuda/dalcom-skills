# Repository contract

## Offensive posture

Work offensive-first: replace broken structure contract-first instead of patching around it. [Tony Hoare]

Let the break drive the scope: reproduce the fault class, then remove it; migrate every caller and leave no shim. [Tony Hoare]

Take only offensive moves that advance the contract; add no defensive scaffolding, speculative hardening, or busywork. [Tony Hoare]

Finish actionable work in this pass: ship no placeholder, deferred phase, or follow-up promise. [Tony Hoare]

Raise no invented excuse: when authority or a prerequisite is missing and unreachable through tools or context, finish all independent reachable work first, then report blocked. [Tony Hoare]

Forge no evidence and bypass no security boundary; this posture grants no new remote or destructive authority. [Tony Hoare]

Repository maintenance workflow, including publishing, gates, and distribution, lives in `CONTRIBUTING.md`; read it before maintainer work. [Tony Hoare]

## Code intent

Write no explanatory code comments and keep no commented-out code; remove commented-out code when found. [J.R.R. Tolkien]

Carry intent in names, types, and control flow so the code reads without commentary. [J.R.R. Tolkien]

Keep the narrow compiler/lint/invariant exception: minimum `// SAFETY:` comments where `undocumented_unsafe_blocks` is denied, plus necessary rustdoc and module invariants, load-bearing clause identifiers, evidence rows, and measured numbers. [Tony Hoare]

Claim no supplied count as a measured outcome; the meaning and proof floor outranks any reduction percentage. [Tony Hoare]

Weaken no existing lint and invent no new lint requirement. [Tony Hoare]

## Test strength

Reject any weak test; a test that cannot fail on a plausible real fault earns no place in the tree. [Tony Hoare]

Accept only independent invariant or adversarial oracles that detect a plausible real fault and survive equivalent refactors. [Tony Hoare]

Fixture inputs and setup are allowed; fixture oracles are not: reject snapshot fixture oracles, contract literal pins, naive regression captures, mock echoes, and source-text assertions. [Tony Hoare]

Keep the proof set selective: keep only oracles that each detect a distinct plausible fault; reject the rest. [Tony Hoare]

Use each proof as an offensive move: break the fault class first, then hold the invariant. [Tony Hoare]

