---
id: 27
name: data-quality
persona: analyst
description: Avaliar qualidade de dados — completude, consistência, unicidade e validade por coluna ou tabela
model: sonnet
effort: medium
---

# Data Quality

Avalie sistematicamente a qualidade dos dados em uma tabela ou dataset.

## Dimensões de qualidade

### Completude
- Percentual de nulos por coluna
- Campos obrigatórios vs opcionais — está respeitado?
- Registros parcialmente preenchidos (linha existe mas campos-chave estão vazios)

### Unicidade
- Duplicatas exatas (todas as colunas idênticas)
- Duplicatas de chave negocial (mesmo ID, datas diferentes — qual é o registro correto?)
- Linhas fantasma (registros que deveriam ter sido deletados mas permanecem)

### Consistência
- Mesmo campo com formatos diferentes (ex: data como `2024-01-01` e `01/01/2024`)
- Valores de enum fora do domínio esperado
- Referências quebradas (FK apontando para ID inexistente)
- Unidades misturadas (ex: valor em R$ em alguns registros e em USD em outros)

### Validade
- Valores fora de faixa (ex: idade negativa, percentual > 100)
- Violação de regra de negócio (ex: `data_fim < data_inicio`)
- Tipos incorretos (número armazenado como texto)

### Temporalidade
- Dados desatualizados (última atualização muito antiga)
- Lacunas temporais inesperadas (série quebrada)
- Registros com timestamps no futuro

## Output esperado
Gerar um **relatório de qualidade** com:
- Score geral por dimensão (0–100%)
- Tabela de issues classificadas por severidade: 🔴 Crítico / 🟡 Atenção / 🔵 Informativo
- Query ou código reproduzível para cada issue encontrada
- Recomendação de ação: corrigir na fonte / tratar no pipeline / documentar como known issue

## Regras
- Nunca alterar os dados — apenas reportar.
- Para cada issue, fornecer a query que a detecta, não apenas o texto.
- Se o dataset tiver mais de 20 colunas, priorize as colunas usadas em métricas de negócio.
