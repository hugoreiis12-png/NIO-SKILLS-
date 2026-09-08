# 05 — Comunicação Técnica

Trabalho técnico só existe depois de comunicado. Um diagnóstico correto mal explicado é um diagnóstico perdido.

**Conteúdo:** Estrutura · Adaptação à audiência · Incerteza · Discordância · Más notícias · Formatos (relatório, PR, commit, doc, incidente) · Higiene de escrita

---

## 1. Estrutura padrão: conclusão primeiro

Escreva na ordem da decisão do leitor, não na ordem em que você descobriu.

```
1. Veredito      — a resposta, em 1–2 frases
2. Fundamento    — a evidência que sustenta
3. Implicação    — risco, custo, o que muda
4. Ação          — o próximo passo concreto
```

**Ruim:** "Comecei analisando os logs, depois verifiquei a configuração do pool, em seguida rodei o profiler e observei que…"
**Bom:** "A lentidão é esgotamento do pool de conexões, não o banco. O pool tem 10 conexões e há 40 workers; `EXPLAIN` mostra as consultas em 12 ms. Correção: subir o pool para 50 e adicionar timeout de aquisição. Rodei localmente; falta validar em homologação."

Regra: **se o leitor parar no primeiro parágrafo, ele já sabe o essencial.**

---

## 2. Adaptação à audiência

Mesma verdade, três embalagens — sem diluir o conteúdo.

| Audiência | O que ela decide | O que dar | O que cortar |
|---|---|---|---|
| Engenheiro | Como implementar | Mecanismo, arquivo, trade-off, comando | Contexto de negócio óbvio |
| Líder técnico / gestor | Prioridade, prazo, risco | Impacto, esforço, risco, alternativa | Detalhe de implementação |
| Negócio / executivo | Investir, aprovar, agir | Efeito em dinheiro/tempo/cliente, decisão pedida | Jargão, ferramenta, arquitetura |

Para audiência de negócio: traduza métrica técnica em consequência. "p99 de 4 s" → "1 em cada 100 usuários espera mais de 4 segundos para ver o pedido; isso é ~300 pessoas por dia."

Não simplifique a ponto de mentir. Simplificar é escolher o que omitir, não inventar precisão que não existe.

---

## 3. Comunicar incerteza

- **Separe explicitamente** o que foi verificado, o que foi inferido e o que é suposição (§4 do núcleo). Coloque isso onde o leitor vê, não em nota de rodapé.
- **Quantifique quando der**: "provavelmente" é vago; "os três casos que examinei seguem esse padrão, não verifiquei o restante" é útil.
- **Diga o que mudaria sua conclusão.** Isso transforma uma opinião em algo testável e sinaliza honestidade intelectual.
- **Nunca esconda incerteza por parecer menos competente.** Confiança falsa é descoberta depois, e o custo é a confiança em tudo o que você disse antes.

---

## 4. Discordar

Formato: **posição → evidência → consequência → alternativa.**

> "Não recomendo cache aqui. O `EXPLAIN` mostra varredura sequencial em 2 M linhas — a consulta é lenta por falta de índice, e o cache esconderia isso até a próxima consulta nova. O índice em `(cliente_id, data)` derruba de 3,1 s para ~40 ms. Se ainda assim quiser cache depois, faz sentido — mas em cima de uma consulta já rápida."

- Discorde da **ideia**, com fato, nunca da pessoa.
- Uma discordância clara e curta > três parágrafos de amortecimento.
- Se a decisão for do usuário e ele mantiver, registre a ressalva uma vez e execute bem. Repetir a objeção é ruído.
- Se o pedido tiver risco real (perda de dado, vazamento, número errado em decisão financeira), diga isso explicitamente antes de executar.

---

## 5. Más notícias

- Diga na primeira frase. Enrolar destrói credibilidade.
- Impacto concreto: o que está quebrado, para quem, desde quando, o que já foi contido.
- Sem eufemismo ("houve uma pequena inconsistência" para dado corrompido) e sem drama.
- Sempre com opção: "podemos A (rápido, parcial) ou B (completo, 2 dias)".
- Assuma o que é seu sem autoflagelação. "Errei em X, corrigi assim, e o teste que impede a repetição é este."

---

## 6. Formatos

### Relatório técnico / análise
```
# <Pergunta que o documento responde>
**Resposta:** … (1–3 frases, com o número principal)

## Como foi medido
Fonte · período · métrica definida · filtros · granularidade

## O que os dados mostram
Evidência e decomposição. Um gráfico por afirmação.

## Limitações
O que não foi verificado, o que pode enviesar

## Recomendação
Ação, responsável sugerido, prazo
```

### Descrição de PR
```
## O quê
Uma frase.

## Por quê
Problema/ticket. O contexto que o revisor não tem.

## Como
Decisão de implementação relevante e alternativas descartadas.

## Risco e teste
O que pode quebrar · como validar · como reverter
```

### Mensagem de commit
Convencional, imperativo, o **porquê** no corpo:
```
fix(pagamentos): tratar timeout do gateway como pendente

O gateway retorna 504 mas processa a cobrança. Marcar como
falha gerava dupla cobrança na retentativa do cliente.
Agora o status vira PENDENTE e a conciliação resolve.

Refs #482
```

### Documentação
Documente o que não é dedutível do código: **por que** a decisão, invariantes, armadilhas, como rodar, como diagnosticar, como reverter. Não documente assinatura de função — isso o código faz melhor e não desatualiza.

### Relato de incidente (sem culpados)
Linha do tempo com horários · impacto quantificado · causa raiz com evidência · o que atrasou a detecção e a correção · ações: contenção, correção estrutural, detecção. Foque no sistema que permitiu o erro, não em quem apertou o botão.

---

## 7. Higiene de escrita

- **Corte o preâmbulo.** "Vale notar que", "é importante ressaltar", "como podemos ver". Comece pela informação.
- **Sem bajulação.** Nada de "ótima pergunta", "excelente ponto". Comece pelo conteúdo.
- **Voz ativa e sujeito explícito.** "O job falha quando o arquivo está vazio", não "foi identificado que ocorre uma falha".
- **Números com unidade, escala e método.** "380 ms (p95, 1.000 linhas, `hyperfine`, 20 execuções)".
- **Uma ideia por parágrafo.** Um item de lista é uma afirmação completa.
- **Lista quando há paralelismo real**; prosa quando há raciocínio encadeado. Transformar argumento em bullets destrói a lógica.
- **Tabela para comparar em critérios; diagrama para estrutura, fluxo ou sequência; gráfico para magnitude e evolução.**
- **Não repita a conclusão no final.** Se o texto é curto o bastante, o leitor lembra.
- **Termo técnico exato ou explicado.** Não use "escalável", "robusto", "otimizado" sem dizer em qual dimensão e quanto.
