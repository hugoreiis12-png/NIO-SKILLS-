# 04 — Dados

Engenharia de dados, análise, estatística, ciência de dados e BI. O denominador comum: **um número errado com aparência confiável causa mais dano que um sistema fora do ar**, porque ninguém percebe.

**Conteúdo:** Primeiro contato · Engenharia de pipeline · Qualidade · Modelagem dimensional · Análise · Estatística · Ciência de dados/ML · Power BI e DAX · Entrega de resultado

---

## 1. Primeiro contato com qualquer base

Nunca escreva transformação ou análise antes de responder isto — com consulta, não com suposição:

1. **Granularidade.** Uma linha representa o quê, exatamente? (Um pedido? Um item de pedido? Um item por dia?) Quase todo erro de agregação nasce aqui.
2. **Chave.** Existe? É única de fato? `SELECT chave, COUNT(*) ... HAVING COUNT(*) > 1`.
3. **Volume e período.** Contagem por mês. Revela lacunas, cortes de carga e mudança de regra de negócio.
4. **Nulidade e cardinalidade** por coluna relevante. Coluna 90% nula muda a análise inteira.
5. **Domínio dos categóricos.** `GROUP BY` nas categorias: revela `"SP"`, `"sp"`, `"São Paulo"`, `""` e `"N/A"` como quatro coisas diferentes.
6. **Faixa e outliers** dos numéricos: mín, máx, percentis. Valor negativo em quantidade, data em 1900 ou 2099, `-1` como sentinela.
7. **Datas**: fuso horário, tipo (data ou timestamp), qual data é a relevante (emissão? competência? pagamento?). Confundi-las é o erro mais comum em relatório financeiro.
8. **Duplicatas** e o que as gera (reprocessamento, integração que reenvia, junção que multiplica).

**Regra de junção:** antes de qualquer `JOIN`, saiba a cardinalidade dos dois lados. Compare a contagem antes e depois. Fato inflado por junção com dimensão duplicada é o bug clássico que passa despercebido por meses.

---

## 2. Engenharia de pipeline

- **Camadas explícitas.** Bruto/bronze (imutável, como veio, com metadado de carga) → limpo/silver (tipado, deduplicado, conformado) → consumo/gold (modelo dimensional ou agregado). Nunca transforme sobre o bruto destrutivamente: o bruto é a única forma de reprocessar.
- **Idempotência é requisito, não virtude.** Rodar duas vezes produz o mesmo resultado. Padrão: escrita por partição com sobrescrita (`delete+insert` da janela ou `MERGE` por chave), nunca `INSERT` cego.
- **Carga incremental por marca d'água**, com sobreposição de segurança (reprocessa as últimas N horas) para pegar registro atrasado. Registre a marca d'água em lugar durável.
- **Particione pelo que você filtra** (normalmente data do evento). Partição errada = varredura total todo dia.
- **Contrato de dados na origem**: esquema esperado, tipos, obrigatoriedade, semântica. Falhe a carga quando o contrato quebra — não deixe passar coluna nova ignorada nem tipo alterado silenciosamente.
- **Metadado de linhagem** em toda tabela derivada: origem, timestamp da carga, id da execução, versão da lógica. Sem isso, investigar divergência é arqueologia.
- **Falha explícita > resultado parcial.** Pipeline que grava metade e reporta sucesso é a pior falha possível em dados.
- **Reprocessamento (backfill) previsto desde o desenho.** Se você não consegue reprocessar março de 2024 hoje, seu pipeline é frágil.
- **Slowly Changing Dimension:** decida conscientemente entre Tipo 1 (sobrescreve, perde histórico) e Tipo 2 (versiona com vigência). Relatório histórico com dimensão Tipo 1 muda o passado retroativamente — e alguém vai notar no fechamento.

---

## 3. Qualidade de dados — testes obrigatórios

Trate como teste de unidade do pipeline. Rodam a cada carga, falham alto.

| Categoria | Teste |
|---|---|
| Unicidade | Chave primária sem duplicata |
| Completude | Colunas críticas sem nulo; taxa de nulos dentro do histórico |
| Referencial | Toda chave do fato existe na dimensão (e vice-versa, quando aplicável) |
| Domínio | Categóricos dentro do conjunto permitido |
| Faixa | Valores dentro de mín/máx plausíveis; sem negativo onde é impossível |
| Volumetria | Contagem do dia dentro da faixa esperada vs histórico |
| Frescor | Dado mais recente dentro do SLA |
| Reconciliação | Total do consumo bate com o total da origem (por período e por chave) |

