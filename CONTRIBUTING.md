## LaTeX

A LaTeX dirstribution is required. Download one [here](https://www.latex-project.org/get/)

## Python

Python 3 with `pymupdf` is required for the pre-save checks (`scripts/check_line_fill.py`, `scripts/check_page_fill.py`). Install with `pip install pymupdf`.

## Extensions

LaTeX Workshop

## Scripts

Set your name in the variable `destName` in ./scripts/rename-pdf.ps1 script.

`scripts/save.ps1` runs three pre-save checks before saving:
- `pre-save.ps1` blocks unreviewed (asterisk-marked) draft bullets.
- `check_line_fill.py` compiles the draft and blocks any wrapped line whose last line is under 50% full (e.g. a bullet wrapping down to a single short word).
- `check_page_fill.py` compiles the draft and blocks the save if it spans more than one page, or if the page is left mostly blank at the bottom (under 90% of the usable page height by default). The page-break boundary isn't hardcoded — it's queried directly from pdfLaTeX by compiling a throwaway probe that reuses `draft.tex`'s own preamble, so it stays correct if the template's margins ever change.

Fix the flagged issue in `draft.tex` and rerun the save.
