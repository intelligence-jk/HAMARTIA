from fractions import Fraction as F

import pytest

from trapbank import TRAPS, diagnose, distractors, get, search
from trapbank.__main__ import main


def test_hand_checked_values():
    assert distractors("add-fractions-across", dict(a=1, b=2, c=1, d=3)) == (F(5, 6), F(2, 5))
    assert distractors("square-of-difference", dict(a=5, b=2)) == (F(9), F(21))
    assert distractors("square-of-sum", dict(a=3, b=4)) == (F(49), F(25))
    assert distractors("minus-bracket", dict(a=10, b=4, c=3)) == (F(9), F(3))
    assert distractors("power-of-power", dict(x=2, m=3, n=2)) == (F(64), F(32))
    assert distractors("percent-up-then-down", dict(v=200, p=10)) == (F(198), F(200))
    assert distractors("average-of-averages", dict(n1=10, m1=60, n2=30, m2=80)) == (F(75), F(70))


def test_correct_matches_expansion_identity():
    # (a-b)^2 = a^2 - 2ab + b^2 over a grid of integers
    t = get("square-of-difference")
    for a in range(-6, 7):
        for b in range(-6, 7):
            assert t.correct(a, b) == a * a - 2 * a * b + b * b


def test_fraction_sum_identity():
    t = get("add-fractions-across")
    for a in range(1, 6):
        for b in range(1, 6):
            for c in range(1, 6):
                for d in range(1, 6):
                    assert t.correct(a, b, c, d) == F(a * d + b * c, b * d)


def test_diagnose():
    v = dict(a=1, b=2, c=1, d=3)
    assert diagnose("add-fractions-across", v, F(5, 6)) == "correct"
    assert diagnose("add-fractions-across", v, "2/5") == "trap"
    assert diagnose("add-fractions-across", v, 1) == "other"


def test_degenerate_numbers_rejected():
    with pytest.raises(ValueError):
        distractors("square-of-difference", dict(a=4, b=0))  # a^2 either way


def test_errors():
    with pytest.raises(KeyError):
        get("nope")
    with pytest.raises(ValueError):
        diagnose("minus-bracket", dict(a=1), 0)


def test_bank_shape():
    ids = [t.id for t in TRAPS]
    assert len(ids) == len(set(ids)) == 7
    assert {t.topic for t in TRAPS} >= {"fractions", "algebra", "indices"}
    assert [t.id for t in search("indices")] == ["power-of-power"]
    assert all(chr(0x2014) not in (t.mistake + t.rule) for t in TRAPS)


def test_cli(capsys):
    assert main(["list"]) == 0
    assert "minus-bracket" in capsys.readouterr().out
    assert main(["show", "minus-bracket", "a=10", "b=4", "c=3"]) == 0
    out = capsys.readouterr().out
    assert "Correct: 9" in out and "Trap:    3" in out
    assert main(["show", "minus-bracket", "a=1"]) == 1
