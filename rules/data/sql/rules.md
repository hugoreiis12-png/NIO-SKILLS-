# Regras — SQL

Valem para todas as queries SQL produzidas pelo setor de dados.

## Legibilidade
- Keywords em maiúsculo: `SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, `HAVING`.
- Uma cláusula por linha. Vírgulas no início da linha (não no fim) para facilitar diff.
- CTEs com nomes descritivos — não `cte1`, `temp`, `aux`. O nome deve dizer o que a CTE representa.
- Aliases descritivos: `u` para `users` é aceitável; `a` para `allocations` também. `t1`, `x` não.
- Comentários apenas para o porquê — não para o quê (o SQL já diz o quê).

## Corretude
- Toda coluna qualificada com alias da tabela quando há JOIN (previne ambiguidade futura).
- NULLs tratados explicitamente: use `IS NULL` / `IS NOT NULL`, nunca `= NULL`.
- `LEFT JOIN` com filtro na cláusula `WHERE` sobre a tabela da direita vira `INNER JOIN` silenciosamente — use o filtro no `ON`.
- `COUNT(coluna)` ignora NULLs; `COUNT(*)` não. Use conscientemente.
- Funções de janela (window functions) sempre com `ORDER BY` explícito — comportamento sem ele é indefinido.

## Performance
- `SELECT *` proibido em queries de produção ou pipelines.
- Filtros aplicados o mais cedo possível — dentro da CTE ou subquery, não no SELECT final.
- Funções sobre colunas indexadas no `WHERE` impedem uso do índice: evite `YEAR(created_at) = 2024`; prefira `created_at BETWEEN '2024-01-01' AND '2024-12-31'`.
- Subquery correlacionada em SELECT ou WHERE é candidata a N+1 — reescreva com JOIN ou window function.
- `DISTINCT` para corrigir JOIN com multiplicação de linhas é um bug disfarçado — corrija o JOIN.

## Boas práticas
- Toda query de produção é testada contra os casos-limite: dataset vazio, nulos em todas as colunas-chave, período sem dados.
- Hardcoded dates e valores de negócio viram parâmetros ou constantes nomeadas em CTE.
- Queries com mais de 50 linhas ganham um comentário de bloco no topo explicando o objetivo.
- Nunca use `ORDER BY` sem `LIMIT` em query de produção — custo desnecessário.
