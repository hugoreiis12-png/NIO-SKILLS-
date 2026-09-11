#!/usr/bin/env node
// Valida a integridade estrutural do bundle antes de entrar na esteira: taxonomia
// de skills/agents/commands, `name:` batendo com a pasta, JSON parseável, scripts
// de hook existentes, `min_cli_version` no formato, e a forma da camada NOOA
// opcional das skills. Roda no CI (.github/workflows/validate.yml) e como
// pre-push local. `--selftest` exercita os classificadores puros. Exit 1 se algo falha.
import { readdirSync, readFileSync, existsSync } from "node:fs";
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

/** Forma do path de um SKILL.md: core/skill, role/general/skill ou role/area/<stack|general>/skill. */
function validSkillPath(relPath) {
  const segs = relPath.split("/").slice(1, -1); // sem `skills` e sem `SKILL.md`
  if (segs[0] === "core") return segs.length === 2; // skills/core/<skill>/ — sem área/stack
  if (segs.length === 3) return segs[1] === "general";
  if (segs.length === 4) return segs[1] !== "general" && !!segs[2];
  return false;
}

/** Nome do pacote Python da camada NOOA de uma skill (hífen → underscore). */
function nooaPkgName(skillId) {
  return `nio_skill_${skillId.replace(/-/g, "_")}`;
}

function nioSkillsField(key) {
  try {
    return JSON.parse(readFileSync(join(ROOT, "nio-skills.json"), "utf8"))[key] ?? null;
  } catch {
    return null;
  }
}

function checkSkills() {
  for (const abs of walk(join(ROOT, "skills"))) {
    const r = rel(abs);
    if (basename(abs) !== "SKILL.md") continue; // STANDARDS.md, *-PATTERN.md, templates/* = docs de apoio
    if (!validSkillPath(r)) fail(`skills: path fora da taxonomia — ${r}`);
    const folder = basename(dirname(abs));
    const name = frontmatterName(abs);
    if (name && name !== folder) fail(`skills: name: "${name}" != pasta "${folder}" — ${r}`);
  }
}

/**
 * Camada NOOA (opcional, aditiva). Uma pasta de skill PODE trazer
 * `pyproject.toml` + `nio_skill_<id>/`. Só a forma é checada aqui — o CI
 * `nooa-layer-check` importa os pacotes. Ver docs/nooa-integration.md.
 */
function checkNooaLayers() {
  const pinned = nioSkillsField("nooa_version");
  for (const abs of walk(join(ROOT, "skills"))) {
    if (basename(abs) !== "pyproject.toml") continue;
    const dir = dirname(abs);
    const r = rel(abs);
    const id = basename(dir);
    if (!existsSync(join(dir, "SKILL.md")))
      fail(`nooa: pyproject.toml sem SKILL.md ao lado — ${r}`);
    const pkg = nooaPkgName(id);
    if (!existsSync(join(dir, pkg, "__init__.py")))
      fail(`nooa: falta o pacote ${pkg}/__init__.py — ${r}`);
    const toml = readFileSync(abs, "utf8");
    if (!/\[project\.entry-points\."nooa\.skills"\]/.test(toml))
      fail(`nooa: falta [project.entry-points."nooa.skills"] — ${r}`);
    if (!new RegExp(`"nio\\.${id}"\\s*=\\s*"${pkg}(:[A-Za-z_]\\w*)?"`).test(toml))
      fail(`nooa: entry-point esperado "nio.${id}" = "${pkg}[:Classe]" — ${r}`);
    if (!pinned) fail(`nooa: camada presente mas nio-skills.json sem nooa_version — ${r}`);
    else if (!toml.includes(pinned))
      fail(`nooa: dep "nooa" não pinada em ${pinned} (nio-skills.json) — ${r}`);
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
    if (name && name !== stem) fail(`agents: name: "${name}" != arquivo "${stem}" — ${r}`);
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

function checkNioSkillsJson(data) {
  const v = data?.min_cli_version;
  if (typeof v !== "string" || !/^\d+\.\d+\.\d+$/.test(v))
    fail(`nio-skills.json: min_cli_version ausente ou fora de x.y.z — ${JSON.stringify(v)}`);
  const n = data?.nooa_version;
  if (n !== undefined && !/^v\d+\.\d+\.\d+$/.test(n))
    fail(`nio-skills.json: nooa_version fora de vX.Y.Z — ${JSON.stringify(n)}`);
}

function selftest() {
  const assert = (c, m) => {
    if (!c) throw new Error(m);
  };
  assert(validSkillPath("skills/core/senior-engineering-core/SKILL.md"), "core/skill");
  assert(!validSkillPath("skills/core/foo/bar/SKILL.md"), "core so aceita 1 nivel");
  assert(validSkillPath("skills/dev/general/zoom-out/SKILL.md"), "role/general/skill");
  assert(validSkillPath("skills/data/general/model-card/SKILL.md"), "data/general/skill");
  assert(validSkillPath("skills/dev/front-end/general/emil/SKILL.md"), "role/area/general/skill");
  assert(validSkillPath("skills/dev/front-end/nextjs/foo/SKILL.md"), "role/area/stack/skill");
  assert(!validSkillPath("skills/dev/foo/bar/SKILL.md"), "depth3 sem general = invalido");
  assert(!validSkillPath("skills/dev/general/SKILL.md"), "raso demais");
  assert(skillDepth("skills/a/b/c/SKILL.md") === 3, "skillDepth");
  assert(nooaPkgName("council") === "nio_skill_council", "nooaPkgName simples");
  assert(nooaPkgName("to-doc") === "nio_skill_to_doc", "nooaPkgName com hifen");
  console.log("selftest ok");
}

function main() {
  checkSkills();
  checkNooaLayers();
  checkAgents();
  checkCommands();
  checkJson("nio-skills.json", checkNioSkillsJson);
  checkJson("hooks/hooks.json", checkHooksJson);
  checkJson(".nio-ids.json");
  if (errors.length) {
    console.error(`x validate: ${errors.length} problema(s)`);
    for (const e of errors) console.error(`  - ${e}`);
    process.exit(1);
  }
  console.log("ok validate: bundle integro");
}

process.argv.includes("--selftest") ? selftest() : main();
