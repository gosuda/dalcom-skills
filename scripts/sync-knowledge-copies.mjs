#!/usr/bin/env node
// Mirror authored compound knowledge contracts into autolearn as byte-identical
// copies so standalone installs keep working.
//
// Direction is fixed: compound sources are authored, autolearn destinations are
// generated. Never hand-edit a destination; edit the compound source and render.
//
// Pairs:
//   compound/references/schema.md        -> autolearn/references/schema.md
//   compound/references/concepts.md      -> autolearn/references/concepts.md
//   compound/scripts/validate-record.py  -> autolearn/scripts/validate-record.py
//
// Default mode writes missing or drifted destinations with the exact source
// bytes. --check reports drift and exits 1 without writing, which is how the
// pre-commit hook runs it.
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));

const PAIRS = [
  [
    "plugins/odin-core/skills/compound/references/schema.md",
    "plugins/odin-core/skills/autolearn/references/schema.md",
  ],
  [
    "plugins/odin-core/skills/compound/references/concepts.md",
    "plugins/odin-core/skills/autolearn/references/concepts.md",
  ],
  [
    "plugins/odin-core/skills/compound/scripts/validate-record.py",
    "plugins/odin-core/skills/autolearn/scripts/validate-record.py",
  ],
];

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
  const src = join(ROOT, srcRel);
  const dest = join(ROOT, destRel);
  let srcBuf;
  try {
    srcBuf = readFileSync(src);
  } catch (e) {
    errors.push(srcRel + " unreadable: " + e.message);
    continue;
  }
  let destBuf = null;
  if (existsSync(dest)) {
    try {
      destBuf = readFileSync(dest);
    } catch (e) {
      errors.push(destRel + " unreadable: " + e.message);
      continue;
    }
  }
  if (destBuf !== null && destBuf.equals(srcBuf)) {
    continue;
  }
  if (check) {
    drifted.push(destRel + (destBuf === null ? " (missing)" : " (differs)"));
    continue;
  }
  mkdirSync(dirname(dest), { recursive: true });
  writeFileSync(dest, srcBuf);
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
