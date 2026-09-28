# Epic: Shout option for greet()

<!-- Written by the head. Every field is required; write "none" rather than leaving one empty.
     Save as <product repo>/plans/<epic-slug>/epic.md -->

- **Product:** factory-sandbox
- **Epic slug:** shout-greeting
- **Status:** approved
- **Approved by operator:** yes, 2026-09-28

## Goal

Let callers of `greet()` ask for the greeting in uppercase, and expose that as a `--shout` flag on the
command line. Today `greet()` has one fixed output and the CLI has no options at all, so the sandbox
has no way to exercise a code change that spans a library API and its command-line surface.

## User-visible outcome

- `python3 -c "from greet import greet; print(greet('Ada', shout=True))"` prints `HELLO, ADA!`
- `python3 greet.py Ada --shout` prints `HELLO, ADA!`
- The existing behaviour is unchanged: `greet("Ada")` and `python3 greet.py Ada` both print
  `Hello, Ada!`, and `python3 greet.py` still prints `Hello, world!`

## Non-goals

- No other formatting options (no `--lower`, no `--punctuation`, no i18n).
- No change to the existing default output, the existing test's expectation, or the CI workflow.
- No packaging work: no `pyproject.toml`, no console entry point, no installable CLI.
- No new modules. The library change and the CLI change both live in `greet.py`.

## Risks and unknowns

| Risk | Likelihood | Impact | Mitigation or spike |
| --- | --- | --- | --- |
| The two tasks are done against different assumptions about the `shout` parameter (name, default, positional vs keyword-only), so task 02 calls `greet()` wrongly | med | med | Task 01 pins the exact signature `greet(name: str, shout: bool = False) -> str` as an acceptance criterion; task 02 only calls it, it does not redefine it |
| Introducing `argparse` changes CLI behaviour for arguments it rejects (previously ignored) | low | low | The spec fixes the expected output for every supported invocation, including the no-argument and `--help` cases, and task 02 covers them with tests; task 02 also states that argparse's default rejection behaviour is intended, so no executor adds custom error handling (critic finding 3) |
| Uppercasing is applied to the name only, or to the whole string, inconsistently between the library and CLI paths | low | low | Spec says the whole final string is uppercased via `str.upper()`, and both paths are covered by acceptance criteria |
| `python3 -m unittest discover -s tests -t .` is the only check CI runs, so a subprocess-based CLI test could pass locally and fail in CI (working directory, `sys.executable`) | low | med | The CLI test builds its path from `__file__` and runs `sys.executable`, and CI runs the same discovery command |

## Tasks

Each task is one card and one spec file. Order is the suggested execution order.

| # | Task | Spec file | Depends on | Size |
| --- | --- | --- | --- | --- |
| 01 | Add `shout` parameter to `greet()` | `01-shout-parameter.md` | none | S (<1h) |
| 02 | Add `--shout` flag to the CLI | `02-shout-flag.md` | 01 | S (<1h) |

## Verification of the whole epic

After both tasks are merged into `main`:

1. `python3 -c "from greet import greet; print(greet('Ada')); print(greet('Ada', shout=True))"` →
   two lines: `Hello, Ada!` then `HELLO, ADA!`
2. `python3 greet.py Ada --shout` → `HELLO, ADA!`
3. `python3 greet.py Ada` → `Hello, Ada!`
4. `python3 greet.py` → `Hello, world!`
5. `python3 greet.py --shout` → `HELLO, WORLD!`
6. `python3 -m unittest discover -s tests -t .` → `OK`, and CI is green on the merged commits.

## Critic review

Critic ran 2026-09-28 via `factory critic factory-sandbox <workspace>/plans/shout-greeting`; full text
in `critic.md` in this folder. Verdict: no blockers; both tasks small, testable, correctly ordered.

1. **should-fix — Task 02's automated tests miss the two cases its own reviewer notes call the
   riskiest.** The reviewer notes flag the no-argument and flag-order cases, but the test section only
   required subprocess coverage for `["Ada", "--shout"]` and `["Ada"]`; a fast model would follow the
   test section and skip the rest.
   **Resolved: changed plan.** Task 02's "Tests to add or update" now requires all three of
   `["Ada", "--shout"]`, `["--shout", "Ada"]` and `[]`, plus `["--help"]`.
2. **should-fix — Unspecified invocation: `python3 greet.py --shout`.** Neither the behaviour table
   nor the acceptance criteria pinned the flag-with-no-name case (argparse gives `HELLO, WORLD!`,
   exit 0; the old hand-rolled parser would have printed `Hello, --shout!`).
   **Resolved: changed plan.** Added the row to task 02's behaviour table, an acceptance criterion
   for it, and an epic-level verification step.
3. **consider — Underspecified argparse-rejection behaviour.** `python3 greet.py --bogus` used to
   print `Hello, --bogus!` (exit 0); after task 02 it exits 2 with an argparse error on stderr.
   **Resolved: changed plan.** Task 02's Change section now states that argparse's default rejection
   is intended and that no custom error handling is to be added; the epic risk table points at it.
4. **consider — CI runs Python 3.12, acceptance commands run against the box's 3.13.5.** Nothing in
   this plan is version-sensitive (argparse and `str.upper` are identical there).
   **Resolved: accepted, no change.** Noted as a recurring trap for this repo, not a change here.
5. **consider — Task 01's docstring check is unverifiable.** The signature is pinned exactly, but
   "say that shout uppercases the greeting" had no corresponding check.
   **Resolved: changed plan.** Added a docstring acceptance criterion to task 01.

No finding was rejected.

## Approval

Approved in the HQ pane on 2026-09-28 after the head presented the goal, the two-task list, the top
risks and the critic findings.

Operator's words: "yes"
