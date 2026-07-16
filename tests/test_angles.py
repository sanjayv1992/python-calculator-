import random

from agromanch_ai.utils.angles import ANGLES, angle_directive, select_angle


def test_select_returns_listed_angle():
    assert select_angle() in ANGLES


def test_seeded_selection_is_deterministic():
    a = select_angle(random.Random(42))
    b = select_angle(random.Random(42))
    assert a == b


def test_avoid_excludes_recent():
    recent = ANGLES[0]
    for _ in range(50):
        assert select_angle(avoid=recent) != recent


def test_angle_directive_mentions_angle():
    d = angle_directive("Myth vs Fact")
    assert "Myth vs Fact" in d
    assert "fresh" in d.lower()
