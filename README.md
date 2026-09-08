# @nio-cli/skills

Conteúdo (skills, commands, agents, rules, hooks, dependencies) para a **NIO-CLI**
— setor de dados e desenvolvimento de software. Consumido como **repo aberto**
(zipball do GitHub, branch `main`), cache em `~/.nio/skills`. Contrato de consumo
e plano de alinhamento: [`docs/nio-cli-alignment.md`](docs/nio-cli-alignment.md).

## Escopo

| Perfil / persona | Cobertura |
|--------|----------------|
| **Analista de dados** | Exploração de datasets, qualidade de dados, revisão de SQL, plano de análise |
| **Cientista de dados** | Model cards, design de experimentos, revisão de notebooks, feature engineering |
| **Business Intelligence** | Especificação de dashboards, frameworks de KPIs, relatórios, data storytelling |
| **Desenvolvimento de software** | SDD loop (spec → tickets → implement → ship), revisão de código, refatoração |

## Estrutura

A CLI descobre **roles/áreas/stacks a partir da árvore `skills/`**
(`skills/<role>/<área|general>/<stack|general>/<skill>/SKILL.md`). Pastas de stack
só com `.gitkeep` mantêm o stack selecionável e puxam seus `rules`/`dependencies`.

```
commands/           Slash-commands (role dev): /implement, /ship, /build
skills/
  core/             senior-engineering-core — toda sessão, qualquer perfil
  dev/
    general/        Skills genéricas de engenharia (sempre, role dev)
    front-end/general/   Skills de front-end (área front-end)
    front-end/{nextjs,lovable}/   stacks (.gitkeep — puxam rules/deps)
    back-end/{general,django,fastapi}/   stacks (.gitkeep)
  data/
    general/        TODAS as skills de dados (flat) + data-standards
agents/
  dev/              repo-scout, code-executor, code-reviewer
  data/             data-explorer, sql-reviewer
rules/
  core/             Modo operacional padrão — toda sessão, antes das regras de código
  dev/general/      Camada raiz — todo código
  dev/back-end/     Baseline + stacks (general, django)
  dev/front-end/    Baseline + stacks (general, nextjs, lovable)
                    (não há rules/data — a CLI só concatena rules/core/ + rules/dev/**)
hooks/              hooks.json (flat) + scripts .py de qualidade no git
dependencies/       Libs externas declaradas, na mesma taxonomia de skills
scripts/            Tooling de manutenção do repo (não vai pra CLI)
```

## Núcleo (`skills/core/` + `rules/core/`)

O **módulo default da arquitetura** — provisionado em toda sessão, qualquer perfil,
sem depender de seleção de role. Contrato e mudança na CLI: [`docs/core-module.md`](docs/core-module.md).

| Item | Papel |
|------|-------|
| `rules/core/senior-core.md` | Bloco curto sempre-em-contexto (`docs/_rules/nio.md`), antes das regras de código. Força o carregamento da skill. |
| `skills/core/senior-engineering-core/SKILL.md` | Protocolo operacional — postura, loop, disciplina de evidência, roteador N0–N3, critérios de decisão, portão de verificação, contrato de saída. |
| `.../references/01–06.md` | Análise/diagnóstico · arquitetura · código · dados · comunicação · revisão. Carregadas sob demanda pelo roteador §3. |

## Skills de dados (`skills/data/general/`)

Todas flat sob `data/general/` (a CLI só provisiona `skills/<role>/general/**`
para roles não-dev). `persona:` no frontmatter marca o público — não é estrutural.

| Skill | persona | Descrição |
|-------|---------|-----------|
| `data-standards` | — | As convenções do setor de dados (SQL, Python, ML, BI) — o "harness" de dados |
| `explore-dataset` | analyst | Mapear um dataset desconhecido — schema, tipos, distribuição, qualidade |
| `data-quality` | analyst | Avaliar completude, unicidade, consistência e validade dos dados |
| `review-sql` | analyst | Revisar queries SQL: corretude, performance, legibilidade |
| `to-analysis` | analyst | Criar um plano de análise a partir de uma pergunta de negócio |
| `model-card` | scientist | Documentar um modelo de ML: dados, métricas, limitações, uso |
| `experiment-design` | scientist | Desenhar um experimento controlado ou teste A/B |
| `review-notebook` | scientist | Revisar notebook Jupyter: reprodutibilidade, clareza, performance |
| `feature-check` | scientist | Avaliar features e sugerir feature engineering |
| `dashboard-spec` | bi | Especificar um dashboard: KPIs, filtros, granularidade, público |
| `kpi-framework` | bi | Definir um framework de KPIs conectado aos objetivos de negócio |
| `report-spec` | bi | Especificar um relatório analítico |
| `data-storytelling` | bi | Estruturar insights em narrativa acionável para stakeholders |

## Skills de engenharia

| Skill | Descrição |
|-------|-----------|
| `init-sdd` | Scaffoldar estrutura SDD (specs, bugs, ADRs, AGENTS.md) |
| `to-doc` | Criar spec, bug report ou ADR |
| `to-tickets` | Fatiar spec em tickets tracer-bullet com DAG de dependências |
| `review-changes` | Revisar diff quanto a qualidade, bloat e duplicação |
| `drytify` | Identificar e remover duplicação real no código |
| `council` | Framework de decisão com 5 lentes |
| `detect-patterns` | Detectar padrões no código ou nos dados |

## Agentes

| Agente | Modelo | Função |
|--------|--------|--------|
| `repo-scout` | Haiku | Explorador read-only do repositório |
| `code-executor` | Sonnet | Implementa um ticket em worktree isolado |
| `code-reviewer` | Opus | Valida diff contra rules + critérios do ticket |
| `data-explorer` | Haiku | Mapeia estrutura de datasets e bancos de dados |
| `sql-reviewer` | Sonnet | Revisa queries SQL |

## Manutenção

```bash
npm run ids    # Atribui IDs estáveis a novos items sem id
```
