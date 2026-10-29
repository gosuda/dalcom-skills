---
name: resolve-pr-comments
description: 'Use when handling GitHub PR review threads, top-level comments, or review bodies on one named PR in a single batch: enumerate completely, judge against current code, repair valid findings at the root, and post only explicitly approved replies and resolutions. Not for repeated review loops, merge policy, or conflict resolution.'
---

# Resolve PR comments

## Contract

| Field | Bound contract |
|---|---|
| Trigger | An explicit request to handle review feedback on one PR: blank for the current branch PR, a PR number, or a comment/thread URL for targeted scope. |
| Authority | Read-only intake and judgment. Local reversible source edits for valid repairs. Human-gated remote reply, thread resolution, and push of explicitly approved repair commits to the explicitly approved ref. No merge, base change, history rewrite, reopen, credential change, or publication beyond the approved set. A configured remote alone grants no authority. |
| Side effect | Local edits and targeted proof for valid findings. Only explicitly approved replies, resolutions, and pushes reach the remote. |
| Done | Every actionable item carries one verdict with evidence at the recorded head. Valid repairs are applied locally with proof. Every authorized reply, resolution, and push carries a parsed receipt plus read-back. The observed open set matches the intended open set. New findings return as next-batch input. |

One batch lives here: validity against current code, root repair, and authorized thread handling. Repeated coordination across batches belongs to the caller. Landing policy belongs to the gate. Stopped-hunk mechanics belongs to conflict resolution. This skill has no aliases.

Preconditions: owner/repo, PR number, PR state, full 40-hex head OID and ref, base repository/ref/OID, and the code revision read for judgment are recorded before any verdict. Postconditions: no verdict without cited code evidence at the recorded revision; no remote write without exact-text approval and a verified receipt; no claim that silence, state, exit zero, or a green run proves handling. Preserved invariants: full node IDs are the identity; subjects, paths, positions, markers, prefixes, suffixes, and vendor counts are hints only; an empty or failed search proves nothing.

## Inputs

- Target: blank, PR number, or comment/thread URL. Required.
- Checkout: PR head at the recorded full OID, or the exact file revision read for each verdict. Required for any fix or decline.
- Access: authenticated `gh` for reads; reply, resolve, and push permission only when each posting was approved. Report authentication or remote failures and stop.
- Approved mutation set: exact reply bodies, resolution choices, exact repair commits and push destination ref, expected full head OID, acting account. Required before any write. Timeout or auto-selection is not consent.
- Proof command: the targeted test or project check used for each repair, recorded when used.

## Procedure

1. Bind target and freshness. Record owner/repo, PR number, open or closed state, full head OID and ref, base repository/ref/OID, and the revision read for judgment. Resolve a blank target from the current branch inside the target repository. Resolve a comment URL with `scripts/get-thread-for-comment` before judging. Confirm the working checkout equals the recorded head with `git rev-parse HEAD`. A merged or closed PR is not an active fix branch: report state and stop without recreating its head or opening a follow-up. Done when: one target identity and one full head OID are recorded and matched to the checkout.

2. Enumerate the complete batch before judging. Keep resolved threads in the accounting census. Run `scripts/get-pr-comments <PR> [OWNER/REPO]` once: the action view is `review_threads` (unresolved threads with `isOutdated` intact), `pr_comments` (non-author top-level comments), and `review_bodies` (non-empty non-author review bodies). The accounting census is the same output `all_review_threads` with per-thread `totalCount`; completeness is the same output `coverage` object: `threads_complete` true and `truncated_comment_threads` empty. The bundled helper retains full node IDs for every source: thread comment nodes carry `id`, top-level comment nodes carry `id`, and review-body nodes carry `id`; the caller requires those IDs for identity and per-item output. Feed pages from files through `jq`, never through argv. Split each body into distinct items, including body-only review and top-level comment findings that never became threads. Drop only non-actionable wrappers, approvals, badges, and status summaries with a stated reason. Keep actionable bot findings. A prior reply suppresses rework only when its content addresses the same finding and its evidence still holds at the recorded head. Deduplicate only on complete finding plus location or symbol, failure preconditions, requested contract, and disposition; keep all original IDs as aliases. If the census was not run or `coverage` reports truncation, report the gap explicitly and do not claim a complete result. Done when: the action view plus the resolved-inclusive census comparison are recorded with no actionable body finding hidden, or the missing census is reported as a gap.

3. Judge each item against current code. Read the referenced file at the recorded revision. Recompute numbers, check guards and caller effects, and weigh severity against the governing contract, not the comment summary. Re-anchor moved code with one same-file anchor search; when the anchor is gone, mark `not-addressing` with the search evidence or `needs-human` when intent is unclear. Distinguish approved decisions from proposals and governing requirements from descriptive text. For branch attribution, inspect the merge-base delta, relevant changes on both sides, and candidate behavior; path presence or absence in branch history alone proves nothing. Done when: every item maps to code evidence at the recorded head.

4. Assign exactly one verdict per item: `fixed`, `fixed-differently`, `replied`, `not-addressing`, `declined`, or `needs-human`. A question needing no code change is `replied`. A missing premise with search evidence is `not-addressing`. An item needing an author decision the PR has not made is `needs-human` and stays open with no closing claim. Done when: every item carries one of the six names.

