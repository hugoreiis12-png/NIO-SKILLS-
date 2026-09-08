---
id: 44
name: data-standards
description: As convenções do setor de dados — reprodutibilidade, qualidade, granularidade, privacidade, e as regras de SQL, Python, ML e BI. Use como referência sempre que produzir análise, query, notebook, modelo ou dashboard, ou quando revisar trabalho de dados.
model: sonnet
effort: low
---

# Data standards

O harness do setor de dados. As demais skills de dados (`explore-dataset`,
`review-sql`, `model-card`, `dashboard-spec`, …) assumem estas regras — este
documento é a fonte única. Código em inglês; texto de análise/UI no idioma do
produto.

## Fundamentos (toda função de dados)

### Reprodutibilidade
- Todo trabalho é reproduzível por outra pessoa, em outra máquina.
- Seed fixa para qualquer operação aleatória. Seed padrão: **`42`**
  (`np.random.seed(42)`, `random.seed(42)`, seed de split/treino).
- Versões de bibliotecas registradas (`requirements.txt` / `pyproject.toml` com
  versões fixadas; cabeçalho de notebook).
- Paths relativos, nunca absolutos. Credenciais em variável de ambiente ou `.env`
  — nunca hardcoded.

### Qualidade antes de quantidade
- Valide os dados na **entrada**, não só no output.
- Dados com qualidade desconhecida não viram métrica de negócio sem disclaimer
  explícito.
- Um número errado publicado para a liderança é pior do que nenhum número.

### Granularidade e agregação
- Saiba sempre a granularidade do dado (uma linha = o quê?).
- Nunca agregue sem entender o que acontece com nulos na agregação.
- Cuidado com `GROUP BY` que descarta linhas silenciosamente.
- Somas de percentuais quase sempre erradas — some numeradores e denominadores
  separadamente. Média de médias com pesos diferentes → use média ponderada.

### Privacidade e segurança
- PII não aparece em logs, prints de console ou relatórios públicos.
- Dado sensível em dev é anonimizado ou sintético.
- Acesso a produção é auditável — não use credencial de produção localmente sem
  necessidade.

