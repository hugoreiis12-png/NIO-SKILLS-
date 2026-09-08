# 03 — Código

Escrever, revisar, refatorar, testar e endurecer código como quem vai mantê-lo por anos.

**Conteúdo:** Design de módulo · Nomes · Erros · Tipos e invariantes · Concorrência · Testes · Refatoração · Performance · Segurança · Cheiros · Revisão · Diretrizes por linguagem

---

## 1. Design de módulo e função

- **Profundidade > superfície.** Interface pequena escondendo bastante trabalho. Uma função com sete parâmetros de configuração está expondo sua implementação.
- **Uma função faz uma coisa em um nível de abstração.** Misturar "calcular imposto" com "abrir conexão" na mesma função é o que torna teste impossível.
- **Separe decisão de efeito.** Núcleo puro (calcula, decide, transforma) + casca fina (I/O, rede, banco, tempo, aleatoriedade). Isso é o que faz o teste ser rápido e determinístico sem mock elaborado.
- **Injete o que é ambiente**: relógio, gerador aleatório, cliente HTTP, caminho de arquivo. Código que chama `now()` internamente é intestável e quebra na virada do ano.
- **Torne o caso comum trivial e o caso raro possível.** Não o contrário.
- **Sem parâmetro booleano de controle de fluxo.** `processar(pedido, true)` não é legível; são duas funções.
- **Retorne cedo.** Guard clauses eliminam aninhamento; aninhamento profundo esconde caso de borda.
- **Imutabilidade por padrão.** Mutação compartilhada é a origem da maior parte dos bugs difíceis.

---

## 2. Nomes

Nome errado custa mais que código errado, porque o código errado é encontrado.

- Nome revela **intenção e unidade**, não tipo: `atrasoMs`, `valorLiquidoBRL`, `pedidosPendentesRevisao`.
- Booleano é afirmação: `estaAtivo`, `temSaldo`, `podeCancelar`. Nunca negativo (`naoInvalido` é tortura).
- Função é verbo; a que retorna sem efeito colateral não tem verbo de ação (`totalDoPedido`, não `calculaEProcessaTotal`).
- Consistência lexical no projeto: um conceito, um nome. `cliente`/`customer`/`usuario` para a mesma coisa é dívida cognitiva permanente.
- Nome longo e claro > nome curto e enigmático. O autocompletar existe.
- Comentário explica **por quê**, nunca **o quê**. Comentário que descreve o código vira mentira no primeiro refactor. Bons comentários: decisão não óbvia, referência a ticket/regra de negócio, armadilha conhecida, invariante.

---

## 3. Erros

- **Distinga erro esperado de bug.** Esperado (entrada inválida, recurso ausente, indisponibilidade externa) faz parte do contrato e vira valor de retorno tipado ou exceção específica. Bug é violação de invariante — deve estourar alto e cedo.
- **Nunca engula.** `except: pass`, `catch {}`, `.fillna(0)` sem justificativa, `?? default` mascarando falha. Se precisa ignorar, comente o porquê e registre.
- **Capture o específico.** `except Exception` genérico no meio do fluxo esconde `KeyboardInterrupt`, erro de digitação e falha de infra na mesma vala.
- **Mensagem de erro acionável**: o que falhou, com qual entrada (sem dado sensível), qual o efeito e o que fazer. `"Erro ao processar"` é ruído.
- **Preserve a causa** (`raise ... from e`, `cause`). Rastreamento perdido é hora de depuração perdida.
- **Falhe rápido na fronteira; recupere apenas onde há decisão a tomar.** Camadas intermediárias que capturam e relançam sem agregar nada só poluem o rastro.
- **Nada de estado meio-atualizado.** Operação que altera várias coisas: transação, ou compensação explícita, ou torne idempotente.

---

## 4. Tipos e invariantes

Mova erro de tempo de execução para tempo de compilação/carga sempre que possível.

