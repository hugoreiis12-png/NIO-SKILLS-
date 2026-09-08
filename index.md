# @nio-cli/skills — índice

> Consumido pela NIO-CLI como repo aberto (zipball, branch `main`). Contrato e
> plano de alinhamento em [`docs/nio-cli-alignment.md`](docs/nio-cli-alignment.md).

## Núcleo (`core/` — toda sessão, qualquer perfil)

Provisionado sempre, sem depender de seleção de role. Ver [`docs/core-module.md`](docs/core-module.md).

| Arquivo | ID | Descrição |
|---------|----|-----------|
| `rules/core/senior-core.md` | — | Bloco sempre-em-contexto; força o carregamento da skill |
| `skills/core/senior-engineering-core/SKILL.md` | 45 | Modo operacional padrão — postura, loop, evidência, roteador N0–N3, decisão, verificação, saída |
| `skills/core/senior-engineering-core/references/01–06.md` | — | Docs de apoio (análise · arquitetura · código · dados · comunicação · revisão), sob demanda |

## Comandos (`commands/`, role `dev`)

| Arquivo | ID | Descrição |
|---------|----|-----------|
| `commands/implement.md` | 1 | `/implement` — executa spec/bug/tickets em worktree isolado |
| `commands/ship.md` | 6 | `/ship` — commit → push → PR → fecha issues |
| `commands/build.md` | 42 | `/build` — orquestra implement → review → ship em loop |

## Skills — Dados (`skills/data/general/`)

Todas as skills de dados ficam sob `data/general/` (a CLI só provisiona
`skills/<role>/general/**` para roles não-dev). O `persona:` no frontmatter marca
o público (não é estrutural).

| Arquivo | ID | persona | Descrição |
|---------|----|---------|-----------|
| `data-standards/SKILL.md` | 44 | — | As convenções do setor de dados (SQL, Python, ML, BI) |
| `explore-dataset/SKILL.md` | 26 | analyst | Explorar dataset desconhecido |
| `data-quality/SKILL.md` | 27 | analyst | Avaliar qualidade de dados |
| `review-sql/SKILL.md` | 28 | analyst | Revisar query SQL |
| `to-analysis/SKILL.md` | 29 | analyst | Criar plano de análise |
| `model-card/SKILL.md` | 30 | scientist | Documentar modelo ML |
| `experiment-design/SKILL.md` | 31 | scientist | Desenhar experimento controlado |
| `review-notebook/SKILL.md` | 32 | scientist | Revisar notebook Jupyter |
| `feature-check/SKILL.md` | 33 | scientist | Avaliar features e sugerir engenharia |
| `dashboard-spec/SKILL.md` | 34 | bi | Especificar dashboard |
| `kpi-framework/SKILL.md` | 35 | bi | Definir framework de KPIs |
| `report-spec/SKILL.md` | 36 | bi | Especificar relatório analítico |
| `data-storytelling/SKILL.md` | 37 | bi | Estruturar narrativa com dados |

## Skills — Engenharia de software

### Genéricas (`skills/dev/general/`)

| Arquivo | ID | Descrição |
|---------|----|-----------|
| `caveman/SKILL.md` | 10 | Respostas ultra-comprimidas |
| `council/SKILL.md` | 11 | Decisão com 5 lentes |
| `detect-patterns/SKILL.md` | 43 | Escreve `docs/_patterns.md` (a CLI lê o corpo como prompt da análise) |
| `drytify/SKILL.md` | 12 | Remover duplicação |
| `grill-me/SKILL.md` | 13 | Desafiar decisões |
| `handoff/SKILL.md` | 14 | Comprimir conversa para continuidade |
| `init-sdd/SKILL.md` | 21 | Scaffoldar estrutura SDD |
| `review-changes/SKILL.md` | 15 | Revisar diff |
| `to-doc/SKILL.md` | 22 | Criar spec/bug/ADR |
| `to-tickets/SKILL.md` | 23 | Fatiar spec em tickets |
| `zoom-out/SKILL.md` | 16 | Abstrair e mapear módulos |

### Front-end — área `front-end` (`skills/dev/front-end/general/`)

| Arquivo | ID | Descrição |
|---------|----|-----------|
| `animation-vocabulary/SKILL.md` | 7 | Glossário reverso de motion |
| `emil-design-eng/SKILL.md` | 8 | Filosofia de polish de UI (Emil Kowalski) |
| `review-animations/SKILL.md` | 9 | Revisar código de animation |

Stacks reservados (`.gitkeep`, mantêm o stack selecionável): `front-end/nextjs/`,
`front-end/lovable/`; `back-end/{general,django,fastapi}/`.

## Agentes

| Arquivo | ID | Modelo | Role | Descrição |
|---------|----|--------|------|-----------|
| `agents/dev/repo-scout.md` | 19 | Haiku | dev | Explorador read-only do repo |
| `agents/dev/code-executor.md` | 40 | Sonnet | dev | Implementa ticket em worktree |
| `agents/dev/code-reviewer.md` | 41 | Opus | dev | Valida diff |
| `agents/data/data-explorer.md` | 38 | Haiku | data | Mapeia datasets e bancos |
| `agents/data/sql-reviewer.md` | 39 | Sonnet | data | Revisa queries SQL |

## Rules (`rules/dev/**` — só role `dev`; cascata derivada do path)

| Arquivo | Escopo |
|---------|--------|
| `rules/dev/general/general-rules.md` | Camada raiz — todo código |
| `rules/dev/back-end/general/rules.md` | Back-end — baseline da área |
| `rules/dev/back-end/django/rules.md` | Django/DRF |
| `rules/dev/front-end/general/rules.md` | Front-end — baseline da área |
| `rules/dev/front-end/nextjs/rules.md` | Next.js (App Router / RSC) |
| `rules/dev/front-end/lovable/rules.md` | House-style Lovable/React (Vite) — Shadcn + TanStack + Supabase/RLS |

> Regras de dados: não há `rules/data/` — a CLI só concatena `rules/dev/**`. As
> convenções de dados vivem na skill `data-standards`.
