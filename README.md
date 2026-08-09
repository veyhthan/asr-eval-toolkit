# asr-eval-toolkit

A small, transparent toolkit for scoring automatic speech recognition (ASR)
output and auditing annotation quality. Built for students and independent
researchers who need reproducible, scriptable evaluation without paying for a
closed lab platform.

## What it does

- Scores ASR transcripts against reference text using WER/CER and a few
  agreement metrics.
- Flags annotation inconsistencies (filler tags, timestamp spacing, speaker
  boundaries) so human reviewers can fix them before training.
- Runs as a single command, outputs a short markdown report.

## Why

Most evaluation tooling is locked behind paid labs or built for large teams.
This gives solo researchers and small academic groups a pipeline they can read,
audit, and extend.

## Usage

```bash
python score.py --ref ref.txt --hyp hyp.txt --out report.md
```

## Status

Early, maintained alongside coursework. Contributions and issue reports welcome.
