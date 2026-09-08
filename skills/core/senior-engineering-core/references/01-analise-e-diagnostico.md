# 01 — Análise, Diagnóstico e Decisão

Como transformar um pedido vago ou um sintoma confuso em um problema bem-posto e resolvido.

**Conteúdo:** Enquadramento · Requisitos e invariantes · Diagnóstico diferencial · Técnicas de localização · Causa raiz · Decisão sob incerteza · Estimativa · Leitura de sistema desconhecido

---

## 1. Enquadramento: do pedido ao problema

Pedidos chegam como soluções propostas. O trabalho é recuperar o problema.

> "Coloca um cache no endpoint de relatório." → O problema pode ser: consulta sem índice, N+1, relatório gerado sob demanda quando poderia ser materializado, ou usuário abrindo a tela 40x por dia porque não confia no número. Cache resolve um desses e piora dois.

**Quatro perguntas de enquadramento** (responda antes de agir; pergunte ao usuário o que não conseguir inferir):

1. **Resultado observável.** Como saberemos que acabou? Qual número, comportamento ou artefato muda?
2. **Restrições reais.** Stack fixa, prazo, compatibilidade retroativa, volume, janela de manutenção, quem opera depois.
3. **Fora de escopo.** O que explicitamente não vamos tocar.
4. **Custo do erro.** O que acontece se a solução falhar em produção? Isso define o nível do roteador.

**Sinais de que o pedido está mal-posto** — pare e esclareça:
- Substantivo sem definição operacional ("relatório lento", "melhorar a qualidade dos dados", "deixar mais escalável").
- Duas interpretações com consequências divergentes.
- Solução especificada sem sintoma ("usa Kafka aqui").
- Restrição que contradiz o objetivo (tempo real + processamento em lote noturno).

---

## 2. Requisitos e invariantes

Para qualquer coisa maior que N1, separe explicitamente:

- **Funcional** — o que o sistema faz. Escreva como cenário: *dado … quando … então …*.
- **Não funcional** — números, não adjetivos: latência p95, throughput, volume de dados hoje e em 24 meses, disponibilidade, janela de recuperação (RPO/RTO), retenção, requisito regulatório.
- **Invariantes** — o que precisa ser verdade **sempre**. Esta é a parte que quase todo mundo pula e é a que gera corrupção silenciosa.

> Exemplos de invariante: saldo nunca negativo · toda venda pertence a um cliente existente · um pedido não pode sair de `cancelado` para `pago` · o total do agregado bate com a soma da linha · nenhum registro do fato sem chave na dimensão.

Invariante bem definido vira constraint no banco, tipo no código ou teste de dados — não comentário.

- **Critérios de aceite** — a lista verificável que fecha a tarefa. Se você não consegue escrevê-los, você não entendeu o pedido ainda.

---

## 3. Diagnóstico diferencial

Empreste da medicina: sintoma → hipóteses concorrentes → teste discriminante → causa.

**Protocolo:**

1. **Descreva o sintoma com precisão.** O que exatamente acontece, com quais entradas, em qual ambiente, desde quando, com que frequência, para quem. Vago é 90% do tempo perdido.
2. **Reproduza.** Sem reprodução confiável, você está adivinhando. Se não reproduz, reduza a variação: mesmos dados, mesma versão, mesma configuração, mesmo horário.
3. **Levante 3+ hipóteses.** Force pluralidade — inclua uma que contradiga sua intuição inicial.
4. **Para cada hipótese, defina o teste que a mata.** Priorize testes que eliminam várias hipóteses de uma vez e que são baratos.
5. **Execute e elimine.** Registre o que foi descartado — isso impede refazer o mesmo caminho depois.

**Formato de trabalho:**

| Hipótese | Prediz o quê | Teste discriminante | Resultado |
|---|---|---|---|
| Índice ausente | Plano com seq scan | `EXPLAIN ANALYZE` | ✅ confirmado |
| N+1 no ORM | Centenas de queries curtas | log de queries | ❌ descartado |
| Serialização lenta | CPU alta no app, DB ocioso | métricas do app | ❌ descartado |

**Regra do "mudou o quê?"**: se funcionava e parou, a causa está no delta — deploy, versão de dependência, dado novo, mudança de configuração, expiração de certificado, virada de mês/ano, mudança de fuso, cota atingida. Comece pelo delta antes de teorizar.

---

## 4. Técnicas de localização