### Comunicação de incerteza
- Estimativa vem com intervalo de confiança ou margem de erro quando possível;
  se não dá pra quantificar, declare qualitativamente ("preliminar", "sujeito a
  revisão").
- Nunca comunique resultado como definitivo quando os dados são parciais ou a
  metodologia é experimental.

### Documentação mínima
- Todo dataset manipulado tem dicionário de dados associado (mesmo interno).
- Toda análise começa com a pergunta que responde e termina com a conclusão.
- Decisões metodológicas (por que esse filtro? por que esse modelo?) são
  registradas.

## SQL

**Legibilidade** — keywords em maiúsculo; uma cláusula por linha; vírgulas no
início da linha; CTEs com nomes descritivos (não `cte1`/`temp`/`aux`); aliases
descritivos (`u`/`allocations` ok, `t1`/`x` não); comentário só para o porquê.

**Corretude** — coluna qualificada com alias sempre que há JOIN; NULLs com
`IS NULL`/`IS NOT NULL` (nunca `= NULL`); filtro de tabela à direita de
`LEFT JOIN` vai no `ON`, não no `WHERE` (senão vira `INNER` silenciosamente);
`COUNT(coluna)` ignora NULL, `COUNT(*)` não; window function sempre com
`ORDER BY` explícito.

**Performance** — sem `SELECT *` em produção/pipeline; filtre o mais cedo
possível (dentro da CTE, não no SELECT final); sem função sobre coluna indexada
no `WHERE` (`created_at BETWEEN …`, não `YEAR(created_at) = …`); subquery
correlacionada é candidata a N+1 → reescreva com JOIN/window; `DISTINCT` para
mascarar JOIN multiplicativo é bug — conserte o JOIN; nunca `ORDER BY` sem
`LIMIT` em produção.

**Boas práticas** — teste contra casos-limite (dataset vazio, nulos nas chaves,
período sem dados); datas e valores de negócio viram parâmetros/constantes em
CTE; query > 50 linhas ganha comentário de bloco no topo.

## Python para dados

**Estilo** — PEP 8 (`ruff`/`black`); função com uma responsabilidade (nome com
"e" → divida); type hints ao sair de notebook para módulo.

**Pandas / Polars** — operações vetorizadas, não loops; `.apply()` com função
Python pura é loop disfarçado; evite `inplace=True`; `groupby` + `agg` > `apply`
para agregação padrão; dataset > 1 GB → Polars lazy ou leitura por chunks.

**Notebooks** — célula ≤ 20 linhas executáveis; função > 10 linhas vai para
módulo `.py`; toda célula que gera gráfico tem título, labels e unidades; ordem:
imports → constantes/config → lógica; "restart + run all" do zero tem que
funcionar (sem dependência de estado de execução).

**Qualidade** — script de pipeline tem smoke test; função de transformação tem
teste de caso-limite (vazio, nulo, extremo); `logging` em vez de `print` em
produção (INFO progresso, WARNING anomalia, ERROR falha).

## Machine Learning

**Antes de modelar** — entenda o baseline (regra simples / média histórica); o
modelo complexo só se justifica se superar o baseline de forma consistente.
Defina a métrica de sucesso **antes** de ver os dados. Entenda o custo de cada
tipo de erro (falso positivo vs. negativo) e otimize para o que importa.

**Prevenção de data leakage** — o conjunto de teste nunca é visto antes da
avaliação final; toda transformação (scaler/encoder/imputer) é fitada só no
treino; cross-validation encapsula o pipeline inteiro (feature engineering +
seleção); features temporais sem informação de `t+1`; target encoding sempre
com regularização (k-fold / smoothing).

**Avaliação honesta** — reporte mais de uma métrica (accuracy sozinha engana em
dados desbalanceados); analise os erros (há padrão? o que custam?); avalie por
segmento (região/produto/cohort) — a média esconde subgrupos ruins; curva de
aprendizado (ainda melhora com mais dados?).

**Versionamento** — seed em treino/split; git hash/tag junto ao artefato do
modelo; hiperparâmetros, métricas e artefatos rastreados (MLflow/W&B/arquivo de
metadados); dados de treino versionados ou com hash.

**Produção** — monitoramento de drift (dados e performance); rollback sem
re-treinar (mantenha o modelo anterior acessível); predições logadas com inputs
para auditoria; todo modelo em produção tem model card (skill `model-card`) e
critério de retreinamento definido.

## Business Intelligence

**Definição de métricas** — definição única, documentada e acessível; numerador
e denominador explícitos para taxas; nomes diferentes para a mesma coisa →
escolha uma e deprecie a outra; mudança de definição tem data e registro.

**Dashboards** — um dashboard responde a **uma** pergunta central (mais de três
→ dashboards separados); todo visual com título afirmativo ("Conversão caiu 15%
em março", não "Conversão por mês"); sem pizza com > 4 fatias (barra horizontal
para ranking); cores com significado consistente (verde bom / vermelho ruim /
cinza neutro); filtros globais afetam todos os visuals salvo exceção
documentada; carregamento > 30 s pede otimização de query ou cache.

**Atualização e confiabilidade** — SLA de atualização definido e monitorado; se
o dado está atrasado, o dashboard informa; dados parciais (dia não fechado, mês
em andamento) sinalizados visualmente; nunca exiba número sem saber quando foi
atualizado.

**Comunicação com stakeholders** — relatório sem contexto é só números:
adicione a interpretação; linguagem de negócio, não técnica ("receita por
cliente ativo", não `AVG(revenue) WHERE status='active'`); quando um número cai,
traga a hipótese de causa junto; caveats documentados antes de perguntarem.
