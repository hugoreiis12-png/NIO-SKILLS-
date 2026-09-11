"""FrontendDeskSkill — a camada NOOA da desk frontend-desk.

Agregador de perfil: ativa em cascata o toolkit e não faz o trabalho.
Delega a lógica a `_core` (pura). Ver ../SKILL.md e docs/nooa-integration.md.
"""

from __future__ import annotations

from nooa import Skill

from . import _core


class FrontendDeskSkill(Skill):
    """Desk frontend — Trabalhando como engenheiro(a) de front-end.

    Agregador de perfil. Fluxo:

    1. `self.frontend_desk.equip()` uma vez — ativa em cascata o toolkit do perfil
       (emil-design-eng, animation-vocabulary, review-animations, review-changes, drytify, council). Cada skill vira `self.<nome>`; puxe o guia com
       `doc(self.<nome>)`.
    2. `self.frontend_desk.roster()` — os ids do toolkit.
    3. `self.frontend_desk.status()` — o que já está ativo.

    Não faz o trabalho do perfil — entrega as skills que fazem.
    """

    context_block = ("frontend_desk", "self.frontend_desk.status()")

    def equip(self) -> str:
        """Ativa em cascata todas as skills deste perfil. Chame uma vez ao começar."""
        return _core.equipped_report(_core.run_cascade(self._agent))

    def roster(self) -> tuple[str, ...]:
        """Os ids das skills deste perfil."""
        return _core.ROSTER

    def status(self) -> str:
        """Render do context block: o toolkit do perfil e o que já está ativo."""
        return _core.status_text(self._agent)
