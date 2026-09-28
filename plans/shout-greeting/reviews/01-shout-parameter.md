# Review: task 01 Add `shout` parameter to `greet()`

- **Card:** (from board card ID)
- **PR:** https://github.com/en3r0/factory-sandbox/pull/3
- **Review round:** 1
- **Verdict:** PASS

## Acceptance criteria re-run

| # | Criterion | Command or check | Result | Evidence |
| --- | --- | --- | --- | --- |
| 1 | `greet('Ada')` returns `Hello, Ada!` | `python3 -c "from greet import greet; print(greet('Ada'))"` | pass | `Hello, Ada!` |
| 2 | `greet('Ada', shout=True)` returns `HELLO, ADA!` | `python3 -c "from greet import greet; print(greet('Ada', shout=True))"` | pass | `HELLO, ADA!` |
| 3 | `greet('Ada', True)` returns `HELLO, ADA!` (positional) | `python3 -c "from greet import greet; print(greet('Ada', True))"` | pass | `HELLO, ADA!` |
| 4 | `greet('Ada', shout=False)` returns `Hello, Ada!` | `python3 -c "from greet import greet; print(greet('Ada', shout=False))"` | pass | `Hello, Ada!` |
| 5 | Signature is `(name: str, shout: bool = False) -> str` | `python3 -c "import inspect, greet; print(inspect.signature(greet.greet))"` | pass | `(name: str, shout: bool = False) -> str` |
| 6 | Tests pass (`OK`, 2 tests) | `python3 -m unittest discover -s tests -t .` | pass | `.. OK (2 tests)` |
| 7 | Docstring mentions `shout` | `python3 -c "import greet; print(greet.greet.__doc__)"` | pass | `Return a greeting for name; uppercases it when shout is True.` |

## CI

- `test` — pass

## Diff vs spec and WORKPLAN

- **Matches the spec:** yes. Signature `def greet(name: str, shout: bool = False) -> str` matches criterion 5 exactly. Behaviour: `shout=True` uppercases the result via `str.upper()`. Docstring updated and mentions `shout`. The `__main__` block is untouched. The existing `test_greet` method is preserved exactly as-is.
- **Out-of-scope changes:** none. Only `greet.py` and `tests/test_greet.py` were changed, as specified.
- **WORKPLAN followed:** yes. Steps 1–5 were executed correctly.

## Findings

No blockers, should-fixes, or nits.

| Severity | File:line | Problem | Required fix |
| --- | --- | --- | --- |
| — | — | None. | — |

## For the executor (if FAIL)

N/A — verdict is PASS.