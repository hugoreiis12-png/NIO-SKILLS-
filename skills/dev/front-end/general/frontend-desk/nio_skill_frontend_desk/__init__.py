"""Camada NOOA da desk frontend-desk (opcional). Ver ../SKILL.md e docs/nooa-integration.md."""

__all__ = ["FrontendDeskSkill"]


def __getattr__(name: str):
    # Lazy: só importa o wrapper (e o nooa) quando alguém pede FrontendDeskSkill.
    # Mantém `nio_skill_frontend_desk._core` importável sem o nooa (testes puros).
    if name == "FrontendDeskSkill":
        from .skill import FrontendDeskSkill

        return FrontendDeskSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
