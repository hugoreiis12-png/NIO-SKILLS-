# Skills · dev

Pra escrever, revisar e projetar código. Agrupadas por **stack** — a pasta é organização, não muda a invocação.

## general — agnóstico de stack

- [caveman](general/caveman/SKILL.md) — resposta ultra-comprimida (~75% menos tokens).
- [council](general/council/SKILL.md) — conselho de 5 lentes que mata concordância fácil numa decisão.
- [detect-patterns](general/detect-patterns/SKILL.md) — escreve `docs/_patterns.md` com os padrões reais do repo (roda no init/sync ou sob demanda).
- [drytify](general/drytify/SKILL.md) — acha e remove duplicação real de código (DRY com bom senso).
- [grill-me](general/grill-me/SKILL.md) — te sabatina sobre um plano/design até resolver cada decisão.
- [handoff](general/handoff/SKILL.md) — compacta a conversa num doc de continuidade pra outro agente.
- [init-sdd](general/init-sdd/SKILL.md) — monta a estrutura SDD (`docs/`, templates, `AGENTS.md`) no repo. Templates em [templates/](general/init-sdd/templates/).
- [review-changes](general/review-changes/SKILL.md) — review de qualidade/limpeza do diff (não caça bug).
- [to-doc](general/to-doc/SKILL.md) — cria um doc do SDD (spec/bug/adr) e para. Padrões por tipo: [SPEC](general/to-doc/SPEC-PATTERN.md) · [BUG](general/to-doc/BUG-PATTERN.md) · [ADR](general/to-doc/ADR-PATTERN.md).
- [to-tickets](general/to-tickets/SKILL.md) — fatia spec/plano/conversa em tickets tracer-bullet (DAG); publica local ou NOS + GitHub. Padrões em [TICKET-PATTERNS](general/to-tickets/TICKET-PATTERNS.md).
- [zoom-out](general/zoom-out/SKILL.md) — sobe um nível de abstração e mapeia módulos/callers.

## front-end

- [general/animation-vocabulary](front-end/general/animation-vocabulary/SKILL.md) — glossário reverso: descrição vaga → termo exato de motion.
- [general/emil-design-eng](front-end/general/emil-design-eng/SKILL.md) — filosofia de polish de UI e craft (Emil Kowalski).
- [general/review-animations](front-end/general/review-animations/SKILL.md) — revisa código de animation contra uma régua alta de craft ([STANDARDS](front-end/general/review-animations/STANDARDS.md)).
- `front-end/nextjs/`, `front-end/lovable/` — stacks reservados (`.gitkeep`; puxam os `rules`/`dependencies` do stack).

## back-end

`back-end/{general,django,fastapi}/` — stacks reservados (`.gitkeep`). Skills de
API, dados e infra entram aqui.
