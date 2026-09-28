# Review: task 02 Add `--shout` flag to the CLI

- **Card:** 3
- **PR:** https://github.com/en3r0/factory-sandbox/pull/4
- **Review round:** 1
- **Verdict:** PASS

## Acceptance criteria re-run

| # | Criterion | Command or check | Result | Evidence |
| --- | --- | --- | --- | --- |
| 1 | `python3 greet.py` prints `Hello, world!` exit 0 | `python3 greet.py; echo "exit=$?"` | pass | stdout: `Hello, world!` exit: `0` |
| 2 | `python3 greet.py Ada` prints `Hello, Ada!` exit 0 | `python3 greet.py Ada; echo "exit=$?"` | pass | stdout: `Hello, Ada!` exit: `0` |
| 3 | `python3 greet.py --shout` prints `HELLO, WORLD!` exit 0 | `python3 greet.py --shout; echo "exit=$?"` | pass | stdout: `HELLO, WORLD!` exit: `0` |
| 4 | `python3 greet.py Ada --shout` prints `HELLO, ADA!` exit 0 | `python3 greet.py Ada --shout; echo "exit=$?"` | pass | stdout: `HELLO, ADA!` exit: `0` |
| 5 | `python3 greet.py --shout Ada` prints `HELLO, ADA!` exit 0 | `python3 greet.py --shout Ada; echo "exit=$?"` | pass | stdout: `HELLO, ADA!` exit: `0` |
| 6 | `python3 greet.py --help` exit=0, output contains `--shout` | `python3 greet.py --help; echo "exit=$?"` | pass | exit: `0`; output contains `--shout` |
| 7 | `from greet import greet; print(greet('Ada', shout=True))` prints `HELLO, ADA!` | `python3 -c "from greet import greet; print(greet('Ada', shout=True))"; echo "exit=$?"` | pass | stdout: `HELLO, ADA!` exit: `0` |
| 8 | `python3 -m unittest discover -s tests -t .` prints `OK` | `python3 -m unittest discover -s tests -t .; echo "exit=$?"` | pass | `OK` (8 tests) exit: `0` |

## CI

| Check | State |
| --- | --- |
| test / CI | pass |

## Diff vs spec and WORKPLAN

- **Matches the spec:** Yes. The `__main__` block in `greet.py` was replaced with argparse as specified: positional `name` (`nargs="?"`, `default="world"`), `--shout` flag (`action="store_true"`), and `print(greet(args.name, shout=args.shout))`. The `greet()` function is unchanged. The test file adds `TestGreetCLI` covering all required argument combinations.
- **Out-of-scope changes:** None. Only `greet.py` and `tests/test_greet.py` were changed.
- **WORKPLAN followed:** Yes. Steps matched the plan.

## Findings

| Severity | File:line | Problem | Required fix |
| --- | --- | --- | --- |
| nit | tests/test_greet.py:end | Trailing newline was removed from the end of the file during edits (the `if __name__` block lost its final newline). | None — cosmetic only, no functional impact. |

No blockers or should-fix findings.

## Verdict

PASS. All acceptance criteria pass, CI is green, the diff is within scope, and the implementation is correct.