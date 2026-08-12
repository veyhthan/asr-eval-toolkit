"""ASR scoring core: WER/CER via edit distance, filler tag detection.

Provides the scoring primitives used by the asr-eval-toolkit CLI and API.
"""

import re
from collections import Counter
from typing import List, Tuple


def edit_distance(a: List[str], b: List[str]) -> int:
    """Levenshtein edit distance between two token lists.

    Args:
        a: First sequence of tokens (words or characters).
        b: Second sequence of tokens.

    Returns:
        Minimum number of insertions, deletions, or substitutions to turn a into b.

    """
    la, lb = len(a), len(b)
    dp = list(range(lb + 1))
    for i in range(1, la + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, lb + 1):
            temp = dp[j]
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
            prev = temp
    return dp[lb]


def tokenize(text: str) -> List[str]:
    """Split text into word tokens, lowercased.

    Args:
        text: Input text.

    Returns:
        List of word tokens, lowercased.

    """
    return re.findall(r"\S+", text.lower())


def score_pair(ref: str, hyp: str) -> Tuple[float, float]:
    """Score a single reference/hypothesis pair.

    Computes word error rate (WER) and character error rate (CER) for one pair.
    CER is case-insensitive by default (lowercased before comparison).

    Args:
        ref: Reference transcription.
        hyp: Hypothesis (ASR output) transcription.

    Returns:
        Tuple of (wer, cer). Both are floats in [0, inf).

    """
    rt, ht = tokenize(ref), tokenize(hyp)

    # WER
    wer = (1.0 if len(ht) > 0 else 0.0) if len(rt) == 0 else edit_distance(rt, ht) / len(rt)

    # CER (case-insensitive: lowercase before char comparison)
    rc = list(ref.lower().replace(" ", ""))
    hc = list(hyp.lower().replace(" ", ""))

    cer = (1.0 if len(hc) > 0 else 0.0) if len(rc) == 0 else edit_distance(rc, hc) / len(rc)

    return wer, cer


def score_file(
    ref_path: str,
    hyp_path: str,
    filler_pattern: str = r"\[(uh|um|eh|ah)\]",
) -> dict:
    """Score all utterance pairs from two transcript files.

    Reads reference and hypothesis files (one utterance per line, matched by
    position) and returns aggregate statistics including WER, CER, and filler
    tag counts.

    Args:
        ref_path: Path to reference transcript file.
        hyp_path: Path to hypothesis transcript file.
        filler_pattern: Regex pattern for filler tags to detect. Defaults to
            common spoken fillers [uh], [um], [eh], [ah].

    Returns:
        Dictionary with:
            - utterances: number of utterance pairs scored (min of ref/hyp lines)
            - mean_wer: mean WER across all pairs (0.0 if no pairs)
            - mean_cer: mean CER across all pairs (0.0 if no pairs)
            - filler_counts: dict mapping filler tag to count
            - per_utterance: list of dicts with wer, cer per pair

    """
    with open(ref_path, encoding="utf-8") as f:
        refs = f.read().splitlines()
    with open(hyp_path, encoding="utf-8") as f:
        hyps = f.read().splitlines()

    wers, cers = [], []
    filler = Counter()
    per_utterance: List[dict] = []

    for r, h in zip(refs, hyps):
        w, c = score_pair(r, h)
        wers.append(w)
        cers.append(c)
        per_utterance.append({"wer": w, "cer": c})
        for m in re.findall(filler_pattern, h):
            filler[m] += 1

    n = len(per_utterance)
    if n == 0:
        return {
            "utterances": 0,
            "mean_wer": 0.0,
            "mean_cer": 0.0,
            "filler_counts": {},
            "per_utterance": [],
        }

    return {
        "utterances": n,
        "mean_wer": sum(wers) / n,
        "mean_cer": sum(cers) / n,
        "filler_counts": dict(filler) or {},
        "per_utterance": per_utterance,
    }


def write_report(stats: dict, out_path: str = "report.md") -> str:
    """Write a scoring report to a markdown file.

    Args:
        stats: Dictionary returned by score_file().
        out_path: Output file path. Defaults to "report.md".

    Returns:
        Path to the written report file.

    """
    lines = [
        "# ASR scoring report",
        "",
        f"- Utterances: {stats['utterances']}",
        f"- Mean WER: {stats['mean_wer']:.3f}",
        f"- Mean CER: {stats['mean_cer']:.3f}",
    ]

    if stats["filler_counts"]:
        counts = ", ".join(f"'{k}': {v}" for k, v in stats["filler_counts"].items())
        lines.append(f"- Filler tags seen: {{{counts}}}")
    else:
        lines.append("- Filler tags seen: none")

    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return out_path
