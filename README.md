# HAMARTIA: Greek for missing the mark, the tragic error

Formerly `trap-bank`.

A small bank of common maths mistakes, each with the exact wrong answer that mistake produces.

## What it solves
When you write a multiple-choice question, a quiz or a worked-example "spot the error" task, the wrong options should be the answers real mistakes give, not random numbers. Each trap here knows the correct answer and the answer its mistake gives, for any numbers you choose. It can also tell a student's answer apart: correct, this exact trap, or something else. Pure Python 3.10+, standard library only, exact `Fraction` arithmetic. The traps are written in our own words; there is no copied exam or textbook material.

## Example
```bash
python -m trapbank list
python -m trapbank show add-fractions-across a=1 b=2 c=1 d=3
```
```
Mistake: the student adds the tops and adds the bottoms
Rule:    a/b + c/d = (ad + bc)/(bd)
Correct: 5/6
Trap:    2/5
```
In Python:
```python
from trapbank import diagnose
diagnose("add-fractions-across", dict(a=1, b=2, c=1, d=3), "2/5")   # 'trap'
```

## The maths behind it
Seven traps are included: adding fractions across, squaring a difference or a sum without the middle term, a minus sign before a bracket, a power of a power, a percentage added then taken off, and a mean of two group means. For 1/2 + 1/3 the correct sum is (1x3 + 2x1)/(2x3) = 5/6, while the trap gives (1 + 1)/(2 + 3) = 2/5. For (a - b)^2 the correct value is a^2 - 2ab + b^2 and the trap gives a^2 - b^2; they agree only when b = 0 or a = b (the two differ by 2b(a - b) in size), so numbers such as a = 4, b = 0 or a = 3, b = 3 are refused because they cannot separate the two. Increasing by p percent and then decreasing by p percent gives v(1 + p/100)(1 - p/100) = v(1 - p^2/10000), never v. Everything is computed with exact fractions, so a "trap" match is an exact match.

## Install and run
```bash
python -m pip install -e .
python -m trapbank list
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
