# asr-eval-toolkit

A small, transparent toolkit for scoring ASR transcripts and auditing annotation quality.

Built for students, researchers, and small teams who need reproducible evaluation without a closed lab platform.

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

## Documentation

- [Usage Guide](usage.md) — installation, quick start, CLI reference, Python API, input/output formats, filler tags
- [API Reference](api.md) — detailed function signatures, parameters, return types, type checking info