**Reconciliação é o teste que salva.** Em migração ou refatoração de relatório, compare o número antigo e o novo por período e por dimensão, e explique **toda** divergência antes de promover. Divergência não explicada = não vai para produção.

---

## 4. Modelagem dimensional

- **Esquema estrela por padrão.** Fato no centro (métricas + chaves), dimensões descritivas ao redor. Floco de neve só quando a dimensão é realmente grande e compartilhada. Modelo normalizado em ferramenta de BI mata desempenho e confunde o usuário.
- **Uma granularidade por tabela fato.** Declare-a por escrito antes de criar. Misturar granularidades na mesma fato é irreparável depois.
- **Tipos de fato:** transacional (uma linha por evento) · snapshot periódico (saldo por dia) · snapshot acumulado (marcos de um processo). Escolher errado gera métrica impossível de calcular.
- **Aditividade da métrica:** aditiva (valor de venda) · semiaditiva (saldo — soma em cliente, não em tempo) · não aditiva (percentual, taxa — recalcule, nunca some).
- **Dimensão Data dedicada e completa**, marcada como tabela de datas, com atributos de negócio (ano fiscal, dia útil, feriado, semana). Calendário derivado do fato quebra em período sem movimento.
- **Chave substituta (surrogate)** nas dimensões; chave natural preservada como atributo.
- **Nomes voltados ao negócio**, não ao sistema de origem. O usuário final não deveria ver `VBRK_KUNAG`.

---

## 5. Análise — do pedido ao insight

- **Reformule a pergunta em algo mensurável.** "As vendas caíram?" → "A receita líquida do canal X caiu no mês corrente vs mesmo período do ano anterior, controlando por dias úteis?"
- **Defina a métrica sem ambiguidade**: numerador, denominador, filtro, período, granularidade, tratamento de devolução/cancelamento/desconto. Metade das discordâncias entre áreas é definição divergente da mesma palavra.
- **Estabeleça a linha de base.** Um número sozinho não significa nada. Comparar com: período anterior, mesmo período do ano anterior, meta, segmento par, média histórica.
- **Decomponha antes de teorizar.** Quebre a variação por dimensão (produto, região, canal, cliente, vendedor). Quase sempre a "queda geral" é um segmento específico.
- **Efeito mix.** Um total pode cair com todos os segmentos subindo, se a composição mudou. Separe efeito de volume, preço e mix antes de atribuir causa.
- **Paradoxo de Simpson.** A direção do agregado pode inverter no desagregado. Sempre olhe pelo menos um nível abaixo antes de concluir.
- **Correlação não é causa** — e a distinção não é formalidade: pergunte sobre confundidores, causalidade reversa, seleção da amostra e sazonalidade.
- **Viés de sobrevivência e de seleção.** Quem saiu da base não aparece nela. Analisar só clientes ativos para explicar churn é circular.
- **Sazonalidade e calendário** antes de qualquer conclusão sobre tendência: dias úteis, feriados, virada de mês, campanha, mudança de regra.
- **Mudança na coleta parece mudança no mundo.** Antes de explicar um degrau no gráfico, verifique deploy, integração, regra nova ou fonte alterada naquela data.

---

## 6. Estatística com honestidade

- **Significância ≠ relevância.** Com amostra grande, tudo é significante. Reporte **tamanho do efeito** e intervalo de confiança, e diga se o efeito importa para a decisão.
- **Intervalo de confiança sempre.** Ponto estimado sem incerteza é ilusão de precisão.
- **Não fatie até achar significância** (p-hacking). Hipótese e recorte definidos antes de olhar o resultado; se explorar depois, rotule como exploratório e corrija para múltiplas comparações.
- **Amostra pequena**: não reporte percentual sobre denominador minúsculo ("crescimento de 200%" sobre 3 casos). Mostre o absoluto.
- **Média mente com cauda longa.** Use mediana e percentis para tempo, valor de pedido, latência, receita por cliente.
- **Teste A/B:** defina métrica primária, tamanho de amostra e duração antes; respeite ciclo semanal completo; não pare ao ver ganho (peeking); verifique desequilíbrio na aleatorização.
- **Previsão**: comece com baseline ingênuo (último valor, média sazonal). Um modelo que não bate o ingênuo não deveria existir. Valide sempre com corte temporal, nunca com embaralhamento aleatório.

