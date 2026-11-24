"""A small bank of common maths mistakes.

Each trap knows the correct answer and the exact wrong answer that the mistake
produces, for any numbers you give it. All arithmetic uses Fraction.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from typing import Callable


@dataclass(frozen=True)
class Trap:
    id: str
    topic: str
    mistake: str  # what the student does
    rule: str  # the correct rule
    inputs: tuple[str, ...]  # names of the numbers it needs
    correct: Callable[..., F]
    wrong: Callable[..., F]


def _t(*a) -> Trap:
    return Trap(*a)


TRAPS: tuple[Trap, ...] = (
    _t("add-fractions-across", "fractions",
       "adds the tops and adds the bottoms",
       "a/b + c/d = (ad + bc)/(bd)",
       ("a", "b", "c", "d"),
       lambda a, b, c, d: F(a, b) + F(c, d),
       lambda a, b, c, d: F(a + c, b + d)),
    _t("square-of-difference", "algebra",
       "squares each term and drops the middle term",
       "(a - b)^2 = a^2 - 2ab + b^2",
       ("a", "b"),
       lambda a, b: F(a - b) ** 2,
       lambda a, b: F(a) ** 2 - F(b) ** 2),
    _t("square-of-sum", "algebra",
       "squares each term and drops the middle term",
       "(a + b)^2 = a^2 + 2ab + b^2",
       ("a", "b"),
       lambda a, b: F(a + b) ** 2,
       lambda a, b: F(a) ** 2 + F(b) ** 2),
    _t("minus-bracket", "algebra",
       "changes only the first sign inside a bracket that follows a minus",
       "a - (b - c) = a - b + c",
       ("a", "b", "c"),
       lambda a, b, c: F(a) - (F(b) - F(c)),
       lambda a, b, c: F(a) - F(b) - F(c)),
    _t("power-of-power", "indices",
       "adds the powers when a power is raised to a power",
       "(x^m)^n = x^(mn)",
       ("x", "m", "n"),
       lambda x, m, n: F(x) ** (m * n),
       lambda x, m, n: F(x) ** (m + n)),
    _t("percent-up-then-down", "percentages",
       "takes off the same percentage after adding it and expects the start value",
       "v(1 + p/100)(1 - p/100) = v(1 - p^2/10000)",
       ("v", "p"),
       lambda v, p: F(v) * (1 + F(p, 100)) * (1 - F(p, 100)),
       lambda v, p: F(v)),
    _t("average-of-averages", "statistics",
       "averages two group means without weighting by group size",
       "combined mean = (n1 m1 + n2 m2)/(n1 + n2)",
       ("n1", "m1", "n2", "m2"),
       lambda n1, m1, n2, m2: (F(n1) * m1 + F(n2) * m2) / (n1 + n2),
       lambda n1, m1, n2, m2: (F(m1) + F(m2)) / 2),
)

_BY_ID = {t.id: t for t in TRAPS}


def get(trap_id: str) -> Trap:
    try:
        return _BY_ID[trap_id]
    except KeyError:
        raise KeyError(f"no trap called {trap_id!r}; known: {', '.join(_BY_ID)}") from None


def search(topic: str) -> list[Trap]:
    return [t for t in TRAPS if t.topic == topic]


def _inputs(trap: Trap, values: dict) -> list:
    missing = [n for n in trap.inputs if n not in values]
    if missing:
        raise ValueError(f"{trap.id} needs {', '.join(trap.inputs)}; missing {', '.join(missing)}")
    return [values[n] for n in trap.inputs]


def diagnose(trap_id: str, values: dict, answer) -> str:
    """'correct', 'trap' (matches this mistake exactly) or 'other'."""
    t = get(trap_id)
    args = _inputs(t, values)
    ans = F(answer)
    if ans == t.correct(*args):
        return "correct"
    if ans == t.wrong(*args):
        return "trap"
    return "other"


def distractors(trap_id: str, values: dict) -> tuple[F, F]:
    """(correct answer, the trap's wrong answer). Raises if the numbers do not separate them."""
    t = get(trap_id)
    args = _inputs(t, values)
    c, w = t.correct(*args), t.wrong(*args)
    if c == w:
        raise ValueError("these numbers give the same answer both ways; pick numbers that separate them")
    return c, w
