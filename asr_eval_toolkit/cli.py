#!/usr/bin/env python3
"""Command-line interface for asr-eval-toolkit.

Usage:
    asr-eval --ref ref.txt --hyp hyp.txt [--out report.md]

Install via: pip install asr-eval-toolkit
Then run: asr-eval --ref ref.txt --hyp hyp.txt
"""

import argparse
import sys

from .scoring import score_file, write_report


def main() -> None:
    """Score ASR transcripts and audit annotation quality."""
    ap = argparse.ArgumentParser(
        prog="asr-eval",
        description="Score ASR transcripts and audit annotation quality.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  asr-eval --ref ref.txt --hyp hyp.txt
  asr-eval --ref ref.txt --hyp hyp.txt --out results.md
  asr-eval --ref ref.txt --hyp hyp.txt --out results.md --format json
        """,
    )

    ap.add_argument(
        "--ref",
        required=True,
        help="Reference transcript file (one utterance per line)",
    )
    ap.add_argument(
        "--hyp",
        required=True,
        help="Hypothesis / ASR output transcript file (one utterance per line)",
    )
    ap.add_argument(
        "--out",
        default="report.md",
        help="Output report path (default: report.md)",
    )
    ap.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Output format (default: md)",
    )
    ap.add_argument(
        "--filler-pattern",
        default=r"\[(uh|um|eh|ah)\]",
        help="Regex pattern for filler tags to detect (default: spoken fillers)",
    )

    args = ap.parse_args()

    try:
        stats = score_file(args.ref, args.hyp, args.filler_pattern)
    except FileNotFoundError as e:
        print(f"Error: file not found — {e.filename}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        import json

        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
        print(
            f"Wrote {args.out}: "
            f"{stats['utterances']} utterances, "
            f"mean WER {stats['mean_wer']:.3f}"
        )
    else:
        write_report(stats, args.out)
        print(
            f"Wrote {args.out}: "
            f"{stats['utterances']} utterances, "
            f"mean WER {stats['mean_wer']:.3f}"
        )


if __name__ == "__main__":
    main()
