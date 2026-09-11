---
id: 46
name: analyst-desk
description: "Desk do perfil analyst — Trabalhando como analista de dados. Ativa em cascata o toolkit do perfil (data-standards, explore-dataset, data-quality, review-sql, to-analysis, council). Use quando começar a trabalhar como analyst."
---

# Desk — analyst

Trabalhando como analista de dados.

Esta skill é um **agregador de perfil**: não faz o trabalho, entrega o toolkit.

## Toolkit do perfil

- `data-standards`
- `explore-dataset`
- `data-quality`
- `review-sql`
- `to-analysis`
- `council`

## Uso (host NOOA)

1. Ative a desk: `self.skills.activate(["*.analyst-desk"])`.
2. Equipe o toolkit uma vez: `self.analyst_desk.equip()` — ativa em cascata as
   skills acima. Cada uma vira `self.<nome>`; puxe o guia com `doc(self.<nome>)`.
3. `self.analyst_desk.roster()` lista os ids; `status()` mostra o que já está ativo.

Sem host NOOA, o `SKILL.md` de cada skill do toolkit funciona sozinho.

## Camada NOOA (opcional)

Pacote `nio_skill_analyst_desk/` — ver `docs/nooa-integration.md`. Nunca executado pelo
repo nem pela CLI; roda só num host NOOA com sandbox de SO.
