---
id: 48
name: dba-desk
description: "Desk do perfil dba — Trabalhando como DBA / engenheiro(a) de dados. Desk enxuta — sem skills próprias de DBA ainda. Ativa em cascata o toolkit do perfil (data-standards, review-sql, council). Use quando começar a trabalhar como dba."
---

# Desk — dba

Trabalhando como DBA / engenheiro(a) de dados. Desk enxuta — sem skills próprias de DBA ainda.

Esta skill é um **agregador de perfil**: não faz o trabalho, entrega o toolkit.

## Toolkit do perfil

- `data-standards`
- `review-sql`
- `council`

## Uso (host NOOA)

1. Ative a desk: `self.skills.activate(["*.dba-desk"])`.
2. Equipe o toolkit uma vez: `self.dba_desk.equip()` — ativa em cascata as
   skills acima. Cada uma vira `self.<nome>`; puxe o guia com `doc(self.<nome>)`.
3. `self.dba_desk.roster()` lista os ids; `status()` mostra o que já está ativo.

Sem host NOOA, o `SKILL.md` de cada skill do toolkit funciona sozinho.

## Camada NOOA (opcional)

Pacote `nio_skill_dba_desk/` — ver `docs/nooa-integration.md`. Nunca executado pelo
repo nem pela CLI; roda só num host NOOA com sandbox de SO.
