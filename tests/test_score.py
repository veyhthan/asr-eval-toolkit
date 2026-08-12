#!/usr/bin/env python3
"""Tests for score.py scoring helpers."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from score import edit_distance, score_pair, tokenize  # noqa: E402


def test_edit_distance_identical():
    """Identical sequences have zero edit distance."""
    assert edit_distance(list("abc"), list("abc")) == 0


def test_edit_distance_substitution():
    """One substitution costs 1."""
    assert edit_distance(list("abc"), list("axc")) == 1


def test_edit_distance_insertion():
    """One insertion costs 1."""
    assert edit_distance(list("ab"), list("abc")) == 1


def test_tokenize_lowercases_and_splits():
    """Tokenize lowercases and splits on whitespace."""
    assert tokenize("Hello World") == ["hello", "world"]


def test_score_pair_perfect():
    """Perfect match gives WER=0, CER=0."""
    wer, cer = score_pair("the cat sat", "the cat sat")
    assert wer == 0.0
    assert cer == 0.0


def test_score_pair_partial():
    """Partial match gives fractional WER."""
    wer, cer = score_pair("a b c", "a b")
    assert wer == 1 / 3
    assert 0.0 < cer < 1.0


if __name__ == "__main__":
    test_edit_distance_identical()
    test_edit_distance_substitution()
    test_edit_distance_insertion()
    test_tokenize_lowercases_and_splits()
    test_score_pair_perfect()
    test_score_pair_partial()
    print("All tests passed.")
