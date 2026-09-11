# Integração NOOA — camada de agente executável por skill

> **Objetivo.** Dar a cada skill do NIO-SKILLS uma **camada opcional e aditiva**:
> além do `SKILL.md` (guidance, funciona em qualquer host), um **`Skill` NOOA**
> (Python) com as ferramentas e habilidades executáveis daquela skill. A camada
> NOOA compõe **ao lado do engine** (`senior-engineering-core`) — não o substitui.
>
> Base: análise do framework em `github.com/NVIDIA-NeMo/labs-OO-Agents` @ `fbbbfb1`
> (2026-09-07). NOOA é **alpha (v0.0.x)**, com breaking changes ativas — daí a
> ênfase deste documento em estabilidade e isolamento.

---

## 1. Veredito

O formato de skill do NOOA (`TextSkill`) **é** o `SKILL.md` do Claude Code — o
mesmo que este repo já produz. A integração é natural, mas tem **um risco real**:
NOOA executa código Python gerado por LLM. A regra que governa tudo abaixo:

> **A camada NOOA é 100% opcional e nunca é executada pelo repo nem pela NIO-CLI.
> Toda skill continua completa só com o `SKILL.md`. A execução acontece só num
> host NOOA com sandbox de SO.**

---

## 2. O modelo de camadas

Cada skill passa a ter (no máximo) duas camadas:

```
skills/<role>/<área>/<stack>/<skill>/
├── SKILL.md              ← guidance — SEMPRE presente, funciona em qualquer host
├── pyproject.toml        ← [opcional] declara a camada NOOA: deps + entry-point
└── nio_skill_<skill>/    ← [opcional] pacote Python com o Skill e suas ferramentas
    ├── __init__.py       ←   exporta uma subclasse de `nooa.Skill`
    └── tools.py          ←   os métodos determinísticos (as "ferramentas")
```

**Como cada host vê:**

| Host | Lê | Ignora |
|---|---|---|
| OpenCode (alvo atual da NIO-CLI), Claude Code, Codex | `SKILL.md` como texto | `pyproject.toml`, `nio_skill_*/` (arquivos inertes) |
| Host NOOA (TUI `nooa`, `nooa-acp`, ou `nio` se embutir o runtime) | `SKILL.md` → `TextSkill` (`cmd.<id>`) **+** o pacote → `Skill` anexado como `self.<skill>` com `doc()` | — |

Numa sessão NOOA, o `SKILL.md` vira o texto de orientação e o pacote vira a
**API**: o LLM chama `self.<skill>.<ferramenta>(...)` a partir do CodeAct, e a
skill pode trazer `@slash_command`s e um `context_block`.

**A unidade é `Skill`, não `Agent`.** Um `Skill` NOOA já carrega ferramentas
determinísticas, pode declarar dependências (`requires`), registrar um bloco de
contexto, e — quando a parte fuzzy exige raciocínio LLM isolado — instanciar um
**subagente privado** (`self._worker = Worker(llm=self.llm)`). Criar um `Agent`
de topo por skill (LLM próprio, histórico próprio, lock próprio) só quando o
isolamento for o ponto.

**Binding `.md` ↔ pacote.** A chave é o **id da skill** (nome da pasta):
`SKILL.md` `name: drytify` → `TextSkill.id = drytify` → `cmd.drytify`;
`pyproject.toml` `[project.entry-points."nooa.skills"]` `"nio.drytify" =
"nio_skill_drytify:DrytifySkill"` → registrado `nio.drytify`, anexado
`self.drytify`. O corpo do `SKILL.md` referencia a companheira quando ela existe
("se o host tiver a camada NOOA, use `self.drytify.find_duplication(path)`").

---

## 3. Estabilidade — regras

1. **NOOA é dependência opcional, pinada em tag exata.** Nunca `@main`. Fonte
   única da versão: campo `nooa_version` em `nio-skills.json` (ao lado de
   `min_cli_version`). Cada `pyproject.toml` de skill pina a mesma tag.
2. **A camada NOOA é aditiva, nunca requerida.** `to-tickets` sem NOOA = o
   humano/modelo segue o `.md`. Com NOOA = existe `self.to_tickets.slice_spec()`.
   Remover o pacote de uma skill não pode quebrar a skill.
3. **Um pacote Python por skill, nome de topo único** (`nio_skill_<skill>`). A
   descoberta de libs do NOOA alerta em colisão de nome de pacote de topo e
   dois checkouts sob o mesmo nome num processo se contaminam. Nomes únicos
   tornam isso impossível.
4. **Cada `pyproject.toml` pina as próprias deps** com piso e teto, estilo
   `exclude-newer`. Sem faixa aberta.
5. **CI `nooa-layer-check`** (novo job): instala o NOOA pinado, importa todo
   `nio_skill_*/`, roda os testes de cada um. Skip limpo quando não há camada
   NOOA. É o gate que pega uma breaking change do NOOA **antes** de shipar.
