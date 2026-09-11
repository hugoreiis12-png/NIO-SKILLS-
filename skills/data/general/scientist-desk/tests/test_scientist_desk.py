"""Testes da lógica pura da desk scientist. Rodam sem NOOA (Python >= 3.12).

O wrapper ScientistDeskSkill (que importa nooa) é exercitado no CI nooa-layer-check.
"""

from nio_skill_scientist_desk import _core


def test_roster():
    assert len(_core.ROSTER) >= 2
    assert all(isinstance(s, str) and s for s in _core.ROSTER)
    assert "council" in _core.ROSTER
    assert _core.PROFILE == "scientist"


def test_cascade_patterns():
    assert _core.cascade_patterns() == [f"*.{s}" for s in _core.ROSTER]


def test_run_cascade_sem_registry():
    class Bare:
        pass

    assert _core.run_cascade(Bare()) == []


def test_run_cascade_ok():
    class FakeReg:
        def __init__(self):
            self.calls = []

        def activate(self, pats):
            self.calls.append(list(pats))

        def activated(self):
            return []

    class Agent:
        def __init__(self):
            self.skills = FakeReg()

    agent = Agent()
    assert _core.run_cascade(agent) == list(_core.ROSTER)
    assert agent.skills.calls == [_core.cascade_patterns()]


def test_status_text_lista_o_roster():
    class Agent:
        pass

    txt = _core.status_text(Agent())
    assert "scientist" in txt
    for sid in _core.ROSTER:
        assert sid in txt
