---
name: proof
description: 'Use when asked to publish, read, comment on, suggest to, or pull a Proof collaborative markdown document. Not for proofreading, math proofs, or test evidence.'
---

# Proof

Work with collaborative markdown documents on the hosted Proof service through its grounded HTTP API from `Bash`. The local file stays canonical; a Proof link is a share, never a second knowledge store. The single durable learning bundle remains the YAML `docs/solutions/` records owned by `compound`.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User names a local markdown file to share, pastes a Proof URL to read, review, comment, or edit, or asks to pull a Proof document back to disk. |
| Authority | Human-gated outward: publish, edit, comment, suggest, presence, title change, pull-overwrite, and delete each require explicit invocation for that operation. Credentials (`accessToken` everyday bearer; `ownerSecret` owner-only) live in shell variables or session memory only, never in repo-tracked files, commits, or durable logs; `ownerSecret` never appears in user-facing copy. Hand humans the tokenized `tokenUrl`, never a bare `/d/<slug>`. Never put secrets, credentials, API keys, private tokens, or sensitive personal data into a Proof doc without explicit approval. Never silently replace a repo-tracked project doc with a Proof link. |
| Side effect | Creates, reads, edits, comments, suggests, or pulls one hosted markdown document; optionally deletes it on explicit cleanup. Local pull overwrites the named local file atomically. |
| Done | Create is confirmed by the returned `tokenUrl`; mutation by `ok: true` (on `202` or `partial: true`, by re-reading `v3/document`); pull by the local file written; read by the content returned; plus a short summary and the result link or path. |

Ownership boundary: owns Proof share, read, review, edit, and pull plumbing. Does not own durable learning (`compound`, `autolearn`), PR bodies (`create-pull-request`), or local doc authoring (`docs-writing`, `doc-coauthoring`). It publishes source-file bytes; it never hand-writes the shared body.

Source: `EveryInc/compound-engineering-plugin` pinned `fbd794f329f5b65d0ea00a5e6487336c385ff2be`, `skills/ce-proof/SKILL.md` plus `references/api.md` and `references/workflows.md`. Identity `ai:compound-engineering` and display `Compound Engineering` are preserved as wire defaults; a caller may pass a distinct sub-agent identity pair when that agent owns the doc. No trademark SVG is reused as branding.

## Inputs

- Operation: `publish`, `read`, `review`, `comment`, `edit`, `suggest`, `pull`, `title`, or `delete`.
- Local markdown path for publish or pull; Proof URL with slug and token for read, review, comment, edit, suggest, title, or delete.
- Explicit approval for publish, for pull when it overwrites as a side effect, for delete, and for any sensitive content placed in the doc.

## Procedure

