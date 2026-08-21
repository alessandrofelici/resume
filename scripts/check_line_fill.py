"""
Flags wrapped lines in a compiled resume PDF whose last visual line is
under a fill-ratio threshold relative to the column's right margin
(e.g. a bullet that wraps down to a single short word).

Usage: python check_line_fill.py <pdf-path> [--threshold 0.5]
Exit code: 0 = clean, 1 = flagged lines found, 2 = error (bad path / missing pymupdf).
"""

import argparse
import re
import sys

Y_TOLERANCE = 1.5   # points; lines within this y0 delta are treated as the same row
X_TOLERANCE = 1.0   # points; slack when comparing a line's x0 to its run's starting x0
BULLET_CHARS = ("•", "-", "*")


def is_bold(font_name):
    return bool(re.search(r"bold|bx", font_name, re.I))


def merge_rows(lines):
    """Group dict-mode 'lines' that share a y0 (same physical row, different
    tabular columns) into rows. Returns rows in original order, each tagged
    multi=True if it merged 2+ line entries (never a wrap candidate)."""
    rows = []
    for line in lines:
        bbox = line["bbox"]
        spans = line["spans"]
        if not spans:
            continue
        text = "".join(s["text"] for s in spans)
        entry = {
            "y0": bbox[1], "y1": bbox[3],
            "x0": bbox[0], "x1": bbox[2],
            "text": text, "font": spans[0]["font"],
        }
        if rows and abs(rows[-1]["_last_y0"] - entry["y0"]) <= Y_TOLERANCE:
            rows[-1]["multi"] = True
            rows[-1]["x1"] = max(rows[-1]["x1"], entry["x1"])
        else:
            rows.append({**entry, "multi": False, "_last_y0": entry["y0"]})
    return rows


def build_runs(page_dict):
    """Walk the page's blocks/rows and group consecutive single-segment rows
    into wrap-runs (one entry per LaTeX paragraph that word-wrapped)."""
    runs = []
    for block in page_dict["blocks"]:
        if "lines" not in block:
            continue
        rows = merge_rows(block["lines"])
        current_run = []
        run_start_x0 = None
        prev_multi = True
        for row in rows:
            if row["multi"]:
                if current_run:
                    runs.append(current_run)
                current_run = []
                prev_multi = True
                continue

            starts_bullet = row["text"].lstrip().startswith(BULLET_CHARS)
            continues = (
                current_run
                and not prev_multi
                and not starts_bullet
                and not is_bold(row["font"])
                and row["x0"] >= run_start_x0 - X_TOLERANCE
            )
            if continues:
                current_run.append(row)
            else:
                if current_run:
                    runs.append(current_run)
                current_run = [row]
                run_start_x0 = row["x0"]
            prev_multi = False
        if current_run:
            runs.append(current_run)
    return runs


def check_pdf(pdf_path, threshold):
    import pymupdf

    doc = pymupdf.open(pdf_path)
    flagged = []
    for page_no, page in enumerate(doc, start=1):
        d = page.get_text("dict")
        runs = build_runs(d)

        all_x1 = [
            row["x1"]
            for block in d["blocks"] if "lines" in block
            for row in merge_rows(block["lines"])
        ]
        if not all_x1:
            continue
        right_margin = max(all_x1)

        for run in runs:
            if len(run) < 2:
                continue
            last = run[-1]
            available = right_margin - last["x0"]
            if available <= 0:
                continue
            fill_ratio = (last["x1"] - last["x0"]) / available
            if fill_ratio < threshold:
                flagged.append((page_no, fill_ratio, last["text"]))
    return flagged


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_path")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    try:
        flagged = check_pdf(args.pdf_path, args.threshold)
    except FileNotFoundError:
        print(f"Error: PDF not found at {args.pdf_path}")
        return 2
    except ImportError:
        print("Error: pymupdf is not installed. Run: pip install pymupdf")
        return 2

    if not flagged:
        print("Line-fill check passed: no sparse wrapped lines found.")
        return 0

    print(f"Line-fill check failed: {len(flagged)} wrapped line(s) under {int(args.threshold * 100)}% fill.")
    for page_no, ratio, text in flagged:
        print(f"  p{page_no} ({ratio:.0%} full): \"{text}\"")
    print("Tighten or extend the wording of these bullets so the wrap isn't left mostly empty, then save again.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
