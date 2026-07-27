# Regras — Python para dados

Valem para scripts, notebooks e pipelines Python no setor de dados.

## Estilo e estrutura
- Siga PEP 8. Use `ruff` ou `black` para formatação automática.
- Funções com uma responsabilidade. Se o nome precisar de "e" (ex: `limpa_e_agrega`), divida.
- Nomes em inglês para código (variáveis, funções, classes). Comentários e docstrings em pt-BR.
- Type hints em funções que saem de notebooks para módulos reutilizáveis.

## Pandas e Polars
- Prefira operações vetorizadas a loops Python sobre DataFrame.
- `.apply()` com função Python pura é loop disfarçado — use operações nativas ou `np.vectorize` se necessário.
- Nunca modifique um DataFrame in-place sem necessidade (`inplace=True` oculta bugs).
- Encadeie operações com method chaining, mas quebre em CTE se ficar ilegível.
- `groupby` + `agg` é mais rápido e claro que `apply` para agregações padrão.
- Para datasets > 1GB, considere Polars (lazy evaluation) ou leitura por chunks.

## Notebooks
- Células de notebook têm no máximo 20 linhas de código executável.
- Funções com mais de 10 linhas vão para um módulo `.py` importado no notebook.
- Toda célula de output que gera um gráfico tem título, labels de eixo e unidades.
- Primeira célula: imports. Segunda célula: constantes e configuração. Lógica depois.
- Reiniciar o kernel e executar do zero deve funcionar — sem dependência de estado de execução.

## Qualidade e testes
- Scripts de pipeline têm testes de smoke (o script roda sem erro com dados de exemplo).
- Funções de transformação têm pelo menos um teste com casos-limite (vazio, nulo, valor extremo).
- Logging em vez de `print` para código que vai para produção. Nível INFO para progresso, WARNING para anomalias, ERROR para falhas.

## Reprodutibilidade
- Seed no início de qualquer script com aleatoriedade: `np.random.seed(42)`, `random.seed(42)`.
- Dependências em `requirements.txt` ou `pyproject.toml` com versões fixadas.
- Variáveis de ambiente para credenciais — nunca hardcoded.