1. Select the narrowest operation. Publish is one-way: read the named local markdown file in full and post its bytes. Read and review start from `GET /api/agent/<slug>/v3/document` as source of truth. Edit from the fresh read with the narrowest op. Pull syncs the live markdown down to a local file. Delete only on explicit cleanup.
2. Bind presence for the session with the CE identity defaults:
```bash
TOKEN="xxx"; SLUG="abc123"; AGENT="ai:compound-engineering"
curl -sS -X POST "https://www.proofeditor.ai/api/agent/$SLUG/presence" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Agent-Id: $AGENT" \
  -d '{"name":"Compound Engineering","status":"reading","summary":"Reviewing doc"}'
```
Prefer typed `proof_*` MCP tools when the harness already offers them; otherwise use these HTTP recipes. Pass `?token=` as `shareToken` for edits and presence on docs the signer does not own. In MCP mode the server injects `by`, `X-Agent-Id`, and presence identity.
3. Publish only markdown and only source-file bytes. Encode with `jq --rawfile` so newlines, quotes, and backticks survive; never hand-write or placeholder the body. When the source is an HTML unified plan, return the local browser or open path instead of uploading. Label a unified plan title by readiness when known.
```bash
SRC="path/to/plan.md"; TITLE="Plan: Foo"
RESPONSE=$(jq -n --arg title "$TITLE" --rawfile md "$SRC" '{title:$title, markdown:$md}' \
  | curl -sS -X POST https://www.proofeditor.ai/share/markdown \
    -H "Content-Type: application/json" -d @-)
URL=$(printf '%s' "$RESPONSE" | jq -r '.tokenUrl')
SLUG=$(printf '%s' "$RESPONSE" | jq -r '.slug')
TOKEN=$(printf '%s' "$RESPONSE" | jq -r '.accessToken')
OWNER_SECRET=$(printf '%s' "$RESPONSE" | jq -r '.ownerSecret')
```
Keep `OWNER_SECRET` in session memory only. Persist both credentials for the session separately; `ownerSecret` is required for owner delete while unclaimed. Capture `slug`, `accessToken`, and `ownerSecret` immediately. After a planning-handoff publish, surface the URL and return control; do not auto-delete review docs.
4. Read and review from `v3/document`. `comments[]` and `suggestions[]` are the review state: reply, resolve, unresolve, accept, reject, or modify by id. There is no delete-comment op. An `orphaned: true` thread stays readable and replyable but its old quote is not a live anchor.
```bash
DOC=$(curl -sS "https://www.proofeditor.ai/api/agent/$SLUG/v3/document" \
  -H "Authorization: Bearer $TOKEN" -H "X-Agent-Id: $AGENT")
```
When `mutationReady` is false and `revision` is null, omit `baseRevision` and re-read shortly.
5. Edit with `POST /api/agent/<slug>/v3/edit` sending `{by, baseRevision?, operations[]}`. Targets are visible text, never raw markdown syntax or block refs. Prefer `replace`, `insert`, or `delete` for prose; `suggest` for visible tracked changes; `set_document` only for an explicitly requested whole-doc replacement or an inexpressible narrow change. At most 100 ops per request; at most 2 MiB of markdown for `set_document`.
```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/$SLUG/v3/edit" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Agent-Id: $AGENT" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"by":"ai:compound-engineering","operations":[{"op":"replace","find":"old visible text","with":"new text"}]}'
```
On `TARGET_AMBIGUOUS` disambiguate with `occurrence`, `before`, or `after` from `error.candidates`; never assume silent first-match. On `retryable: false` fix the request; on `retryable: true` with `error.current` re-resolve and retry once. On `202`, `PENDING`, or `ok: false` with `partial: true`, re-read before chaining and retry only the failed op with the same `Idempotency-Key`. After one fresh read plus one safe retry, report the bug per the service bridge rather than looping.
6. Pull with the canonical read and an atomic rename; `jq -jr` preserves trailing newlines without shell interpolation.
```bash
SLUG=<slug>; TOKEN=<accessToken>; LOCAL=<absolute-path>
STATE_TMP=$(mktemp "${TMPDIR:-/tmp}/ce-proof-state.XXXXXX")
curl -sS "https://www.proofeditor.ai/api/agent/$SLUG/v3/document" \
  -H "Authorization: Bearer $TOKEN" -H "X-Agent-Id: $AGENT" > "$STATE_TMP"
TMP="${LOCAL}.proof-sync.$$"
jq -jr '.markdown' "$STATE_TMP" > "$TMP" && mv "$TMP" "$LOCAL"
rm -f "$STATE_TMP"
```
Confirm the path first when the pull is a side effect rather than the request. A silent overwrite is a defect.
7. Title and delete: set the title only when asked; delete only when the user asks or when finishing an explicitly ephemeral scratch doc. Deletion needs `ownerSecret` while unclaimed or the owner session after claim; viewer, commenter, and editor tokens cannot delete. Two responses mean the secret was revoked (`403 DOCUMENT_DELETE_FORBIDDEN/CREDENTIAL_NOT_OWNER`, or `401` on the creation secret): stop using it rather than retrying. `DOCUMENT_HAS_NO_OWNER` means only the original secret can delete. Emptying the markdown does not scrub comment marks; a content wipe is not a privacy cleanup.
```bash
curl -sS -X PUT "https://www.proofeditor.ai/api/documents/$SLUG/title" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Updated title"}'
curl -sS -X DELETE "https://www.proofeditor.ai/api/documents/$SLUG" \
  -H "Authorization: Bearer $OWNER_SECRET"
```

## Failure and recovery

- Ambiguous target, failed mutation after one safe retry, revoked owner secret, or missing credentials: stop, report the exact code and slug, leave the doc and local files unchanged.
- Request to place secrets or sensitive data without explicit approval: refuse and name the required approval.
- HTML unified-plan source for publish: do not upload; return the local path.
- Side-effect pull without confirmed path: stop before overwriting.
- Empty markdown wipe requested as privacy cleanup: refuse as cleanup; offer owner delete.

## Output

The tokenized URL or pulled local path, the confirmed revision or `ok` state, and a short summary. Review docs linger; deletion happens only on explicit cleanup.
