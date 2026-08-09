# Contributing

Thanks for considering a contribution. This toolkit stays small and readable
on purpose.

## How to contribute

1. Fork the repo and create a branch off `main`.
2. Keep changes focused. Add or update a test in `tests/` for any logic change.
3. Run `python tests/test_score.py` before opening a PR.
4. Open a PR with a one-line description of the change.

## Scope

We want to keep this a transparent, auditable scoring tool for ASR and
annotation QA. New metrics are welcome if they are well documented and have a
test. Please avoid heavy dependencies; the goal is a scriptable pipeline that
runs anywhere with just Python.
