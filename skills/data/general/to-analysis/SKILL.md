---
id: 29
name: to-analysis
persona: analyst
description: Criar um documento de análise exploratória ou relatório analítico a partir de uma pergunta de negócio
model: sonnet
effort: medium
---

# To Analysis

Transforme uma pergunta de negócio em um documento de análise estruturado.

## Quando usar
- Analista recebeu uma demanda ("por que as vendas caíram?", "quem são nossos melhores clientes?")
- Time precisa de um plano antes de abrir o notebook
- Há necessidade de alinhar expectativas com stakeholder antes de executar

## Etapas

### 1 — Entendimento da demanda
Pergunte (ou extraia do contexto):
- Qual é a pergunta central?
- Quem vai consumir a análise e qual decisão ela informa?
- Qual é o prazo?
- Quais dados estão disponíveis?
- O que já foi tentado antes?

### 2 — Enquadramento analítico
Defina:
- **Hipóteses** — quais são as explicações prováveis para o fenômeno?
- **Métricas-chave** — o que vamos medir para validar/refutar cada hipótese?
- **Segmentações** — por produto, região, canal, período, cohort?
- **Baseline** — comparação contra o quê? (período anterior, meta, benchmark)

### 3 — Plano de execução
Liste as análises a realizar em ordem lógica:
- Análise descritiva → tendência → segmentação → causa-raiz
- Para cada análise: fonte de dados, métrica, granularidade, ferramenta

### 4 — Critérios de conclusão
- Quais resultados validam ou refutam cada hipótese?
- O que constitui um "achado acionável"?
- Quando a análise está "boa o suficiente" (sem over-engineering)?

## Template de documento gerado

```markdown
# Análise: <título>

**Pergunta central:** <pergunta>
**Decisão que informa:** <decisão>
**Prazo:** <data>
**Solicitante:** <nome/time>

## Hipóteses
1. <hipótese>
2. <hipótese>

## Dados disponíveis
- <fonte>: <descrição, período>

## Plano de análise
| # | Análise | Fonte | Métrica | Granularidade |
|---|---------|-------|---------|---------------|
| 1 | | | | |

## Critérios de conclusão
- [ ] <critério>

## Achados
> (preencher após execução)

## Recomendações
> (preencher após execução)
```

## Regras
- Não execute a análise — documente o plano. A execução vem depois.
- Se a pergunta for vaga, reformule e confirme com o usuário antes de prosseguir.
- Mantenha o documento em menos de 2 páginas — clareza vale mais que completude.
