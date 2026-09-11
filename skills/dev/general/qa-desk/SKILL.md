---
id: 52
name: qa-desk
description: "Desk do perfil qa — Trabalhando como QA / engenheiro(a) de qualidade. Desk enxuta — sem skills próprias de QA ainda. Ativa em cascata o toolkit do perfil (review-changes, detect-patterns, drytify, council). Use quando começar a trabalhar como qa."
---

# Desk — qa

Trabalhando como QA / engenheiro(a) de qualidade. Desk enxuta — sem skills próprias de QA ainda.

Esta skill é um **agregador de perfil**: não faz o trabalho, entrega o toolkit.

## Toolkit do perfil

- `review-changes`
- `detect-patterns`
- `drytify`
- `council`

## Uso (host NOOA)

1. Ative a desk: `self.skills.activate(["*.qa-desk"])`.
2. Equipe o toolkit uma vez: `self.qa_desk.equip()` — ativa em cascata as
   skills acima. Cada uma vira `self.<nome>`; puxe o guia com `doc(self.<nome>)`.
3. `self.qa_desk.roster()` lista os ids; `status()` mostra o que já está ativo.

Sem host NOOA, o `SKILL.md` de cada skill do toolkit funciona sozinho.

## Camada NOOA (opcional)

Pacote `nio_skill_qa_desk/` — ver `docs/nooa-integration.md`. Nunca executado pelo
repo nem pela CLI; roda só num host NOOA com sandbox de SO.
