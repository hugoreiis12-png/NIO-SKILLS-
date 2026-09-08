---
id: 36
name: report-spec
persona: bi
description: Especificar um relatório analítico — pergunta, dados, metodologia, formato e cadência de entrega
model: sonnet
effort: medium
---

# Report Spec

Especifique um relatório analítico antes de produzi-lo.

## Diferença entre relatório e dashboard
- **Dashboard:** monitoramento contínuo, self-service, atualização automática.
- **Relatório:** análise pontual ou recorrente, narrativa + números, produzido por uma pessoa.

## Etapas

### 1 — Escopo e objetivo
- **Pergunta central:** qual questão o relatório responde?
- **Decisão que suporta:** qual escolha será tomada com base nele?
- **Prazo de entrega:** quando precisa estar pronto?
- **Destinatário:** quem recebe e qual é seu nível de familiaridade com dados?
- **Formato de entrega:** slide deck, PDF, e-mail, planilha, dashboard estático?

### 2 — Dados e fontes
- Quais tabelas/sistemas serão consultados?
- Qual é o período de análise?
- Existem dados faltantes ou de qualidade conhecidamente baixa?
- Quem valida os dados antes da publicação?

### 3 — Metodologia
- Tipo de análise: descritiva, diagnóstica, preditiva ou prescritiva?
- Métricas calculadas (com fórmula explícita)
- Segmentações e filtros aplicados
- Comparações (período anterior, meta, benchmark externo)
- Tratamento de outliers ou anomalias

### 4 — Estrutura do relatório
Seções previstas:
1. Sumário executivo (3–5 bullets — o que a liderança precisa saber)
2. Contexto e período analisado
3. Principais métricas (tabela ou scorecard)
4. Análise por segmento
5. Causas identificadas (se diagnóstico)
6. Recomendações
7. Apêndice (metodologia, queries, dados brutos)

### 5 — Processo de revisão
- Quem revisa antes de enviar?
- Há checklist de qualidade?
- Como versionar relatórios recorrentes?

### 6 — Cadência (se recorrente)
- Frequência: semanal, mensal, trimestral?
- Data de entrega (ex: toda segunda-feira até as 9h)
- O que muda entre edições e o que permanece fixo?

## Output esperado
Um documento de spec preenchido com todas as seções, pronto para ser aprovado pelo solicitante antes de iniciar a análise.

## Regras
- Sumário executivo é a seção mais importante. Escreva por último.
- Nunca inclua um dado que você não consegue explicar de onde veio.
- Se o relatório é recorrente, automatize o que for possível e documente o que é manual.
