"""Camada NOOA da desk analyst-desk (opcional). Ver ../SKILL.md e docs/nooa-integration.md."""

__all__ = ["AnalystDeskSkill"]


def __getattr__(name: str):
    # Lazy: só importa o wrapper (e o nooa) quando alguém pede AnalystDeskSkill.
    # Mantém `nio_skill_analyst_desk._core` importável sem o nooa (testes puros).
    if name == "AnalystDeskSkill":
        from .skill import AnalystDeskSkill

        return AnalystDeskSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
