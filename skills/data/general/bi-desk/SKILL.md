---
id: 47
name: bi-desk
description: "Desk do perfil bi — Trabalhando como analista de BI. Ativa em cascata o toolkit do perfil (data-standards, dashboard-spec, kpi-framework, report-spec, data-storytelling, council). Use quando começar a trabalhar como bi."
---

# Desk — bi

Trabalhando como analista de BI.

Esta skill é um **agregador de perfil**: não faz o trabalho, entrega o toolkit.

## Toolkit do perfil

- `data-standards`
- `dashboard-spec`
- `kpi-framework`
- `report-spec`
- `data-storytelling`
- `council`

## Uso (host NOOA)

1. Ative a desk: `self.skills.activate(["*.bi-desk"])`.
2. Equipe o toolkit uma vez: `self.bi_desk.equip()` — ativa em cascata as
   skills acima. Cada uma vira `self.<nome>`; puxe o guia com `doc(self.<nome>)`.
3. `self.bi_desk.roster()` lista os ids; `status()` mostra o que já está ativo.

Sem host NOOA, o `SKILL.md` de cada skill do toolkit funciona sozinho.

## Camada NOOA (opcional)

Pacote `nio_skill_bi_desk/` — ver `docs/nooa-integration.md`. Nunca executado pelo
repo nem pela CLI; roda só num host NOOA com sandbox de SO.
