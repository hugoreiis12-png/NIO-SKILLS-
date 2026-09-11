---
id: 51
name: frontend-desk
description: "Desk do perfil frontend — Trabalhando como engenheiro(a) de front-end. Ativa em cascata o toolkit do perfil (emil-design-eng, animation-vocabulary, review-animations, review-changes, drytify, council). Use quando começar a trabalhar como frontend."
---

# Desk — frontend

Trabalhando como engenheiro(a) de front-end.

Esta skill é um **agregador de perfil**: não faz o trabalho, entrega o toolkit.

## Toolkit do perfil

- `emil-design-eng`
- `animation-vocabulary`
- `review-animations`
- `review-changes`
- `drytify`
- `council`

## Uso (host NOOA)

1. Ative a desk: `self.skills.activate(["*.frontend-desk"])`.
2. Equipe o toolkit uma vez: `self.frontend_desk.equip()` — ativa em cascata as
   skills acima. Cada uma vira `self.<nome>`; puxe o guia com `doc(self.<nome>)`.
3. `self.frontend_desk.roster()` lista os ids; `status()` mostra o que já está ativo.

Sem host NOOA, o `SKILL.md` de cada skill do toolkit funciona sozinho.

## Camada NOOA (opcional)

Pacote `nio_skill_frontend_desk/` — ver `docs/nooa-integration.md`. Nunca executado pelo
repo nem pela CLI; roda só num host NOOA com sandbox de SO.
