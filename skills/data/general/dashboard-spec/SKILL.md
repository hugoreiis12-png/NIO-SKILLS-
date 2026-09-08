---
id: 34
name: dashboard-spec
persona: bi
description: Especificar um dashboard — KPIs, filtros, granularidade, público e critérios de atualização
model: sonnet
effort: medium
---

# Dashboard Spec

Crie uma especificação completa de dashboard antes de construí-lo.

## Por que especificar antes de construir
Dashboards construídos sem especificação viram "frankensteins" — acumulam visuals sem propósito, são difíceis de manter e não informam decisões. A spec garante que o que será construído é o que o negócio precisa.

## Etapas

### 1 — Contexto e público
- **Público-alvo:** quem vai usar? (ex: diretores, operadores, time de produto)
- **Frequência de uso:** consultado diariamente, semanalmente, em crises?
- **Decisão que informa:** qual ação o usuário toma depois de olhar o dashboard?
- **Nível de expertise em dados:** o usuário lê gráficos de dispersão ou precisa de semáforos?

### 2 — KPIs e métricas
Para cada métrica:
- **Nome** e **definição exata** (como é calculada, quais regras de negócio)
- **Numerador e denominador** (para taxas e percentuais)
- **Fonte de dados** (tabela/campo)
- **Periodicidade** de atualização
- **Meta ou benchmark** de referência
- **Owner** (quem é responsável pela métrica)

### 3 — Dimensões e filtros
- Quais dimensões o usuário pode recortar? (ex: produto, região, canal, período)
- Filtros obrigatórios vs. opcionais
- Hierarquias (ex: País → Estado → Cidade)
- Granularidade temporal: diário, semanal, mensal?

### 4 — Visuals e layout
Para cada visual:
- Tipo (linha, barra, pizza, tabela, scorecard, mapa, funil)
- Métricas representadas
- Dimensão do eixo X/Y ou cor
- Ordenação e limite de itens exibidos
- Comportamento ao filtrar (drill-down? cross-filter?)

### 5 — Regras de negócio e alertas
- Quando uma métrica deve aparecer em vermelho? (threshold)
- Comparação padrão: período anterior, meta, YoY?
- Dados faltantes: exibir zero, N/D ou omitir?
- Fuso horário e localização dos dados

### 6 — Dados e pipeline
- Quais tabelas alimentam o dashboard?
- Transformações necessárias (aggregations, joins, filtros de limpeza)
- SLA de atualização: quanto tempo de atraso é aceitável?
- Onde será publicado (Metabase, Looker, Power BI, Superset, etc.)?

## Template de output

```markdown
# Dashboard: <nome>

**Público:** <quem usa>
**Decisão:** <qual ação informa>
**Atualização:** <frequência>
**Plataforma:** <ferramenta>

## KPIs
| Nome | Definição | Fonte | Meta | Owner |
|------|-----------|-------|------|-------|
| | | | | |

## Filtros
- <filtro>: <valores possíveis>

## Visuals
| # | Tipo | Métrica | Dimensão | Notas |
|---|------|---------|----------|-------|
| 1 | | | | |

## Regras de alerta
- <métrica> fica vermelho quando < <threshold>
```

## Regras
- Um dashboard tem uma pergunta central. Se houver mais de três perguntas distintas, divida em dashboards separados.
- Não inclua uma métrica só porque é fácil de calcular. Inclua apenas o que informa decisão.
- Valide a spec com o usuário final antes de construir.
