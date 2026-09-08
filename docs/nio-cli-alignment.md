# Plano arquitetural — alinhar `@nio-cli/skills` ao refactor da NIO-CLI

> Base: análise da NIO-CLI em `github.com/hugoreiis12-png/NIO-CLI-` @ `fa3cefe`
> (26 ago 2026). Este documento mapeia o **contrato real** que a CLI já implementa
> para consumir este repo, o que já bate, os gaps, e a migração recomendada.

---

## Status — migração repo-side aplicada (branch `chore/align-with-nio-cli`)

| Passo (§6) | Estado |
|---|---|
| 1 · pacote `@nio-cli/skills` + keywords | ✅ feito |
| 2 · `skills/data/**` achatado p/ `skills/data/general/<skill>/` + `persona:` | ✅ feito (12 skills) |
| 3 · `rules/data/` foldado → skill `data-standards` (id 44) + removido | ✅ feito |
| 4 · `rules/dev/front-end/` alinhado (`tanstack-start` → `lovable` nas 3 árvores; títulos/`applies-to`/`extends`) | ✅ feito |
| 5 · mover craft skills p/ `dev/general` | ⏸️ **não feito** — `emil-design-eng`/`animation-vocabulary`/`review-animations` mantidos em `front-end/general` (todos legítimos de front-end). Rever se algum é craft geral. |
| 6 · `init-sdd` + path do OpenCode | ✅ feito |
| 7 · `hooks/README.md` flat | ✅ feito |
| 8 · `npm run ids` | ✅ feito (`data-standards` → 44; `.nio-ids.json` next 45) |
| 9 · índices (`index.md`, `README.md`, sub-READMEs, `skills/data/README.md` novo) | ✅ feito |

**Pendente de decisão do owner:** passo 5; o corpo de `rules/dev/front-end/lovable/rules.md`
ainda tem escolhas de stack que valem uma revisão (React Router v7, Zustand, VITE\_).

**Aberto com o time da CLI:** §7 (C1–C6). Nada bloqueia — mas **C1** decide se o
agrupamento `persona:` volta a ser estrutural, e **C2** se `rules/data/` deveria
existir. Enquanto C1/C2 não entram, o estado acima é o alvo correto.

---

## 1. Contexto — o que a NIO-CLI virou

A NIO-CLI **v2** deixou de ser cliente do sistema NOS (tasks/sprints/ponto) e
virou um **orquestrador de ambientes de desenvolvimento**. A entidade central é a
`Session` (Postgres dedicado `nio_cli`). O rebrand `noclaf → nio` está **done, sem
compat** (`docs/specs/rebrand/0005-noclaf-to-nio.md`): `@nio-cli/cli`, binários
`nio` + `nio-cli`, `~/.nio/`, `nio.json`, env `NIO_*`, PAT `nio_`.

Este repo (`NIO-SKILLS-`) continua sendo a **fonte de conteúdo** — skills,
commands, agents, rules, hooks, dependencies. Mudanças no modelo de consumo:

| Antes (noclaf) | Agora (nio, como codado) |
|---|---|
| Pacote npm | **Repo aberto** — zipball do GitHub (`codeload.github.com/<repo>/zip/refs/heads/<ref>`), sem `git`. Cache em `~/.nio/skills`. `nio sync` re-baixa a branch. |
| `@noclaf/skills` | `brand.skillsPackage = '@nio-cli/skills'` (só usado em msg de erro + fallback `require.resolve`); `brand.skillsRepo = 'hugoreiis12-png/NIO-SKILLS-'`, `brand.skillsRef = 'main'`. |
| Clientes: claude-code, codex, cowork | Alvo **ativo**: **OpenCode** (`~/.config/opencode/{commands,skills,agents}`). `claudeTarget`/`codexTarget` existem no código mas **fora de `ALL_TARGETS`** (dormentes, decisão 2026-07-27). |
| — | Overrides: `NIO_SKILLS_DIR` (checkout local, vence tudo), `NIO_SKILLS_REPO`, `NIO_SKILLS_REF`. |

Fetch é **`refs/heads/<ref>` only** — branches, não tags (`skills-cache.ts:93`).

---

