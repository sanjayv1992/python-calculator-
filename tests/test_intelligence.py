import random

from agromanch_ai.intelligence import competitor_inspiration, select_angles
from agromanch_ai.intelligence.angle_generator import AngleSelection
from agromanch_ai.utils.angles import ANGLES


def test_select_returns_two_distinct_listed_angles():
    sel = select_angles(random.Random(1))
    assert sel.primary in ANGLES and sel.secondary in ANGLES
    assert sel.primary != sel.secondary


def test_seeded_selection_is_deterministic():
    assert select_angles(random.Random(7)) == select_angles(random.Random(7))


def test_avoid_excludes_recent_primary():
    recent = ANGLES[0]
    for seed in range(30):
        assert select_angles(random.Random(seed), avoid=recent).primary != recent


def test_competitor_block_borrows_structure_never_copies():
    block = competitor_inspiration(AngleSelection("Myth vs Fact", "Save Money"))
    assert "STRUCTURE only" in block
    assert "never copy" in block.lower()
    assert "Primary format" in block and "Secondary format" in block
