# Dependencies

Ferramentas **externas** ao `@nio-cli/cli` que alguns commands precisam em runtime. **Não** vão pra `~/.claude` — o worker instala na máquina; a CLI só as lista no fim do `sync`.

Cada arquivo `.md` sob `dependencies/` **é** uma dependência declarada — a presença no diretório basta. Ficam na **mesma taxonomia das skills** (`dependencies/<role>/<área|general>/<stack|general>/*.md`) e são escopadas pela mesma seleção. A CLI lista as aplicáveis no fim do `sync`/`init`.

**Campos de instalador** (precedência `npm` > `skills` > `git` > `claude-plugin` > `manual`):

| Campo | Formato | Ação |
|---|---|---|
| `npm:` | nome de pacote npm | `npm install -g <pkg>` |
| `skills:` | `owner/repo` ou `owner/repo/skill` | `npx --yes skills add …` |
| `git:` | `https://github.com/…` | clona em `~/.nio/deps/<id>` |
| `claude-plugin:` | `<owner/repo> <plugin@marketplace>` | `claude plugin marketplace add` + `install` |
| `manual:` | bloco `\|` | impresso, nunca executado |
| `detect:` | globs (`~`,`*`,`**`; segue symlink) | se algum existe → "instalada" (selo ✓) |
| `install:` | qualquer | **só exibição, nunca executado** |

## Prioridade local sobre skills.sh

O que declaramos localmente (em `skills/`, `commands/`, `agents/`) **tem prioridade** sobre a mesma skill online — as nossas são *overrides* customizados. Por isso **não** criamos dependency pra skill da skills.sh que já temos local (`caveman`, `handoff`, `grill-me`, `to-tickets`, `implement`, `emil-design-eng`, `review`…). Só puxamos skills da skills.sh que **acrescentam** algo que não temos — tipicamente as que **reforçam as rules**. Ao adicionar uma nova, cheque se já existe um equivalente em `skills/` antes.

## Índice

### Runtime — usadas por commands/skills

- [dev/general/ponytail](dev/general/ponytail.md) — engine de scaffolding (plugin de marketplace, install manual). Usada por [init-sdd](../skills/dev/general/init-sdd/SKILL.md).
- [dev/general/improve](dev/general/improve.md) — validação/refino de spec (instalador de linha única). Usada por [init-sdd](../skills/dev/general/init-sdd/SKILL.md).
- [dev/general/gh](dev/general/gh.md) — CLI do GitHub (install manual + `gh auth login`). Usada por [to-doc](../skills/dev/general/to-doc/SKILL.md) (spec) + [to-tickets](../skills/dev/general/to-tickets/SKILL.md) pra publicar issues.

### Reforço de rules — skills externas (skills.sh)

- [dev/front-end/general/vercel-react-best-practices](dev/front-end/general/vercel-react-best-practices.md) — reforça `rules/dev/front-end/general/rules.md`.
- [dev/front-end/nextjs/vercel-composition-patterns](dev/front-end/nextjs/vercel-composition-patterns.md) — reforça `rules/dev/front-end/nextjs/rules.md`.
- [dev/front-end/lovable/shadcn](dev/front-end/lovable/shadcn.md) — reforça `rules/dev/front-end/lovable/rules.md` (UI).
- [dev/front-end/lovable/supabase-postgres-best-practices](dev/front-end/lovable/supabase-postgres-best-practices.md) — reforça `rules/dev/front-end/lovable/rules.md` (dados/RLS).
- [dev/back-end/general/domain-modeling](dev/back-end/general/domain-modeling.md) — reforça `rules/dev/back-end/general/rules.md`.
