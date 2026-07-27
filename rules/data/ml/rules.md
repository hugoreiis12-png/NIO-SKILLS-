# Regras — Machine Learning

Valem para desenvolvimento, avaliação e implantação de modelos no setor de dados.

## Antes de modelar
- Entenda o baseline: regra de negócio simples, modelo mais simples possível, ou média histórica. O modelo complexo só se justifica se superar o baseline de forma consistente.
- Defina a métrica de sucesso antes de ver os dados. Métricas escolhidas após ver os resultados são métricas escolhidas para parecerem boas.
- Entenda o custo de cada tipo de erro: falso positivo vs. falso negativo. Otimize para o que importa.

## Prevenção de data leakage
- O conjunto de teste nunca é visto antes da avaliação final. Nunca.
- Toda transformação (scaler, encoder, imputer) é fitada apenas no conjunto de treino, aplicada nos demais.
- Cross-validation encapsula o pipeline completo — incluindo feature engineering e seleção.
- Features temporais: dados de t não podem incluir informação de t+1 (leakage temporal).
- Target encoding: sempre com regularização (k-fold ou smoothing) para evitar leakage.

## Avaliação honesta
- Reporte sempre mais de uma métrica. Accuracy sozinha é enganosa para dados desbalanceados.
- Analise os erros: onde o modelo erra? Há padrão nos erros? O que os erros custam?
- Avalie por segmento quando aplicável (por região, produto, cohort). Performance média pode esconder subgrupos com desempenho péssimo.
- Curva de aprendizado: o modelo ainda melhora com mais dados? Ou estabilizou?

## Reprodutibilidade e versionamento
- Seed fixada para treino, split e qualquer operação aleatória.
- Versão do código (git hash ou tag) registrada junto ao artefato do modelo.
- Hyperparâmetros, métricas e artefatos rastreados (MLflow, W&B, ou arquivo de metadados).
- Dados de treinamento versionados ou com hash registrado.

## Documentação
- Todo modelo em produção tem um model card (ver skill `model-card`).
- Limitações conhecidas documentadas — não descobertas pelo usuário final.
- Critério de retreinamento definido: quando o modelo está desatualizado?

## Produção
- Modelos em produção têm monitoramento de drift (de dados e de performance).
- Rollback é possível sem re-treinar: mantenha o modelo anterior acessível.
- Predições são logadas com inputs para auditoria e diagnóstico futuro.
