# Skills

Skills são **model-invoked**: o agente ativa sozinho quando o contexto bate com a
`description` do `SKILL.md`.

Taxonomia (a CLI descobre roles/áreas/stacks daqui):
`skills/<role>/<área|general>/<stack|general>/<nome>/SKILL.md`. `general` (do role
e da área) entra sempre em cascata. Id de invocação = **nome da pasta do `SKILL.md`**.

## Roles

- **[core](core/)** — `skills/core/<skill>/SKILL.md` (sem área/stack). Provisionado
  em **toda sessão, qualquer perfil** — não depende de seleção de role. Hoje:
  `senior-engineering-core` (o modo operacional padrão). Ver
  [`docs/core-module.md`](../docs/core-module.md).
- **[dev](dev/README.md)** — engenharia de software. Áreas: `front-end`,
  `back-end`. `general` = agnóstico de stack.
- **[data](data/README.md)** — setor de dados. **Tudo sob `data/general/`** (flat)
  — a CLI só provisiona `skills/<role>/general/**` para roles não-dev. O público
  (analyst/scientist/bi) fica no campo `persona:` do frontmatter, que **não é
  estrutural**.

> A pasta é organização — não muda a invocação. Regra de idioma: skill/command/doc
> em **pt-BR**, código em **inglês**.
