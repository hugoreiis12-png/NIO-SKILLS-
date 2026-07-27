---
id: 35
name: kpi-framework
description: Definir um framework de KPIs — objetivo de negócio, métricas, dimensões, metas e owners
model: sonnet
effort: high
---

# KPI Framework

Construa um framework de KPIs conectado aos objetivos do negócio.

## Princípios
- KPI sem objetivo de negócio é um número sem propósito.
- Métrica sem owner não é gerenciada.
- Meta sem baseline é arbitrária.
- Nunca defina mais de 3–5 KPIs primários por área.

## Estrutura

### Nível 1 — Objetivo de negócio
O que o negócio precisa alcançar no período?
Exemplos: crescer receita 20%, reduzir churn 30%, aumentar NPS para 60.

### Nível 2 — KPI primário
A métrica que mede diretamente o objetivo.
- **Nome** e **definição precisa**
- **Fórmula** (numerador / denominador × 100)
- **Fonte de dados** (tabela, campo, sistema)
- **Frequência** de medição
- **Meta** (com baseline e período de referência)
- **Owner** (nome e time)

### Nível 3 — Métricas de diagnóstico
Métricas que explicam o porquê do KPI primário subir ou cair.
Para cada KPI primário, defina 2–4 métricas de diagnóstico.

Exemplo:
> KPI: Taxa de conversão de checkout
> Diagnóstico: abandono por etapa (pagamento, endereço, revisão), tempo médio por etapa, taxa de erro de formulário

### Nível 4 — Dimensões de análise
Por quais ângulos cada KPI pode ser analisado?
- Produto, categoria, SKU
- Canal (orgânico, pago, referral, direto)
- Região, estado, cidade
- Segmento de cliente (tier, cohort, plano)
- Período (diário, semanal, mensal, YoY)

### Nível 5 — Regras de integridade
- Definição única e compartilhada (sem "cada time calcula diferente")
- Cadência de revisão da meta (trimestral?)
- Processo de contestação (quem aprova mudança de definição?)
- Documentação versionada

## Output esperado

```markdown
# Framework de KPIs — <área/produto>

**Período:** <vigência>
**Revisor:** <responsável>

## Objetivo: <descrição>

### KPI 1 — <nome>
- **Definição:** <fórmula detalhada>
- **Fonte:** <tabela/sistema>
- **Meta:** <valor> (baseline: <valor atual>, referência: <período>)
- **Frequência:** <diário/semanal/mensal>
- **Owner:** <nome/time>

#### Métricas de diagnóstico
1. <métrica>: <definição>
2. <métrica>: <definição>

#### Dimensões
- <dimensão>
```

## Regras
- Toda meta precisa de baseline. Sem baseline, a meta é chute.
- Cada KPI tem exatamente um owner. Dois owners = zero owners.
- Se você não consegue calcular o KPI hoje, documente o gap de dados antes de assumir a meta.
