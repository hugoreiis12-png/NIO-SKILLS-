---
id: 32
name: review-notebook
description: Revisar um Jupyter notebook quanto a reprodutibilidade, clareza, performance e boas práticas de ciência de dados
model: sonnet
effort: medium
---

# Review Notebook

Revise um Jupyter notebook cobrindo quatro eixos.

## Eixos de revisão

### 1 — Reprodutibilidade
- Seeds fixadas para todos os componentes aleatórios (numpy, random, sklearn, torch)?
- Versões das bibliotecas registradas (requirements.txt, pyproject.toml ou magic `%pip freeze`)?
- Células executadas em ordem? (sem dependência de estado de execução fora de ordem)
- Dados de entrada versionados ou com hash registrado?
- Paths hardcoded que quebram em outra máquina?
- Variáveis de ambiente ou secrets vazando no output?

### 2 — Clareza e estrutura
- Notebook tem seções claras (ingestão → EDA → feature engineering → modelagem → avaliação)?
- Células de código longas que deveriam ser funções?
- Magic numbers sem contexto (ex: `0.7`, `42`, `100`)?
- Markdown explicando o porquê das escolhas, não apenas o que o código faz?
- Gráficos sem título, labels de eixo ou unidades?
- Conclusões intermediárias presentes após cada etapa?

### 3 — Performance
- Loop Python sobre DataFrame onde operação vetorizada resolveria?
- `.apply()` onde `groupby` ou operação nativa seria mais rápido?
- Dataset carregado inteiro na memória quando leitura por chunks ou lazy resolve?
- Modelo treinado múltiplas vezes sem cache de resultado intermediário?
- Joins desnecessariamente caros (sem filtro antes do join)?

### 4 — Boas práticas de ML
- Dados de teste vistos antes da avaliação final? (data leakage)
- Pipeline de preprocessing dentro do cross-validation? (leakage via fit no treino completo)
- Apenas uma métrica reportada sem análise de erros?
- Classes desbalanceadas tratadas? (ou pelo menos reconhecidas)
- Feature importance ou interpretabilidade presente?
- Overfitting checado (curva de aprendizado, diferença treino/validação)?

## Output esperado
- Lista de issues por eixo, classificadas: 🔴 Crítico / 🟡 Atenção / 🔵 Sugestão
- Para cada issue: célula afetada + descrição + correção recomendada
- Score geral de maturidade do notebook: Exploratório / Revisável / Compartilhável / Produtizável

## Regras
- Foco em notebooks de análise e ML — não é uma revisão de código Python genérico.
- Não reescreva o notebook inteiro — aponte os problemas e mostre como corrigir o trecho afetado.
- Se o notebook for puramente exploratório (EDA), relaxe os critérios de reprodutibilidade e foque em clareza.
