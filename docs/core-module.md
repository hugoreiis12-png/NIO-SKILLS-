# Módulo `core/` — provisionado em toda sessão, qualquer perfil

> **Rota C** do plano de integração do `senior-engineering-core`. Este documento é
> o contrato do conceito `core/` e a lista de mudanças que a **NIO-CLI** precisa
> para consumi-lo. A parte deste repo (`rules/core/`, `skills/core/`,
> `scripts/validate.mjs`) já está aplicada.

---

## 1. O que é

`core/` é uma **camada acima de role**. Diferente de `dev`/`data`, não é um perfil
que o usuário seleciona — é conteúdo que entra **sempre**, antes de qualquer regra
ou skill escopada por seleção.

```
rules/core/*.md                          → prepended em docs/_rules/nio.md, antes de rules/dev/**
skills/core/<skill>/SKILL.md              → provisionado sempre (flatten → skills/<skill>/)
skills/core/<skill>/references/*.md       → docs de apoio, copiados junto
```

Hoje o único ocupante é `senior-engineering-core`:

| Arquivo | Papel |
|---|---|
| `rules/core/senior-core.md` | Bloco curto (~30 linhas) sempre-em-contexto. 6 regras que valem antes da skill carregar + ordem de carregar a skill. |
| `skills/core/senior-engineering-core/SKILL.md` | Protocolo operacional (~200 linhas), carregado no início da sessão via a regra acima. |
| `.../references/01–06.md` | Carregadas sob demanda pelo roteador §3 do SKILL. Não recebem `id` (docs de apoio). |

Estrutura deliberada — o mesmo desenho do pacote original (`bootstrap → SKILL →
references`): injetar ~1.200 linhas em toda sessão dilui a instrução. O bloco
sempre-em-contexto é mínimo; a profundidade é puxada quando o roteador manda.

---

## 2. Taxonomia

```
skills/core/<skill>/SKILL.md              ← sem <área>/<stack>; 1 nível só
skills/core/<skill>/<apoio>.md            ← docs de apoio (references/*)
rules/core/*.md                           ← flat; sem cascata interna
```

`validate.mjs` deste repo já aceita: `validSkillPath` trata `segs[0] === 'core'`
como válido com exatamente 2 segmentos (`core/<skill>`).

`assign-ids.mjs` não precisou de mudança — só `SKILL.md` é "item"; as referências
não recebem id.

---

## 3. Mudanças necessárias na NIO-CLI

> Referências de arquivo pelo mapa em `docs/nio-cli-alignment.md` §2 (base commit
> `fa3cefe`). **Confirmar contra o código atual antes de aplicar.**

### 3.1 `src/lib/sections.ts`

- **`discoverRoles`** — excluir `core` da lista de roles retornada. `core` nunca
  aparece no checkbox "Qual seu perfil?". (Alternativa: manter o filtro no wizard,
  em `src/cli/flows/sections.ts`.)
- **`includePath`** — para os kinds `skills` / `rules` / `dependencies`: se
  `parts[1] === 'core'`, `return true` **antes** de qualquer checagem de
  `sel.roles` / `sel.stacks`. Entra independente da seleção.
- **`flattenSelection`** — `skills/core/<skill>/…` → `skills/<skill>/…` (mesmo
  achatamento de `skills/<role>/general/<skill>/…`).

### 3.2 `src/lib/rules.ts`

- **`concatenateRules`** — hoje: `if (!sel.roles.includes(DEV_ROLE)) return ''`.
  Novo: sempre começar lendo `rules/core/*.md` (ordem alfabética), emitir como
  seção `## core`, **depois** seguir a cascata de `dev` se o role `dev` estiver na
  seleção. Resultado: uma seleção só-`data` ainda recebe `docs/_rules/nio.md` com
  o bloco core.
- **`harness.ts`** — garantir que a âncora `@docs/_rules/nio.md` no `AGENTS.md` do
  usuário seja escrita mesmo quando a seleção não inclui `dev` (hoje pode estar
  atrás do mesmo guard).
- **`collectRuleSkills`** — opcional: ler `skills:` de `rules/core/*.md`. O valor
  atual (`senior-engineering-core`) é uma skill **local** já provisionada, não um
  slug externo — pode ser ignorado ou tratado como no-op.

### 3.3 Provisionamento

`SYNCED_SUBDIRS` já inclui `skills`; nada muda além do `includePath`/`flatten`.
`rules/` continua sem ser copiado pro cliente (só alimenta `concatenateRules`).

### 3.4 Legado / guards

- `clean.ts` — nada a fazer; `core` não colide com nenhum id legado.
- Dual-write Codex (`toCodexDocs`) — exige nome de pasta único entre
  commands+skills. `senior-engineering-core` é único hoje. Manter.

---

## 4. Verificação (com `NIO_SKILLS_DIR` local)

```bash
export NIO_SKILLS_DIR=/caminho/para/NIO-SKILLS-

# 1. core aparece como skill, não como role
nio skills status          # → skill  skills/core/senior-engineering-core/SKILL.md
nio init                    # → o checkbox de perfil NÃO lista "core"

# 2. seleção só-data provisiona o core
#    (nio init num repo teste, marcar só `data`)
ls ~/.config/opencode/skills/senior-engineering-core/   # → SKILL.md + references/
cat docs/_rules/nio.md                                  # → começa com ## core

# 3. seleção dev + back-end + django
cat docs/_rules/nio.md      # → ## core, depois ## general, ## back-end, ## back-end · django

# 4. sem regressão de id
npm run ids                 # → "Todos os N items já têm id"
```

Checagens estáticas (já cobertas pelo CI deste repo):

```bash
node scripts/validate.mjs --selftest && node scripts/validate.mjs
```
