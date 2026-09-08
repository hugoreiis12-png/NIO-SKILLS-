# Agents

Subagentes que o worker recebe no `nio sync`. Cada um é um `<nome>.md` com frontmatter + prompt. Organizados por seção — a pasta agrupa pro time achar.

## Seções

- **[dev](dev/README.md)** — subagentes de execução e **exploração** de código (`repo-scout`, `code-executor`, `code-reviewer`).
- **data** — subagentes do setor de dados: `data-explorer` (mapeia datasets e bancos, Haiku) e `sql-reviewer` (revisa queries SQL, Sonnet).
