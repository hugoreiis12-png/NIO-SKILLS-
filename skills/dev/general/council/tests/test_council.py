"""Testes da lógica pura do council. Rodam sem NOOA (Python >= 3.12).

O wrapper CouncilSkill (que importa nooa) é exercitado no CI nooa-layer-check.
"""

import pytest

from nio_skill_council import _core

LENS_NAMES = {
    "O Contrário",
    "Primeiros Princípios",
    "O Expansionista",
    "O Forasteiro",
    "O Executor",
}


def test_cinco_lentes():
    assert len(_core.LENSES) == 5
    assert _core.LENSES[0].name == "O Contrário"
    assert {lens.name for lens in _core.LENSES} == LENS_NAMES


def test_forasteiro_nao_recebe_contexto():
    prompts = _core.build_prompts("Migrar para Postgres", context="temos 40M linhas hoje")
    assert "40M linhas" not in prompts["O Forasteiro"]
    assert "40M linhas" in prompts["O Contrário"]


def test_prompts_sao_anti_diplomaticos():
    for prompt in _core.build_prompts("X").values():
        assert "diplomacia" in prompt.lower()


def test_decision_vazia_e_erro():
    with pytest.raises(ValueError):
        _core.build_prompts("   ")


def test_validate_verdict_incompleto():
    missing = _core.validate_verdict("⚖️ VEREDITO: sim")
    assert "POR QUÊ" in missing
    assert "▶️ PRÓXIMO PASSO" in missing


def test_validate_verdict_placeholder_conta_como_vazio():
    assert _core.validate_verdict(_core.VERDICT_FORMAT) == list(_core.VERDICT_SECTIONS)


def test_validate_verdict_ok():
    good = (
        "⚖️ VEREDITO: sim\n"
        "POR QUÊ: a, b, c\n"
        "⚠️ O QUE PODE MATAR: o risco x\n"
        "▶️ PRÓXIMO PASSO: fazer y amanhã"
    )
    assert _core.validate_verdict(good) == []
