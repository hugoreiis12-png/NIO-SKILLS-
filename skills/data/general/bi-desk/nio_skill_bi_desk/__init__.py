"""Camada NOOA da desk bi-desk (opcional). Ver ../SKILL.md e docs/nooa-integration.md."""

__all__ = ["BiDeskSkill"]


def __getattr__(name: str):
    # Lazy: só importa o wrapper (e o nooa) quando alguém pede BiDeskSkill.
    # Mantém `nio_skill_bi_desk._core` importável sem o nooa (testes puros).
    if name == "BiDeskSkill":
        from .skill import BiDeskSkill

        return BiDeskSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
