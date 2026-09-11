"""Camada NOOA da desk scientist-desk (opcional). Ver ../SKILL.md e docs/nooa-integration.md."""

__all__ = ["ScientistDeskSkill"]


def __getattr__(name: str):
    # Lazy: só importa o wrapper (e o nooa) quando alguém pede ScientistDeskSkill.
    # Mantém `nio_skill_scientist_desk._core` importável sem o nooa (testes puros).
    if name == "ScientistDeskSkill":
        from .skill import ScientistDeskSkill

        return ScientistDeskSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