## 2. O contrato, como a CLI o implementa

### 2.1 Taxonomia de diretórios (`src/lib/sections.ts`)

```
skills/<role>/<área|general>/<stack|general>/<skill>/SKILL.md
rules/<role>/<área|general>/<stack|general>/rules.md
dependencies/<role>/<área|general>/<stack|general>/*.md
agents/<role>/<name>.md            ← role só, sem área/stack
commands/<name>.md                 ← flat, SEMPRE dev
hooks/hooks.json + hooks/*.py      ← flat, SEMPRE dev
```

**Descoberta** (`discoverRoles/Areas/Stacks`): lê **só a árvore `skills/`**.
- roles = subpastas de `skills/` → hoje `dev`, `data`.
- áreas de um role = subpastas de `skills/<role>/` menos `general`.
- stacks de uma área = subpastas de `skills/<role>/<área>/` menos `general`.
- **Uma pasta de stack só com `.gitkeep` ainda conta** — é o que mantém o stack
  selecionável e puxa os `rules.md`/`dependencies` daquele stack. Padrão já usado
  em `skills/dev/front-end/{nextjs,tanstack-start}/`.

**Regra de inclusão** (`includePath`, decide o que entra por seleção):

| kind | regra |
|---|---|
| `commands`, `hooks` | entra se a seleção inclui o role **`dev`** |
| `agents` | entra se a seleção inclui `parts[1]` (o role) |
| `skills`/`rules`/`dependencies` | role tem que bater; `seg2 === 'general'` → entra sempre (geral do role); senão `seg2` (a área) **tem que estar em `sel.stacks`**; `seg3` tem que ser `general` **ou** o stack escolhido daquela área |

**Achatamento** on-disk (`flattenSelection`): `skills/<role>/general/<skill>/…` e
`skills/<role>/<área>/<stack>/<skill>/…` → ambos viram `skills/<skill>/…`.
`agents/<role>/<name>` → `agents/<name>`. Commands/hooks já flat.

### 2.2 Wizard de seleção (`src/cli/flows/sections.ts`)

1. `discoverRoles` → checkbox "Qual seu perfil?" (`ROLE_LABELS` só tem
   `dev: "Desenvolvedor"`, `management: "Gestão"` — `data` apareceria como `data`).
2. **Só se `roles` inclui `dev`** → pergunta áreas de dev + stack por área.
3. **Roles não-dev não recebem prompt de área/stack** → `sel.stacks` fica `{}`
   para eles.

**Consequência crítica:** para um role não-dev, `includePath` só deixa passar
`skills/<role>/general/<skill>/SKILL.md` (`seg2 === 'general'`). Qualquer skill
sob uma sub-área (`skills/data/analyst/…`) é **filtrada fora** porque a área nunca
entra em `sel.stacks`.

### 2.3 Frontmatter que a CLI lê (`src/lib/skills.ts`)

Parser próprio (não YAML completo): `key: value` de 1 linha + blocos `>` / `|`.
Campos usados:

| Campo | Uso |
|---|---|
| `id` | `uid` — id sequencial estável de telemetria (sobrevive a rename). `null` se ausente. A CLI **nunca escreve** de volta — o repo é dono da numeração. |
| `title` \|\| `name` \|\| humanize(pasta) | título exibido |
| `description` | descrição (Codex/Cowork usam como seletor) |
| `clients` | lista `,`/espaço de `claude-code \| codex \| cowork \| opencode`. Vazio/ausente = todos. Doc restrito a um surface não aparece nos outros. |
| `argument-hint` | vira "Expected input" na skill Codex / arg do prompt MCP |
| `disable-model-invocation`, `user-invocable`, `model`, `effort`, `allowed-tools` | **não lidos pela CLI** — passam verbatim no arquivo copiado (Claude-native) |

`type` vem do path: `commands/*`→command · `skills/**/SKILL.md`→skill ·
`skills/**/<outro>.md`→doc (arquivo de apoio) · `agents/*`→agent ·
`dependencies/*`→dependency. `id` de skill = **nome da pasta do `SKILL.md`**.

