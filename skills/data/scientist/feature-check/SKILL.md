---
id: 33
name: feature-check
description: Avaliar features existentes e sugerir feature engineering para melhorar um modelo de ML
model: sonnet
effort: medium
---

# Feature Check

Avalie as features existentes e identifique oportunidades de feature engineering.

## Etapas

### 1 — Inventário de features atuais
Para cada feature:
- Nome e tipo (numérica, categórica, binária, temporal, textual)
- Proporção de nulos
- Cardinalidade
- Distribuição (skewed? bimodal? uniforme?)
- Correlação com o target (se supervisionado)

### 2 — Diagnóstico de problemas
- **Alta cardinalidade** em categórica → encoding problemático
- **Distribuição muito skewed** → pode precisar de transformação (log, sqrt, box-cox)
- **Correlação muito alta entre features** → multicolinearidade (VIF > 10)
- **Feature com variância zero ou quase zero** → candidata a remoção
- **Leakage suspeito** → feature criada com informação do futuro?
- **Magnitude muito diferente entre features** → normalização necessária para modelos sensíveis a escala

### 3 — Sugestões de feature engineering

#### Numéricas
- Binning/discretização para capturar relação não-linear
- Interações entre features (produto, razão, diferença)
- Transformações matemáticas (log, raiz, reciproco)
- Lags e rolling windows para séries temporais

#### Categóricas
- Target encoding (com regularização para evitar leakage)
- Embeddings para alta cardinalidade
- Agrupamento de categorias raras em "outros"
- One-hot encoding para baixa cardinalidade (<10 categorias)

#### Temporais
- Extração: dia da semana, hora, mês, trimestre, feriado, dia útil
- Lag features: valor de N períodos atrás
- Rolling statistics: média, desvio, min/max em janela
- Sazonalidade: Fourier features para padrões periódicos

#### Textuais
- TF-IDF para bag of words
- Embeddings (sentence-transformers) para semântica
- Features simples: contagem de palavras, presença de termos-chave

### 4 — Priorização
Classifique as sugestões por impacto esperado × custo de implementação:
- 🔥 Alto impacto, baixo custo — fazer primeiro
- 🟡 Alto impacto, alto custo — planejar
- 🔵 Baixo impacto, baixo custo — fazer se houver tempo
- ❌ Baixo impacto, alto custo — descartar

## Regras
- Toda sugestão de feature engineering deve ter justificativa ("por que isso pode ajudar o modelo?").
- Não sugira features sem verificar se os dados para criá-las existem.
- Sempre alerte quando uma sugestão pode causar leakage.
- O objetivo é melhorar o modelo, não maximizar o número de features.
