#!/usr/bin/env node
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  chmodSync,
  existsSync,
  mkdirSync,
  readFileSync,
  statSync,
  writeFileSync,
} from "node:fs";

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));

const PAIRS = [
  [
    "plugins/dstack-core/skills/compound/references/schema.md",
    "plugins/dstack-core/skills/autolearn/references/schema.md",
  ],
  [
    "plugins/dstack-core/skills/compound/references/concepts.md",
    "plugins/dstack-core/skills/autolearn/references/concepts.md",
  ],
  [
    "plugins/dstack-core/skills/compound/scripts/validate-record.py",
    "plugins/dstack-core/skills/autolearn/scripts/validate-record.py",
  ],

  [
    "plugins/dstack-core/skills/resolve/scripts/get-pr-comments",
    "plugins/dstack-core/skills/resolve-pr-comments/scripts/get-pr-comments",
  ],
  [
    "plugins/dstack-core/skills/resolve/scripts/get-thread-for-comment",
    "plugins/dstack-core/skills/resolve-pr-comments/scripts/get-thread-for-comment",
  ],
  [
    "plugins/dstack-core/skills/resolve/scripts/reply-to-pr-thread",
    "plugins/dstack-core/skills/resolve-pr-comments/scripts/reply-to-pr-thread",
  ],
  [
    "plugins/dstack-core/skills/resolve/scripts/resolve-pr-thread",
    "plugins/dstack-core/skills/resolve-pr-comments/scripts/resolve-pr-thread",
  ],
  [
    "plugins/dstack-core/skills/resolve/scripts/gitlab-mr.py",
    "plugins/dstack-core/skills/resolve-pr-comments/scripts/gitlab-mr.py",
  ],

  [
    "plugins/dstack-core/skills/resolve/scripts/get-pr-comments",
    "plugins/dstack-git/skills/gate-and-merge/scripts/get-pr-comments",
  ],
  [
    "plugins/dstack-core/skills/resolve/scripts/get-thread-for-comment",
    "plugins/dstack-git/skills/gate-and-merge/scripts/get-thread-for-comment",
  ],
  [
    "plugins/dstack-core/skills/resolve/scripts/reply-to-pr-thread",
    "plugins/dstack-git/skills/gate-and-merge/scripts/reply-to-pr-thread",
  ],
  [
    "plugins/dstack-core/skills/resolve/scripts/resolve-pr-thread",
    "plugins/dstack-git/skills/gate-and-merge/scripts/resolve-pr-thread",
  ],
  [
    "plugins/dstack-core/skills/resolve/scripts/gitlab-mr.py",
    "plugins/dstack-git/skills/gate-and-merge/scripts/gitlab-mr.py",
  ],

  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-core/skills/audit-project/scripts/inspect_mr_checks.py",
  ],
  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-core/skills/commit-push-pr/scripts/inspect_mr_checks.py",
  ],
  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-core/skills/resolve-pr-comments/scripts/inspect_mr_checks.py",
  ],
  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-core/skills/review-fix-loop/scripts/inspect_mr_checks.py",
  ],

  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-git/skills/modernize/scripts/inspect_mr_checks.py",
  ],
  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-git/skills/watch-and-repair-pr/scripts/inspect_mr_checks.py",
  ],
  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-git/skills/gate-and-merge/scripts/inspect_mr_checks.py",
  ],

  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-run/skills/implement-spec/scripts/inspect_mr_checks.py",
  ],
  [
    "plugins/dstack-core/skills/ci-fix/scripts/inspect_mr_checks.py",
    "plugins/dstack-infra/skills/ci-cd/scripts/inspect_mr_checks.py",
  ],

  [
    "plugins/dstack-core/skills/resolve/scripts/gitlab-mr.py",
    "plugins/dstack-review/skills/review/scripts/gitlab-mr.py",
  ],
];

const CANONICAL_SOURCES = new Set(PAIRS.map(([src]) => src));

function usage() {
  process.stderr.write(
    "usage: node scripts/sync-knowledge-copies.mjs [--check]\n",
  );
  process.exit(2);
}

const args = process.argv.slice(2);
const check = args.includes("--check");
if (args.some((a) => a !== "--check")) {
  usage();
}

let wrote = 0;
const drifted = [];
const errors = [];

for (const [srcRel, destRel] of PAIRS) {
  if (CANONICAL_SOURCES.has(destRel)) {
    errors.push(destRel + " cannot overwrite canonical source");
    continue;
  }
  const src = join(ROOT, srcRel);
  const dest = join(ROOT, destRel);
  let srcBuf;
  let srcStat;
  try {
    srcBuf = readFileSync(src);
    srcStat = statSync(src);
  } catch (e) {
    errors.push(srcRel + " unreadable: " + e.message);
    continue;
  }
  let destBuf = null;
  let destStat = null;
  if (existsSync(dest)) {
    try {
      destBuf = readFileSync(dest);
      destStat = statSync(dest);
    } catch (e) {
      errors.push(destRel + " unreadable: " + e.message);
      continue;
    }
  }

  const srcExecuteBits = srcStat.mode & 0o111;
  const destExecuteBits = destStat !== null ? destStat.mode & 0o111 : null;

  if (destBuf !== null && destBuf.equals(srcBuf) && destExecuteBits === srcExecuteBits) {
    continue;
  }
  if (check) {
    drifted.push(destRel + (destBuf === null ? " (missing)" : " (differs)"));
    continue;
  }
  mkdirSync(dirname(dest), { recursive: true });
  writeFileSync(dest, srcBuf);
  chmodSync(dest, srcStat.mode & 0o777);
  wrote += 1;
  process.stdout.write("sync-knowledge-copies: wrote " + destRel + "\n");
}

if (errors.length) {
  for (const e of errors) {
    process.stderr.write("sync-knowledge-copies: error " + e + "\n");
  }
  process.exit(1);
}

if (check && drifted.length) {
  for (const d of drifted) {
    process.stderr.write("sync-knowledge-copies: drift " + d + "\n");
  }
  process.stderr.write(
    "sync-knowledge-copies: " + drifted.length + " drifted file(s)\n",
  );
  process.exit(1);
}

if (!check) {
  process.stdout.write(
    "sync-knowledge-copies: " + wrote + " file(s) updated\n",
  );
}