`SKILL_KINDS` lidos como docs: `commands`, `skills`, `agents`, `dependencies`.
**`rules/`, `hooks/`, `index.md`, `README.md`, `scripts/`, `package.json`,
`.nio-ids.json` são ignorados** por `skills.ts` (rules e hooks têm leitores
próprios; o resto é repo-only).

### 2.4 Provisionamento (`provision-collect.ts`, `provision.ts`, `targets.ts`)

- `SYNCED_SUBDIRS = ['commands','skills','agents']` copiados pro cliente.
  `.gitkeep`, `.DS_Store`, `README.md` nunca copiados.
- Alvo ativo: `opencodeTarget` — `~/.config/opencode`, surface `opencode`,
  `mapDocs = docs => docs` (mesmo layout do Claude, sem tradução).
- Codex (dormente) faz **dual-write**: cada command/skill vira
  `skills/<id>/SKILL.md` **e** `prompts/<id>.md`; **id (nome da pasta) tem que ser
  único** entre todos os commands+skills senão `toCodexDocs` lança.
- Prune: só remove o que saiu do bundle de verdade, nunca o que foi só filtrado
  pela seleção do run.

### 2.5 Rules (`src/lib/rules.ts`)

- **`concatenateRules` é hardcoded no role `dev`** (`if (!sel.roles.includes(DEV_ROLE)) return ''`).
- Cascata **derivada do path, não do `extends:`** (a CLI ignora `extends:`):
  `rules/dev/general/general-rules.md` → por área selecionada
  `rules/dev/<área>/general/rules.md` → por stack escolhido
  `rules/dev/<área>/<stack>/rules.md`.
- Resultado é gravado pela `harness.ts` em **`docs/_rules/nio.md`** do repo do
  usuário (header "não edite à mão"), + âncoras `@docs/_rules/nio.md` e
  `@docs/_patterns.md` no `AGENTS.md`, + `CLAUDE.md` fino (`@AGENTS.md`).
- `collectRuleSkills` lê o frontmatter `skills:` de `<área>/general/rules.md` + do
  stack escolhido e **oferece instalar** (skills.sh) no fim do sync.

### 2.6 Hooks (`src/lib/hooks.ts`)

- Lê **`hooks/hooks.json` flat** (o layout `hooks/<role>/hooks.json` do nosso
  README **está errado**). Entrada: `{ id?, event, matcher?, description?, script, clients? }`.
- Copia scripts pro namespace **`hooks/nio/`** sob o targetDir e faz merge
  não-destrutivo do binding no `settings.json`.
- **Só provisiona pro `claudeTarget`** (`if (target === claudeTarget)` em `sync.ts`
  e `init`). Como `claudeTarget` está fora de `ALL_TARGETS`, **os hooks hoje não
  são provisionados por ninguém.** (Estado da CLI, não deste repo.)
- Só entra se a seleção inclui `dev`.

### 2.7 Dependencies (`src/lib/dependencies.ts`)

Campos de instalador, precedência `npm` > `skills` > `git` > `claude-plugin` > `manual`:

| Campo | Formato validado | Ação |
|---|---|---|
| `npm:` | nome de pacote npm | `npm install -g <pkg>` |
| `skills:` | `owner/repo` ou `owner/repo/skill` | `npx --yes skills add …` |
| `git:` | `https://github.com/…` só | clona em `~/.nio/deps/<id>` |
| `claude-plugin:` | `<owner/repo> <plugin@marketplace>` | `claude plugin marketplace add` + `install` |
| `manual:` | bloco `\|` | impresso, nunca executado |
| `detect:` | globs `,`/`\n` (`~`,`*`,`**`, segue symlink) | se algum existe → "instalada" |
| `install:` | qualquer | **só exibição, nunca executado** |

Escopo por seleção (`readDependencies`) usa a **mesma** `includePath`.

### 2.8 Legado que o `nio clean-legacy` remove (`src/cli/commands/clean.ts`)

- `FULLY_REMOVED`: `new-spec`, `new-bug`, `new-adr`, `apply-spec`, `apply-bug`,
  `to-skill` → **não podem existir** neste repo (não existem ✓).
- `COMMAND_TO_SKILL`: `init-sdd`, `to-tickets` → têm que ser **skill**, não command
  (são skills ✓).

