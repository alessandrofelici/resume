## LaTeX

A LaTeX dirstribution is required. Download one [here](https://www.latex-project.org/get/)

## Python

Python 3 with `pymupdf` is required for the pre-save checks (`scripts/check_line_fill.py`, `scripts/check_page_fill.py`). Install with `pip install pymupdf`.

## Extensions

LaTeX Workshop

## Scripts

Set your name in the variable `destName` in ./scripts/rename-pdf.ps1 script.

## Pre-Save Hooks

`scripts/save.ps1` runs a sequence of pre-save hooks before it will copy `draft.tex` into `saved-resumes/`. Each hook is a standalone script that exits non-zero to block the save; `save.ps1` stops at the first failure, prints why, and leaves `saved-resumes/` untouched. Fix the flagged issue in `draft.tex` and rerun the save.

### Existing hooks

- **Draft review gate** (`pre-save.ps1`) — blocks the save if any `\resumeItem{*...}` still has its leading review asterisk. Per `CLAUDE.md`'s Draft Review rule, only you may remove that asterisk, so this hook stops an AI-drafted or AI-edited bullet from being saved before you've actually looked at it.

- **Page saturation hooks** (`check_line_fill.py`, `check_page_fill.py`) — catch wasted whitespace at two different scales:
  - `check_line_fill.py` compiles the draft and inspects the rendered PDF's actual glyph geometry (via PyMuPDF) to find wrapped lines whose last line is under 50% full — e.g. a bullet that wraps down to a single short word. It groups visual lines back into paragraphs (telling a real wrap apart from a tabular date column or a new bold-labeled skills field) before checking fill.
  - `check_page_fill.py` compiles the draft and enforces the one-page rule, plus flags a page that's left mostly blank at the bottom (under 90% of the usable page height by default). The page-break boundary isn't hardcoded — it's queried directly from pdfLaTeX by compiling a throwaway probe that reuses `draft.tex`'s own preamble and has it report `\textheight`, `\topmargin`, etc., so the threshold stays correct even if the template's margins ever change.

### Adding your own hook

1. Write a standalone script (PowerShell or Python) that takes whatever input it needs — typically the compiled PDF path or `draftPath` — and exits `0` on pass, non-zero on fail, printing a clear reason plus what to do about it (match the tone of the existing hooks: state the problem, then how to fix it).
2. Wire it into `scripts/save.ps1` alongside the other hooks, **before** the `Copy-Item` step that writes into `saved-resumes/` — hooks only guard the save, they never run after. Follow the existing pattern:
   ```powershell
   & <your-hook> <args>
   if ($LASTEXITCODE -ne 0) {
       exit 1
   }
   ```
3. If your hook needs a fresh compile of `draft.tex`, reuse `$draftBuildDir` (already compiled to by the earlier hooks) rather than recompiling again.
4. Document the new hook in this section and, if it introduces a new dependency, add it under **Python** or **LaTeX** above.
