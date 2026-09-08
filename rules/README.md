# rules

Rules são **convenções de código versionadas**. A NIO-CLI as concatena pela
seleção (role → área → stack) e grava o resultado no repo do usuário em
**`docs/_rules/nio.md`** (com âncora `@docs/_rules/nio.md` no `AGENTS.md`).

**`rules/core/`** entra em **toda sessão, qualquer perfil** (não depende de role) e
é prepended antes de tudo. **`rules/dev/**`** só entra no role `dev`
(`concatenateRules` é hardcoded em `dev`). Não há `rules/data/`; as convenções de
dados vivem na skill
[`data-standards`](../skills/data/general/data-standards/SKILL.md). Ver
[`docs/core-module.md`](../docs/core-module.md) e
[`docs/nio-cli-alignment.md`](../docs/nio-cli-alignment.md) §Gap B / §C2.

## Cascata (derivada do path, não do `extends:`)

A CLI monta o harness a partir do **caminho**, na ordem:

0. **`core/*.md`** — modo operacional padrão; toda sessão, antes de qualquer regra de código.
1. **`dev/general/general-rules.md`** — raiz; todo código.
2. **`dev/<área>/general/rules.md`** — baseline da área (por área selecionada).
3. **`dev/<área>/<stack>/rules.md`** — o stack escolhido.

O frontmatter (`title`, `description`, `applies-to`, `extends`) é **para humano** —
a CLI só lê o corpo e o campo `skills:`. Mantenha `extends:` correto por higiene:
`../../general/general-rules.md` na baseline de área, `../general/rules.md` no stack.

## Índice

### core/
- [senior-core](core/senior-core.md) — modo operacional padrão de toda sessão; força o carregamento da skill `senior-engineering-core`.

### dev/general/
- [general-rules](dev/general/general-rules.md) — tamanho/forma, DRY/YAGNI, nomes, higiene, erros e testes.

### dev/back-end/
- [general/rules](dev/back-end/general/rules.md) — baseline: verticalização por domínio, service layer, N+1, paginação, transação/idempotência.
- [django/rules](dev/back-end/django/rules.md) — Django/DRF: queryset pela entidade (nunca `qs`), fat services/thin views, paginação default.
- `fastapi/` — reservado (`.gitkeep`).

### dev/front-end/
- [general/rules](dev/front-end/general/rules.md) — baseline: tipos/schemas fora do componente, server-state vs UI-state, a11y, loading/erro/vazio.
- [nextjs/rules](dev/front-end/nextjs/rules.md) — Next.js (App Router / RSC): fronteira server/client, data-fetching no server, cache, params por schema.
- [lovable/rules](dev/front-end/lovable/rules.md) — house-style Lovable/React (Vite): ShadcnUI + Tailwind, TanStack Query/Form + Zod, Axios, Supabase/RLS.

## Skills externas (`skills:`)

Um `rules.md` de área/stack pode apontar uma skill de terceiro (ex.:
`vercel-labs/agent-skills/...`) que **reforça** o padrão. A CLI colhe esses slugs
(`collectRuleSkills`) e **oferece instalar** (`npx skills add`) no fim do `sync` —
mas só se a skill também estiver declarada como **dependency**
(`dependencies/**/<slug>.md` com `skills:`). Sem o arquivo de dependency, o `skills:`
do rule é só documentação.