### 2.9 Ids de skill que a CLI referencia por nome

- **`detect-patterns`** — `patterns.ts` lê o **corpo** dessa skill como prompt da
  análise de patterns (fallback embutido se ausente). Manter o id e o corpo úteis.
- Nenhum outro id é hardcoded (`implement`/`ship`/`build`/trio são soltos).

---

## 3. Situação de alinhamento

### ✅ Já bate

- `skills/dev/**` — taxonomia `role/área/stack/skill` correta; `general` em
  cascata; pastas de stack `.gitkeep` (`front-end/{nextjs,tanstack-start}`,
  `back-end/{general,django,fastapi}`) mantêm stacks selecionáveis.
- `rules/dev/**` — `concatenateRules` monta certo pelo path
  (`general/general-rules.md`, `<área>/general/rules.md`, `<área>/<stack>/rules.md`
  todos existem). `skills:` no frontmatter é colhido.
- `agents/dev/*` e `agents/data/*` — `agents/<role>/<name>.md` correto.
- `dependencies/dev/**` — taxonomia correta; `improve` (`skills:`), `ponytail`
  (`claude-plugin:` + `detect:` + `manual:`), `gh` (`manual:` + `install:`),
  `vercel-*`/`shadcn`/`supabase`/`domain-modeling` (`skills:`) — todos no formato.
- `hooks/hooks.json` — **flat na raiz** (o layout que a CLI lê), com `id`/`event`/
  `matcher`/`description`/`script`/`clients`.
- `commands/` — flat; `implement`/`ship`/`build` sem colisão de id.
- Harness — `code-executor.md`/`code-reviewer.md`/`implement.md`/`detect-patterns`
  referenciam `docs/_rules/nio.md` + `docs/_patterns.md` (pós-rename desta rodada).
- Rename `noclaf → nio` completo (esta rodada) — `grep noclaf` = 0.
- `to-doc` (pasta = `name:`, esta rodada).
- `README.md` de qualquer pasta — a CLI ignora; servem só pra humano.

### ❌ Gaps

| # | Severidade | Gap |
|---|---|---|
| A | **bloqueia** | **Skills de `data/` nunca são provisionadas.** |
| B | alto | **`rules/data/**` é código morto** para a CLI. |
| C | médio | `package.json` `name` era `@nio/skills`, contrato = `@nio-cli/skills`. ✅ corrigido |
| D | médio | `hooks/README.md` descreve layout `hooks/<role>/` que não existe. |
| E | baixo | Skills de `front-end/general` só entram se a área front-end for escolhida. |
| F | baixo | `rules/dev/front-end/` — nome de pasta ≠ conteúdo; `extends:` quebrado. |
| G | baixo | `clients:` + surface `opencode` — se um dia restringir, incluir `opencode`. |
| H | baixo | `init-sdd` não procura templates no path do OpenCode. |

---

## 4. Gaps em detalhe + correção

### Gap A — skills de `data/` nunca provisionam  ⟶ **bloqueia**

**Evidência.** `skills/data/analyst/data-quality/SKILL.md` → `includePath`:
role `data` ok, mas `seg2 = 'analyst'` não é `general` e **nunca está em
`sel.stacks`** (o wizard só preenche stacks para `dev`). `return false`.
A estrutura também está 1 nível curta vs a taxonomia
(`data/<área>/<skill>/` em vez de `data/<área>/<stack|general>/<skill>/`).

**Correção recomendada (repo-side, funciona hoje):** achatar todas as 12 skills
de dados para

```
skills/data/general/<skill>/SKILL.md
```

- `includePath`: `seg2 === 'general'` → entra sempre que o role `data` for
  escolhido. `flattenSelection` → `skills/<skill>/…`.
- A distinção analyst/scientist/bi deixa de ser estrutural. Preservar como:
  - a `description` (já diz "para analistas…", "modelo de ML…", etc.), e/ou
  - um campo **não-estrutural** no frontmatter, ex.: `persona: analyst` — a CLI
    ignora, mas serve pra humano e pra um filtro futuro.
- Mover `agents/data/*` fica como está (agents são role-only).
- Se surgirem dependências de dados: `dependencies/data/general/*.md`.