- **Torne estados ilegais irrepresentáveis.** Se um pedido cancelado não pode ter data de pagamento, o tipo deveria impedir isso — não uma validação espalhada.
- **Valide na borda, confie no núcleo.** Faça o dado externo virar tipo de domínio uma vez, na entrada (Pydantic, Zod, dataclass validada, tipo nominal). Depois disso, o núcleo não revalida.
- **Tipos nominais para conceitos**: `CPF`, `Email`, `IdCliente` em vez de `str` em toda parte. Isso previne troca de argumentos posicionais, um dos bugs mais silenciosos que existem.
- **Sem valores mágicos** — nem `-1` como "não encontrado", nem `""` como "ausente", nem `0` como "sem dado". Use `Optional`/`Result`/enum.
- **Constraint no banco também é tipo**: `NOT NULL`, `UNIQUE`, `CHECK`, chave estrangeira. Validação só na aplicação não sobrevive a um script ad hoc.

---

## 5. Concorrência

Onde moram os bugs que não reproduzem.

- **Prefira não compartilhar.** Passe mensagem, use fila, isole por partição. Estado compartilhado com lock é a última opção.
- **Toda operação assíncrona precisa de timeout e cancelamento.**
- **Idempotência** em qualquer consumidor de mensagem ou webhook: chave de deduplicação persistida.
- **Ordem não é garantida** em fila distribuída, a menos que você pague por isso. Desenhe para chegar fora de ordem e duplicado.
- **Cuidado com leitura-modificação-escrita**: use `UPDATE ... WHERE versao = ?` (bloqueio otimista) ou operação atômica do banco, não `SELECT` seguido de `UPDATE` na aplicação.
- **Não bloqueie o loop de eventos** (Node, asyncio) com CPU ou I/O síncrono.

---

## 6. Testes

O objetivo é confiança para mudar, não cobertura.

- **Teste comportamento observável pela fronteira do módulo**, não estrutura interna. Teste acoplado à implementação transforma refatoração em reescrita de teste.
- **Pirâmide invertida em cima:** muitos testes de unidade rápidos no núcleo puro · testes de integração nos pontos que realmente integram (banco real em contêiner > mock de banco) · poucos ponta a ponta nos fluxos críticos de dinheiro/acesso.
- **Mock só o que você não controla** (rede, terceiro, relógio). Mockar o próprio banco produz teste que passa e sistema que quebra.
- **Um teste, uma razão para falhar.** Nome do teste descreve o cenário e o esperado: `cancelamento_apos_pagamento_gera_estorno`.
- **Priorize os casos de borda**: vazio, um elemento, limite exato, acima do limite, nulo, duplicado, negativo, unicode, fuso, entrada máxima, concorrente.
- **Teste baseado em propriedade** para lógica com invariante clara (serializar→desserializar é identidade; total nunca negativo; ordenação é permutação). Encontra o que o exemplo escolhido a dedo não encontra.
- **Todo bug corrigido ganha um teste que falha antes da correção.** Sem isso, ele volta.
- **Teste determinístico ou não existe.** Teste instável treina o time a ignorar vermelho — pior que não ter teste.
- **Cobertura é diagnóstico, não meta.** 100% de cobertura com asserção fraca é teatro.

---

## 7. Refatoração

- **Nunca refatore e mude comportamento no mesmo commit.** Um dos dois vai esconder o bug do outro.
- **Rede antes do trapézio**: caracterização de comportamento atual → refatoração → verificação.
- **Passos pequenos e reversíveis**, verde entre cada um.
- **Refatore o que você está tocando** (regra do escoteiro, com moderação) — não o repositório inteiro porque estava lá.
- **Sequência típica de resgate**: extrair função → nomear conceitos → separar I/O de lógica → introduzir tipo → mover para módulo com fronteira → remover duplicação que agora ficou óbvia.
- **Duplicação enganosa é pior que duplicação.** Dois trechos parecidos que mudam por motivos diferentes devem permanecer separados.

---

## 8. Performance

- **Meça primeiro, sempre.** Perfil (profiler), plano de execução, `EXPLAIN ANALYZE`, contador de alocação, tempo com percentis. Intuição sobre gargalo erra a maior parte das vezes.
- **Otimize a ordem de grandeza antes da constante**: algoritmo e acesso a dados antes de micro-otimização.
- **Os gargalos reais, por frequência:** consulta sem índice · N+1 · trabalho em laço que deveria ser em lote · serialização de payload gigante · I/O síncrono em série que poderia ser paralelo · alocação em laço quente · falta de paginação.
- **Meça p95/p99, não média.** Média esconde exatamente o que o usuário reclama.
- **Faça a conta antes de otimizar.** Se o total do processo é 200 ms e a função representa 5 ms, ela não é o problema.
- **Registre o antes/depois com número e método.** Otimização sem medida reportada é alegação.

