"""asr-eval-toolkit: ASR scoring and annotation QA toolkit for researchers."""

from .scoring import edit_distance, score_file, score_pair, tokenize, write_report

__version__ = "0.1.0"
__author__ = "Veyhthan Saravanan"
__email__ = "veyhthan@gmail.com"
__description__ = "ASR scoring and annotation QA toolkit for researchers"
__url__ = "https://github.com/veyhthan/asr-eval-toolkit"

__all__ = [
    "edit_distance",
    "tokenize",
    "score_pair",
    "score_file",
    "write_report",
]
