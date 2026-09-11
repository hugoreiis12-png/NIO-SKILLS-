"""Camada NOOA da desk qa-desk (opcional). Ver ../SKILL.md e docs/nooa-integration.md."""

__all__ = ["QaDeskSkill"]


def __getattr__(name: str):
    # Lazy: só importa o wrapper (e o nooa) quando alguém pede QaDeskSkill.
    # Mantém `nio_skill_qa_desk._core` importável sem o nooa (testes puros).
    if name == "QaDeskSkill":
        from .skill import QaDeskSkill

        return QaDeskSkill
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
