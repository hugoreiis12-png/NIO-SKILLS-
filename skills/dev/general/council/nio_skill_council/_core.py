"""Lógica pura do council — sem dependência do NOOA, testável isolada."""

from __future__ import annotations

from typing import NamedTuple


class Lens(NamedTuple):
    name: str
    mandate: str
    forbidden: str


LENSES: tuple[Lens, ...] = (
    Lens(
        "O Contrário",
        "Rasgue a ideia. Ache os 3 furos concretos que a matam.",
        "Proibido elogiar ou amortecer.",
    ),
    Lens(
        "Primeiros Princípios",
        "Ignore a pergunta. Reformule o que se tenta resolver de verdade e "
        "diga se esta decisão é a alavanca certa.",
        "Não aceite o enquadramento dado.",
    ),
    Lens(
        "O Expansionista",
        "Cace o ganho 10x que a decisão atual não enxerga.",
        "Não se contente com a melhoria incremental.",
    ),
    Lens(
        "O Forasteiro",
        "Você recebe só a decisão em uma frase, sem contexto. Aponte o óbvio "
        "que quem está dentro parou de notar.",
        "Não peça mais contexto.",
    ),
    Lens(
        "O Executor",
        "Só o que muda amanhã de manhã: o menor passo testável e o custo de errar.",
        "Ignore estratégia de longo prazo.",
    ),
)

#: A única lente que recebe a decisão sem o contexto — de propósito.
NO_CONTEXT_LENS = "O Forasteiro"

VERDICT_SECTIONS: tuple[str, ...] = (
    "⚖️ VEREDITO",
    "POR QUÊ",
    "⚠️ O QUE PODE MATAR",
    "▶️ PRÓXIMO PASSO",
)

VERDICT_FORMAT = (
    "⚖️ VEREDITO: <uma frase>\n"
    "POR QUÊ: <3 pontos que sobreviveram à revisão entre pares>\n"
    "⚠️ O QUE PODE MATAR: <o risco mais letal, do Contrário>\n"
    "▶️ PRÓXIMO PASSO: <uma ação única e testável pra amanhã de manhã>"
)


def build_prompts(decision: str, context: str = "") -> dict[str, str]:
    """Um prompt anti-diplomático por lente. O Forasteiro nunca recebe o contexto."""
    decision = decision.strip()
    if not decision:
        raise ValueError("decision não pode ser vazio")
    context = context.strip()
    out: dict[str, str] = {}
    for lens in LENSES:
        head = f"Decisão: {decision}"
        if context and lens.name != NO_CONTEXT_LENS:
            head += f"\n\nContexto: {context}"
        out[lens.name] = (
            f"{head}\n\n"
            f"Seu papel — {lens.name}: {lens.mandate}\n"
            f"{lens.forbidden} Nada de diplomacia."
        )
    return out


def validate_verdict(text: str) -> list[str]:
    """Seções ausentes ou vazias no veredito do Presidente. Lista vazia = ok."""
    missing: list[str] = []
    for section in VERDICT_SECTIONS:
        idx = text.find(section)
        if idx == -1:
            missing.append(section)
            continue
        rest = text[idx + len(section):].lstrip(": \t")
        lines = rest.splitlines()
        first = lines[0].strip() if lines else ""
        if not first or first.startswith("<"):
            missing.append(section)
    return missing
