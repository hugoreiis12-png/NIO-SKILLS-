---
id: 30
name: model-card
description: Documentar um modelo de machine learning — problema, dados, métricas, limitações e uso recomendado
model: sonnet
effort: medium
---

# Model Card

Gere um model card completo para um modelo de machine learning.

## O que é um model card
Um model card é a documentação oficial de um modelo — o equivalente ao README de um software, mas para ML. Deve ser legível por quem vai usar o modelo, não apenas por quem o treinou.

## Seções obrigatórias

### 1 — Visão geral
- Nome e versão do modelo
- Problema que resolve (classificação, regressão, clustering, recomendação, etc.)
- Data de treinamento e data de atualização prevista
- Responsável pelo modelo (time/pessoa)

### 2 — Dados de treinamento
- Fonte e período dos dados
- Tamanho do dataset (linhas, features)
- Como foi feito o split (treino/validação/teste) e proporções
- Preprocessing aplicado (normalização, encoding, imputação)
- Vieses conhecidos nos dados de origem

### 3 — Arquitetura e treinamento
- Algoritmo/framework usado
- Hiperparâmetros relevantes
- Tempo de treinamento e infraestrutura
- Versão do código de treinamento (git hash ou tag)

### 4 — Métricas de desempenho
- Métricas principais (ex: AUC, F1, RMSE, MAPE) — sempre com contexto
- Performance por segmento (se aplicável): por produto, região, cohort
- Comparação com baseline (regra de negócio, modelo anterior)
- Métricas de negócio impactadas

### 5 — Limitações e riscos
- Em quais cenários o modelo se degrada?
- Que tipos de entrada devem ser evitados?
- Vieses identificados na saída
- O que NÃO deve ser feito com esse modelo

### 6 — Uso recomendado
- Como integrar (API, batch, embedded)
- Input esperado (schema com tipos)
- Output gerado (schema, interpretação)
- Threshold recomendado e como ajustá-lo

### 7 — Monitoramento
- Métricas a monitorar em produção
- Sinal de alerta para retreinamento
- Frequência de avaliação

## Regras
- Se uma seção não for aplicável, escreva `N/A — <motivo>`. Nunca deixe em branco.
- Métricas sem contexto são inúteis. Sempre inclua: métrica, valor, dataset, período.
- O model card é um contrato — não prometa o que o modelo não entrega.
