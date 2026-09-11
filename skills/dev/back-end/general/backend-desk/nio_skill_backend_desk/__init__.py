"""Camada NOOA da desk backend-desk (opcional). Ver ../SKILL.md e docs/nooa-integration.md."""

__all__ = ["BackendDeskSkill"]


def __getattr__(name: str):
    # Lazy: só importa o wrapper (e o nooa) quando alguém pede BackendDeskSkill.
    # Mantém `nio_skill_backend_desk._core` importável sem o nooa (testes puros).
    if name == "BackendDeskSkill":
        from .skill import BackendDeskSkill

        return BackendDeskSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
