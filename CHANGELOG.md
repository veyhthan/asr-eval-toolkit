# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-12

### Added
- Initial public release of asr-eval-toolkit
- WER (Word Error Rate) and CER (Character Error Rate) scoring via edit distance
- Filler tag detection and counting ([uh], [um], [eh], [ah])
- Markdown report output with aggregate and per-utterance statistics
- Python standard library only — no third-party dependencies
- Command-line interface (`asr-eval`)
- Scores via Python API (`asr_eval_toolkit.scoring`)
- Test suite with pytest
- GitHub Actions CI on Python 3.8 and 3.11
- CONTRIBUTING.md with contribution guide
- CODE_OF_CONDUCT.md (Contributor Covenant 2.1)
- SECURITY.md with vulnerability reporting process
- CITATION.cff for academic citation
- pyproject.toml with full Python package metadata
- PyPI installability (`pip install asr-eval-toolkit`)
- GitHub topics: asr, speech-recognition, evaluation, nlp, python, wer, cer, annotation-qa, speech, transcription

### Known Limitations
- Per-utterance detail in report output is not yet available
- TSV/CSV export for pipeline integration not yet available
- Timestamp annotation checking not yet available
- Speaker boundary flagging not yet available
