import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CLAUDE_PLUGIN_SCHEMA =
  "https://json.schemastore.org/claude-code-plugin-manifest.json";
const CLAUDE_MARKETPLACE_SCHEMA =
  "https://json.schemastore.org/claude-code-marketplace.json";

export function loadCatalog(root = ROOT) {
  const catalog = JSON.parse(
    readFileSync(join(root, "catalog/plugins.json"), "utf8"),
  );
  if (catalog.schema !== "odin-plugin-catalog/v1")
    throw new Error(`unexpected catalog schema: ${catalog.schema}`);
  const seen = new Set();
  catalog.entries.forEach((entry, i) => {
    if (entry.index !== i + 1)
      throw new Error(`${entry.id}: index ${entry.index} out of order at ${i + 1}`);
    if (seen.has(entry.id)) throw new Error(`duplicate plugin id: ${entry.id}`);
    seen.add(entry.id);
    if (entry.directory !== `plugins/${entry.id}`)
      throw new Error(`${entry.id}: directory must be plugins/${entry.id}`);
    if (
      !/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(entry.id) ||
      entry.id.length > 64 ||
      entry.id.includes("--")
    )
      throw new Error(`${entry.id}: invalid plugin name`);
  });
  return catalog;
}

const author = (catalog) => ({
  name: catalog.owner.name,
  url: catalog.owner.url,
});

const hasMcp = (entry) => existsSync(join(ROOT, entry.directory, "mcp.json"));

export function renderClaudePluginManifest(catalog, entry) {
  const manifest = {
    $schema: CLAUDE_PLUGIN_SCHEMA,
    name: entry.id,
    displayName: entry.display_name,
    version: catalog.releaseVersion,
    description: entry.description,
    author: author(catalog),
    homepage: entry.homepage,
    repository: catalog.repository,
    license: catalog.license,
    keywords: entry.tags,
  };
  if (hasMcp(entry)) manifest.mcpServers = "./mcp.json";
  if (existsSync(join(ROOT, entry.directory, "output-styles")))
    manifest.outputStyles = "./output-styles";
  return manifest;
}

export function renderCodexPluginManifest(catalog, entry) {
  const manifest = {
    name: entry.id,
    version: catalog.releaseVersion,
    description: entry.description,
    keywords: entry.tags,
    author: author(catalog),
  };
  if (hasMcp(entry)) manifest.mcpServers = "./mcp.json";
  manifest.interface = {
    displayName: entry.display_name,
    shortDescription: entry.description,
    category: entry.category,
  };
  return manifest;
}

export function renderCursorPluginManifest(catalog, entry) {
  return {
    name: entry.id,
    version: catalog.releaseVersion,
    description: entry.description,
    author: author(catalog),
    homepage: entry.homepage,
    repository: catalog.repository,
    license: catalog.license,
    keywords: entry.tags,
    category: entry.category,
  };
}

export function renderGrokPluginManifest(catalog, entry) {
  const manifest = {
    name: entry.id,
    version: catalog.releaseVersion,
    description: entry.description,
    author: author(catalog),
    homepage: entry.homepage,
    repository: catalog.repository,
    license: catalog.license,
    keywords: entry.tags,
  };
  if (hasMcp(entry)) manifest.mcpServers = "./mcp.json";
  return manifest;
}

export function renderKimiPluginManifest(catalog, entry) {
  const manifest = {
    name: entry.id,
    version: catalog.releaseVersion,
    description: entry.description,
    keywords: entry.tags,
    homepage: entry.homepage,
    license: catalog.license,
    author: { name: catalog.owner.name },
    skills: "./skills",
  };
  if (hasMcp(entry))
    manifest.mcpServers = JSON.parse(
      readFileSync(join(ROOT, entry.directory, "mcp.json"), "utf8"),
    ).mcpServers;
  manifest.interface = {
    displayName: entry.display_name,
    shortDescription: entry.description,
  };
  return manifest;
}

export function renderHermesPluginManifest(catalog, entry) {
  const q = (value) => JSON.stringify(value);
  return [
    `name: ${q(entry.id)}`,
    `version: ${q(catalog.releaseVersion)}`,
    `description: ${q(entry.description)}`,
    `author: ${q(catalog.owner.name)}`,
    "manifest_version: 2",
    `license: ${q(catalog.license)}`,
    `homepage: ${q(entry.homepage)}`,
    `tags: [${entry.tags.map(q).join(", ")}]`,
    "",
  ].join("\n");
}

export const HERMES_PLUGIN_ENTRY = `import json
from pathlib import Path


def _scalar(raw):
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    return value


def _description(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\\n"):
        return ""
    end = text.find("\\n---", 4)
    for line in text[4:end].splitlines():
        key, separator, raw = line.partition(":")
        if separator and key == "description":
            return _scalar(raw)
    return ""


def register(ctx):
    skills = Path(__file__).parent / "skills"
    for child in sorted(skills.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.is_file():
            ctx.register_skill(child.name, skill_md, _description(skill_md))
`;

