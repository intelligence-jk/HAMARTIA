"""python -m trapbank list | show ID a=1 b=2 ..."""
import sys

from .core import TRAPS, distractors, get


def main(argv=None) -> int:
    a = sys.argv[1:] if argv is None else argv
    if a[:1] == ["list"]:
        for t in TRAPS:
            print(f"{t.id:24s} {t.topic:12s} {t.rule}")
        return 0
    if a[:1] == ["show"] and len(a) >= 2:
        try:
            t = get(a[1])
            vals = {k: int(v) for k, v in (x.split("=") for x in a[2:])}
            c, w = distractors(a[1], vals)
        except (KeyError, ValueError) as e:
            print(f"Cannot show: {e}", file=sys.stderr)
            return 1
        print(f"Mistake: the student {t.mistake}")
        print(f"Rule:    {t.rule}")
        print(f"Correct: {c}")
        print(f"Trap:    {w}")
        return 0
    print("usage: python -m trapbank list | show ID name=value ...", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
