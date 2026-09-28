# Critic review: shout-greeting

Reviewed against the actual repo state (greet.py, tests/test_greet.py, .github/workflows/ci.yml)
and the factory AGENTS.md Definition of Ready. Overall this is a genuinely good plan: both tasks
are small, testable, correctly ordered, and the signature contract between them is pinned with an
inspect-based check. No blockers. Findings below, most serious first.

1. **should-fix — Task 02's automated tests miss the two cases its own reviewer notes call the
   riskiest.** "Notes for the reviewer" says the risky part is the no-argument and flag-order cases
   (acceptance criteria 2 and 4), but "Tests to add or update" only requires subprocess coverage for
   `["Ada", "--shout"]` and `["Ada"]`. A fast model will do exactly what the test section says and
   skip the cases the notes flag. Fix: require the subprocess test to cover all three —
   `["Ada", "--shout"]`, `["--shout", "Ada"]`, and `[]` (expect `HELLO, ADA!` twice, then
   `Hello, world!`). Same coverage bump for criterion 5 (`--help`) if cheap.

2. **should-fix — Unspecified invocation: `python3 greet.py --shout`.** The expected-behaviour
   table and acceptance criteria never pin the flag-with-no-name case (argparse will produce
   `HELLO, WORLD!`, exit 0). It is the natural first thing a user tries with a flag whose positional
   is optional, and the old hand-rolled parser behaved differently (`--shout` treated as the name:
   "Hello, --shout!"). Add one row to the behaviour table and one acceptance criterion.

3. **consider — Underspecified argparse-rejection behaviour.** Epic risk table admits argparse
   changes behaviour for arguments it rejects but the mitigation only covers supported invocations.
   `python3 greet.py --bogus` previously printed `Hello, --bogus!` (exit 0); after task 02 it exits
   2 with an argparse error on stderr. Almost certainly fine (arguably better), but the spec should
   say so explicitly so the executor does not "helpfully" add error handling, and so the reviewer
   knows the exit-2 output is intended. One sentence in Task 02's Change section is enough.

4. **consider — CI runs Python 3.12, acceptance commands run against the box's 3.13.5.**
   Nothing in this plan is version-sensitive (argparse and str.upper are identical there), so no
   action needed — but any future acceptance criterion pinned to exact interpreter output should be
   checked against both versions. Noted as a recurring trap for this repo, not a change to this plan.

5. **consider — Task 01 docstring check is unverifiable.** Criterion 5 pins the signature exactly
   and is great; the docstring requirement ("say that shout uppercases the greeting") has no
   corresponding check, so a reviewer cannot verify it from the criteria alone. Either accept that
   (it is cosmetic) or add a one-line criterion like
   `python3 -c "import greet; print(greet.__doc__)"` → contains "shout".

Hidden-work sweep: no migrations, no secrets, no config, no packaging, no backwards-compat concern
beyond findings 2–3, rollback is trivial (revert the PRs). CI and AGENTS.md are correctly out of
scope. The existing test is protected by an explicit "keep unchanged" instruction in both specs.

Pre-mortem (three most likely failure modes, one month later):
- The merged code works but the subprocess test silently skips the no-arg/flag-order cases and
  someone later regresses them — mitigated by finding 1.
- An executor "improves" the argparse error path (custom exit message, catch-and-print) and fails
  review because the spec never said the argparse defaults were the spec — mitigated by finding 3.
- Nothing else realistic fails: the plan is well within both the box's and CI's capability.

END
