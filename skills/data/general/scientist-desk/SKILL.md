---
id: 49
name: scientist-desk
description: "Desk do perfil scientist — Trabalhando como cientista de dados. Ativa em cascata o toolkit do perfil (data-standards, model-card, experiment-design, review-notebook, feature-check, council). Use quando começar a trabalhar como scientist."
---

# Desk — scientist

Trabalhando como cientista de dados.

Esta skill é um **agregador de perfil**: não faz o trabalho, entrega o toolkit.

## Toolkit do perfil

- `data-standards`
- `model-card`
- `experiment-design`
- `review-notebook`
- `feature-check`
- `council`

## Uso (host NOOA)

1. Ative a desk: `self.skills.activate(["*.scientist-desk"])`.
2. Equipe o toolkit uma vez: `self.scientist_desk.equip()` — ativa em cascata as
   skills acima. Cada uma vira `self.<nome>`; puxe o guia com `doc(self.<nome>)`.
3. `self.scientist_desk.roster()` lista os ids; `status()` mostra o que já está ativo.

Sem host NOOA, o `SKILL.md` de cada skill do toolkit funciona sozinho.

## Camada NOOA (opcional)

Pacote `nio_skill_scientist_desk/` — ver `docs/nooa-integration.md`. Nunca executado pelo
repo nem pela CLI; roda só num host NOOA com sandbox de SO.
