#!/usr/bin/env python3
"""OCR / text-layer triage for BIS Annual Report PDFs.

For every PDF under <root>/raw, reports per page: characters in the text
layer, image coverage, and a crude OCR-quality score (share of tokens
that are dictionary-like words), then aggregates per file.

Writes <root>/triage/pages.csv and <root>/triage/files.csv and prints a
summary table. Requires PyMuPDF (pip install pymupdf).

Usage:  python ocr_triage.py --root <corpus-root> [--lang en]
"""
import argparse
import csv
import re
import statistics
from pathlib import Path

import fitz  # PyMuPDF

# Small built-in stoplists: enough to separate real text from OCR noise.
WORDS = {
    "en": set("""the of and to in a is that for it as was with be by on not he this are or his from
    at which but have an had they you were their one all we can her has there been if more when
    will would who so no out up into than them its about may these two only time some over also
    year bank banks central gold credit market markets rate rates exchange currency monetary
    financial reserves deposits capital balance sheet report annual interest prices economic
    countries country policy international settlements board directors general meeting
    million per cent during period increase decrease total position foreign payments""".split()),
    "fr": set("""le la les de des du un une et en est que qui pour dans par sur au aux ce cette
    ces il elle ils ont été a avec pas plus comme sont banque banques centrale or crédit marché
    taux change monnaie monétaire financier réserves dépôts capital bilan rapport annuel
    intérêt prix économique pays politique internationale règlements conseil administration
    assemblée générale millions pendant période augmentation diminution total étranger paiements""".split()),
}
TOKEN = re.compile(r"[A-Za-zÀ-ÿ]{2,}")


def quality(text: str, lang: str) -> float:
    toks = TOKEN.findall(text)
    if len(toks) < 20:
        return 0.0
    vocab = WORDS.get(lang, WORDS["en"])
    hits = sum(1 for t in toks if t.lower() in vocab)
    return hits / len(toks)


def triage_file(path: Path, lang: str):
    rows = []
    with fitz.open(path) as doc:
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text")
            area = page.rect.width * page.rect.height or 1.0
            img_area = 0.0
            for img in page.get_images(full=True):
                try:
                    for r in page.get_image_rects(img[0]):
                        img_area += r.width * r.height
                except Exception:  # noqa: BLE001
                    pass
            rows.append({
                "file": path.name, "page": i,
                "chars": len(text),
                "img_cover": round(min(img_area / area, 1.0), 3),
                "quality": round(quality(text, lang), 3),
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--lang", default="en")
    args = ap.parse_args()
    root = Path(args.root)
    out = root / "triage"
    out.mkdir(parents=True, exist_ok=True)

    all_rows, file_rows = [], []
    for pdf in sorted((root / "raw").rglob("*.pdf")):
        rows = triage_file(pdf, args.lang)
        all_rows.extend(rows)
        chars = [r["chars"] for r in rows]
        q = [r["quality"] for r in rows if r["chars"] > 200]
        scanned = sum(1 for r in rows if r["img_cover"] > 0.5)
        file_rows.append({
            "file": pdf.name, "pages": len(rows),
            "pages_scanned_look": scanned,
            "pages_no_text": sum(1 for c in chars if c < 50),
            "median_chars": int(statistics.median(chars)) if chars else 0,
            "median_quality": round(statistics.median(q), 3) if q else 0.0,
            "p10_quality": round(sorted(q)[max(0, len(q) // 10 - 1)], 3) if q else 0.0,
            "verdict": "",
        })
        f = file_rows[-1]
        if f["pages_no_text"] > 0.2 * f["pages"]:
            f["verdict"] = "needs OCR (text layer missing)"
        elif f["median_quality"] < 0.15:
            f["verdict"] = "re-OCR advised (noisy layer)"
        elif f["p10_quality"] < 0.08:
            f["verdict"] = "usable; spot-correct worst pages"
        else:
            f["verdict"] = "usable as is"

    with open(out / "pages.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
        w.writeheader(); w.writerows(all_rows)
    with open(out / "files.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(file_rows[0].keys()))
        w.writeheader(); w.writerows(file_rows)

    hdr = f"{'file':28s}{'pages':>6s}{'scan':>6s}{'notxt':>6s}{'medch':>7s}{'medQ':>7s}{'p10Q':>7s}  verdict"
    print(hdr)
    for f in file_rows:
        print(f"{f['file']:28s}{f['pages']:>6d}{f['pages_scanned_look']:>6d}{f['pages_no_text']:>6d}"
              f"{f['median_chars']:>7d}{f['median_quality']:>7.3f}{f['p10_quality']:>7.3f}  {f['verdict']}")


if __name__ == "__main__":
    main()
