# asr-eval-toolkit Documentation

Welcome to **asr-eval-toolkit** — a minimal, dependency-free toolkit for scoring
automatic speech recognition (ASR) output and auditing annotation quality.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [CLI Reference](#cli-reference)
4. [Python API](#python-api)
5. [Input Format](#input-format)
6. [Output Formats](#output-formats)
7. [Filler Tags](#filler-tags)
8. [Extending the Toolkit](#extending-the-toolkit)
9. [Citing](#citing)

---

## Installation

### Option 1: pip install (recommended)

```bash
pip install asr-eval-toolkit
```

Then use the `asr-eval` command:

```bash
asr-eval --ref ref.txt --hyp hyp.txt
```

### Option 2: Install from source

```bash
git clone https://github.com/veyhthan/asr-eval-toolkit.git
cd asr-eval-toolkit
pip install -e ".[dev]"
```

### Option 3: No install (zero dependencies)

The toolkit uses only the Python standard library. You can run it directly
without installing anything:

```bash
python -m asr_eval_toolkit.cli --ref ref.txt --hyp hyp.txt
```

Or run the legacy script:

```bash
python score.py --ref ref.txt --hyp hyp.txt
```

### Requirements

- Python 3.8 or higher
- No third-party dependencies required for basic use
- Optional dev dependencies: pytest, pytest-cov, ruff

---

## Quick Start

Score a pair of transcript files and get a markdown report:

```bash
asr-eval --ref examples/sample_ref.txt --hyp examples/sample_hyp.txt --out report.md
```

View the report:

```bash
cat report.md
```

```
# ASR scoring report

- Utterances: 4
- Mean WER: 0.132
- Mean CER: 0.092
- Filler tags seen: {'uh': 1, 'um': 1}
```

Or get JSON output for pipeline integration:

```bash
asr-eval --ref ref.txt --hyp hyp.txt --out results.json --format json
```

---

## CLI Reference

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

### Examples

**Basic scoring:**

```bash
asr-eval --ref ref.txt --hyp hyp.txt
```

**Custom output path:**

```bash
asr-eval --ref ref.txt --hyp hyp.txt --out results.md
```

**JSON output for automation:**

```bash
asr-eval --ref ref.txt --hyp hyp.txt --out results.json --format json
```

**Custom filler pattern:**

```bash
asr-eval --ref ref.txt --hyp hyp.txt --filler-pattern '\[(uh|um|eh|ah|mm|oh)\]'
```

---

## Python API

### `score_pair(ref, hyp) -> (wer, cer)`

Score a single reference/hypothesis pair. Returns WER and CER as a tuple of floats.

```python
from asr_eval_toolkit.scoring import score_pair

wer, cer = score_pair("the cat sat on the mat", "the cat sat on a mat")
print(f"WER: {wer:.3f}, CER: {cer:.3f}")
# WER: 0.200, CER: 0.043
```

### `score_file(ref_path, hyp_path, filler_pattern=None) -> dict`

Score all utterance pairs from two files. Returns a dictionary with aggregate
statistics and per-utterance detail.

```python
from asr_eval_toolkit.scoring import score_file, write_report

stats = score_file("ref.txt", "hyp.txt")
print(f"Mean WER: {stats['mean_wer']:.3f}")
print(f"Mean CER: {stats['mean_cer']:.3f}")
print(f"Filler tags: {stats['filler_counts']}")
print(f"Per-utterance: {stats['per_utterance']}")

write_report(stats, "report.md")
```

The returned dictionary has the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `utterances` | int | Number of utterance pairs scored |
| `mean_wer` | float | Mean WER across all pairs |
| `mean_cer` | float | Mean CER across all pairs |
| `filler_counts` | dict | Mapping of filler tag to count |
| `per_utterance` | list | List of `{wer, cer}` dicts per pair |

### `write_report(stats, out_path) -> str`

Write a scoring report to a markdown file.

```python
from asr_eval_toolkit.scoring import score_file, write_report

stats = score_file("ref.txt", "hyp.txt")
write_report(stats, "report.md")  # returns "report.md"
```

### `edit_distance(a, b) -> int`

Low-level Levenshtein edit distance between two token lists. Used internally
for WER/CER computation.

```python
from asr_eval_toolkit.scoring import edit_distance

dist = edit_distance(list("kitten"), list("sitting"))
print(dist)  # 3
```

### `tokenize(text) -> list`

Split text into lowercased word tokens.

```python
from asr_eval_toolkit.scoring import tokenize

tokens = tokenize("Hello, World!")
print(tokens)  # ['hello,', 'world!']
```

---

## Input Format

Both reference and hypothesis files use the same format:

- One utterance per line
- Lines are matched by position (line 1 in ref vs line 1 in hyp, etc.)
- UTF-8 encoded

Example `ref.txt`:

```
the quick brown fox jumps over the lazy dog
she sells sea shells by the sea shore
hello world this is a test
the patient presented with mild fever and cough
```

Example `hyp.txt`:

```
the quick brown fox jumps over lazy dog
she sells sea shells by the [uh] sea shore
hello world this is test
the patient presented with mild fever and [um] cough
```

---

## Output Formats

### Markdown (default)

Human-readable, version-control-friendly. Good for review and documentation.

```markdown
# ASR scoring report

- Utterances: 4
- Mean WER: 0.132
- Mean CER: 0.092
- Filler tags seen: {'uh': 1, 'um': 1}
```

### JSON

Machine-readable. Good for pipeline integration and automation.

```json
{
  "utterances": 4,
  "mean_wer": 0.132,
  "mean_cer": 0.092,
  "filler_counts": {"uh": 1, "um": 1},
  "per_utterance": [
    {"wer": 0.143, "cer": 0.043},
    {"wer": 0.200, "cer": 0.067},
    {"wer": 0.250, "cer": 0.125},
    {"wer": 0.000, "cer": 0.000}
  ]
}
```

---

## Filler Tags

Filler tags are annotations in transcripts that mark disfluent speech —
pauses, repetitions, filled pauses. Common examples:

- `[uh]` — filled pause
- `[um]` — filled pause
- `[eh]` — filled pause
- `[ah]` — filled pause

The toolkit detects and counts filler tags in hypothesis transcripts by
default using the pattern `\[(uh|um|eh|ah)\]`. You can customize this with
`--filler-pattern`:

```bash
asr-eval --ref ref.txt --hyp hyp.txt --filler-pattern '\[(uh|um|eh|ah|mm|oh|mhm)\]'
```

Why this matters: undetected filler tags in training data can bias ASR models
and inflate evaluation metrics. Catching them before training is the whole
point of the annotation QA feature.

---

## Extending the Toolkit

The toolkit is designed to be small and readable. You can extend it by:

### Adding a new metric

Add a function to `asr_eval_toolkit/scoring.py` and document it. Keep it
tested and dependency-free.

```python
def my_new_metric(ref, hyp) -> float:
    """My new metric. Returns a float."""
    ...
```

### Adding a new output format

Add a writer function and hook it into the CLI's `--format` option.

### Custom filler patterns

Use the `--filler-pattern` CLI option or pass `filler_pattern` to `score_file()`.
Any valid regex that captures groups works.

---

## Citing

If you use this toolkit in published research, please cite:

```bibtex
@software{asr_eval_toolkit2026,
  author = {Saravanan, Veyhthan},
  title = {{asr-eval-toolkit: ASR Scoring and Annotation QA Toolkit}},
  version = {0.1.0},
  year = {2026},
  url = {https://github.com/veyhthan/asr-eval-toolkit},
  license = {MIT}
}
```

A `CITATION.cff` file is included in the repository for automated citation.
