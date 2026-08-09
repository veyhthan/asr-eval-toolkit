#!/usr/bin/env python3
"""Minimal ASR scoring helper: WER/CER + annotation flag report.

Usage:
    python score.py --ref ref.txt --hyp hyp.txt --out report.md
"""
import argparse
import re
from collections import Counter


def edit_distance(a, b):
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


def tokenize(text):
    return re.findall(r"\S+", text.lower())


def score_pair(ref, hyp):
    rt, ht = tokenize(ref), tokenize(hyp)
    wer = edit_distance(rt, ht) / max(len(rt), 1)
    rc, hc = list(ref.replace(" ", "")), list(hyp.replace(" ", ""))
    cer = edit_distance(rc, hc) / max(len(rc), 1)
    return wer, cer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--hyp", required=True)
    ap.add_argument("--out", default="report.md")
    args = ap.parse_args()

    with open(args.ref, encoding="utf-8") as f:
        refs = f.read().splitlines()
    with open(args.hyp, encoding="utf-8") as f:
        hyps = f.read().splitlines()

    wers, cers = [], []
    filler = Counter()
    for r, h in zip(refs, hyps):
        w, c = score_pair(r, h)
        wers.append(w)
        cers.append(c)
        for m in re.findall(r"\[(uh|um|eh|ah)\]", h):
            filler[m] += 1

    n = max(len(refs), 1)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("# ASR scoring report\n\n")
        f.write(f"- Utterances: {n}\n")
        f.write(f"- Mean WER: {sum(wers)/n:.3f}\n")
        f.write(f"- Mean CER: {sum(cers)/n:.3f}\n")
        f.write(f"- Filler tags seen: {dict(filler) or 'none'}\n")

    print(f"Wrote {args.out}: mean WER {sum(wers)/n:.3f}")


if __name__ == "__main__":
    main()
