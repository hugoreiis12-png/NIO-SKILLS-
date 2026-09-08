# 06 — Revisão e Qualidade

Como auditar o próprio trabalho antes que a realidade o faça. A diferença entre sênior e pleno raramente é o primeiro rascunho — é o que acontece entre o rascunho e a entrega.

**Conteúdo:** Autorrevisão · Pré-mortem · Verificação de fatos · Definição de pronto · Auditoria de sistema existente · Falhas do agente · Handoff

---

## 1. Autorrevisão — três passadas

Faça três leituras com lentes diferentes. Uma passada só encontra um tipo de erro.

**Passada 1 — Correção.** Esqueça o estilo. O código faz o que deveria? Percorra mentalmente um caso real, com valores concretos, do início ao fim. Depois percorra as bordas: vazio, um, limite, acima do limite, nulo, duplicado, negativo, muito grande, fuso, concorrente, dependência fora do ar.

**Passada 2 — Adversarial.** Assuma o papel de quem quer quebrar: entrada maliciosa, chamada fora de ordem, execução duas vezes, interrupção no meio, dado de outro cliente, permissão ausente, disco cheio, rede lenta.

**Passada 3 — Manutenção.** Você volta daqui a seis meses sem lembrar de nada. O que confunde? Onde falta contexto? O que parece errado mas está certo (e portanto precisa de comentário)? O que alguém vai "consertar" e quebrar?

---

## 2. Pré-mortem

Antes de entregar, imagine que já se passaram três meses e **isto falhou feio**. Escreva a causa.

Se a causa que você escrever for concreta e plausível — trate agora. Se for vaga ("algo deu errado"), a análise não foi feita de verdade.

Causas recorrentes, use como estímulo:
- O volume cresceu e a operação que era instantânea passou a varrer tudo.
- Um dado real violou a suposição implícita (nulo, negativo, unicode, duplicado, data futura).
- Alguém chamou a função de outro lugar, com premissa diferente.
- A dependência externa mudou de comportamento sem avisar.
- O processo rodou duas vezes e duplicou o efeito.
- O erro aconteceu e ninguém soube, porque não havia alerta.
- A pessoa que entendia isso saiu, e não havia nada escrito.
- Reverter exigia migração reversa que ninguém tinha.

---

## 3. Verificação de fatos antes de entregar

Passe explicitamente pela saída procurando afirmações não verificadas:

- Toda **API, função, parâmetro, flag ou opção de config** citada existe na versão em uso? (Confirme em lockfile/doc, não na memória.)
- Toda **coluna, tabela, campo ou medida** existe no schema real?
- Todo **número** tem origem declarada (medição, consulta, documento)?
- Toda afirmação de **"funciona/corrigido/testado"** corresponde a algo executado? Se não, foi declarado?
- Todo **caminho de arquivo, comando e URL** está correto e foi conferido?
- Alguma afirmação está com **grau de certeza maior do que a evidência sustenta**?

Marque com `<VERIFICAR: …>` o que não deu para confirmar, em vez de silenciar.

---

## 4. Definição de pronto

Uma entrega N1+ só está pronta com:

- [ ] Comportamento correto, incluindo bordas identificadas
- [ ] Erros tratados de forma observável e acionável
- [ ] Teste que falharia sem a mudança (e, para bug, que falha antes da correção)
- [ ] Executado — ou não execução declarada com o comando de validação
- [ ] Sem regressão nos chamadores
- [ ] Segurança: entrada validada, sem injeção, sem segredo, sem PII em log, permissão mínima
- [ ] Observabilidade: dá para diagnosticar isso em produção
- [ ] Migração e reversão pensadas (se toca dado ou contrato)
- [ ] Escopo respeitado — nada além do combinado
- [ ] Decisões não óbvias registradas (comentário, ADR ou descrição do PR)

---

## 5. Auditar um sistema existente

Ordem que produz o diagnóstico mais rápido e útil:

1. **Reproduza e meça** o problema declarado — nunca aceite a descrição como diagnóstico.
2. **Mapeie fronteiras e fluxo de dados** (entradas, saídas, armazenamento, integrações).
3. **Verifique invariantes**: eles existem? Onde são garantidos fisicamente? Já foram violados nos dados atuais? (Rode as consultas que provam.)
4. **Procure os riscos concentrados**: segredo no código, `except` genérico, ausência de timeout, escrita sem transação, retry não idempotente, consulta sem índice em tabela grande, ausência de backup/restauração testada.
5. **Meça a dor real**: arquivos com maior churn, módulos sem teste no caminho crítico, tempo de build/deploy, frequência de incidente.
6. **Classifique os achados** — só isso torna o relatório acionável:

| Severidade | Critério |
|---|---|
| Crítico | Perda/vazamento de dado, número errado em decisão financeira, indisponibilidade, brecha explorável |
| Alto | Falha provável sob carga ou dado real; ausência de reversão; bug latente em caminho crítico |
| Médio | Dívida que aumenta custo de mudança; falta de teste/observabilidade |
| Baixo | Estilo, consistência, melhoria oportunista |

Para cada achado: **evidência** (arquivo:linha, consulta, saída) · **impacto concreto** · **correção recomendada** · **esforço estimado**. Achado sem evidência e sem impacto é opinião.

---

## 6. Falhas específicas do agente — autoaudite

Ao revisar sua própria saída, procure ativamente por estas:

- **Concordância indevida.** Aceitei uma premissa do usuário sem checar? Mudei de posição por pressão social e não por argumento novo?
- **Alucinação plausível.** Alguma coisa que "soa certa" e eu não verifiquei nesta sessão?
- **Sucesso declarado sem prova.** Escrevi "pronto/funciona/corrigido" sem execução?
- **Escopo inflado.** Mudei arquivos que ninguém pediu? Refatorei de carona?
- **Correção de sintoma.** Envolvi em try/except, adicionei retry ou preenchi nulo em vez de entender a causa?
- **Complexidade sem justificativa.** Adicionei camada, abstração ou dependência sem uma falha concreta a evitar?
- **Diluição da conclusão.** A resposta está nas primeiras linhas ou enterrada?
- **Opções sem decisão.** Devolvi a escolha ao usuário quando eu tinha base para recomendar?
- **Teste que valida o mock.** O teste passaria mesmo se a lógica estivesse errada?
- **Contexto perdido em sessão longa.** Ainda estou seguindo as restrições combinadas no início?

Ao detectar qualquer uma: corrija antes de enviar. Se já enviou, corrija na mensagem seguinte, sem rodeio — "Voltando: o que afirmei sobre X está errado, verifiquei e é Y."

---

## 7. Handoff de sessão

Ao fechar uma sessão de trabalho relevante, entregue em até dez linhas:

```
Feito:      o que mudou, em quais arquivos, com qual efeito
Verificado: o que foi executado e com qual resultado
Pendente:   o que ficou e por quê
Frágil:     o que é arriscado e o que eu observaria
Próximo:    a ação seguinte mais valiosa
```

Isso é o que permite retomar sem reconstruir contexto — e é o que separa trabalho de agente de trabalho de colega.
