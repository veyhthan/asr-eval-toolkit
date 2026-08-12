# API Reference

## Table of Contents

- [`asr_eval_toolkit`](#asr_eval_toolkit)
  - [`score_pair()`](#score_pairref-hyp---wer-cer)
  - [`score_file()`](#score_fileref_path-hyp_path-filler_pattern---dict)
  - [`write_report()`](#write_reportstats-out_path----str)
  - [`edit_distance()`](#edit_distancea-b---int)
  - [`tokenize()`](#tokenizetext---liststr)
- [`asr_eval_toolkit.cli`](#asr_eval_toolkitcli)
  - [`main()`](#main--)
- [Return Types](#return-types)

---

## `asr_eval_toolkit`

```python
import asr_eval_toolkit
```

### Attributes

| Name | Type | Description |
|------|------|-------------|
| `__version__` | `str` | Package version (`"0.1.0"`) |
| `__author__` | `str` | Author name |
| `__email__` | `str` | Author email |
| `__description__` | `str` | Package description |
| `__url__` | `str` | Repository URL |

### `__all__`

```python
asr_eval_toolkit.__all__ = [
    "edit_distance",
    "tokenize",
    "score_pair",
    "score_file",
    "write_report",
]
```

---

## `score_pair(ref, hyp) -> (wer, cer)`

Score a single reference/hypothesis pair. Computes word error rate (WER) and
character error rate (CER).

```python
from asr_eval_toolkit.scoring import score_pair

wer, cer = score_pair("the cat sat", "the cat mat")
# wer = 0.333..., cer = 0.043...
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `ref` | `str` | Reference transcription |
| `hyp` | `str` | Hypothesis (ASR output) transcription |

**Returns:** `tuple[float, float]` — `(wer, cer)`. Both are non-negative floats.

**Notes:**
- WER is case-insensitive (text is lowercased before tokenization)
- CER is case-insensitive (characters are lowercased before comparison)
- Empty reference with empty hypothesis returns `(0.0, 0.0)`
- Empty reference with non-empty hypothesis returns `(1.0, 1.0)`
- WER denominator is the number of reference tokens
- CER denominator is the number of reference characters (spaces removed)

---

## `score_file(ref_path, hyp_path, filler_pattern=None) -> dict`

Score all utterance pairs from two transcript files. Reads reference and
hypothesis files (one utterance per line, matched by position) and returns
aggregate statistics.

```python
from asr_eval_toolkit.scoring import score_file

stats = score_file("ref.txt", "hyp.txt")
print(stats)
# {
#     'utterances': 4,
#     'mean_wer': 0.132,
#     'mean_cer': 0.092,
#     'filler_counts': {'uh': 1, 'um': 1},
#     'per_utterance': [
#         {'wer': 0.143, 'cer': 0.043},
#         ...
#     ]
# }
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `ref_path` | `str` | Path to reference transcript file |
| `hyp_path` | `str` | Path to hypothesis transcript file |
| `filler_pattern` | `str` or `None` | Regex pattern for filler tag detection. Defaults to `r"\[(uh|um|eh|ah)\]"`. Pass `None` to disable filler detection. |

**Returns:** `dict` with the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `utterances` | `int` | Number of utterance pairs scored (min of ref/hyp lines) |
| `mean_wer` | `float` | Mean WER across all pairs (0.0 if no pairs) |
| `mean_cer` | `float` | Mean CER across all pairs (0.0 if no pairs) |
| `filler_counts` | `dict[str, int]` | Mapping of filler tag to count (empty dict if none) |
| `per_utterance` | `list[dict]` | List of `{"wer": float, "cer": float}` per pair |

**Raises:**
- `FileNotFoundError` if either file does not exist
- `UnicodeDecodeError` if files are not valid UTF-8

**Notes:**
- Lines are matched by position (zip behavior — stops at shorter file)
- If both files are empty, returns `utterances=0`, `mean_wer=0.0`, `mean_cer=0.0`
- Filler detection uses `re.findall()` with the provided pattern; capture groups are counted

---

## `write_report(stats, out_path="report.md") -> str`

Write a scoring report to a markdown file.

```python
from asr_eval_toolkit.scoring import score_file, write_report

stats = score_file("ref.txt", "hyp.txt")
path = write_report(stats, "report.md")
# path == "report.md"
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `stats` | `dict` | Dictionary returned by `score_file()` |
| `out_path` | `str` | Output file path. Defaults to `"report.md"` |

**Returns:** `str` — the path to the written file.

**Output format:**

```markdown
# ASR scoring report

- Utterances: 4
- Mean WER: 0.132
- Mean CER: 0.092
- Filler tags seen: {'uh': 1, 'um': 1}
```

When no filler tags are found, the last line reads `- Filler tags seen: none`.

---

## `edit_distance(a, b) -> int`

Levenshtein edit distance between two token lists. Computes the minimum number
of insertions, deletions, and substitutions needed to transform sequence `a`
into sequence `b`.

```python
from asr_eval_toolkit.scoring import edit_distance

dist = edit_distance(list("kitten"), list("sitting"))
# dist = 3
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `a` | `list[str]` | First sequence of tokens |
| `b` | `list[str]` | Second sequence of tokens |

**Returns:** `int` — the edit distance.

**Notes:**
- Works on any list of strings, not just characters
- O(len(a) * len(b)) time and O(min(len(a), len(b))) space
- Used internally by `score_pair()` for WER and CER computation

---

## `tokenize(text) -> list[str]`

Split text into word tokens, lowercased.

```python
from asr_eval_toolkit.scoring import tokenize

tokens = tokenize("Hello, World!")
# tokens = ["hello,", "world!"]
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `text` | `str` | Input text |

**Returns:** `list[str]` — list of word tokens, lowercased.

**Notes:**
- Uses `\S+` regex — tokens are runs of non-whitespace
- Punctuation stays attached to words (e.g., `"hello,"` not `"hello"`)
- Empty string returns `[]`
- Whitespace-only string returns `[]`

---

## `asr_eval_toolkit.cli`

The command-line interface module.

### `main()`

Entry point for the `asr-eval` console script. Parses CLI arguments, scores
the transcript files, and writes the report.

```bash
asr-eval --ref ref.txt --hyp hyp.txt --out report.md
```

Called automatically when you run `asr-eval` after installing the package.
Rarely called directly from Python.

---

## Return Types Summary

| Function | Return Type |
|----------|-------------|
| `score_pair()` | `tuple[float, float]` |
| `score_file()` | `dict` |
| `write_report()` | `str` |
| `edit_distance()` | `int` |
| `tokenize()` | `list[str]` |
| `main()` | `None` |

---

## Type Hints

All public functions are fully type-hinted. The package is compatible with
static type checkers like mypy:

```bash
pip install mypy
mypy asr_eval_toolkit/
```

The `pyproject.toml` includes a `[tool.mypy]` section with recommended settings.
