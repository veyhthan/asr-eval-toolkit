# asr-eval-toolkit

A small, transparent toolkit for scoring automatic speech recognition (ASR)
output and auditing annotation quality. Built for students and independent
researchers who need reproducible, scriptable evaluation without paying for a
closed lab platform.

## What it does

- Scores ASR transcripts against reference text using WER/CER and a few
  agreement metrics.
- Flags annotation inconsistencies (filler tags such as `[uh]`/`[um]`, timestamp
  spacing, speaker boundaries) so human reviewers can fix them before training.
- Runs as a single command, outputs a short markdown report.
- No third-party dependencies: standard library only, runs anywhere with Python 3.8+.

## Why

Most evaluation tooling is locked behind paid labs or built for large teams.
This gives solo researchers and small academic groups a pipeline they can read,
audit, and extend.

## Usage

```bash
python score.py --ref examples/sample_ref.txt --hyp examples/sample_hyp.txt --out report.md
```

Input format: one utterance per line in each file, lines matched by position.
Filler tags inside brackets are counted and reported.

## Tests

```bash
python tests/test_score.py
```

## CI

GitHub Actions runs the test suite and a CLI smoke test on Python 3.8 and 3.11
for every push and pull request (see `.github/workflows/ci.yml`).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Scope is kept narrow and dependency-free
on purpose.

## License

MIT, see [LICENSE](LICENSE).