**Alternativa (precisa de mudança na CLI) — item C1 abaixo.**

### Gap B — `rules/data/**` é código morto

**Evidência.** `concatenateRules` retorna `''` se a seleção não inclui `dev`, e só
lê `rules/dev/...`. `rules/data/{general,sql,python,ml,bi}/rules.md` nunca chegam
a `docs/_rules/nio.md`.

**Correção recomendada (repo-side):**

- **Fold** o conteúdo de cada `rules/data/<x>/rules.md` para dentro do corpo da(s)
  skill(s) de dados correspondente(s) — é orientação que a skill já deveria
  carregar (a skill é o veículo de entrega para roles não-dev):
  - `rules/data/sql` → `review-sql` (+ `explore-dataset`)
  - `rules/data/ml` → `model-card`, `experiment-design`, `feature-check`, `review-notebook`
  - `rules/data/python` → skills de analyst/scientist que tocam Python
  - `rules/data/bi` → `dashboard-spec`, `kpi-framework`, `report-spec`, `data-storytelling`
  - `rules/data/general` → um preâmbulo curto em cada skill, ou um arquivo de apoio
    `skills/data/general/_shared/DATA-RULES.md` (type `doc`, inline no Cowork).
- Depois **remover `rules/data/`** e ajustar `rules/README.md` (a árvore vira só `dev/`).

**Alternativa (CLI) — item C2 abaixo.**

### Gap C — nome do pacote

`brand.skillsPackage = '@nio-cli/skills'`; comentário em `brand.ts` diz "ASSUME
mesma org (`nio-cli`) — confirmar". Como o modelo é repo-aberto (zipball), o `name`
do `package.json` só importa para (1) o fallback `require.resolve('@nio-cli/skills/package.json')`
e (2) as mensagens "Instale/publique …".

**Correção:** `package.json` → `"name": "@nio-cli/skills"`. Ajustar `keywords`
(`nio-cli`), manter `repository.url`. Decidir com o time da CLI se o pacote
**algum dia** publica no npm (senão, o fallback `require.resolve` pode sair da CLI
— item C4).

### Gap D — `hooks/README.md` errado

A CLI lê `hooks/hooks.json` **flat**; namespace de destino `hooks/nio/`;
só `claude-code`; só role `dev`; `id` opcional. Reescrever o README pra essa
realidade (remover o modelo `hooks/<role>/`, a tabela de campos fica, ajustar as
"Notas"). O `hooks.json` e os dois scripts **já estão certos**.

### Gap E — skills de `front-end/general`

`animation-vocabulary`, `emil-design-eng`, `review-animations` só entram se o
usuário marcar a área **front-end**. Se `emil-design-eng` / `animation-vocabulary`
são craft de UI geral (valem pra qualquer dev de produto), mover pra
`skills/dev/general/`. `review-animations` é claramente front-end → fica.
**Decisão do dono do repo** — sem impacto de contrato.

### Gap F — `rules/dev/front-end/` pasta ≠ conteúdo

- `tanstack-start/rules.md` → título "Lovable / React (Vite)", `applies-to:
  front-end/lovable`; conteúdo é house-style Lovable/Vite.
- `nextjs/rules.md` → título "Front-end SSR" genérico.
- O usuário escolhe o **nome da pasta** como stack no wizard → escolhe
  "tanstack-start" e recebe regras de Lovable.

**Correção:** decidir os stacks reais de front-end e alinhar **as três árvores em
lockstep** (`skills/dev/front-end/<stack>/`, `rules/dev/front-end/<stack>/`,
`dependencies/dev/front-end/<stack>/`) + `title`/`applies-to`/`extends:` dos
`rules.md`. `extends:` é cosmético (a CLI ignora) mas conserte pra humano:
`../../general/general-rules.md` na baseline de área, `../general/rules.md` no stack.

### Gap G — `clients:` e o surface `opencode`

Nenhum doc usa `clients:` hoje → todos visíveis. Se um dia restringir um doc,
**inclua `opencode`** (é o único alvo ativo) — `clients: claude-code` esconderia
o doc do OpenCode.

### Gap H — `init-sdd` e o path do OpenCode

