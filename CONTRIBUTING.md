# Contributing to asr-eval-toolkit

<div align="center">

**Small. Transparent. Dependency-free.**

*This guide is short on purpose — the project is too.*
</div>

---

## What this project is

`asr-eval-toolkit` is a minimal Python toolkit for scoring automatic speech
recognition (ASR) output and auditing annotation quality. It is:

- **Small** — the whole scoring engine is one file. Read it in ten minutes.
- **Transparent** — no hidden logic, no third-party dependencies, no black boxes.
- **Dependency-free** — Python standard library only, runs anywhere with Python 3.8+.

If you want to add something that makes the project bigger or heavier, you
probably shouldn't. If you want to add something that makes it more useful
while staying small, read on.

## Getting started

```bash
git clone https://github.com/veyhthan/asr-eval-toolkit.git
cd asr-eval-toolkit
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running the project

```bash
# Score a pair of transcript files
asr-eval --ref examples/sample_ref.txt --hyp examples/sample_hyp.txt --out report.md

# Run the test suite
pytest

# Run with coverage
pytest --cov=asr_eval_toolkit --cov-report=term-missing
```

## Running the tests

The test suite lives in `tests/`. Run it before you open a PR:

```bash
pytest tests/
```

All tests must pass. Coverage should not decrease.

## Code style

- **Lint with ruff** before committing:
  ```bash
  ruff check .
  ruff format .
  ```
- **Type-check with mypy** (optional, run in CI):
  ```bash
  mypy asr_eval_toolkit
  ```
- Keep it readable. This is a small project — the code should be understandable
  in a single sitting.
- Docstrings on public functions.
- No linting enforcement is strict yet, but please don't make it worse.

## What we're looking for

| Change | Welcome? |
|--------|----------|
| New scoring metrics (well documented, tested) | ✅ Yes |
| Bug fixes (with a regression test) | ✅ Yes |
| Documentation improvements | ✅ Yes |
| CLI improvements | ✅ Yes |
| CI improvements | ✅ Yes |
| Adding third-party dependencies | ❌ No |
| Large refactors without clear benefit | ❌ No |
| Breaking the stdlib-only constraint | ❌ No |

## Pull request process

1. Make sure the test suite passes: `pytest`
2. Run the lint check: `ruff check . && ruff format --check .`
3. Open a PR with a clear description of what changed and why
4. Link any related issue if there is one

## Reporting issues

- **Bugs** — use the bug report template. Include the Python version, OS, and
  the exact command you ran.
- **Feature requests** — use the feature request template. Explain the problem
  you're trying to solve, not just what you want built.
- **Questions** — open a GitHub discussion or issue. No such thing as a dumb
  question.

## Release process

Maintainers only.

1. Update `CHANGELOG.md` with the new version and changes.
2. Bump the version in `asr_eval_toolkit/__init__.py`.
3. Commit, tag, and push:
   ```bash
   git commit -am "Bump version to X.Y.Z"
   git tag X.Y.Z
   git push origin main --tags
   ```
4. CI builds and publishes automatically (when configured).

## License

By contributing, you agree that your contributions will be licensed under the
MIT License — see [LICENSE](LICENSE).

---

**Questions?** Open an issue. No such thing as a dumb question.
