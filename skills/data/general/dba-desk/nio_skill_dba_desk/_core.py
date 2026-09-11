"""Lógica pura da desk dba — sem dependência do NOOA, testável isolada."""

from __future__ import annotations

PROFILE = "dba"
HEADLINE = "Trabalhando como DBA / engenheiro(a) de dados. Desk enxuta — sem skills próprias de DBA ainda."

ROSTER: tuple[str, ...] = (
    "data-standards",
    "review-sql",
    "council",
)

# ponytail: cascade_patterns/run_cascade/status_text/equipped_report são glue
# idêntico nas 7 desks. Vendored de propósito — um pacote compartilhado custaria
# um dep git que teria que resolver depois do provisionamento. Mantenha em sync.


def cascade_patterns() -> list[str]:
    """Um glob por skill do roster — casa `cmd.<id>` e `nio.<id>` (se houver camada)."""
    return [f"*.{sid}" for sid in ROSTER]


def run_cascade(agent) -> list[str]:
    """Ativa o roster no SkillRegistry do host (best-effort). Devolve o que pediu."""
    registry = getattr(agent, "skills", None)
    if registry is None or not hasattr(registry, "activate"):
        return []
    try:
        registry.activate(cascade_patterns())
    except Exception:
        return []
    return list(ROSTER)


def equipped_report(activated: list[str]) -> str:
    if not activated:
        return f"[{PROFILE}] nada equipado — host sem SkillRegistry."
    return (
        f"[{PROFILE}] equipado: {', '.join(activated)}. "
        f"Puxe o guia de cada um com doc(self.<nome>)."
    )


def status_text(agent) -> str:
    registry = getattr(agent, "skills", None)
    active = set(registry.activated()) if registry and hasattr(registry, "activated") else set()
    lines = [f"Desk {PROFILE} — {HEADLINE}", "Toolkit:"]
    for sid in ROSTER:
        mark = "x" if (f"cmd.{sid}" in active or f"nio.{sid}" in active) else " "
        lines.append(f"  [{mark}] {sid}")
    lines.append(f"Equipar tudo: self.{PROFILE}_desk.equip()")
    return "\n".join(lines)
