#!/usr/bin/env python3
"""Pilot fetch for the BIS Annual Report corpus.

Standard library only, so it runs anywhere with Python 3.8+.
Downloads the pilot report-years into raw/<year>/, verifies each file,
and writes manifest.json + manifest.csv with URL, size, pages (if
PyMuPDF is available), SHA-256 and fetch time.

Usage:
    python fetch_pilot.py --out <corpus-root> [--years 1931 1961 1986 2005 2025]
                          [--langs en] [--dry-run]
"""
import argparse
import csv
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA = "bis-corpus-pilot/0.1 (academic research)"
BASE = "https://www.bis.org"
PAUSE_S = 2.0  # polite spacing between requests


def candidates(year: int, lang: str):
    """Candidate URLs for one report-year, most likely first.

    1931-1996  scanned archive:        publ/arpdf/archive/ar{Y}_{lang}.pdf
    1997-2017  born-digital, full:     publ/arpdf/ar{Y}{l}.pdf   (l = e/f/g/i/s)
    2018-      AER (economic part):    publ/arpdf/ar{Y}{l}.pdf
               Annual Report (bank):   about/areport/areport{Y}.pdf  (English)
    """
    l1 = {"en": "e", "fr": "f", "de": "g", "it": "i", "es": "s"}[lang]
    items = []
    if year <= 1996:
        items.append(("full", f"{BASE}/publ/arpdf/archive/ar{year}_{lang}.pdf"))
    elif year <= 2017:
        items.append(("full", f"{BASE}/publ/arpdf/ar{year}{l1}.pdf"))
    else:
        # verified 2025: publications/aer-2025.pdf (126 pp), publications/annual-report-2025.pdf (262 pp)
        items.append(("aer", f"{BASE}/publications/aer-{year}.pdf"))
        items.append(("aer-alt", f"{BASE}/publ/arpdf/ar{year}{l1}.pdf"))
        if lang == "en":
            items.append(("annual-report", f"{BASE}/publications/annual-report-{year}.pdf"))
            items.append(("annual-report-alt", f"{BASE}/about/areport/areport{year}.pdf"))
    return items


def head_ok(url: str):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            ctype = r.headers.get("Content-Type", "")
            clen = r.headers.get("Content-Length")
            return r.status == 200 and "pdf" in ctype.lower(), ctype, int(clen) if clen else None
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}", None
    except Exception as e:  # noqa: BLE001
        return False, repr(e), None


def download(url: str, dest: Path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    h = hashlib.sha256()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 16)
            if not chunk:
                break
            f.write(chunk)
            h.update(chunk)
    return h.hexdigest(), dest.stat().st_size


def page_count(path: Path):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None
    try:
        with fitz.open(path) as doc:
            return doc.page_count
    except Exception:  # noqa: BLE001
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="corpus root (raw/ and manifest go here)")
    ap.add_argument("--years", nargs="+", type=int, default=[1931, 1961, 1986, 2005, 2025])
    ap.add_argument("--langs", nargs="+", default=["en"])
    ap.add_argument("--dry-run", action="store_true", help="HEAD-check only, no download")
    args = ap.parse_args()

    root = Path(args.out)
    raw = root / "raw"
    rows = []
    for year in args.years:
        for lang in args.langs:
            for part, url in candidates(year, lang):
                ok, ctype, clen = head_ok(url)
                time.sleep(PAUSE_S)
                row = {
                    "year": year, "lang": lang, "part": part, "url": url,
                    "head_ok": ok, "content_type": ctype, "content_length": clen,
                    "path": "", "bytes": None, "sha256": "", "pages": None,
                    "fetched_utc": "",
                }
                print(f"{year} {lang} {part:16s} {'OK ' if ok else 'no '} {url}", file=sys.stderr)
                primary_done = any(r["year"] == year and r["lang"] == lang and r["sha256"]
                                   and r["part"] == part.replace("-alt", "") for r in rows)
                if ok and not args.dry_run and not (part.endswith("-alt") and primary_done):
                    dest = raw / str(year) / Path(url).name
                    sha, nbytes = download(url, dest)
                    row.update({
                        "path": str(dest.relative_to(root)), "bytes": nbytes, "sha256": sha,
                        "pages": page_count(dest),
                        "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    })
                    time.sleep(PAUSE_S)
                rows.append(row)

    root.mkdir(parents=True, exist_ok=True)
    (root / "manifest.json").write_text(json.dumps(rows, indent=2))
    with open(root / "manifest.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    got = sum(1 for r in rows if r["sha256"])
    print(f"\n{got} files downloaded; manifest at {root/'manifest.csv'}", file=sys.stderr)


if __name__ == "__main__":
    main()
