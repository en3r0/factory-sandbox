# Task 02: Add `--shout` flag to the CLI

<!-- Written by the head (planner). Every field is required; write "none" rather than leaving one empty.
     Save as <product repo>/plans/<epic-slug>/<NN>-<task-slug>.md
     A task that fails the Definition of Ready in the factory AGENTS.md must be split or clarified. -->

- **Epic:** `plans/shout-greeting/epic.md`
- **Size:** S (<1h)
- **Depends on:** 01
- **Model override:** none

## Context

`python3 greet.py Ada` prints a greeting, using a hand-rolled `sys.argv[1]` lookup in the `__main__`
block of `greet.py`; there is no way to pass an option. Task 01 has already added
`greet(name: str, shout: bool = False) -> str` to the module. This task replaces the hand-rolled
argument handling with `argparse` and adds the `--shout` flag that reaches that parameter.

## Files to read first

- `greet.py`: the `__main__` block is the only thing this task changes; `greet()` itself is done and
  must not change here.
- `plans/shout-greeting/01-shout-parameter.md`: the signature contract this task calls into.
- `tests/test_greet.py`: where the CLI test goes, and the existing import style.
- `AGENTS.md`: how to run the tests, and the rule that this repo is Python 3 standard library only.

## Change

In `greet.py`, replace the body of the `if __name__ == "__main__":` block with `argparse`-based
parsing that does exactly this:

- `name`: a positional argument with `nargs="?"` and `default="world"`, so the no-argument case keeps
  working.
- `--shout`: `action="store_true"`, with help text saying the greeting is printed in uppercase.
- Print `greet(args.name, shout=args.shout)` — one line to stdout, no trailing extra output.

Use `argparse` from the standard library (`import argparse` inside the `__main__` block, next to the
existing `import sys`, which may be dropped if it becomes unused). Keep the `if __name__ ==
"__main__":` guard and keep `greet()` unchanged. A short `description` for the parser is fine;
do not add subcommands, short flags, or extra options.

Expected behaviour of the resulting CLI:

| Invocation | stdout | exit code |
| --- | --- | --- |
| `python3 greet.py` | `Hello, world!` | 0 |
| `python3 greet.py Ada` | `Hello, Ada!` | 0 |
| `python3 greet.py --shout` | `HELLO, WORLD!` | 0 |
| `python3 greet.py Ada --shout` | `HELLO, ADA!` | 0 |
| `python3 greet.py --shout Ada` | `HELLO, ADA!` | 0 |
| `python3 greet.py --help` | usage text mentioning `--shout` | 0 |

Argparse's default behaviour for an unknown option is the intended behaviour here: `python3 greet.py
--bogus` exits 2 with an argparse error on stderr. Do not add custom error handling, a custom usage
string, or a catch-and-print around the parse — the defaults are the spec.

## Acceptance criteria

Each one is a command or an observable check with its expected result. The reviewer re-runs all of them.
A criterion that can't run on the factory box (heavy build, browser, running service) must name the CI
job that verifies it: `CI job <name>` → <expected result>.

1. `python3 greet.py` → prints exactly `Hello, world!`, exit code 0
2. `python3 greet.py Ada` → prints exactly `Hello, Ada!`, exit code 0
3. `python3 greet.py --shout` → prints exactly `HELLO, WORLD!`, exit code 0
4. `python3 greet.py Ada --shout` → prints exactly `HELLO, ADA!`, exit code 0
5. `python3 greet.py --shout Ada` → prints exactly `HELLO, ADA!`, exit code 0
6. `python3 greet.py --help; echo "exit=$?"` → exit=0 and the output contains `--shout`
7. `python3 -c "from greet import greet; print(greet('Ada', shout=True))"` → prints exactly
   `HELLO, ADA!` (the library behaviour from task 01 still works after the CLI change)
8. `python3 -m unittest discover -s tests -t .` → prints `OK`

## Tests to add or update

- `tests/test_greet.py`: add a test class or method that runs the CLI through a subprocess and
  asserts stdout and exit code for **all** of these argument lists: `["Ada", "--shout"]` →
  `HELLO, ADA!`, `["--shout", "Ada"]` → `HELLO, ADA!`, `[]` → `Hello, world!`, `["Ada"]` →
  `Hello, Ada!`, and `["--shout"]` → `HELLO, WORLD!`. Build the script path from `__file__` (the
  repo root is the parent of the `tests` directory) and run `[sys.executable, "greet.py", ...]` with
  that directory as `cwd`, using `capture_output=True, text=True`. Compare `stdout.strip()` and the
  exit code. Add a `["--help"]` case asserting exit code 0 and that `--shout` appears in the output.
  Do not add a new dependency.
- Keep every existing test passing unchanged.

## Out of scope

- Any change to `greet()`'s signature, default output, or uppercase behaviour — that is task 01.
- Extra flags, short flags, subcommands, or a `--version` option.
- Packaging: no `pyproject.toml`, no `setup.py`, no console entry point.
- `AGENTS.md`, `.github/workflows/ci.yml`, and any new file outside `greet.py` and
  `tests/test_greet.py`.

## Verification commands

```bash
python3 greet.py Ada --shout
python3 greet.py --shout Ada
python3 greet.py --shout
python3 greet.py Ada
python3 greet.py
python3 greet.py --help
python3 -m unittest discover -s tests -t .
```

## Notes for the reviewer

The risky part is the no-argument and flag-order cases, which the old hand-rolled parsing did not
have to handle: check acceptance criteria 1, 3, 5 and 6 by running them, not by reading the code.
Also confirm `greet()` was not edited in this task's diff, and that the subprocess test really covers
every argument list listed in "Tests to add or update" rather than only the two easy ones.
