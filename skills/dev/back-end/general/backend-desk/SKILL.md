---
id: 50
name: backend-desk
description: "Desk do perfil backend — Trabalhando como engenheiro(a) de back-end. Ativa em cascata o toolkit do perfil (to-doc, to-tickets, review-changes, drytify, detect-patterns, council). Use quando começar a trabalhar como backend."
---

# Desk — backend

Trabalhando como engenheiro(a) de back-end.

Esta skill é um **agregador de perfil**: não faz o trabalho, entrega o toolkit.

## Toolkit do perfil

- `to-doc`
- `to-tickets`
- `review-changes`
- `drytify`
- `detect-patterns`
- `council`

## Uso (host NOOA)

1. Ative a desk: `self.skills.activate(["*.backend-desk"])`.
2. Equipe o toolkit uma vez: `self.backend_desk.equip()` — ativa em cascata as
   skills acima. Cada uma vira `self.<nome>`; puxe o guia com `doc(self.<nome>)`.
3. `self.backend_desk.roster()` lista os ids; `status()` mostra o que já está ativo.

Sem host NOOA, o `SKILL.md` de cada skill do toolkit funciona sozinho.

## Camada NOOA (opcional)

Pacote `nio_skill_backend_desk/` — ver `docs/nooa-integration.md`. Nunca executado pelo
repo nem pela CLI; roda só num host NOOA com sandbox de SO.