5. Repair valid findings at the root in the local tree. `fixed` and `fixed-differently` change the general case so the reported case is absorbed; an input-specific conditional is not a repair. Work directly in this batch with no second repair fleet and no numeric batch or cycle caps. Add or update a biting regression proof where one can discriminate: state the failing behavior without the fix and the required behavior with it. Run the targeted proof per repair, then one combined proof after all edits. A failure in an untouched file is not automatically pre-existing; attribute it with the same scenario and comparable configuration on base and candidate. Do not suppress a verifier or count a zero-matched selection as proof. Done when: every accepted repair has targeted and combined proof recorded.

6. Stage the authorized mutation set and obtain explicit approval. Record exact reply bodies quoting each finding and outcome, exact resolution choices, the exact repair commits and push destination ref, the expected full head OID, and the acting account. Approval covers exact bytes and the exact push ref; any body edit, commit change, or head movement needs renewed approval. A reply grant does not imply resolution or push authority, and a push grant covers only the listed commits to the listed ref. `needs-human` items are approved as left-open. Done when: the exact mutation set, including commits and push ref when pushing, is approved in this turn.

7. Validate the whole batch before the first write. Confirm full thread and comment IDs, target repository and PR, current head equal to the approved head, thread ownership, disposition, listed commits and push ref when pushing, and current evidence. Compare full OIDs, never prefixes. After any rewrite, re-anchor every cited commit with full objects, compared patches or trees, and current repair behavior. Squashed, split, dropped, or reworded repairs need explicit re-anchoring and renewed exact-text approval. Done when: every write, including push, is validated against current identity and evidence.

8. Post only approved writes and verify each receipt. `scripts/reply-to-pr-thread` and `scripts/resolve-pr-thread` reject GraphQL errors and emit structured receipts; a successful process exit alone still never proves the intended thread changed, so caller-side validation and read-back remain required for every write. For a reply, confirm the helper output parses as JSON, has no `errors` object, and contains the reply comment `id` and `url`. For a resolution, confirm no `errors` and the returned thread `id` equals the expected thread ID with `isResolved == true`. For a push, confirm the local head still equals the approved head, push only the approved refspec, then confirm the accepted remote OID and ref update from transport output, never from exit status alone. Bodies travel file-backed: write the body to a temp file and pipe it on stdin; never expand page JSON or bodies into argv. Retain each ID and URL and read the posted body back under the acting account with the census fetch. Reply first; resolve only after that reply is confirmed and resolution was authorized. Use `gh pr comment` only for review-body and conversation items; it has no helper-side receipt, so its proof is the author-inclusive re-enumeration delta: exactly one new comment ID under the acting account with the exact posted body, where that ID was absent in that post immediate pre-snapshot, with complete paginated coverage. On any uncertain or failed write, stop remaining writes and inspect live receipts before any retry. When the same approved body already exists under the acting account on the exact thread, report and verify it rather than duplicate it. Respect rate-limit and abuse signals. Done when: each authorized write, including push, has a parsed receipt plus read-back, and partial execution is reported exactly.

9. Reconcile and report one batch. Rerun `scripts/get-pr-comments <PR> [OWNER/REPO]` and compare its `review_threads` action view and `all_review_threads` census against the intended open set, then separately re-enumerate top-level state with the same author-inclusive source used for top-level receipts. Explain every retained pending or intentionally open item, including resolved threads kept for accounting and body-only items. New findings and changed-head evidence are next-batch input for the caller, not an internal loop. Done when: the open sets reconcile and the per-thread report is delivered.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| Empty action view with complete census | Return `No actionable comments` and change nothing. |
| Incomplete pages or missing census | Report incomplete input with the exact missing surface. Do not claim zero items. |
| Target merged or closed | Report state and stop. No head recreation or follow-up without a separate grant. |
| Inaccessible code | Mark `needs-human` with the exact access failure. No guessed verdict or repair. |
| Identity unmapped | Stop the affected scope and report the exact unresolved ID. Never guess an ID. |
| `gh` unauthenticated or no remote | Report and stop. No credential repair. |
| Head moved after approval | Stop writes, re-evaluate at the new head, seek renewed exact-text approval. |
| Fix fails validation | Re-fix or revert locally. Never post, resolve, or push an unvalidated repair. |
| Receipt missing or mismatched | Stop remaining writes, report exactly which writes landed, retry only on a concrete transient signal with identical bytes. |
| Write without explicit approval | Refuse and record the blocked attempt. |
| User rejects preview | Post nothing, resolve nothing, push nothing, report the rejection. |

## Output

One per-item record in order with item and thread IDs plus source, file and line or anchor, verdict, code evidence at the recorded head OID, repair and proof for `fixed` and `fixed-differently`, exact reply body and receipt URL for posted replies, resolution receipt for resolved threads, push ref and accepted remote OID for pushed commits, and the held reason for `needs-human`. Plus batch totals, approved and observed head OIDs, the resolved-inclusive census comparison or its reported gap, commit SHAs if pushed, the observed versus intended open sets, and new findings as next-batch input. No remote change beyond approved receipts.