---

## 7. Ciência de dados e ML

- **Baseline burro primeiro.** Regra simples, heurística de negócio ou modelo linear. Muitos problemas terminam aí, e sempre calibra a expectativa.
- **Vazamento de dado (leakage) é a falha nº 1.** Sintoma clássico: métrica boa demais. Causas: variável que só existe depois do desfecho · normalização calculada antes da divisão treino/teste · identificador do mesmo cliente em treino e teste · janela temporal misturada. Suspeite sempre que o resultado surpreender positivamente.
- **Validação espelha a produção.** Se o uso é prever o futuro, a validação é temporal. Se agrupa por cliente, a divisão é por cliente.
- **Métrica escolhida pelo custo do erro.** Acurácia em base desbalanceada é inútil. Falso positivo e falso negativo têm custos diferentes — deixe isso explícito e escolha limiar por ele, não pelo padrão 0,5.
- **Reprodutibilidade**: semente fixa, versão de dado, versão de código, ambiente registrado. Resultado que não reproduz não é resultado.
- **Interpretabilidade é requisito quando há decisão sobre pessoas** (crédito, contratação, priorização). Verifique disparidade entre grupos antes de entregar.
- **Modelo em produção precisa de**: monitoramento de deriva (entrada e desempenho), plano de retreino, versionamento, caminho de reversão e valor padrão para quando falhar.
- **Feature engineering é onde está o ganho real**, muito mais que troca de algoritmo.

---

## 8. Power BI e DAX

- **Modelo antes de medida.** 80% dos problemas de DAX são problema de modelo: granularidade errada, relacionamento bidirecional desnecessário, tabela de datas ausente, dimensão duplicada, coluna de texto de alta cardinalidade inflando o modelo.
- **Relacionamento único, direção simples**, filtro do lado 1 para o lado muitos. Bidirecional só com motivo escrito — ele cria ambiguidade e caminhos de filtro imprevisíveis.
- **Medida, não coluna calculada**, sempre que o valor depender do contexto de filtro. Coluna calculada ocupa memória e é fixa na atualização; medida é dinâmica.
- **Transformação pesada o mais perto da origem possível**: banco > Power Query > DAX. Coluna calculada em DAX é o último recurso.
- **Entenda o contexto antes de escrever**: contexto de filtro (de onde vem o filtro) e contexto de linha (iteradores). `CALCULATE` modifica contexto de filtro — é a função central da linguagem e a origem da maioria dos erros.
- **Padrões corretos**: `VAR` para legibilidade e para avaliar uma vez · `DIVIDE()` em vez de `/` (trata divisão por zero) · `SELECTEDVALUE` em vez de `VALUES` com risco de múltiplos · `TREATAS` para relacionamento virtual · `KEEPFILTERS` quando não quer sobrescrever o filtro do usuário · variáveis capturam o contexto do ponto onde são declaradas — esse é o comportamento que mais confunde.
- **Inteligência temporal** exige tabela de datas marcada e contígua. `DATEADD`/`SAMEPERIODLASTYEAR` falham silenciosamente sem isso.
- **Desempenho**: evite iterador sobre tabela grande quando existe agregação nativa; evite `FILTER` sobre a tabela inteira dentro de `CALCULATE` (filtre a coluna); minimize colunas de alta cardinalidade; verifique com o Performance Analyzer e DAX Studio quando houver dúvida — meça, não adivinhe.
- **Nomeie e documente medidas** com descrição e pasta de exibição. Modelo com 200 medidas sem organização é intransitável.
- **Valide toda medida nova contra um número conhecido** antes de publicar. Medida plausível e errada é o pior resultado possível.

---

## 9. Entregar resultado de análise

Ordem obrigatória:

1. **Resposta à pergunta**, em uma frase, com o número principal.
2. **Como foi medido**: definição da métrica, período, filtros, fonte, granularidade.
3. **Evidência**: a decomposição que sustenta a conclusão.
4. **O que isso não diz**: limitações, dados faltantes, hipóteses alternativas não descartadas.
5. **Decisão ou próximo passo**.

Regras: nunca reporte percentual sem o absoluto · sempre diga o período e a fonte · gráfico começa em zero quando compara magnitude · escolha do tipo de gráfico pela pergunta (evolução → linha; composição → barra empilhada ou treemap; comparação → barra; relação → dispersão) · não use pizza com mais de três fatias · rotule eixo com unidade.