- **Bisseção.** Corte o espaço de busca ao meio repetidamente — no tempo (`git bisect`), no dado (metade das linhas), no pipeline (qual estágio), na configuração (desativa metade).
- **Diferencial.** Duas execuções quase idênticas, uma boa e uma ruim. Minimize a diferença até sobrar a causa.
- **Instrumentação antes de leitura.** Em fluxo complexo, um log bem posicionado com valores reais responde em 2 minutos o que 40 minutos de leitura não respondem.
- **Caso mínimo reprodutível.** Reduza até o menor exemplo que ainda falha. O ato de reduzir frequentemente revela a causa.
- **Inversão.** "O que precisaria ser verdade para esse comportamento fazer sentido?" Depois teste isso.
- **Intermitência = concorrência, tempo, ordem, cache ou dado.** Bug que não é determinístico quase sempre é: race condition, dependência de ordem, estado compartilhado, cache stale, timeout, fuso/horário de verão, ou um registro específico no dado.

---

## 5. Causa raiz de verdade

"Cinco porquês" degenera em ficção quando aplicado sem evidência. Use a versão disciplinada:

- **Cada "porquê" precisa de evidência** — log, código, commit, métrica. Sem evidência, é narrativa.
- **A cadeia costuma bifurcar.** Uma falha real tem causa técnica *e* causa de processo (por que não foi detectada antes? por que passou na revisão? por que não tinha teste?).
- **Pare quando chegar a algo acionável e dentro do seu controle**, não em "erro humano" — erro humano é a pergunta, não a resposta.

**Ao concluir um diagnóstico, entregue quatro coisas:**
1. Causa raiz com evidência.
2. Correção imediata (para o sangramento).
3. Correção estrutural (impede a classe inteira do problema).
4. Detecção (teste, alerta ou validação que pega isso na próxima vez).

---

## 6. Decisão sob incerteza

- **Separe o irreversível.** Decisão barata de desfazer: escolha rápido, siga, aprenda. Decisão cara: alternativas, riscos, plano de reversão.
- **Nomeie a informação que falta e o custo de obtê-la.** Se um experimento de 30 minutos elimina a maior incerteza, ele vem antes da decisão.
- **Analise pelo pior caso, não pelo esperado**, quando o pior caso é inaceitável (perda de dado, vazamento, indisponibilidade prolongada).
- **Cuidado com custo afundado.** O trabalho já feito não é argumento para continuar; só o valor futuro conta.
- **Registre a decisão junto com o que a mudaria.** "Escolhemos X; se o volume passar de 50 M linhas/mês, isso deixa de valer." Isso transforma decisão em conhecimento reutilizável.

**Comparação de alternativas — formato:**

| Critério (peso) | Opção A | Opção B |
|---|---|---|
| Correção / risco de dado | | |
| Custo de operação | | |
| Tempo até valor | | |
| Custo de reverter | | |
| Quem consegue manter | | |

Termine sempre com **uma recomendação**, não com a tabela.

---

## 7. Estimativa

- Estime em **faixas**, nunca em ponto único: "2 a 4 dias, sendo o risco a integração com o SAP".
- Decomponha até peças de ≤ 1 dia. O que não decompõe é o que você não entendeu — e é onde o prazo estoura.
- Estime separadamente: implementação, integração, teste, migração de dados, revisão, implantação. Os quatro últimos costumam somar mais que o primeiro.
- Nomeie explicitamente a **maior incerteza** e proponha reduzi-la primeiro (spike com caixa de tempo).
- Não converta pressão em prazo. Reduza escopo, não a estimativa.

---

## 8. Entrar num sistema desconhecido

Ordem que gera entendimento mais rápido:

1. **Como se roda?** README, scripts, `Makefile`, compose, CI. Rodar já revela metade das dependências.
2. **Fronteiras.** O que entra e sai: endpoints, jobs, filas, arquivos, bancos, integrações externas.
3. **Modelo de dados.** Schema, chaves, cardinalidade, constraints. O modelo de dados é a arquitetura real; o código é comentário sobre ele.
4. **Fluxo principal.** Siga *um* caso de uso ponta a ponta, do request ao commit no banco.
5. **Onde mora o risco.** Busque `TODO`, `HACK`, `except`, retry, `sleep`, credencial, código sem teste, arquivo com mais commits (churn alto = dor).
6. **História.** `git log` dos arquivos centrais mostra o que muda junto e por quê.

Só depois disso emita opinião sobre qualidade ou desenho.
