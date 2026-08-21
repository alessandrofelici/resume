"""
Enforces the one-page rule and flags a resume PDF that leaves too much
blank space at the bottom of the page.

The page-break boundary isn't guessed or hardcoded: it's queried straight
from pdfLaTeX by compiling a throwaway probe that reuses draft.tex's own
preamble (so it tracks any future margin/geometry changes automatically)
and has it \typeout the exact lengths (\textheight, \topmargin, etc.) that
determine where LaTeX will actually break to a second page.

Usage: python check_page_fill.py <pdf-path> [--tex draft.tex] [--threshold 0.90]
Exit code: 0 = clean, 1 = overflow or underfilled page, 2 = error.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# TeX's own inch (72.27pt) vs a PDF "point"/bp (72pt) -- the ~0.4% factor
# that converts \typeout'd TeX lengths into the same units pymupdf reports.
PT_TO_BP = 72.0 / 72.26999

PROBE_TEMPLATE = r"""
\begin{{document}}
\typeout{{PAGEGEOM:voffset=\the\voffset|topmargin=\the\topmargin|headheight=\the\headheight|headsep=\the\headsep|textheight=\the\textheight}}
\end{{document}}
"""


def get_body_bounds_bp(tex_path):
    """Compile a probe sharing draft.tex's preamble; return (top_bp, bottom_bp)
    of the text area in PDF-point units, i.e. the exact box LaTeX paginates
    against."""
    src = Path(tex_path).read_text(encoding="utf-8")
    marker = r"\begin{document}"
    idx = src.find(marker)
    if idx == -1:
        raise ValueError(f"no \\begin{{document}} found in {tex_path}")
    preamble = src[:idx]

    build_dir = Path(tex_path).resolve().parent / "build"
    build_dir.mkdir(exist_ok=True)
    probe_path = build_dir / "_pagegeom_probe.tex"
    probe_path.write_text(preamble + PROBE_TEMPLATE, encoding="utf-8")

    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(build_dir), str(probe_path)],
            capture_output=True, text=True,
        )
        log_path = probe_path.with_suffix(".log")
        log_text = log_path.read_text(encoding="utf-8", errors="ignore") if log_path.exists() else result.stdout
        match = re.search(
            r"PAGEGEOM:voffset=([\d.-]+)pt\|topmargin=([\d.-]+)pt\|headheight=([\d.-]+)pt\|headsep=([\d.-]+)pt\|textheight=([\d.-]+)pt",
            log_text.replace("\n", ""),
        )
        if not match:
            raise ValueError("could not find PAGEGEOM marker in probe log; probe compile likely failed")
        voffset, topmargin, headheight, headsep, textheight = (float(g) for g in match.groups())
    finally:
        for ext in (".tex", ".log", ".aux", ".pdf"):
            p = probe_path.with_suffix(ext)
            if p.exists():
                p.unlink()

    one_inch_pt = 72.26999
    top_pt = one_inch_pt + voffset + topmargin + headheight + headsep
    bottom_pt = top_pt + textheight
    return top_pt * PT_TO_BP, bottom_pt * PT_TO_BP


def check_pdf(pdf_path, tex_path, threshold):
    import pymupdf

    top_bp, bottom_bp = get_body_bounds_bp(tex_path)
    usable_height = bottom_bp - top_bp

    doc = pymupdf.open(pdf_path)
    if len(doc) > 1:
        return {"overflow": True, "pages": len(doc)}

    page = doc[0]
    d = page.get_text("dict")
    bottoms = [b["bbox"][3] for b in d["blocks"] if "lines" in b]
    if not bottoms:
        return {"overflow": False, "fill_ratio": 0.0, "gap_in": usable_height / 72}

    content_bottom = max(bottoms)
    fill_ratio = (content_bottom - top_bp) / usable_height
    gap_in = (bottom_bp - content_bottom) / 72

    return {
        "overflow": False,
        "fill_ratio": fill_ratio,
        "gap_in": gap_in,
        "flagged": fill_ratio < threshold,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_path")
    parser.add_argument("--tex", default="draft.tex")
    parser.add_argument("--threshold", type=float, default=0.90)
    args = parser.parse_args()

    try:
        result = check_pdf(args.pdf_path, args.tex, args.threshold)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 2
    except ImportError:
        print("Error: pymupdf is not installed. Run: pip install pymupdf")
        return 2
    except ValueError as e:
        print(f"Error: {e}")
        return 2

    if result["overflow"]:
        print(f"Page-fill check failed: resume spans {result['pages']} pages (must be exactly 1). Trim content.")
        return 1

    if result["flagged"]:
        print(
            f"Page-fill check failed: page is only {result['fill_ratio']:.0%} full "
            f"({result['gap_in']:.2f}in of blank space at the bottom, threshold {threshold_pct(args.threshold)})."
        )
        print("Add more content (or extend existing bullets) to fill the page, then save again.")
        return 1

    print(f"Page-fill check passed: page is {result['fill_ratio']:.0%} full, 1 page.")
    return 0


def threshold_pct(t):
    return f"{t:.0%}"


if __name__ == "__main__":
    sys.exit(main())
