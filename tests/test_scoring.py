"""Tests for asr_eval_toolkit.scoring.

Run with: pytest tests/
Or: python -m pytest tests/
"""

import importlib.util
import sys
from pathlib import Path

import pytest

# Load the package from the local source tree
spec = importlib.util.spec_from_file_location(
    "asr_eval_toolkit",
    Path(__file__).resolve().parents[1] / "asr_eval_toolkit" / "__init__.py",
)
pkg = importlib.util.module_from_spec(spec)
sys.modules["asr_eval_toolkit"] = pkg
spec.loader.exec_module(pkg)

from asr_eval_toolkit.scoring import (  # noqa: E402
    edit_distance,
    score_file,
    score_pair,
    tokenize,
    write_report,
)

# --- edit_distance ---


class TestEditDistance:
    def test_identical(self):
        assert edit_distance(list("abc"), list("abc")) == 0

    def test_substitution(self):
        assert edit_distance(list("abc"), list("axc")) == 1

    def test_insertion(self):
        assert edit_distance(list("ab"), list("abc")) == 1

    def test_deletion(self):
        assert edit_distance(list("abc"), list("ac")) == 1

    def test_empty_a(self):
        assert edit_distance([], list("abc")) == 3

    def test_empty_b(self):
        assert edit_distance(list("abc"), []) == 3

    def test_both_empty(self):
        assert edit_distance([], []) == 0

    def test_longer_sequences(self):
        a = list("kitten")
        b = list("sitting")
        # k->s (1), e->i (1), insert g (1) = 3
        assert edit_distance(a, b) == 3


# --- tokenize ---


class TestTokenize:
    def test_basic(self):
        assert tokenize("Hello World") == ["hello", "world"]

    def test_single_word(self):
        assert tokenize("hello") == ["hello"]

    def test_punctuation_stays(self):
        assert tokenize("hello, world!") == ["hello,", "world!"]

    def test_empty(self):
        assert tokenize("") == []

    def test_whitespace_only(self):
        assert tokenize("   \t\n") == []

    def test_multiline(self):
        assert tokenize("hello\nworld") == ["hello", "world"]


# --- score_pair ---


class TestScorePair:
    def test_perfect_match(self):
        wer, cer = score_pair("the cat sat", "the cat sat")
        assert wer == pytest.approx(0.0)
        assert cer == pytest.approx(0.0)

    def test_single_word_substitution(self):
        wer, cer = score_pair("cat", "bat")
        assert wer == pytest.approx(1.0)
        assert cer > 0.0

    def test_partial_wer(self):
        wer, cer = score_pair("a b c", "a b")
        assert wer == pytest.approx(1 / 3)
        assert 0.0 < cer < 1.0

    def test_case_insensitive(self):
        wer, cer = score_pair("Hello World", "hello world")
        assert wer == pytest.approx(0.0)
        assert cer == pytest.approx(0.0)

    def test_empty_hyp(self):
        wer, cer = score_pair("hello world", "")
        assert wer == pytest.approx(1.0)
        assert cer == pytest.approx(1.0)

    def test_empty_ref(self):
        wer, cer = score_pair("", "hello world")
        assert wer == pytest.approx(1.0)

    def test_returns_tuple_of_two(self):
        result = score_pair("a b", "c d")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(x, float) for x in result)


# --- score_file ---


class TestScoreFile:
    def test_basic(self, tmp_path):
        ref = tmp_path / "ref.txt"
        hyp = tmp_path / "hyp.txt"
        ref.write_text("the cat sat\nhello world\n")
        hyp.write_text("the cat mat\nhello word\n")

        stats = score_file(str(ref), str(hyp))

        assert stats["utterances"] == 2
        assert stats["mean_wer"] > 0.0
        assert stats["mean_cer"] > 0.0
        assert "filler_counts" in stats
        assert "per_utterance" in stats
        assert len(stats["per_utterance"]) == 2

    def test_filler_detection(self, tmp_path):
        ref = tmp_path / "ref.txt"
        hyp = tmp_path / "hyp.txt"
        ref.write_text("the patient presented\n")
        hyp.write_text("the patient [uh] presented\n")

        stats = score_file(str(ref), str(hyp))

        assert stats["filler_counts"] == {"uh": 1}

    def test_no_filler(self, tmp_path):
        ref = tmp_path / "ref.txt"
        hyp = tmp_path / "hyp.txt"
        ref.write_text("hello world\n")
        hyp.write_text("hello world\n")

        stats = score_file(str(ref), str(hyp))

        assert stats["filler_counts"] == {}

    def test_mismatched_lines(self, tmp_path):
        ref = tmp_path / "ref.txt"
        hyp = tmp_path / "hyp.txt"
        ref.write_text("line1\nline2\nline3\n")
        hyp.write_text("line1\nline2\n")

        stats = score_file(str(ref), str(hyp))

        assert stats["utterances"] == 2  # zip stops at shorter

    def test_empty_files(self, tmp_path):
        ref = tmp_path / "ref.txt"
        hyp = tmp_path / "hyp.txt"
        ref.write_text("")
        hyp.write_text("")

        stats = score_file(str(ref), str(hyp))

        assert stats["utterances"] == 0
        assert stats["mean_wer"] == 0.0


# --- write_report ---


class TestWriteReport:
    def test_writes_file(self, tmp_path):
        stats = {
            "utterances": 4,
            "mean_wer": 0.132,
            "mean_cer": 0.092,
            "filler_counts": {"uh": 1, "um": 1},
            "per_utterance": [],
        }
        out = tmp_path / "report.md"
        path = write_report(stats, str(out))

        assert Path(path).exists()
        content = out.read_text()
        assert "ASR scoring report" in content
        assert "0.132" in content
        assert "0.092" in content

    def test_no_filler(self, tmp_path):
        stats = {
            "utterances": 1,
            "mean_wer": 0.0,
            "mean_cer": 0.0,
            "filler_counts": {},
            "per_utterance": [],
        }
        out = tmp_path / "report.md"
        write_report(stats, str(out))

        content = out.read_text()
        assert "none" in content.lower()
