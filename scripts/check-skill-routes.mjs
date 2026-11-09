import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { ROOT, loadCatalog, skillRows } from "./plugin-surfaces.mjs";

const POINTER_RE = /(?:[:;,]|\() use `?([a-z0-9][a-z0-9*-]*[a-z0-9*])`?/g;
const ARTICLES = new Set(["a", "an", "the", "your", "its"]);
export function danglingPointers(descriptions, slugs) {
  const out = [];
  for (const [dir, description] of descriptions) {
    for (const m of description.matchAll(POINTER_RE)) {
      const target = m[1];
      if (ARTICLES.has(target)) continue;
      const rx = new RegExp(`^${target.replace(/[.+?^${}()|[\]\\]/g, "\\$&").replace(/\*/g, "[a-z0-9-]*")}$`);
      if (![...slugs].some((s) => rx.test(s))) out.push(`${dir}: dangling pointer use ${target}`);
    }
  }
  return out;
}

if (process.argv.includes("--self-test")) {
  const slugs = new Set(["design", "from-moat-perspective", "from-skeptic-perspective"]);
  const planted = new Map([
    ["p/skills/a", "Use when x. Not for picking: use design."],
    ["p/skills/b", "Use when y. Not for a seat take: use from-*-perspective seats."],
    ["p/skills/c", "Use when z (use design). Not for running it: use the mewt CLI."],
    ["p/skills/d", "Use when w. Not for review: use no-such-skill."],
    ["p/skills/e", "Use when v. Not for seats: use nothing-*-here."],
  ]);
  const got = danglingPointers(planted, slugs);
  const want = ["p/skills/d: dangling pointer use no-such-skill", "p/skills/e: dangling pointer use nothing-*-here"];
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    process.stderr.write(`check-skill-routes self-test: expected ${JSON.stringify(want)}, got ${JSON.stringify(got)}\n`);
    process.exit(1);
  }
  process.stdout.write("check-skill-routes self-test: 5 planted descriptions, 2 dangling caught\n");
  process.exit(0);
}

const errors = [];
const skills = loadCatalog().entries.flatMap((entry) =>
  skillRows(entry).map((slug) => [slug, `${entry.directory}/skills/${slug}`]),
);

function parseFrontmatterYaml(text) {
  if (!text.startsWith("---\n")) return null;
  const end = text.indexOf("\n---", 4);
  if (end === -1) return { error: "unterminated frontmatter", entries: [] };
  const block = text.slice(4, end);
  const entries = [];
  const stack = [];
  for (const line of block.split("\n")) {
    if (line.trim() === "" || /^\s*#/.test(line)) continue;
    const indent = line.length - line.trimStart().length;
    while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop();
    const trimmed = line.trimStart();
    const m = /^([A-Za-z0-9][A-Za-z0-9_-]*):\s?(.*)$/.exec(trimmed);
    if (!m) continue;
    const key = m[1];
    const rawVal = m[2];
    const prefix = stack.length ? stack[stack.length - 1].pathPrefix + "." : "";
    const path = prefix + key;
    if (rawVal.trim() === "") {
      stack.push({ indent, pathPrefix: path });
      continue;
    }
    let value, quote = null;
    const v = rawVal.trim();
    let qm = /^'((?:[^']|'')*)'(?:\s+#.*)?$/.exec(v);
    if (qm) {
      value = qm[1].replace(/''/g, "'");
      quote = "'";
    } else if ((qm = /^"((?:[^"\\]|\\.)*)"(?:\s+#.*)?$/.exec(v))) {
      value = qm[1].replace(/\\"/g, '"').replace(/\\\\/g, "\\");
      quote = '"';
    } else {
      value = v;
    }
    entries.push({ path, key, value, quote, raw: rawVal });
  }
  return { entries, error: null };
}

const badName = [];
const badFrontmatter = [];
const parsed = new Map();
for (const [slug, dir] of skills) {
  const skillPath = join(ROOT, dir, "SKILL.md");
  if (!existsSync(skillPath)) {
    badFrontmatter.push(`${dir}: missing SKILL.md`);
    continue;
  }
  const fm = parseFrontmatterYaml(readFileSync(skillPath, "utf8"));
  if (fm === null) {
    badFrontmatter.push(`${dir}: no frontmatter block`);
    continue;
  }
  if (fm.error) {
    badFrontmatter.push(`${dir}: ${fm.error}`);
    continue;
  }
  parsed.set(dir, fm);
  const nameEntry = fm.entries.find((e) => e.path === "name");
  if (!nameEntry) {
    badFrontmatter.push(`${dir}: frontmatter has no name`);
    continue;
  }
  if (nameEntry.value !== slug) badName.push(`${dir}: name is ${nameEntry.value}`);
}
if (badFrontmatter.length)
  errors.push(
    `route-breaking frontmatter: ${badFrontmatter.slice(0, 5).join("; ")} (${badFrontmatter.length} total)`,
  );