O bloco bash de `init-sdd/SKILL.md` procura templates em `~/.claude/skills/…`,
`~/.codex/skills/…`, `~/.nio/skills/skills/dev/general/init-sdd/templates`.
No OpenCode o path provisionado é `~/.config/opencode/skills/init-sdd/templates/`
(achatado). Adicionar essa entrada à lista (o fallback relativo à skill já cobre,
mas melhor explicitar).

---

## 5. Arquitetura-alvo

```
skills/
  dev/
    general/<skill>/SKILL.md               # sempre (role dev)
    front-end/
      general/<skill>/SKILL.md             # área front-end
      <stack>/<skill>/SKILL.md   (+ .gitkeep nos stacks sem skill)
    back-end/
      general/<skill>/SKILL.md
      <stack>/<skill>/SKILL.md   (+ .gitkeep)
  data/
    general/<skill>/SKILL.md               # TODAS as 12 skills de dados, flat
    general/_shared/DATA-RULES.md          # (opcional) regras de dados como doc de apoio
rules/
  dev/
    general/general-rules.md
    <área>/general/rules.md
    <área>/<stack>/rules.md
  # rules/data/  → REMOVIDO (conteúdo foldado nas skills de data)
agents/
  dev/<name>.md
  data/<name>.md
dependencies/
  dev/general/*.md
  dev/<área>/general/*.md
  dev/<área>/<stack>/*.md
  # data/general/*.md  se/quando surgir
hooks/
  hooks.json            # flat
  *.py
commands/
  *.md                  # flat, role dev
index.md · README.md · package.json · .nio-ids.json · scripts/   # repo-only (CLI ignora)
```

---

## 6. Plano de migração (ordenado)

1. **Pacote** — `package.json` `name` → `@nio-cli/skills`; `keywords`.
2. **Achatar `skills/data/`** — `git mv skills/data/<área>/<skill>` →
   `skills/data/general/<skill>` (12 pastas). Adicionar `persona:` no frontmatter
   se quiser preservar o agrupamento. Reescrever `skills/data/README.md`.
3. **Resolver `rules/data/`** — foldar conteúdo nas skills de dados (§Gap B),
   opcionalmente criar `skills/data/general/_shared/DATA-RULES.md`, remover
   `rules/data/`, ajustar `rules/README.md`.
4. **Alinhar `rules/dev/front-end/`** — decidir os stacks reais, renomear as três
   árvores (`skills`/`rules`/`dependencies`) em lockstep, consertar
   `title`/`applies-to`/`extends:`.
5. **(Opcional) mover craft skills** de `front-end/general` → `dev/general`
   (`emil-design-eng`, `animation-vocabulary`), se for a intenção.
6. **`init-sdd`** — adicionar o path `~/.config/opencode/skills/init-sdd/templates`
   à lista do bloco bash.
7. **`hooks/README.md`** — reescrever pro layout flat real.
8. **`npm run ids`** — reatribuir ids aos novos paths; conferir que nenhum id de
   skill colide com id de command (guard do dual-write Codex).
9. **Índices** — `index.md`, `README.md` topo, sub-READMEs.
10. **Verificação** — §8.

Passos 1, 6, 7, 9 são baixo risco e independentes — podem ir primeiro. 2–5 são a
reestruturação de verdade.

---

## 7. Itens de coordenação com o time da CLI

Cada um exige mudança na CLI **ou** uma decisão conjunta. Nenhum bloqueia a
migração repo-side acima, mas mudam o alvo.

- **C1 — seleção de área/stack para roles não-dev.**
  Se `data` deve manter analyst/scientist/bi como **níveis provisionáveis**,
  `src/cli/flows/sections.ts` tem que perguntar áreas/stacks para **todo** role
  selecionado (hoje: `if (roles.includes(DEV_ROLE))`). `includePath` já suporta.
  Também: adicionar `ROLE_LABELS['data'] = 'Dados'` (ou similar).
  → Se C1 entrar, o Gap A vira `skills/data/<área>/general/<skill>/` e o
  agrupamento sobrevive.

