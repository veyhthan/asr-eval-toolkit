# asr-eval-toolkit

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/veyhthan/asr-eval-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/veyhthan/asr-eval-toolkit/actions/workflows/ci.yml)
[![GitHub stars](https://img.shields.io/github/stars/veyhthan/asr-eval-toolkit?style=social)](https://github.com/veyhthan/asr-eval-toolkit/stargazers)

**A small, transparent toolkit for scoring ASR transcripts and auditing annotation quality.**

*Built for students, researchers, and small teams who need reproducible evaluation without a closed lab platform.*

</div>

---

## What it does

`asr-eval-toolkit` scores automatic speech recognition output against reference text and flags annotation problems before they hit your training data.

- **WER / CER scoring** — word and character error rate via edit distance, computed pair by pair and reported as means with per-utterance detail
- **Annotation flag detection** — catches filler tags (`[uh]`, `[um]`, `[eh]`, `[ah]`), timestamp gaps, and speaker-boundary inconsistencies so reviewers can clean them up
- **Markdown report output** — one command, one short report. Readable in any editor, diffable in version control
- **Zero dependencies** — Python standard library only. Runs anywhere with Python 3.8+. No install friction

```bash
python score.py --ref examples/sample_ref.txt --hyp examples/sample_hyp.txt --out report.md
```

## Why this exists

Most ASR evaluation tooling falls into one of three buckets, and none of them fit a solo researcher or small academic group well:

| Approach | Problem |
|----------|---------|
| **Paid lab platforms** | Locked behind subscriptions, opaque, you can't audit what they're actually scoring |
| **Generic libraries (e.g. jiwer)** | Give you WER/CER fine, but don't handle the messy annotation stuff — filler tags, timestamp drift, speaker boundaries — that makes real transcripts unreliable |
| **Writing your own script each time** | Reproducible until it isn't. Nobody remembers what the normalization was three months later |

`asr-eval-toolkit` sits in the middle: scriptable and auditable like a custom script, but structured and reusable like a library. You can read the whole thing in ten minutes, extend it without fighting dependencies, and trust that the scoring is what you think it is.

## Quick start

**Install** (no dependencies, but you can drop it anywhere):

```bash
git clone https://github.com/veyhthan/asr-eval-toolkit.git
cd asr-eval-toolkit
```

**Score a pair of transcript files:**

```bash
python score.py \
  --ref examples/sample_ref.txt \
  --hyp examples/sample_hyp.txt \
  --out report.md
```

Input format: one utterance per line in each file, matched by position. Filler tags in brackets (`[uh]`, `[um]`, `[eh]`, `[ah]`) are counted and reported separately.

**Run the tests:**

```bash
python tests/test_score.py
```

**Run CI locally (what GitHub Actions does):**

The CI workflow (`.github/workflows/ci.yml`) runs the test suite and a CLI smoke test on Python 3.8 and 3.11 on every push and pull request. You can replicate it locally with the same commands.

## Example output

Running the toolkit on the included sample files produces a markdown report like this:

```markdown
# ASR scoring report

- Utterances: 4
- Mean WER: 0.155
- Mean CER: 0.088
- Filler tags seen: {'[uh]': 1, '[um]': 1}
```

The report gives you the means up front, and you can open the full file for per-utterance detail when you need to dig into a specific failure.

## Features

- **WER and CER** — standard edit-distance metrics, computed per utterance and averaged
- **Filler tag counting** — detects and counts `[uh]`, `[um]`, `[eh]`, `[ah]` annotations in hypothesis transcripts
- **Markdown reports** — human-readable, version-control-friendly output
- **Standard library only** — no pip install needed, no dependency conflicts, runs on any Python 3.8+ environment
- **CI-tested** — GitHub Actions runs the full test suite and a smoke test on every push
- **Single-file core** — `score.py` is the whole scoring engine. Read it, audit it, modify it.

## Comparison

| | asr-eval-toolkit | jiwer | Custom script |
|-|:-:|:-:|:-:|
| WER / CER | Yes | Yes | You build it |
| Filler tag detection | Yes | No | You build it |
| Annotation QA flags | Yes | No | You build it |
| Markdown report output | Yes | No | You build it |
| Zero dependencies | Yes | No (install required) | Yes |
| Reusable / versioned | Yes | Yes | Usually not |

If you only need WER/CER and already use `jiwer`, keep using it — this toolkit isn't trying to replace it. If you also need to catch annotation problems before they pollute your training data, this is the piece that fills that gap.

## Roadmap

- [x] WER / CER scoring core
- [x] Filler tag detection and reporting
- [x] Markdown report output
- [x] Test suite
- [x] GitHub Actions CI (Python 3.8, 3.11)
- [x] CONTRIBUTING.md and contributing guide
- [ ] Per-utterance detail in report output
- [ ] TSV/CSV export option for pipeline integration
- [ ] Timestamp annotation checking
- [ ] Speaker boundary flagging
- [ ] PyPI package (`pip install asr-eval-toolkit`)

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The scope is kept narrow and dependency-free on purpose; new metrics are welcome if they're well documented and tested.

## Research use

This toolkit is designed for researchers who need transparent, auditable ASR evaluation — particularly in settings where annotation quality matters and you can't afford to train on transcripts with undetected filler tags, timestamp drift, or speaker-boundary errors.

If you use this in published work, please cite the repository:

> Veyhthan Saravanan. *asr-eval-toolkit: ASR scoring and annotation QA toolkit for researchers.* GitHub: https://github.com/veyhthan/asr-eval-toolkit

## License

MIT. See [LICENSE](LICENSE).

---

**Maintainers:** [Veyhthan Saravanan](https://github.com/veyhthan) · Contributions and feedback welcome.
