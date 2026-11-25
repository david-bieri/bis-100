# bis-100

Research repository for *Serial Reinvention: A Centenary History of the Bank for International Settlements*.

## Layout

```
proposal/          LaTeX book proposal, figures, appendix tables
corpus/
  manifest.csv     one row per fetched file: year, part, URL, pages, SHA-256, fetch time
  manifest.json    same, machine-readable
  raw/<year>/      original PDFs as downloaded (gitignored; see docs/corpus-notes.md to rebuild)
  text/            extracted text and the paragraph table (gitignored, derived)
  triage/          per-page and per-file OCR triage results
  crosswalk/       hand-maintained chapter → functional-category tables (committed)
  scripts/         fetch_pilot.py, ocr_triage.py, later segment.py, build_corpus.py
analysis/          notebooks / scripts per analytical layer (A–F in docs/plan.md)
figures/           generated figures with their data provenance
docs/
  plan.md          research plan
  gap-log.md       skill-builder gap log
  corpus-notes.md  judgement calls and provenance
```

## Pipeline

1. **Fetch** — `python corpus/scripts/fetch_pilot.py --out corpus [--years ...] [--langs en fr]`
   HEAD-checks URL candidates per regime, downloads politely, writes the manifest.
   bis.org must be reachable from the shell that runs it; otherwise download in a browser into `corpus/raw/<year>/` and run with `--dry-run` to write the manifest skeleton, then `python corpus/scripts/ocr_triage.py` fills pages.
2. **Triage** — `python corpus/scripts/ocr_triage.py --root corpus [--lang en]`
   Per-page text-layer size, image cover and dictionary-hit quality; per-file verdict (usable / spot-correct / re-OCR / needs OCR).
3. **Segment** (to come) — report → part → chapter → section → paragraph, joined to `corpus/crosswalk/`.
4. **Analyse** (to come) — layers A–F in `docs/plan.md`.

Requirements: Python 3.10+, `pymupdf`; Tesseract 5 with `eng fra deu` for re-OCR.

## URL regimes (bis.org)

| Years | Pattern |
|---|---|
| 1931–1996 | `publ/arpdf/archive/arYYYY_{en,fr,de,it}.pdf` (scans with OCR layer) |
| 1997–2017 | `publ/arpdf/arYYYY{e,f,g,i,s}.pdf`; chapters `arYYYYeN.pdf` |
| 2018– | `publications/aer-YYYY.pdf` (economic) and `publications/annual-report-YYYY.pdf` (bank) |

Note: `publications/annual-report-YYYY` for pre-2018 years serves only the activities/financial extract, not the full report.
