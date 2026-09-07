#!/usr/bin/env node
// Valida a integridade estrutural do bundle antes de entrar na esteira: taxonomia
// de skills/agents/commands, `name:` batendo com a pasta, JSON parseável, scripts
// de hook existentes, `min_cli_version` no formato, e zero resíduo `noclaf`.
// Roda no CI (.github/workflows/validate.yml) e como pre-push local. `--selftest`
// exercita os classificadores puros. Exit 1 se algo falha.
import { readdirSync, readFileSync, statSync, existsSync } from "node:fs";
import { join, dirname, basename } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const errors = [];
const fail = (m) => errors.push(m);

function walk(dir, out = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".")) continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.isFile()) out.push(p);
  }
  return out;
}

function rel(abs) {
  return abs.slice(ROOT.length + 1).split(/[\\/]/).join("/");
}

function frontmatterName(abs) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(readFileSync(abs, "utf8"));
  if (!m) return null;
  const n = /^name:\s*(.+)$/m.exec(m[1]);
  return n ? n[1].trim().replace(/^["']|["']$/g, "") : null;
}

/** Nº de segmentos de diretório entre `skills/` e o arquivo. */
function skillDepth(relPath) {
  return relPath.split("/").slice(1, -1).length;
}

/** A forma do path de um SKILL.md é válida? (role/general/skill ou role/area/<stack|general>/skill) */
function validSkillPath(relPath) {
  const segs = relPath.split("/").slice(1, -1); // sem `skills` e sem `SKILL.md`
  if (segs.length === 3) return segs[1] === "general";
  if (segs.length === 4) return segs[1] !== "general" && !!segs[2];
  return false;
}

function checkSkills() {
  for (const abs of walk(join(ROOT, "skills"))) {
    const r = rel(abs);
    if (basename(abs) !== "SKILL.md") continue; // STANDARDS.md, *-PATTERN.md, templates/* = docs de apoio
    if (!validSkillPath(r)) fail(`skills: path fora da taxonomia — ${r}`);
    const folder = basename(dirname(abs));
    const name = frontmatterName(abs);
    if (name && name !== folder) fail(`skills: name: "${name}" ≠ pasta "${folder}" — ${r}`);
  }
}

function checkAgents() {
  for (const abs of walk(join(ROOT, "agents"))) {
    const r = rel(abs);
    if (basename(abs) === "README.md") continue;
    if (r.split("/").length !== 3) {
      fail(`agents: esperado agents/<role>/<name>.md — ${r}`);
      continue;
    }
    const name = frontmatterName(abs);
    const stem = basename(abs, ".md");
    if (name && name !== stem) fail(`agents: name: "${name}" ≠ arquivo "${stem}" — ${r}`);
  }
}

function checkCommands() {
  for (const abs of walk(join(ROOT, "commands"))) {
    const r = rel(abs);
    if (basename(abs) === "README.md") continue;
    if (r.split("/").length !== 2) fail(`commands: deve ser flat (commands/<name>.md) — ${r}`);
  }
}

function checkJson(relPath, validate) {
  const abs = join(ROOT, relPath);
  if (!existsSync(abs)) return fail(`json: arquivo ausente — ${relPath}`);
  let data;
  try {
    data = JSON.parse(readFileSync(abs, "utf8"));
  } catch (e) {
    return fail(`json: não parseia — ${relPath}: ${e.message}`);
  }
  if (validate) validate(data);
}

function checkHooksJson(data) {
  if (!Array.isArray(data?.hooks)) return fail(`hooks.json: chave "hooks" não é lista`);
  for (const h of data.hooks) {
    if (!h.event || !h.script) fail(`hooks.json: entrada sem event/script — ${JSON.stringify(h)}`);
    if (h.script && !existsSync(join(ROOT, "hooks", h.script)))
      fail(`hooks.json: script não existe — hooks/${h.script}`);
  }
}

function checkMinCli(data) {
  const v = data?.min_cli_version;
  if (typeof v !== "string" || !/^\d+\.\d+\.\d+$/.test(v))
    fail(`nio-skills.json: min_cli_version ausente ou fora de x.y.z — ${JSON.stringify(v)}`);
}

// só o que a CLI consome — `docs/` e `scripts/` são repo-only, podem citar o histórico
const BUNDLE = ["commands", "skills", "agents", "hooks", "rules", "dependencies"];

function checkNoNoclaf() {
  const hits = [];
  for (const d of BUNDLE) {
    if (!existsSync(join(ROOT, d))) continue;
    for (const abs of walk(join(ROOT, d))) {
      try {
        if (/noclaf/i.test(readFileSync(abs, "utf8"))) hits.push(rel(abs));
      } catch {
        /* binário — ignora */
      }
    }
  }
  if (hits.length) fail(`resíduo "noclaf" no bundle: ${hits.join(", ")}`);
}

function selftest() {
  const assert = (c, m) => {
    if (!c) throw new Error(m);
  };
  assert(validSkillPath("skills/dev/general/zoom-out/SKILL.md"), "role/general/skill");
  assert(validSkillPath("skills/data/general/model-card/SKILL.md"), "data/general/skill");
  assert(validSkillPath("skills/dev/front-end/general/emil/SKILL.md"), "role/area/general/skill");
  assert(validSkillPath("skills/dev/front-end/nextjs/foo/SKILL.md"), "role/area/stack/skill");
  assert(!validSkillPath("skills/dev/foo/bar/SKILL.md"), "depth3 sem general = inválido");
  assert(!validSkillPath("skills/dev/general/SKILL.md"), "raso demais");
  assert(skillDepth("skills/a/b/c/SKILL.md") === 3, "skillDepth");
  console.log("selftest ok");
}

function main() {
  checkSkills();
  checkAgents();
  checkCommands();
  checkJson("nio-skills.json", checkMinCli);
  checkJson("hooks/hooks.json", checkHooksJson);
  checkJson(".nio-ids.json");
  checkNoNoclaf();
  if (errors.length) {
    console.error(`✗ validate: ${errors.length} problema(s)`);
    for (const e of errors) console.error(`  - ${e}`);
    process.exit(1);
  }
  console.log("✓ validate: bundle íntegro");
}

process.argv.includes("--selftest") ? selftest() : main();
