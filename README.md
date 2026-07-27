# @nio/skills

Skills, commands, agents, rules e hooks para o setor de dados e desenvolvimento de software.

## Escopo

Este repositório contém assets para três perfis do setor de dados e um perfil de engenharia:

| Perfil | Áreas cobertas |
|--------|----------------|
| **Analista de dados** | Exploração de datasets, qualidade de dados, revisão de SQL, plano de análise |
| **Cientista de dados** | Model cards, design de experimentos, revisão de notebooks, feature engineering |
| **Business Intelligence** | Especificação de dashboards, frameworks de KPIs, relatórios, data storytelling |
| **Desenvolvimento de software** | SDD loop (spec → tickets → implement → ship), revisão de código, refatoração |

## Estrutura

```
commands/           Slash-commands: /implement, /ship, /build
skills/
  dev/general/      Skills genéricos de engenharia de software
  data/analyst/     Skills para analistas de dados
  data/scientist/   Skills para cientistas de dados
  data/bi/          Skills para Business Intelligence
agents/
  dev/              Sub-agentes de engenharia (repo-scout, code-executor, code-reviewer)
  data/             Sub-agentes de dados (data-explorer, sql-reviewer)
rules/
  dev/              Convenções de engenharia (geral, back-end, Django)
  data/             Convenções de dados (geral, SQL, Python, ML, BI)
hooks/              Scripts de qualidade no git
dependencies/       Ferramentas externas necessárias em runtime
scripts/            Tooling de manutenção do repositório
```

## Skills de dados

### Analista de dados
| Skill | Descrição |
|-------|-----------|
| `explore-dataset` | Mapear um dataset desconhecido — schema, tipos, distribuição, qualidade |
| `data-quality` | Avaliar completude, unicidade, consistência e validade dos dados |
| `review-sql` | Revisar queries SQL: corretude, performance, legibilidade |
| `to-analysis` | Criar um plano de análise a partir de uma pergunta de negócio |

### Cientista de dados
| Skill | Descrição |
|-------|-----------|
| `model-card` | Documentar um modelo de ML: dados, métricas, limitações, uso |
| `experiment-design` | Desenhar um experimento controlado ou teste A/B |
| `review-notebook` | Revisar notebook Jupyter: reprodutibilidade, clareza, performance |
| `feature-check` | Avaliar features e sugerir feature engineering |

### Business Intelligence
| Skill | Descrição |
|-------|-----------|
| `dashboard-spec` | Especificar um dashboard: KPIs, filtros, granularidade, público |
| `kpi-framework` | Definir um framework de KPIs conectado aos objetivos de negócio |
| `report-spec` | Especificar um relatório analítico |
| `data-storytelling` | Estruturar insights em narrativa acionável para stakeholders |

## Skills de engenharia

| Skill | Descrição |
|-------|-----------|
| `init-sdd` | Scaffoldar estrutura SDD (specs, bugs, ADRs, AGENTS.md) |
| `to-docs` | Criar spec, bug report ou ADR |
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
