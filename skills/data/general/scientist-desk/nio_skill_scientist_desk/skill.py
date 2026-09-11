"""ScientistDeskSkill — a camada NOOA da desk scientist-desk.

Agregador de perfil: ativa em cascata o toolkit e não faz o trabalho.
Delega a lógica a `_core` (pura). Ver ../SKILL.md e docs/nooa-integration.md.
"""

from __future__ import annotations

from nooa import Skill

from . import _core


class ScientistDeskSkill(Skill):
    """Desk scientist — Trabalhando como cientista de dados.

    Agregador de perfil. Fluxo:

    1. `self.scientist_desk.equip()` uma vez — ativa em cascata o toolkit do perfil
       (data-standards, model-card, experiment-design, review-notebook, feature-check, council). Cada skill vira `self.<nome>`; puxe o guia com
       `doc(self.<nome>)`.
    2. `self.scientist_desk.roster()` — os ids do toolkit.
    3. `self.scientist_desk.status()` — o que já está ativo.

    Não faz o trabalho do perfil — entrega as skills que fazem.
    """

    context_block = ("scientist_desk", "self.scientist_desk.status()")

    def equip(self) -> str:
        """Ativa em cascata todas as skills deste perfil. Chame uma vez ao começar."""
        return _core.equipped_report(_core.run_cascade(self._agent))

    def roster(self) -> tuple[str, ...]:
        """Os ids das skills deste perfil."""
        return _core.ROSTER

    def status(self) -> str:
        """Render do context block: o toolkit do perfil e o que já está ativo."""
        return _core.status_text(self._agent)
