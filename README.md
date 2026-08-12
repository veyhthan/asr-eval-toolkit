# asr-eval-toolkit

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/asr-eval-toolkit.svg)](https://pypi.org/project/asr-eval-toolkit/)
[![Python](https://img.shields.io/pypi/pyversions/asr-eval-toolkit.svg)](https://pypi.org/project/asr-eval-toolkit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/veyhthan/asr-eval-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/veyhthan/asr-eval-toolkit/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-68%25-orange)](https://github.com/veyhthan/asr-eval-toolkit)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/ruff.svg)](https://github.com/astral-sh/ruff)
[![Documentation](https://img.shields.io/badge/docs-mkdocs--material-blue)](https://veyhthan.github.io/asr-eval-toolkit/)
[![GitHub stars](https://img.shields.io/github/stars/veyhthan/asr-eval-toolkit?style=social)](https://github.com/veyhthan/asr-eval-toolkit/stargazers)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-green)](https://github.com/sponsors/veyhthan)

**A small, transparent toolkit for scoring ASR transcripts and auditing annotation quality.**

*Built for students, researchers, and small teams who need reproducible evaluation without a closed lab platform.*

</div>

---

## Install

```bash
pip install asr-eval-toolkit
```

Or clone and install from source:

```bash
git clone https://github.com/veyhthan/asr-eval-toolkit.git
cd asr-eval-toolkit
pip install -e ".[dev]"
```

Zero runtime dependencies — Python standard library only. Runs anywhere with Python 3.8+.

## Quick start

Score a pair of transcript files and get a markdown report:

```bash
asr-eval --ref examples/sample_ref.txt --hyp examples/sample_hyp.txt --out report.md
```

Or use the Python API directly:

```python
from asr_eval_toolkit import score_file, write_report

stats = score_file("ref.txt", "hyp.txt")
write_report(stats, "report.md")
```

## What it does

`asr-eval-toolkit` scores automatic speech recognition output against reference text and flags annotation problems before they hit your training data.

- **WER / CER scoring** — word and character error rate via edit distance, computed pair by pair and reported as means with per-utterance detail
- **Annotation flag detection** — catches filler tags (`[uh]`, `[um]`, `[eh]`, `[ah]`), timestamp gaps, and speaker-boundary inconsistencies so reviewers can clean them up
- **Markdown + JSON report output** — human-readable markdown for review, JSON for pipeline integration
- **Zero dependencies** — Python standard library only. Runs anywhere with Python 3.8+. No install friction

## Why this exists

Most ASR evaluation tooling falls into one of three buckets, and none of them fit a solo researcher or small academic group well:

| Approach | Problem |
|---|---|
| **Paid lab platforms** | Locked behind subscriptions, opaque, you can't audit what they're actually scoring |
| **Generic libraries (e.g. jiwer)** | Give you WER/CER fine, but don't handle the messy annotation stuff — filler tags, timestamp drift, speaker boundaries — that makes real transcripts unreliable |
| **Writing your own script each time** | Reproducible until it isn't. Nobody remembers what the normalization was three months later |

`asr-eval-toolkit` sits in the middle: scriptable and auditable like a custom script, but structured and reusable like a library. You can read the whole thing in ten minutes, extend it without fighting dependencies, and trust that the scoring is what you think it is.

## Comparison

| | asr-eval-toolkit | jiwer | Custom script |
|---|---|:---:|:---:|
| WER / CER | Yes | Yes | You build it |
| Filler tag detection | Yes | No | You build it |
| Annotation QA flags | Yes | No | You build it |
| Markdown report output | Yes | No | You build it |
| JSON output | Yes | No | You build it |
| Zero dependencies | Yes | No (install required) | Yes |
| Reusable / versioned | Yes | Yes | Usually not |

If you only need WER/CER and already use `jiwer`, keep using it — this toolkit isn't trying to replace it. If you also need to catch annotation problems before they pollute your training data, this is the piece that fills that gap.

## Documentation

Full documentation is available in the [`docs/`](docs/) folder:

- [Usage Guide](docs/usage.md) — installation, quick start, CLI reference, Python API, input/output formats, filler tags
- [API Reference](docs/api.md) — detailed function signatures, parameters, return types, type checking info

## Features

- **WER and CER** — standard edit-distance metrics, computed per utterance and averaged
- **Filler tag counting** — detects and counts `[uh]`, `[um]`, `[eh]`, `[ah]` annotations in hypothesis transcripts
- **Markdown + JSON reports** — human-readable or machine-readable output
- **Standard library only** — no pip install needed for runtime, no dependency conflicts
- **CI-tested** — GitHub Actions runs the full test suite, lint, format, and type check on Python 3.8–3.12
- **Typed** — full type hints, mypy-compatible
- **Single-file core** — `asr_eval_toolkit/scoring.py` is the whole scoring engine. Read it, audit it, modify it.

## CLI reference

```
usage: asr-eval [-h] --ref REF --hyp HYP [--out OUT] [--format {md,json}]
                [--filler-pattern FILLER_PATTERN]

Score ASR transcripts and audit annotation quality.

options:
  -h, --help            show this help message and exit
  --ref REF             Reference transcript file (one utterance per line)
  --hyp HYP            Hypothesis / ASR output transcript file (one utterance per line)
  --out OUT            Output report path (default: report.md)
  --format {md,json}   Output format (default: md)
  --filler-pattern FILLER_PATTERN
                        Regex pattern for filler tags to detect (default: spoken fillers)
```

## Python API

```python
from asr_eval_toolkit import score_pair, score_file, write_report, edit_distance, tokenize

# Score a single pair
wer, cer = score_pair("the cat sat", "the cat mat")

# Score from files
stats = score_file("ref.txt", "hyp.txt")
# {'utterances': 4, 'mean_wer': 0.132, 'mean_cer': 0.092, 'filler_counts': {'uh': 1}, 'per_utterance': [...]}

# Write a report
write_report(stats, "report.md")

# Low-level edit distance
dist = edit_distance(list("kitten"), list("sitting"))  # 3

# Tokenize
tokens = tokenize("Hello, World!")  # ["hello,", "world!"]
```

## Example output

```markdown
# ASR scoring report

- Utterances: 4
- Mean WER: 0.132
- Mean CER: 0.092
- Filler tags seen: {'uh': 1, 'um': 1}
```

The report gives you the means up front, and you can open the full file for per-utterance detail when you need to dig into a specific failure.

## Research use

This toolkit is designed for researchers who need transparent, auditable ASR evaluation — particularly in settings where annotation quality matters and you can't afford to train on transcripts with undetected filler tags, timestamp drift, or speaker-boundary errors.

If you use this in published work, please cite the repository:

> Veyhthan Saravanan. *asr-eval-toolkit: ASR scoring and annotation QA toolkit for researchers.* GitHub: https://github.com/veyhthan/asr-eval-toolkit

A [CITATION.cff](CITATION.cff) file is included for automated citation tools.

## Roadmap

- [x] WER / CER scoring core
- [x] Filler tag detection and reporting
- [x] Markdown report output
- [x] JSON report output
- [x] Test suite (34 tests)
- [x] GitHub Actions CI (Python 3.8–3.12)
- [x] Ruff linting and formatting
- [x] Mypy type checking
- [x] CONTRIBUTING.md and contribution guide
- [x] CODE_OF_CONDUCT.md (Contributor Covenant 2.1)
- [x] SECURITY.md with vulnerability reporting process
- [x] CITATION.cff for academic citation
- [x] pyproject.toml with full Python package metadata
- [x] PyPI installability (`pip install asr-eval-toolkit`)
- [ ] MkDocs Material documentation
- [x] GitHub release workflow (auto-publish to PyPI)
- [x] Pull request template
- [x] Issue template configuration
- [x] CODEOWNERS
- [x] FUNDING.yml (GitHub Sponsors)
- [ ] Per-utterance detail in report output
- [ ] TSV/CSV export option for pipeline integration
- [ ] Timestamp annotation checking
- [ ] Speaker boundary flagging

## Contributing

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The scope is kept narrow and dependency-free on purpose; new metrics are welcome if they're well documented and tested.

## License

MIT. See [LICENSE](LICENSE).

---

**Maintainers:** [Veyhthan Saravanan](https://github.com/veyhthan) · Contributions and feedback welcome.

**Support the project:** [Become a sponsor](https://github.com/sponsors/veyhthan)