---

## 9. Segurança no código

- **Nunca concatene entrada em SQL, comando de shell, caminho de arquivo, HTML ou template.** Consulta parametrizada, `subprocess` com lista de argumentos, normalização de caminho, escape de saída.
- **Valide contra lista de permitidos**, não lista de bloqueados.
- **Segredo nunca no código, no log, no erro, no repositório.** Se vazou, rotacione — remover do histórico não basta.
- **Autorize por recurso, não só por rota.** Verifique se *este* usuário pode acessar *este* objeto (IDOR é a falha mais comum em APIs).
- **Desserialização de dado não confiável** (`pickle`, YAML inseguro, `eval`) é execução remota. Nunca.
- **Dependência**: fixe versão, audite (`pip-audit`, `npm audit`, `cargo audit`), evite pacote sem manutenção. Verifique typosquatting em nome de pacote incomum.
- **Log sem PII, token, senha ou cartão.** Mascare na origem, não no destino.
- **Comparação de segredo em tempo constante** (token, HMAC, assinatura de webhook).

---

## 10. Cheiros de código — o que eles indicam de verdade

| Cheiro | Causa provável |
|---|---|
| Função > 50 linhas com vários níveis de aninhamento | Falta separar decisão de efeito |
| Muitos parâmetros | Falta um tipo que agrupe o conceito |
| Flag booleana de comportamento | São duas funções |
| Mesma condição repetida em pontos distantes | Regra de negócio sem casa |
| Teste que precisa de 5 mocks | Módulo acoplado à infraestrutura |
| Comentário explicando *o quê* | Nome ou estrutura ruim |
| Classe de utilidades genérica crescendo | Conceitos de domínio sem nome |
| `if tipo == "x"` espalhado | Falta polimorfismo ou tabela de despacho |
| Try/except gigante em volta de tudo | Não se sabe o que pode falhar |
| Arquivo com muito churn no `git log` | Fronteira errada nesse ponto |

---

## 11. Revisão de código — ordem de importância

1. **Está correto?** Casos de borda, invariantes, concorrência, erro.
2. **É seguro?** Injeção, autorização, segredo, dado sensível.
3. **Quebra algo?** Chamadores, contrato, migração, compatibilidade.
4. **É diagnosticável?** Log, erro com contexto, métrica.
5. **É testado no que importa?** Não a cobertura — o caminho crítico e as bordas.
6. **É legível?** Nomes, tamanho, nível de abstração.
7. **Estilo.** Por último, e de preferência automatizado (formatter/linter), nunca em debate humano.

Ao revisar: separe **bloqueante** de **sugestão**. Aponte o problema *e* o caminho. Elogie o que resolveu bem quando for verdade — feedback só negativo é ignorado com o tempo.

---

## 12. Diretrizes por linguagem (essencial)

**Python** — tipagem em toda função pública + `mypy`/`pyright`; `dataclass`/Pydantic em vez de dicionário solto; `pathlib`; gerenciador de contexto para recurso; `ruff` como linter/formatter; evite mutável em argumento padrão; `logging` estruturado, nunca `print`; `uv`/`poetry` com lockfile.

**SQL** — CTE nomeada em vez de subconsulta aninhada; `JOIN` explícito; nunca `SELECT *` em produção; entenda o plano antes de indexar; cuidado com função sobre coluna indexada (invalida o índice); `NULL` não é igual a nada — `IS NULL`; janelas (`window functions`) em vez de auto-join; sempre `LIMIT` ao explorar.

**TypeScript/JS** — `strict: true`, sem `any` (use `unknown` + narrowing); valide entrada externa com Zod; `Promise.all` para I/O paralelo, com `allSettled` quando falha parcial é aceitável; nunca `await` dentro de laço quando pode ser em lote; erro tipado em vez de `throw` de string.

**Bash** — `set -euo pipefail`; aspas em toda variável; `shellcheck`; acima de ~80 linhas, migre para Python.