if (badName.length)
  errors.push(
    `name/directory mismatches: ${badName.slice(0, 5).join("; ")} (${badName.length} total)`,
  );

const badQuote = [];
for (const [, dir] of skills) {
  const fm = parsed.get(dir);
  if (!fm) continue;
  for (const entry of fm.entries) {
    if (!entry.raw.includes(": ")) continue;
    if (entry.quote === "'") continue;
    if (entry.quote === '"')
      badQuote.push(`${dir}: double-quoted ': ' value; contract requires single quotes (${entry.path})`);
    else badQuote.push(`${dir}: unquoted frontmatter value contains ': ' (${entry.path})`);
  }
}
if (badQuote.length)
  errors.push(
    `': ' frontmatter values not single-quoted: ${badQuote.slice(0, 5).join("; ")} (${badQuote.length} total)`,
  );

const AGENT_SKILLS_DESCRIPTION_LIMIT = 1024;
const TRIGGERS = [
  "use when ",
  "use this ",
  "use for ",
  "use to ",
  "use after ",
  "use on ",
  "use during ",
  "runs /",
  "invoked ",
  "invoke ",
  "asks to ",
  "asks for ",
  "says ",
];
const badDescription = [];
for (const [, dir] of skills) {
  const fm = parsed.get(dir);
  if (!fm) continue;
  const description = fm.entries.find((e) => e.path === "description")?.value;
  if (!description) {
    badDescription.push(`${dir}: frontmatter has no description`);
    continue;
  }
  if (description.length > AGENT_SKILLS_DESCRIPTION_LIMIT)
    badDescription.push(`${dir}: description ${description.length} chars, limit ${AGENT_SKILLS_DESCRIPTION_LIMIT}`);
  const humanOnly =
    fm.entries.find((e) => e.path === "disable-model-invocation")?.value === "true";
  const lowered = description.toLowerCase();
  if (!humanOnly && !TRIGGERS.some((t) => lowered.includes(t)))
    badDescription.push(`${dir}: description states no trigger`);
}
if (badDescription.length)
  errors.push(
    `unroutable descriptions: ${badDescription.slice(0, 5).join("; ")} (${badDescription.length} total)`,
  );

const descriptions = new Map();
for (const [, dir] of skills) {
  const description = parsed.get(dir)?.entries.find((e) => e.path === "description")?.value;
  if (description) descriptions.set(dir, description);
}
const dangling = danglingPointers(descriptions, new Set(skills.map(([slug]) => slug)));
if (dangling.length)
  errors.push(`${dangling.slice(0, 5).join("; ")} (${dangling.length} total)`);

const byName = new Map();
const missingManifest = [];
for (const [, dir] of skills) {
  const manifestPath = join(ROOT, dir, "agents/openai.yaml");
  if (!existsSync(manifestPath)) {
    missingManifest.push(dir);
    continue;
  }
  const match = /^\s*display_name:\s*(.+)$/m.exec(readFileSync(manifestPath, "utf8"));
  if (!match) {
    missingManifest.push(dir);
    continue;
  }
  const name = match[1].trim().replace(/^["']|["']$/g, "");
  byName.set(name, [...(byName.get(name) ?? []), dir]);
}
if (missingManifest.length)
  errors.push(
    `missing display_name: ${missingManifest.slice(0, 5).join(", ")} (${missingManifest.length} total)`,
  );
const dupes = [...byName.entries()].filter(([, dirs]) => dirs.length > 1);
if (dupes.length)
  errors.push(
    `duplicate display_name: ${dupes
      .slice(0, 5)
      .map(([name, dirs]) => `${name} <- ${dirs.join(", ")}`)
      .join("; ")} (${dupes.length} group(s))`,
  );

if (errors.length) {
  for (const e of errors) process.stderr.write(`check-skill-routes: ${e}\n`);
  process.exit(1);
}
process.stdout.write(`skill-routes ok ${skills.length} skills\n`);