6. **`validate.mjs`** ganha a forma opcional: se um dir de skill tem
   `pyproject.toml`, então tem que ter o pacote `nio_skill_<skill>/` com
   `__init__.py`, entry-point `nooa.skills` declarado, e nome de topo batendo
   com `nio_skill_<id>`.

---

## 4. Segurança — regras

1. **O repo nunca executa código NOOA.** `validate.mjs` só checa forma
   (estático). O CI só **importa** os pacotes num runner efêmero — nunca roda um
   agente, nunca um `CodeActStrategy`.
2. **Provisionar ≠ executar.** A NIO-CLI **copia** arquivos. Ela não pode
   `import` nem rodar o `nio_skill_*/` de nenhuma skill. (O host NOOA importa os
   `.py` de skill ao abrir o repo — isso é comportamento do host, com sandbox, não
   da CLI.)
3. **A execução exige sandbox de SO.** CodeAct = Python gerado por LLM; os
   validadores AST + denylist do NOOA são defesa em profundidade, **não**
   contenção. Um host que rode estas camadas roda dentro de container/VM/OpenShell.
   Registrar isso em `SECURITY.md`.
4. **Zero segredo nos pacotes.** Ferramenta que precisa de credencial recebe do
   ambiente do host / resolve no código chamador. Sem `${VAR}`, sem key hardcoded,
   sem `.env` versionado.
5. **Superfície de ferramenta mínima e determinística.** Operação perigosa vai
   embrulhada num método estreito com erro claro — nunca o objeto cru exposto.
   `@slash_command(..., user_only=True)` em qualquer comando destrutivo (o LLM
   não invoca).
6. **Carrega inativo, ativa por opt-in.** O host descobre a camada mas a deixa
   **loaded, não activated** até o usuário pedir (`/skills` no NOOA). O default é
   guidance-only; a ferramenta só entra no `doc(self)` quando escolhida.
7. **Lint do NOOA no CI.** Os pacotes passam pelo `LintReport` (E001 builtins
   proibidos, E003 star-imports) — o mesmo gate que o NOOA aplica a código que um
   agente escreve.

---

## 5. O que a NIO-CLI precisa mudar

> Referências pelo mapa em `docs/nio-cli-alignment.md` §2 (base `fa3cefe`).
> Confirmar contra o código atual.

| # | Onde | Mudança |
|---|---|---|
| 1 | `src/lib/skills.ts` (classificador) | Tratar `<skill>/pyproject.toml` e `<skill>/nio_skill_*/**` como **payload opaco** — não é skill, não é doc. Não classificar, não numerar id. |
| 2 | `provision*.ts` / `targets.ts` | Provisionar o payload (`pyproject.toml` + `nio_skill_*/`) junto com o `SKILL.md` para **`~/.claude/skills/<skill>/`** (D2) — um root que qualquer host NOOA de coding varre. O dir inteiro já é copiado; garantir que `pyproject.toml` e `.py` não sejam filtrados. |
| 3 | `nio-skills.json` | Adicionar `nooa_version` (a tag do NOOA que as camadas visam). |

Não mexe em: taxonomia de descoberta (`sections.ts` `discoverRoles/Areas/Stacks`
lê só `skills/` — pastas e `SKILL.md`, ignora o resto), `concatenateRules`,
`hooks`, `commands`.

---

## 6. Decisões (fechadas 2026-09-08)

- **D1 — o payload viaja para todos os alvos.** A camada acompanha o `.md`, fica
  inerte no OpenCode, pronta quando um host NOOA aparecer. `pyproject.toml` +
  `nio_skill_*/` aparecem em `~/.config/opencode/skills/<skill>/` (inofensivo).

- **D2 — o `nio` NÃO embute o runtime NOOA — delega a um host externo.** As
  camadas são provisionadas para um root que qualquer host NOOA de coding varre
  automaticamente. O NOOA olha, sob `~/`: `.agents/skills/`, `.claude/skills/`,
  `.claude/commands/`; e, por workspace, os mesmos + `.cursor/skills/` e o que
  `coding.additional_skills_dirs` (em `<ws>/.nooa/settings.yaml`) apontar.
  → **Alvo de provisionamento da camada NOOA: `~/.claude/skills/<skill>/`**
  (já é o path do `claudeTarget` dormente; um host NOOA o lê de graça). O `nio`
  só distribui; nada de runtime no `nio`. Reavaliar embed só se surgir demanda.

- **D3 — dependência NOOA: git-tag pinado.** `nooa @ git+https://github.com/
  NVIDIA-NeMo/labs-OO-Agents.git@vX.Y.Z` em cada `pyproject.toml`; fonte única da
  tag em `nio-skills.json` (`nooa_version`). Bump deliberado, gated por CI.

- **D4 — primeira skill com camada NOOA: `council`.** Framework de 5 lentes — um
  `Skill` que estrutura a decisão. Zero filesystem, zero rede, zero ferramenta
  perigosa. É o caso mais seguro para validar toda a infra da Fase 1/2.

---

## 7. Rollout — estável e seguro, em fases

