# Contributing to asr-eval-toolkit

Thanks for considering a contribution. This toolkit stays small, readable, and dependency-free on purpose — that's the whole point.

## Getting started

1. Fork the repo and create a branch off `main`.
2. Set up a virtual environment if you want isolation:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Run the test suite before you make any changes:
   ```bash
   python tests/test_score.py
   ```
4. Make your change. Keep it focused — one thing per PR.

## What we're looking for

- **New scoring metrics** are welcome if they're well documented and have a test
- **Bug fixes** — please include a test that would have caught the bug
- **Documentation improvements** — README, docstrings, examples
- **CI improvements** — the workflow lives in `.github/workflows/ci.yml`

## What we're not looking for

- Adding third-party dependencies — the goal is a scriptable pipeline that runs anywhere with just Python
- Large refactors without a clear benefit to users
- Breaking the standard-library-only constraint without a strong reason

## Pull request process

1. Make sure the test suite passes (`python tests/test_score.py`)
2. Run the CI smoke test to make sure the CLI still works:
   ```bash
   python score.py --ref examples/sample_ref.txt --hyp examples/sample_hyp.txt --out /tmp/test_report.md
   ```
3. Open a PR with a clear one-line description of what changed and why
4. Link any related issue if there is one

## Code style

- Keep it readable — this is a small project, the code should be understandable in a single sitting
- Docstrings on public functions
- Tests alongside the code they cover
- No linting enforcement yet, but please don't make it worse

## License

By contributing, you agree that your contributions will be licensed under the MIT License — see [LICENSE](../LICENSE).
