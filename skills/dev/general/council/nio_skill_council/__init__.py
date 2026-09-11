"""Camada NOOA da skill `council` (opcional). Ver ../SKILL.md e docs/nooa-integration.md."""

__all__ = ["CouncilSkill"]


def __getattr__(name: str):
    # Lazy: só importa o wrapper (e, com ele, o nooa) quando alguém pede
    # CouncilSkill. Mantém `nio_skill_council._core` importável sem o nooa
    # (os testes puros rodam em qualquer Python >= 3.12).
    if name == "CouncilSkill":
        from .skill import CouncilSkill

        return CouncilSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