export function renderClaudeMarketplace(catalog) {
  return {
    $schema: CLAUDE_MARKETPLACE_SCHEMA,
    name: catalog.marketplace_name,
    owner: catalog.owner,
    plugins: catalog.entries.map((entry) => ({
      name: entry.id,
      source: `./${entry.directory}`,
      description: entry.description,
      version: catalog.releaseVersion,
      author: author(catalog),
      homepage: entry.homepage,
      license: catalog.license,
      keywords: entry.tags,
      category: entry.category,
      policy: { installation: "AVAILABLE", authentication: "ON_USE" },
    })),
  };
}

export function renderCodexMarketplace(catalog) {
  return {
    name: catalog.marketplace_name,
    interface: { displayName: "DStack" },
    plugins: catalog.entries.map((entry) => ({
      name: entry.id,
      source: { source: "local", path: `./${entry.directory}` },
      policy: { installation: "AVAILABLE", authentication: "ON_USE" },
      category: entry.category,
    })),
  };
}

export function renderCursorMarketplace(catalog) {
  return {
    name: catalog.marketplace_name,
    owner: catalog.owner,
    metadata: {
      description: "DStack skill plugins for agent harnesses.",
      version: catalog.releaseVersion,
    },
    plugins: catalog.entries.map((entry) => ({
      name: entry.id,
      source: `./${entry.directory}`,
      description: entry.description,
      version: catalog.releaseVersion,
      author: author(catalog),
      homepage: entry.homepage,
      license: catalog.license,
      keywords: entry.tags,
      category: entry.category,
    })),
  };
}

export function renderGrokMarketplace(catalog) {
  return {
    name: catalog.marketplace_name,
    description: "DStack skill plugins for agent harnesses.",
    owner: { name: catalog.owner.name },
    plugins: catalog.entries.map((entry) => ({
      name: entry.id,
      description: entry.description,
      category: entry.category,
      version: catalog.releaseVersion,
      homepage: entry.homepage,
      keywords: entry.tags,
      source: { type: "local", path: `./${entry.directory}` },
    })),
  };
}

export function renderKimiMarketplace(catalog) {
  return {
    version: "2",
    plugins: catalog.entries.map((entry) => ({
      id: entry.id,
      displayName: entry.display_name,
      description: entry.description,
      version: catalog.releaseVersion,
      homepage: entry.homepage,
      source: `../${entry.directory}`,
    })),
  };
}

