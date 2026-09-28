# Research: argparse behavior on an unknown option

## Question

When a Python `argparse` program receives an unknown option (for example `--bogus`), what exit code
does it use and does the error go to stdout or stderr? Source required by the brief: the official
Python docs.

Narrowing: none needed. The brief names the exact tool (`argparse`), the exact input (an unknown
option) and the exact source (official Python docs), so the question is answerable as written. Scope
is deliberately limited to the *unrecognized-argument* path; `--help` and other exits are noted only
where they clarify the contrast.

**Prior research (built on, not repeated).** `marketing/research/2026-09-28-latest-stable-python-release.md`
(same day, sibling card) establishes the latest stable release as Python 3.14.7. That is consistent
with what this card found independently: the docs served at `docs.python.org/3` were stamped 3.14.7
on 2026-09-28, which corroborates that file's answer. Nothing in that research changed; this card
adds the runtime counterpart below (the installed interpreter here is 3.13.5, older than the latest
stable 3.13 point release, 3.13.14 — which is why the version cross-check in Confidence matters).
No shared conclusions beyond the docs version.

## Short answer

- Exit code is **2**.
- The error goes to **stderr**, not stdout. Stdout receives nothing.
- Output on stderr is the usage line plus `<prog>: error: unrecognized arguments: --bogus`.
- This is the documented default and holds for a standard `ArgumentParser()` (`exit_on_error=True`,
  the default). It is not a choice the program author has to make.
- `exit_on_error=False` (added in 3.9) changes the mechanism — an `ArgumentError` is raised instead
  of the process exiting — so the "exit code 2" answer assumes the default parser.

## Findings

All URLs checked **2026-09-28**. Documentation version served at `docs.python.org/3` on that date:
**Python 3.14.7** (page title). Local interpreter used for corroboration: **Python 3.13.5**.

**F1. `ArgumentParser.error()` documents exit code 2 and stderr (found).**
> "This method prints a usage message, including the *message*, to `sys.stderr` and terminates the
> program with a status code of 2."

Source: https://docs.python.org/3/library/argparse.html#exiting-methods ("Other utilities → Exiting
methods", `ArgumentParser.error(message)` entry), checked 2026-09-28.

This is the load-bearing citation: it states both halves of the answer (stream = `sys.stderr`,
status = 2) in one sentence. An unknown option is routed through this method.

**F2. The same behavior is stated for invalid argument lists generally (found).**
> "Normally, when you pass an invalid argument list to the `parse_args()` method of an
> `ArgumentParser`, it will print a *message* to `sys.stderr` and exit with a status code of 2."

Source: https://docs.python.org/3/library/argparse.html#exit-on-error (`exit_on_error` parameter),
checked 2026-09-28. So the stream/status pair is not specific to one error subtype; it is the
parser-wide default. The same section documents the `exit_on_error=False` escape hatch:
`Changed in version 3.9: exit_on_error parameter was added.`

**F3. The docs' own worked example of an invalid option shows the message text (found).**
> ```
> >>> # invalid option
> >>> parser.parse_args(['--bar'])
> usage: PROG [-h] [--foo FOO] [bar]
> PROG: error: unrecognized arguments: --bar
> ```

Source: https://docs.python.org/3/library/argparse.html#invalid-arguments ("Invalid arguments"),
checked 2026-09-28. Note this section's prose says only "it exits and prints the error along with a
usage message" — it does not repeat the stream and the code; those come from F1/F2. The example is
the docs' canonical illustration of an unknown option.

**F4. The tutorial repeats the same output shape (found).**
> ```
> $ python prog.py --verbose
> usage: prog.py [-h]
> prog.py: error: unrecognized arguments: --verbose   # (with the interpreter's own prefix)
> ```

Source: https://docs.python.org/3/howto/argparse.html#the-basics ("The basics"), checked
2026-09-28. The tutorial's surrounding prose explains the `-h`-only parser "rejects everything
else" but does not itself state the numeric exit code.

