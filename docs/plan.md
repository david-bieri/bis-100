# BIS Annual Reports, 1931–2026: Deep Content Analysis — Research Plan

*Project: Serial Reinvention (BIS centenary book). Drafted 2026-11-25. Canonical copy also in the Claude project `bis-100`.*

## 0. Why this corpus, and what it must deliver for the book

The Annual Report is the one continuous, institutionally authored text the BIS has produced every year since 1931. Its economic chapters were drafted in the Monetary and Economic Department under the Economic Adviser; its Introduction and Conclusion chapters are where the "house view" is stated in the institution's own voice. That makes the series the best available instrument for the book's two axes:

1. **Doctrinal axis** — tracing the credit-cycle / financial-stability strain (Jacobsson → Lamfalussy → White → Shin → Rey) against the soundness/orthodoxy strain (Gilbert, Bockelmann, Cecchetti), year by year, in the Bank's own words rather than in retrospective testimony.
2. **Alignment axis** — whether the ideational chair (Adviser / Head of MED) and the operational chair (General Manager) speak with one voice, measurable through the relationship between the economic chapters and the governance/activities chapters, and through stylistic and thematic shifts at tenure boundaries.

Deliverables: (a) empirical figures for the proposal and book (doctrine-tracking charts, era-break detection, lexical fingerprints by Adviser); (b) a structured, citable corpus with metadata; (c) a methods appendix / standalone working paper on "reading an institution through its annual report".

## 1. Corpus definition

| Era | Reports | Form on bis.org | Notes |
|---|---|---|---|
| 1931–1945 | 1st–15th | Scanned PDF, `publ/arpdf/archive/` | French and English editions; verify the drafting language per year. Wartime reports (1940–45) are a sub-corpus. |
| 1946–1996 | 16th–66th | Scanned PDF | OCR quality variable; English edition is the working text. |
| 1997–2017 | 67th–87th | Born-digital PDF, full + per-chapter (`arYYYYe0…e9`), EN/FR/DE/IT/ES | Clean text; chapter files allow direct segmentation. |
| 2018–2026 | AER + Annual Report | `publications/aer-YYYY.pdf`, `publications/annual-report-YYYY.pdf` | AER continues the economic chapters; Annual Report continues the activities/financial chapters. |

About 96 report-years; 150–280 pages each pre-2018 → an estimated 18–22k pages, 8–10 million English words.

Scope decisions (pilot first, then decide): English only vs EN+FR for the early decades; whether to keep the five-language editions as a translation-stability check; whether Overview booklets and the Annual Report Survey era count as auxiliary texts.

## 2. Acquisition and preservation (Phase 1)

1. Build a manifest: year, ordinal, fiscal year, AGM date, URL(s), language, pages, SHA-256.
2. Download politely, store originals immutably under `corpus/raw/`.
3. Provenance per file; corpus for research only, derived text private, aggregates publishable.
4. Reuse the research-archive pipeline conventions and `research:corpus-search` tooling.

## 3. Text extraction and structuring (Phase 2)

1. **Extraction**: PyMuPDF for born-digital; for scans, compare the embedded OCR layer with fresh Tesseract (eng+fra) on a sample; keep the better layer per decade; log per-page confidence.
2. **Segmentation**: report → part (economic / activities / financial statements) → chapter → section → paragraph; front matter, tables, footnotes, auditors' report tagged, not deleted.
3. **Chapter crosswalk**: hand-maintained mapping of each year's chapters to ~10 functional categories (intro/conclusion; world economy; monetary policy; financial markets; banking & stability; IMS/exchange rates; capital flows & debt; bank activities; governance; financial statements).
4. **Metadata join**: Chairman, GM, Economic Adviser, Head of MED, Secretary General; membership, balance-sheet total, staff.
5. Output: Parquet/SQLite paragraph table with hierarchical IDs; `docs/corpus-notes.md` for every judgement call.

## 4. Analytical programme (Phase 3) — layered, cheapest first

**A. Structural / descriptive** — length, page share by category over time, counts of charts/tables/boxes, how the Bank names its own purpose each year.

**B. Lexical and concept tracking** — two curated dictionaries (credit-cycle/financial-stability strain; soundness/orthodoxy strain) plus a named-intellect dictionary (Wicksell, Hayek, Keynes, Friedman, Minsky, Kindleberger, Tobin, Mundell; later Bernanke, Taylor, Woodford). Normalised frequencies by category and year; keyness between Adviser and GM tenures; collocation networks around "credit" and "stability" by decade.

**C. Topic modelling and semantic drift** — paragraph-level BERTopic on the economic chapters; diachronic embeddings for "liquidity", "stability", "imbalance", "cooperation"; a year-to-year continuity index of Introduction/Conclusion chapters with change-point detection tested against Adviser changes, GM changes and crises.

**D. Structured doctrinal coding (LLM-assisted, human-validated)** — codebook for the ~190 Introduction/Conclusion chapters: diagnosis, cause, remedy, addressee, tone toward consensus, explicit dissent, self-reference to earlier warnings. Claude API codes with evidence spans; a stratified 20% sample is hand-coded; Krippendorff's α reported and disagreements adjudicated.

**E. Authorship and voice (alignment axis)** — stylometric distance between economic and activities chapters per year; Burrows's Delta clustering of Conclusions by Adviser tenure; test whether 2013–2024 Conclusions cluster with Borio-authored papers rather than Shin's. Presented as suggestive, given collective drafting.

**F. Institutional time series** — membership, balance sheet, staff, committees hosted, new services; entity extraction of institutions and countries.

## 5. Triangulation and verification

Cross-check against BIS Archives finding aids, Toniolo (2005), Borio–Toniolo–Clement (2008), James, Yago, the Lamfalussy biography and Piet Clement. Informally pre-register expected era breaks before change-point detection. Every figure gets a reproducible script and a provenance line; dagger convention for uncertain metadata.

## 6. Outputs

1. Private corpus: manifest, raw PDFs, text, paragraph table, crosswalk, metadata, OCR log.
2. Code with one `make all` reproducing every figure.
3. Figures for the proposal: doctrine-strain index 1931–2026; continuity/change-point chart; Adviser lexical fingerprints; alignment-distance series over the existing Figure 5 timeline.
4. Methods appendix / working paper ("The Bank in its own words: ninety-six annual reports").
5. Project docs: corpus notes, codebook, decisions log.

## 7. Phasing and effort

| Phase | Content | Effort | Gate |
|---|---|---|---|
| 0 Pilot | 1931, 1961, 1986, 2005, 2025 end to end | 1 week | OCR usable? crosswalk workable? language scope? |
| 1 Acquire | Manifest, download, checksum all | 2–3 days | Complete manifest |
| 2 Structure | OCR, segmentation, crosswalk, metadata | 3–4 weeks | Paragraph table, QA report |
| 3A–B | Descriptive + dictionary analysis | 2 weeks | First figures |
| 3C | Topics, drift, change points | 2 weeks | Continuity index |
| 3D | Doctrinal coding + validation | 3–4 weeks | α reported |
| 3E–F | Stylometry, institutional series | 2 weeks | Alignment series |
| 4 Write | Methods appendix + figures | 2 weeks | Draft |

## 8. Risks and open questions

OCR quality for 1931–1960s; drafting language in the early decades; chapter drift and the crosswalk as a contestable artefact; collective authorship limiting Adviser attribution; acceptability of LLM coding in a history manuscript; wartime reports as a separate section.
