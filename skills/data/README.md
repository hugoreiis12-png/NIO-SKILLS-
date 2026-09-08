# Skills · data

Skills do setor de dados. **Todas flat sob `data/general/`** — a NIO-CLI só
provisiona `skills/<role>/general/**` para roles não-dev (o wizard só pergunta
área/stack para o role `dev`). Ver [`docs/nio-cli-alignment.md`](../../docs/nio-cli-alignment.md) §Gap A / §C1.

O público-alvo fica no campo `persona:` do frontmatter (`analyst | scientist | bi`)
— é **documentação**, a CLI não filtra por ele.

## Índice

| Skill | persona | O quê |
|-------|---------|-------|
| [data-standards](general/data-standards/SKILL.md) | — | O harness de dados: SQL, Python, ML, BI. As demais skills assumem estas regras. |
| [explore-dataset](general/explore-dataset/SKILL.md) | analyst | Mapear um dataset desconhecido. |
| [data-quality](general/data-quality/SKILL.md) | analyst | Completude, unicidade, consistência, validade. |
| [review-sql](general/review-sql/SKILL.md) | analyst | Revisar query SQL (base: seção SQL de `data-standards`). |
| [to-analysis](general/to-analysis/SKILL.md) | analyst | Plano de análise a partir de uma pergunta de negócio. |
| [model-card](general/model-card/SKILL.md) | scientist | Documentar um modelo de ML. |
| [experiment-design](general/experiment-design/SKILL.md) | scientist | Experimento controlado / A/B. |
| [review-notebook](general/review-notebook/SKILL.md) | scientist | Revisar notebook Jupyter. |
| [feature-check](general/feature-check/SKILL.md) | scientist | Avaliar features / sugerir engenharia. |
| [dashboard-spec](general/dashboard-spec/SKILL.md) | bi | Especificar um dashboard. |
| [kpi-framework](general/kpi-framework/SKILL.md) | bi | Framework de KPIs. |
| [report-spec](general/report-spec/SKILL.md) | bi | Especificar um relatório analítico. |
| [data-storytelling](general/data-storytelling/SKILL.md) | bi | Insights → narrativa acionável. |

## Agentes de dados

Ficam em [`agents/data/`](../../agents/data/): `data-explorer`, `sql-reviewer`.
