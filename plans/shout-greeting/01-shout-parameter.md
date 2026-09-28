# Task 01: Add `shout` parameter to `greet()`

<!-- Written by the head (planner). Every field is required; write "none" rather than leaving one empty.
     Save as <product repo>/plans/<epic-slug>/<NN>-<task-slug>.md
     A task that fails the Definition of Ready in the factory AGENTS.md must be split or clarified. -->

- **Epic:** `plans/shout-greeting/epic.md`
- **Size:** S (<1h)
- **Depends on:** none
- **Model override:** none

## Context

`greet()` in `greet.py` always returns `f"Hello, {name}!"`. This task adds the library-level option
the epic is about: a `shout` keyword argument that uppercases the result. The command-line flag that
uses it is a separate task (02) that depends on this one, so the signature written here is a
contract: task 02 calls `greet(name, shout=...)` and must not have to change this function.

## Files to read first

- `greet.py`: the module being changed; `greet()` is the only function and the `__main__` block is
  task 02's business, not this task's.
- `tests/test_greet.py`: the existing test that pins today's default output; it must keep passing
  unchanged.
- `AGENTS.md`: how to run the tests, and the rule that this repo is Python 3 standard library only.

## Change

In `greet.py`, change the signature of `greet` to exactly:

```python
def greet(name: str, shout: bool = False) -> str:
```

Behaviour:

- Build the greeting exactly as today: `f"Hello, {name}!"`.
- If `shout` is true, return the whole greeting uppercased with `str.upper()`; otherwise return it
  unchanged.
- Keep it a positional-or-keyword parameter with default `False` (not keyword-only), so both
  `greet("Ada", True)` and `greet("Ada", shout=True)` work.
- Update the docstring to say that `shout` uppercases the greeting. Keep the existing one-line
  docstring style.

Do not add a second function, a module-level constant, or any import. Do not touch the `__main__`
block in this task.

## Acceptance criteria

Each one is a command or an observable check with its expected result. The reviewer re-runs all of them.
A criterion that can't run on the factory box (heavy build, browser, running service) must name the CI
job that verifies it: `CI job <name>` → <expected result>.

1. `python3 -c "from greet import greet; print(greet('Ada'))"` → prints exactly `Hello, Ada!`
2. `python3 -c "from greet import greet; print(greet('Ada', shout=True))"` → prints exactly `HELLO, ADA!`
3. `python3 -c "from greet import greet; print(greet('Ada', True))"` → prints exactly `HELLO, ADA!`
   (the parameter is positional as well as a keyword)
4. `python3 -c "from greet import greet; print(greet('Ada', shout=False))"` → prints exactly
   `Hello, Ada!`
5. `python3 -c "import inspect, greet; print(inspect.signature(greet.greet))"` → prints exactly
   `(name: str, shout: bool = False) -> str`
6. `python3 -m unittest discover -s tests -t .` → prints `OK`, and the existing
   `test_greet` still asserts `greet("Ada") == "Hello, Ada!"`
7. `python3 -c "import greet; print(greet.greet.__doc__)"` → the printed docstring mentions `shout`
   (e.g. contains the substring `shout`), so the docstring update is checkable

## Tests to add or update

- `tests/test_greet.py`: add a test method `test_greet_shout` asserting
  `greet("Ada", shout=True) == "HELLO, ADA!"`. Keep the existing `test_greet` method and its
  expectation exactly as they are. Use `unittest` only, no new dependency and no subprocess here.

## Out of scope

- The command-line interface: `python3 greet.py --shout` is task 02. Do not edit the `__main__` block.
- Any other parameter or formatting option on `greet()`.
- `AGENTS.md`, `.github/workflows/ci.yml`, and any new file outside `greet.py` and
  `tests/test_greet.py`.

## Verification commands

```bash
python3 -c "from greet import greet; print(greet('Ada'))"
python3 -c "from greet import greet; print(greet('Ada', shout=True))"
python3 -c "from greet import greet; print(greet('Ada', True))"
python3 -c "import inspect, greet; print(inspect.signature(greet.greet))"
python3 -c "import greet; print(greet.greet.__doc__)"
python3 -m unittest discover -s tests -t .
```

## Notes for the reviewer

The exact signature is a contract with task 02; check it against acceptance criterion 5 rather than
eyeballing it. Confirm `test_greet` was not weakened to make room for the new test.