**F5. Independent runtime corroboration (found, not from docs).** Running the standard library on
this machine reproduces both facts exactly:

```
$ python3 -c "..."   # ArgumentParser(prog='prog'); parse_args(['--bogus'])
exit code: 2
stdout captured: ''
stderr captured: 'usage: prog [-h] [--known KNOWN]\nprog: error: unrecognized arguments: --bogus\n'
python version: 3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]
```

Checked 2026-09-28 on Python 3.13.5. This is a check, not a source: it confirms the 3.14 docs apply
to the 3.13 stdlib installed here, and it is the evidence that **stdout stays empty** — the docs
never say stdout is empty, they only say the message goes to stderr.

**F6. Contrast, for interpreting "2" (found).** `ArgumentParser.exit(status=0, message=None)`
"terminates the program, exiting with the specified *status* and, if given, it prints a *message* to
`sys.stderr`". Source: https://docs.python.org/3/library/argparse.html#exiting-methods, checked
2026-09-28. `error()` is implemented as a call to `exit(status=2, ...)` on the same page's model.

**Inference (labelled as such).** Because `error()` unconditionally *terminates the program*, the
exit code is not observable from inside the program: it surfaces as a `SystemExit` exception (whose
`.code` is 2) if you catch it, or as the process exit status otherwise. F5 observed `.code == 2`.

**Not found (valid finding).** The brief asks "does the error go to stdout or stderr". The docs state
the stderr destination explicitly but never state that stdout is empty; that half of the answer rests
on F5 rather than on documentation. Also not found: any documented exception where an unrecognized
*option* (as opposed to a bad value, a missing argument, or an ambiguous abbreviation) uses a
different code or stream. The docs treat these uniformly.

## What this means for us

There is **no product or marketing implication** — this is an internal technical question about the
Python standard library, asked to exercise the factory's Research column. `factory-sandbox` is a
throwaway repo with no users, no market and no competitors, so there is nothing here to act on
commercially.

The only consumer is engineering: any CLI this project grows should expect exit 2 and stderr output
from `argparse` on bad input, and any test asserting on CLI behavior should assert on **stderr and
the exit code**, never on stdout. Testing the "unknown option" case by capturing stdout would pass
vacuously, since stdout is empty on every error path.

## Confidence and gaps

**Confidence: high.** The answer is stated verbatim in the official docs (the source the brief
requires), in two independent sections of the same authoritative page (F1 for `error()`, F2 for the
parser-wide default), and independently reproduced by running the standard library (F5). Docs
version 3.14.7 and runtime 3.13.5 agree, so this is not a version-sensitive fact.

Gaps and caveats a reader should know:

- The brief's "the official Python docs" is satisfied by `docs.python.org/3`. That URL is the *dev*
  documentation branch and served 3.14.7 at check time; version-pinned pages
  (`docs.python.org/3.13/library/argparse.html`) exist but were not fetched. Low risk: exit-code
  behavior on this path has been stable, and the 3.13 interpreter here matches the 3.14 docs.
- "Exit code 2" is the answer for the default `exit_on_error=True`. With
  `exit_on_error=False` (3.9+) the call raises `ArgumentError` instead and the process does not exit
  at all (F2). A program that catches that exception has no argparse-imposed exit code.
- Python 3.14 added `suggest_on_error` and `color` to `ArgumentParser`. Neither changes the stream or
  the status code on this path, but a 3.14-colored stderr message may carry ANSI escapes.
- The unresolvable part is environmental, not factual: "stderr" under a shell that merges the two
  streams (e.g. `2>&1`, or some CI log collectors) will *look* like stdout. The docs' claim is about
  the file object written to, which is the meaningful distinction.

## Suggested next steps

None required — the question is self-contained and fully answered.

Optional, if the strategist wants this covered for the codebase: a short engineering spec for a test
asserting `SystemExit.code == 2` and non-empty `capsys.readouterr().err` with empty `.out` for an
unknown option on `greet.py`'s CLI. That is a build task, not research, and should not be folded into
this card.
