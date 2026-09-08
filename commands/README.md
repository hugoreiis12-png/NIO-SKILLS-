# Commands

Slash-commands (`/nome`). Hoje todos pertencem ao loop de spec-driven dev e ficam na raiz de `commands/`.

## Índice

| Command | Descrição |
|---------|-----------|
| [`/implement`](implement.md) | Motor único de execução — spec READY, bug ou conjunto de tickets, em worktree isolado; lint/build/testes verdes; **STAGE** (nunca commita). |
| [`/ship`](ship.md) | Commit (Conventional) → push → PR → fecha as issues/tasks entregues (GitHub + NOS). |
| [`/build`](build.md) | Loop autônomo do ticket ao PR: por ticket roda `code-executor` → `code-reviewer` → gate, depois `/ship`. Default `--auto`; `--review` adiciona gate humano. |