| Fase | Entrega | Gate |
|---|---|---|
| **0** (esta) | Este documento. Nenhum código. | Acordo nas D1–D4 |
| **1** | Infra só: `nooa_version` em `nio-skills.json`; `validate.mjs` reconhece a forma opcional; CI `nooa-layer-check` (skip se vazio); `SECURITY.md` + este doc linkados no README. **Sem nenhuma camada ainda.** | CI verde |
| **2** | Camada NOOA para a skill de referência (D4) + 1–2 skills read-only (`drytify` finder, `detect-patterns`). Sandbox documentado. | `nooa-layer-check` roda os testes das camadas |
| **3** | Camadas que precisam de shell/tools, atrás do requisito de sandbox. `requires`, `@slash_command user_only`. | Revisão de superfície de ferramenta por skill |

Fase 1 é baixo risco e não introduz nenhuma execução. Só a Fase 2 traz o primeiro
`Skill` NOOA (`council`) — e mesmo assim inativo até opt-in.

> D2 fechou em "delegar": não há Fase 4 de embed. Se um dia o `nio` precisar
> rodar as camadas, isso vira um documento novo.

---

## 7.1 Fase 3 — desks por perfil (2026-09-09)

Decisões fechadas:

- **Unidade = `Skill` "desk"**, uma por perfil — não `Agent` (não roda no host
  delegado, D2).
- **"Concatenação" = cascata em runtime**, não geração estática. O `SKILL.md` da
  desk é um índice curto; a camada NOOA ativa o roster do perfil via
  `SkillRegistry.activate()` quando o usuário chama `self.<perfil>_desk.equip()`.
  Não infla o contexto — cada skill do roster continua carregada sob demanda.
- **As 7 desks foram criadas já**, mesmo as enxutas (DBA, QA) — sem skills
  próprias ainda, emprestam de perfis vizinhos.

### O padrão de uma desk

```
skills/<role>/<área>/general/<perfil>-desk/
├── SKILL.md                          índice curto — perfil, toolkit, como equipar
├── pyproject.toml                    nooa @<tag>, entry-point nio.<perfil>-desk
├── nio_skill_<perfil>_desk/
│   ├── __init__.py                   lazy __getattr__ (mesmo padrão do council)
│   ├── _core.py                      ROSTER (dado) + cascade_patterns/run_cascade/
│   │                                  status_text/equipped_report (glue, vendored)
│   └── skill.py                      <Perfil>DeskSkill(Skill) — equip()/roster()/status()
└── tests/test_<perfil>_desk.py       lógica pura, sem nooa
```

`equip()` ativa `[f"*.{sid}" for sid in ROSTER]` — glob que casa `cmd.<id>` (a
guidance) e `nio.<id>` (a camada NOOA, quando existe, ex. `council`). É opt-in:
nada ativa sozinho no discovery: só quando o usuário chama `equip()`.

**`ponytail` deliberado:** a glue (`cascade_patterns`/`run_cascade`/`status_text`/
`equipped_report`) é idêntica nas 7 desks, vendorizada em cada `_core.py`. Um
pacote compartilhado exigiria um dep git resolvido depois do provisionamento —
mais frágil que 4 funções duplicadas. Mantenha as 7 cópias em sync manualmente.

### Os 7 perfis

| Perfil | Desk | Roster |
|---|---|---|
| backend | `dev/back-end/general/backend-desk` | to-doc, to-tickets, review-changes, drytify, detect-patterns, council |
| frontend | `dev/front-end/general/frontend-desk` | emil-design-eng, animation-vocabulary, review-animations, review-changes, drytify, council |
| analyst | `data/general/analyst-desk` | data-standards, explore-dataset, data-quality, review-sql, to-analysis, council |
| scientist | `data/general/scientist-desk` | data-standards, model-card, experiment-design, review-notebook, feature-check, council |
| bi | `data/general/bi-desk` | data-standards, dashboard-spec, kpi-framework, report-spec, data-storytelling, council |
| **dba** ⚠️ | `data/general/dba-desk` | data-standards, review-sql, council — **enxuta, sem skill própria** |
| **qa** ⚠️ | `dev/general/qa-desk` | review-changes, detect-patterns, drytify, council — **enxuta, sem skill própria** |

Pendência: criar skills próprias de DBA (ex. `review-migration`, `schema-review`)
e QA (ex. `test-strategy`, `review-coverage`) quando fizer sentido — as duas
desks ficam mais substanciais no dia em que existirem.

---

## 8. Verificação (Fase 1, quando chegar)

```bash
node scripts/validate.mjs --selftest && node scripts/validate.mjs
# → skills sem pyproject.toml: inalteradas
# → skills com pyproject.toml: pacote nio_skill_<id>/ presente, entry-point nooa.skills declarado

# CI nooa-layer-check (pseudo):
uv pip install "nooa @ git+https://github.com/NVIDIA-NeMo/labs-OO-Agents.git@$(jq -r .nooa_version nio-skills.json)"
for pkg in skills/**/nio_skill_*/; do python -c "import ${pkg}"; done   # só importa, nunca roda
```