export function parseScalar(raw) {
  const s = raw.trim();
  if (s.startsWith("'")) {
    const body = s.slice(1, s.lastIndexOf("'"));
    return body.replace(/''/g, "'");
  }
  if (s.startsWith('"')) {
    const body = s.slice(1, s.lastIndexOf('"'));
    return body
      .replace(/\\n/g, "\n")
      .replace(/\\"/g, '"')
      .replace(/\\\\/g, "\\");
  }
  return s;
}

export function parseFrontmatter(text) {
  if (!text.startsWith("---\n")) return null;
  const end = text.indexOf("\n---", 4);
  if (end === -1) return null;
  const out = {};
  for (const line of text.slice(4, end).split("\n")) {
    const m = /^([a-zA-Z_]+):(.*)$/.exec(line);
    if (m) out[m[1]] = parseScalar(m[2]);
  }
  return out;
}

export function firstSentence(desc) {
  const m = /(.+?\.)\s/.exec(desc);
  return m ? m[1] : desc;
}

export function tableCell(text) {
  return text.replace(/\\/g, "\\\\").replace(/\|/g, "\\|").replace(/\s*\n\s*/g, " ").trim();
}

export function skillTrigger(entry, slug) {
  const path = join(ROOT, entry.directory, "skills", slug, "SKILL.md");
  const front = parseFrontmatter(readFileSync(path, "utf8"));
  return firstSentence(front.description ?? "").trim();
}

export function skillRows(entry) {
  const dir = join(ROOT, entry.directory, "skills");
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();
}

const repoSlug = (catalog) =>
  catalog.repository.replace(/^https:\/\/github\.com\//, "");

export function renderPluginReadme(catalog, entry, skills) {
  const lines = [
    `# ${entry.display_name}`,
    "",
    entry.description,
    "",
    `${skills.length} skill${skills.length === 1 ? "" : "s"}, category ${entry.category}. Install the whole plugin below, or take a single skill with \`gh skill install\`.`,
    "",
    "## Install",
    "",
    "```bash",
    `# Claude Code`,
    `/plugin marketplace add gosuda/dalcom-skills`,
    `/plugin install ${entry.id}@${catalog.marketplace_name}`,
    "",
    `# Codex`,
    `codex plugin marketplace add gosuda/dalcom-skills`,
    `codex plugin add ${entry.id}@${catalog.marketplace_name}`,
    "",
    `# Hermes Agent`,
    `hermes plugins install ${repoSlug(catalog)}/${entry.directory} --enable`,
    "```",
    "",
    "### Individual (gh skill)",
    "",
    "```shell",
    `gh skill install ${repoSlug(catalog)} ${entry.directory}/skills/<skill> \\`,
    "  --agent <agent> --scope user",
    "```",
    "",
    "`<agent>` is `claude-code`, `codex`, `cursor`, `grok`, or `kimi-cli`.",
    "",
    "Cursor, Grok, and Kimi install from this same tree. The repository README gives each command.",
    "",
    "## Skills",
    "",
    `Each row states when to reach for the skill. Invoke one as \`/${entry.id}:<name>\` in Claude Code, \`$<name>\` in Codex, \`${entry.id}:<name>\` in Hermes Agent, or type \`/\` and pick it in Cursor.`,
    "",
    "| Skill | Trigger |",
    "|---|---|",
    ...skills.map(
      (slug) => `| ${slug} | ${tableCell(skillTrigger(entry, slug))} |`,
    ),
    "",
    "## Workflows",
    "",
    "[docs/guides/workflows.md](../../docs/guides/workflows.md) shows how these skills chain with the rest of the tree.",
    "",
  ];
  return lines.join("\n");
}

const ROOT_README_TABLE = /(^## Plugins\n\n)(?:\|[^\n]*\n)+/m;

export function renderRootReadme(catalog, current) {
  const entries = catalog.entries;
  const half = Math.ceil(entries.length / 2);
  const rows = [];
  for (let i = 0; i < half; i += 1) {
    const left = entries[i];
    const right = entries[i + half];
    const cells = [left.id, left.category];
    if (right) cells.push(right.id, right.category);
    else cells.push("", "");
    rows.push(`| ${cells.join(" | ")} |`);
  }
  const table = [
    "| Plugin | Category | Plugin | Category |",
    "|---|---|---|---|",
    ...rows,
    "",
  ].join("\n");
  if (!ROOT_README_TABLE.test(current))
    throw new Error("README.md: no plugin table found under a '## Plugins' heading");
  let out = current.replace(ROOT_README_TABLE, `$1${table}`);
  const counts = entries.map((entry) => [entry.id, skillRows(entry).length]);
  const total = counts.reduce((n, [, c]) => n + c, 0);
  const plugins = counts.length;
  if (!/^\d+ skills in \d+ plugins\./m.test(out))
    throw new Error("README.md: no skills-in-plugins sentence found");
  out = out.replace(
    /^\d+ skills in \d+ plugins\./m,
    `${total} skills in ${plugins} plugins.`,
  );
  const top = [...counts].sort((a, b) => b[1] - a[1]).slice(0, 3);
  if (!/^The largest plugins are [^\n]*\n/m.test(out))
    throw new Error("README.md: no largest-plugins sentence found");
  out = out.replace(
    /^The largest plugins are [^\n]*\n/m,
    `The largest plugins are ${top.map(([id, c]) => `\`${id}\` at ${c}`).join(", ").replace(/, ([^,]*)$/, ", and $1")}.\n`,
  );
  return out;
}

export function surfacePlan(catalog) {
  const files = new Map();
  files.set(".claude-plugin/marketplace.json", renderClaudeMarketplace(catalog));
  files.set(".codex-plugin/marketplace.json", renderCodexMarketplace(catalog));
  files.set(".cursor-plugin/marketplace.json", renderCursorMarketplace(catalog));
  files.set(".grok-plugin/marketplace.json", renderGrokMarketplace(catalog));
  files.set(".kimi-plugin/marketplace.json", renderKimiMarketplace(catalog));
  for (const entry of catalog.entries) {
    files.set(
      `${entry.directory}/.claude-plugin/plugin.json`,
      renderClaudePluginManifest(catalog, entry),
    );
    files.set(
      `${entry.directory}/.codex-plugin/plugin.json`,
      renderCodexPluginManifest(catalog, entry),
    );
    files.set(
      `${entry.directory}/.cursor-plugin/plugin.json`,
      renderCursorPluginManifest(catalog, entry),
    );
    files.set(
      `${entry.directory}/.grok-plugin/plugin.json`,
      renderGrokPluginManifest(catalog, entry),
    );
    files.set(
      `${entry.directory}/.kimi-plugin/plugin.json`,
      renderKimiPluginManifest(catalog, entry),
    );
  }
  return files;
}
