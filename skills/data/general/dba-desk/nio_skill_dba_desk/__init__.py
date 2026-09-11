"""Camada NOOA da desk dba-desk (opcional). Ver ../SKILL.md e docs/nooa-integration.md."""

__all__ = ["DbaDeskSkill"]


def __getattr__(name: str):
    # Lazy: só importa o wrapper (e o nooa) quando alguém pede DbaDeskSkill.
    # Mantém `nio_skill_dba_desk._core` importável sem o nooa (testes puros).
    if name == "DbaDeskSkill":
        from .skill import DbaDeskSkill

        return DbaDeskSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
