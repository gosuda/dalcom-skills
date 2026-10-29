---
name: decoded-memo-retention
description: 'Use when a query-scoped decoded-block cache is bounded only by serialized work bytes, or when fallback paths retain many decoded blocks. Not for total-process memory promises: this skill never claims a process-wide bound.'
---

# Decoded memo retention

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A query-scoped decoded-block cache bounded only by serialized work bytes or request count while retaining decoded heap across many identities, or a review of memory amplification from repeated fallback paths. |
| Authority | Reversible local: the named memo, its ownership and eviction contract, one explicitly bounded local measurement instrument, and authorized regression coverage. A production cache-policy change is human-gated. No remote changes, credentials, deployment, paid services, or automatic commit. |
| Side effect | An explicit single-identity retention contract, release-before-replace eviction, ownership and query regressions, and measured retained-memory evidence. |
| Done | The memo retains at most one decoded block through the memo itself, retained decoded ownership is measured before and after with variance, identity reuse and release are proven by tests, the old map representation fails the new retention assertion, and no total-process memory claim is made. |

## Inputs

The named decoded-block memo, its owning component, the full-block fallback path, cache ownership, and lifetime of returned handles. Discover whether untrusted queries can visit many distinct block identities. Establish the representative workload: candidate identities whose full identity does and does not match the request, including consecutive-identity reuse.

## Procedure

1. Trace the full-block fallback path, cache ownership, and lifetime of returned handles. Establish whether untrusted queries can visit many distinct block identities. A serialized-byte work budget does not establish a decoded-heap retention bound; a query can retain many decoded blocks, and concurrent requests multiply that retained state. Done when: the fallback path, ownership, handle lifetime, and reachable identity set are stated.
2. Separate work admission from retention. Keep existing read-count and byte charges unless the task explicitly changes them. Do not relabel serialized bytes as heap bytes. Done when: admission charges are preserved and the retention contract is stated separately.
3. When consecutive-identity reuse meets the requirement, prefer a single entry keyed by the complete `(height, hash)` identity over a map of every block visited. When retaining multiple identities is required, define a genuine decoded-memory policy instead. Done when: the single-slot or explicit multi-identity policy is chosen with its reason.
4. Measure retained decoded ownership before changing the bound. Metric: decoded bytes owned through the memo under the representative workload. State the tool, input identities, conditions, and repeat count; record before bytes with observed variance. Never substitute process RSS: allocator behavior, fragmentation, and other owners can hold RSS steady while owned retention falls. Keep this ownership measurement separate from fetch-count evidence. Done when: before bytes, tool, conditions, and variance are recorded, or the run stops as blocked on noise.
5. Apply release-before-replace. On a cache hit, reuse the shared handle without another fetch or decode. On an identity miss, release the previous cached block before fetching and decoding the replacement. Cache only successfully verified blocks. Revisiting an evicted identity reads and charges it again. Done when: hit reuse, miss release ordering, verified-only caching, and re-read charging are implemented.
6. Re-measure under the same workload, method, conditions, and repeat count. Record after bytes with variance and the before-and-after difference. Revert neutral results, regressions, and wins obtained by dropping required freshness or verification. Report a non-win honestly when the bound adds no retention benefit or costs correctness or performance. Done when: the after measurement is recorded and the change is kept with proof or reverted as a non-win.
7. Inspect callers for handles retained across iterations. A single cache slot bounds cache-owned retention, not arbitrary caller-held handles, output allocations, transient decode memory, or total process heap. Done when: caller-held retention is enumerated and excluded from the cache-owned bound.
8. Prove ownership. Retain a block only through the memo, keep a weak reference, miss on another identity, and assert the weak reference can no longer upgrade before inserting the replacement. Verify exact-identity hits and release when the query budget drops. Done when: the ownership regression is green.
9. Prove query behavior. Exercise several candidate heights whose full script identity does not match the request. Verify correct empty results and distinct-identity body reads. Preserve the existing same-block reuse and cross-query isolation tests. Done when: the query regression is green.
10. Prove the tests are load-bearing by mutation. Restore the actual old map representation and methods while retaining the new tests, and require a compiled test failure at the retention assertion. Separately remove identity matching and require the distinct-height test to fail. A compile failure is not a successful mutation proof. Restore each mutation surgically and compare the source hash with the verified pre-mutation content. Never restore the whole file from HEAD over uncommitted worker changes. Done when: both mutations fail for the required reason and the source is restored exactly.
11. Apply cold-path restraint: refuse added layers, flags, caches on caches, or indirection bought for cold-path microseconds. Keep the bound to the single slot plus its explicit eviction and invalidation terms. Done when: no cold-path complexity is added.
12. Document precisely beside the owning contract clause: the memo retains at most one decoded block, not that every identity is decoded once during the entire query or that the process cannot run out of memory. Place the retention requirement with the exact eviction, reuse, fallback, ownership measurement, and mutation test names. Keep benchmark and total-memory claims separate from fetch-count and ownership evidence. Return a ledger per attempt: candidates, evidence paths, before and after owned bytes with tool and variance, behavior result, and verdict. Done when: the clause states the one-block bound with its test names, the ledger is complete, and no process-wide claim is made.

Peer routes: single-bottleneck speed work is `optimize`; a full measured-floor campaign is `optimize-extremely`. Naming a peer never executes its procedure.

## Failure and recovery

- Missing candidates: the retention pool cannot be established from inspected source. Result: blocked. Do not invent candidates.
- Noisy baseline: retained-ownership measurement cannot clear its variance band. Result: blocked until noise clears.
- Unbounded identities required: consecutive-identity reuse does not meet the requirement and no genuine decoded-memory policy is authorized. Result: blocked. Do not ship the map as a bound.
- Weak reference still upgrades after an identity miss: the previous block is retained outside the memo. Restore release-before-replace and re-prove ownership.
- Stale or unverified block cached: the memo serves a block that failed verification. Revert immediately. Verification gates caching.
- Mutation does not fail: the restored map passes the retention assertion, or removed identity matching still passes the distinct-height test. The tests do not prove retention. Repair the tests before claiming the bound.
- Non-win: the bound does not reduce bounded retention or costs more than it saves. Report the non-win with before-and-after evidence. Never reframe it as an RSS win.
- Beyond authority: the change needs production rollout, credentials, remote mutation, or paid services. Document the requirement and stop without widening authority.

## Output

Return the bounded memo with the single-identity retention contract, release-before-replace eviction, before-and-after retained decoded ownership with tool and variance, green ownership and query regressions, the two mutation results with restored source hashes, and the exact test names beside the owning clause. On failure return the precise blocked, reverted, or non-win state with measurements and the exact blocker. Never claim a total-process memory bound.
