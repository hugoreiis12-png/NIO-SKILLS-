---
id: 26
name: explore-dataset
description: Explorar e entender um dataset desconhecido — schema, tipos, distribuição, nulos e outliers
model: sonnet
effort: medium
---

# Explore Dataset

Você recebeu acesso a um dataset desconhecido. Seu objetivo é mapeá-lo de ponta a ponta antes de qualquer análise.

## Etapas

### 1 — Inventário inicial
- Nome e origem do dataset (tabela, arquivo, API)
- Número de linhas e colunas
- Período ou versão dos dados (se aplicável)
- Quem produz e quem consome esses dados

### 2 — Mapeamento de schema
Para cada coluna:
- Nome, tipo de dado e nullable
- Valores únicos (cardinalidade)
- Exemplos representativos (3–5 valores)
- Semântica provável (o que esse campo representa no negócio?)

### 3 — Qualidade dos dados
- Percentual de nulos por coluna
- Duplicatas (linhas idênticas ou chave duplicada)
- Outliers óbvios (valores fora de faixa esperada)
- Inconsistências de formato (datas misturadas, encoding, encoding de null como string)

### 4 — Distribuição e padrões
- Colunas numéricas: min, max, média, mediana, desvio padrão
- Colunas categóricas: distribuição de frequência das top-10 categorias
- Série temporal (se houver): frequência, lacunas, tendências grosseiras

### 5 — Dependências e relações
- Chaves primárias e estrangeiras (explícitas ou inferidas)
- Joins possíveis com outros datasets conhecidos
- Colunas derivadas (calculadas a partir de outras)

## Output esperado
Produzir um **relatório de exploração** em markdown com:
- Sumário executivo (3–5 bullets sobre o dataset)
- Tabela de schema com semântica
- Alertas de qualidade (classificados: crítico / atenção / informativo)
- Perguntas abertas que precisam de validação com o dono dos dados

## Regras
- Não assuma nada que não está nos dados. Marque explicitamente o que é inferência.
- Se não tiver acesso direto ao dataset, solicite os metadados mínimos antes de continuar.
- Prefira comandos reproduzíveis (SQL, pandas, polars) a respostas narrativas soltas.
