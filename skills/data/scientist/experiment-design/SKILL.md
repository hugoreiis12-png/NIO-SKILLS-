---
id: 31
name: experiment-design
description: Desenhar um experimento controlado ou teste A/B — hipótese, métricas, amostragem e poder estatístico
model: sonnet
effort: high
---

# Experiment Design

Estruture um experimento controlado antes de executá-lo.

## Etapas

### 1 — Hipótese
- **Hipótese nula (H₀):** o que você quer refutar
- **Hipótese alternativa (H₁):** o que você espera observar
- **Efeito mínimo detectável (MDE):** qual a menor diferença que tem significado prático para o negócio?

Exemplo:
> H₀: a nova tela de checkout não altera a taxa de conversão.
> H₁: a nova tela aumenta a conversão em pelo menos 2%.
> MDE: 2% de aumento relativo.

### 2 — Métricas
- **Métrica primária:** a única que decide se o experimento foi bem-sucedido
- **Métricas de guarda:** o que não pode piorar (ex: tempo de sessão, churn)
- **Métricas secundárias:** insights adicionais, não critério de decisão

### 3 — Unidade de randomização
- Por usuário? Por sessão? Por produto? Por região?
- Atenção ao SUTVA (spillover entre variantes)
- Como garantir que o mesmo usuário sempre cai no mesmo grupo?

### 4 — Amostragem e duração
- **Tamanho de amostra por grupo** — calcule com base em:
  - Taxa base atual (baseline rate)
  - MDE
  - Nível de significância (α, tipicamente 5%)
  - Poder estatístico (1−β, tipicamente 80%)
- **Duração mínima:** pelo menos um ciclo completo de comportamento (ex: semana cheia para evitar efeito dia-da-semana)
- **Estratificação:** alguma variável de controle deve ser balanceada entre grupos?

### 5 — Critérios de parada
- Quando você vai olhar os resultados? (evite peeking)
- Condição de parada antecipada (ex: dano grave ao usuário)
- O que acontece se o resultado for inconclusivo?

### 6 — Plano de análise
- Teste estatístico a usar (t-test, chi-quadrado, Mann-Whitney, etc.)
- Correção para múltiplas comparações (Bonferroni, Benjamini-Hochberg)
- Como tratar outliers?
- Como lidar com dados faltantes?

### 7 — Implementação e rollout
- Quem implementa o tratamento e como?
- Como garantir que não há vazamento entre grupos?
- Plano de rollout após decisão (100% gradual ou toggle)

## Output esperado
Um documento de design de experimento com todas as seções preenchidas, incluindo:
- Cálculo de amostra (com parâmetros explícitos)
- Checklist pré-lançamento
- Cronograma (início, análise intermediária se houver, fim)

## Regras
- Não comece a coletar dados sem o design aprovado.
- MDE deve ser definido pelo negócio, não pelo estatístico.
- "Estatisticamente significativo" não é o mesmo que "relevante para o negócio" — sempre reporte o tamanho do efeito observado.
