# @nio/skills — índice

## Comandos

| Arquivo | Descrição |
|---------|-----------|
| `commands/implement.md` | `/implement` — executa spec/bug/tickets em worktree isolado |
| `commands/ship.md` | `/ship` — commit → push → PR → fecha issues |
| `commands/build.md` | `/build` — orquestra implement → review → ship em loop |

## Skills — Dados

### Analista de dados (`skills/data/analyst/`)

| Arquivo | ID | Descrição |
|---------|----|-----------|
| `explore-dataset/SKILL.md` | 26 | Explorar dataset desconhecido |
| `data-quality/SKILL.md` | 27 | Avaliar qualidade de dados |
| `review-sql/SKILL.md` | 28 | Revisar query SQL |
| `to-analysis/SKILL.md` | 29 | Criar plano de análise |

### Cientista de dados (`skills/data/scientist/`)

| Arquivo | ID | Descrição |
|---------|----|-----------|
| `model-card/SKILL.md` | 30 | Documentar modelo ML |
| `experiment-design/SKILL.md` | 31 | Desenhar experimento controlado |
| `review-notebook/SKILL.md` | 32 | Revisar notebook Jupyter |
| `feature-check/SKILL.md` | 33 | Avaliar features e sugerir engenharia |

### Business Intelligence (`skills/data/bi/`)

| Arquivo | ID | Descrição |
|---------|----|-----------|
| `dashboard-spec/SKILL.md` | 34 | Especificar dashboard |
| `kpi-framework/SKILL.md` | 35 | Definir framework de KPIs |
| `report-spec/SKILL.md` | 36 | Especificar relatório analítico |
| `data-storytelling/SKILL.md` | 37 | Estruturar narrativa com dados |

## Skills — Engenharia de software (`skills/dev/general/`)

| Arquivo | ID | Descrição |
|---------|----|-----------|
| `init-sdd/SKILL.md` | 21 | Scaffoldar estrutura SDD |
| `to-docs/SKILL.md` | 22 | Criar spec/bug/ADR |
| `to-tickets/SKILL.md` | 23 | Fatiar spec em tickets |
| `review-changes/SKILL.md` | — | Revisar diff |
| `drytify/SKILL.md` | — | Remover duplicação |
| `council/SKILL.md` | — | Decisão com 5 lentes |
| `caveman/SKILL.md` | — | Respostas ultra-comprimidas |
| `grill-me/SKILL.md` | — | Desafiar decisões |
| `handoff/SKILL.md` | — | Comprimir conversa para continuidade |
| `zoom-out/SKILL.md` | — | Abstrair e mapear módulos |
| `detect-patterns/SKILL.md` | — | Detectar padrões |

## Agentes

| Arquivo | ID | Modelo | Descrição |
|---------|----|--------|-----------|
| `agents/dev/repo-scout.md` | 19 | Haiku | Explorador read-only do repo |
| `agents/dev/code-executor.md` | — | Sonnet | Implementa ticket em worktree |
| `agents/dev/code-reviewer.md` | — | Opus | Valida diff |
| `agents/data/data-explorer.md` | 38 | Haiku | Mapeia datasets e bancos |
| `agents/data/sql-reviewer.md` | 39 | Sonnet | Revisa queries SQL |

## Rules

| Arquivo | Escopo |
|---------|--------|
| `rules/dev/general/general-rules.md` | Convenções gerais de engenharia |
| `rules/dev/back-end/general/rules.md` | Back-end genérico |
| `rules/dev/back-end/django/rules.md` | Django/DRF + Python |
| `rules/data/general/rules.md` | Convenções gerais de dados |
| `rules/data/sql/rules.md` | SQL |
| `rules/data/python/rules.md` | Python para dados |
| `rules/data/ml/rules.md` | Machine Learning |
| `rules/data/bi/rules.md` | Business Intelligence |
