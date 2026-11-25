# bis-100 — Decision records

## ADR-001 — Raw PDFs and derived text are not committed
**Status:** Accepted (2026-11-25)
**Decision:** `corpus/raw/` and `corpus/text/` are gitignored. The manifest (URL + SHA-256) is committed and is sufficient to rebuild them.
**Rationale:** Size (tens of GB across languages) and BIS copyright: the Bank permits brief excerpts with citation, not redistribution of full texts. Aggregates and figures are publishable; the corpus itself stays private.

## ADR-002 — English is the working text; French checked for the early decades
**Status:** Proposed
**Decision:** Analyse the English edition throughout. For 1931–c.1960 run a drafting-language check against the French edition; if French proves original, either add FR as a parallel text for those years or caveat the lexical results.
**Rationale:** One language keeps dictionaries and models consistent; the early-decade translation risk is real and must be measured, not assumed away.

## ADR-003 — Fetch route
**Status:** Accepted (2026-11-25)
**Decision:** bis.org is not on the network allowlist for Claude's cloud or device shells. Pilot files are downloaded in the owner's browser into `corpus/raw/<year>/`. For the full series, request that `www.bis.org` be added to the organisation allowlist, then run `fetch_pilot.py` unattended.
**Rationale:** Two blocked attempts; manual download scales to six files, not to ~500.

## ADR-004 — Pilot years
**Status:** Accepted (2026-11-25)
**Decision:** 1931 (first report, scan, FR/EN), 1961 (Gilbert era, scan), 1986 (Lamfalussy era, scan), 2005 (Knight/White era, born-digital with chapter files), 2025 (post-split AER + Annual Report).
**Rationale:** One report per URL regime and OCR condition, spanning the Adviser lineages the book traces.

## ADR-005 — Judgement calls are logged, not embedded
**Status:** Accepted (2026-11-25)
**Decision:** The chapter crosswalk lives in `corpus/crosswalk/` as editable tables; OCR choices, segmentation rules and codebook versions are recorded in `docs/corpus-notes.md`.
**Rationale:** The crosswalk is an interpretive artefact the book's critics should be able to contest; it must be visible.