- **C2 — rules para roles não-dev.**
  Se dados merece harness provisionado (`docs/_rules/nio.md` com seção de dados),
  `concatenateRules` tem que iterar todos os roles selecionados, não fixar
  `DEV_ROLE`. Idem `hooks.ts` (dados provavelmente não precisa de hooks de código).
  → Se C2 não entrar, `rules/data/` **deve sair** do repo (Gap B).

- **C3 — quais clientes são ativos.**
  `ALL_TARGETS = [opencodeTarget]`. `claudeTarget`/`codexTarget` dormentes;
  hooks só vão pro `claudeTarget` → **hooks hoje não provisionam pra ninguém**.
  Decidir: (a) hooks viram no-op documentado até Claude Code voltar, (b) portar
  hooks pro modelo do OpenCode, ou (c) reativar `claudeTarget`. Afeta se vale
  manter `hooks/` mantido/testado agora.

- **C4 — `skillsPackage` no npm.**
  Confirmar `@nio-cli/skills` como nome, **ou** decidir que o repo nunca publica e
  remover o fallback `require.resolve` da CLI (`skills.ts:57-63`).

- **C5 — profile ↔ selection.**
  Hoje 100% independentes: `pickProfile` (6 perfis de ambiente) e `promptSelection`
  (roles/áreas/stacks) são perguntas separadas. Decidir se escolher o perfil
  `analyst`/`scientist`/`bi` deveria **pré-selecionar** o role `data` (e pular a
  pergunta redundante). Mudança de wizard, não de contrato.

- **C6 — `NIO_SKILLS_REF` e tags.**
  `fetchSkills` baixa `refs/heads/<ref>` — só branches. Se um dia quiser fixar por
  tag/release, a CLI precisa tentar `refs/tags/` também.

---

## 8. Verificação

Com um checkout local e `NIO_SKILLS_DIR` apontando pra ele:

```bash
export NIO_SKILLS_DIR=/caminho/para/NIO-SKILLS-

# 1. a CLI enxerga todos os docs e classifica certo
nio skills status
#   → esperado: todo skill de data listado como `skill  skills/data/general/<x>/SKILL.md`

# 2. seleção de role `data` puxa as skills de dados
#    (rodar `nio init` num repo de teste, marcar só o role `data`)
ls ~/.config/opencode/skills/          # → data-quality/, model-card/, dashboard-spec/, …

# 3. seleção `dev` + área back-end + stack django → rules concatenadas
cat docs/_rules/nio.md                 # → ## general + ## back-end + ## back-end · django

# 4. agents
nio agents                             # → 5 agentes (repo-scout, code-executor, code-reviewer, data-explorer, sql-reviewer)

# 5. dependencies escopadas pela seleção
#    (fim do `nio sync` lista as deps da seleção com selo ✓/instruções)

# 6. sem regressão de id (dual-write Codex)
npm run ids                            # → "Todos os N items já têm id"
```

Checagens estáticas no repo:

```bash
grep -rn "noclaf" . --exclude-dir=.git            # → 0
find skills -name SKILL.md | while read f; do     # → todo SKILL.md a 3 (general) ou 4 (área/stack) segmentos sob skills/<role>/
  echo "$f" | awk -F/ '{print NF-2" "$0}'; done | sort -u
test ! -d rules/data || echo "rules/data ainda existe — decidir C2 ou foldar"
python3 hooks/check-code-size.py selftest && python3 hooks/check-comment-length.py selftest
```

---

## 9. Resumo executivo

- **1 bloqueador:** as skills de `data/` não provisionam — a CLI só filtra
  `skills/<role>/general/**` para roles não-dev. Achatar para
  `skills/data/general/<skill>/` resolve **hoje**; manter o agrupamento
  analyst/scientist/bi exige a mudança **C1** na CLI.
- **`rules/data/` é código morto** — foldar nas skills e remover, ou pedir **C2**.
- O resto de `dev/**` (skills, rules, agents, dependencies, hooks, commands) **já
  está no contrato** — só precisa de higiene (nome do pacote, README de hooks,
  nomes de stack de front-end, path do OpenCode no `init-sdd`).
- **OpenCode é o único cliente ativo.** Hooks, hoje, não chegam a lugar nenhum
  (**C3**).
