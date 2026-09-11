"""CouncilSkill — a camada NOOA da skill `council`.

Fina: delega toda a lógica a `_core` (pura, testável sem NOOA).
Ver ../SKILL.md e docs/nooa-integration.md.
"""

from __future__ import annotations

from nooa import Skill

from . import _core
from ._core import Lens


class CouncilSkill(Skill):
    """Conselho de decisão de 5 lentes — mata o puxa-saquismo do modelo.

    Use quando houver uma decisão real (mais de um caminho):

    1. `self.council.build_prompts(decisão, contexto)` → 5 prompts prontos, um
       por lente, todos anti-diplomáticos. O Forasteiro NÃO recebe o contexto.
       Lentes: O Contrário · Primeiros Princípios · O Expansionista ·
       O Forasteiro · O Executor.
    2. Spawne 5 subagentes em paralelo, um por prompt.
    3. Revisão entre pares: cruze as 5 saídas, marque o que sobrevive.
    4. O Presidente fecha em `self.council.verdict_format()`.
    5. `self.council.validate_verdict(texto)` → seções faltando (vazia = ok)
       antes de mostrar o veredito ao usuário.
    """

    def lenses(self) -> tuple[Lens, ...]:
        """As 5 lentes (nome, mandato, proibição)."""
        return _core.LENSES

    def build_prompts(self, decision: str, context: str = "") -> dict[str, str]:
        """Um prompt pronto por lente. O Forasteiro recebe só `decision`."""
        return _core.build_prompts(decision, context)

    def verdict_format(self) -> str:
        """O template fixo que o Presidente preenche."""
        return _core.VERDICT_FORMAT

    def validate_verdict(self, text: str) -> list[str]:
        """Seções ausentes/vazias no veredito. Lista vazia = ok."""
        return _core.validate_verdict(text)
