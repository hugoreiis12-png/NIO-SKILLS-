---
id: 28
name: review-sql
persona: analyst
description: Revisar uma query SQL quanto a performance, legibilidade, corretude e boas práticas
model: sonnet
effort: low
---

# Review SQL

Revise a query SQL recebida cobrindo quatro eixos. Critério de base: a seção
**SQL** da skill `data-standards`.

## Eixos de revisão

### 1 — Corretude
- A query retorna o que se espera? Há ambiguidade no resultado?
- JOINs podem multiplicar ou perder linhas sem aviso (cartesian product, LEFT JOIN com filtro no WHERE)?
- Funções de agregação com NULLs se comportam como esperado?
- Window functions com PARTITION/ORDER corretos?

### 2 — Performance
- Full table scan onde índice poderia ser usado?
- Filtros aplicados após JOIN em vez de antes (CTE ou subquery mal posicionada)?
- SELECT * em vez de colunas explícitas?
- Funções aplicadas sobre coluna indexada no WHERE (impede uso do índice)?
- N+1 latente (loop implícito via subquery correlacionada)?
- DISTINCT usado para esconder um JOIN errado?

### 3 — Legibilidade
- Aliases descritivos (não `a`, `b`, `t1`)?
- CTEs nomeadas pelo que representam?
- Indentação e capitalização consistentes?
- Lógica complexa sem comentário explicando o porquê?

### 4 — Boas práticas
- Coluna ambígua (mesma coluna em dois JOINs sem qualificar com alias)?
- Comparação de NULL com `=` em vez de `IS NULL`?
- Tipo de dado incompatível em JOIN ou WHERE (cast implícito)?
- Hardcoded values que deveriam ser parâmetros?

## Output esperado
- Lista de issues por eixo, cada uma com:
  - Descrição do problema
  - Trecho da query afetado
  - Versão corrigida (quando aplicável)
- Versão refatorada da query completa (se houver issues de legibilidade ou lógica)
- Estimativa de impacto: alto / médio / baixo

## Regras
- Nunca inventar o schema — se precisar, pergunte quais colunas existem e quais têm índice.
- Se a query for correta e legível, diga isso explicitamente. Não force issues.
- Priorize issues que afetam corretude sobre as de performance.
