# bis-100 — Progress

## Current status

**Phase 0 (pilot) in progress.** Repo scaffolded 2026-11-25. Scripts in place; pilot PDFs not yet downloaded (network allowlist blocks bis.org from Claude's shells).

## Phase 0 — Pilot (1931, 1961, 1986, 2005, 2025)

- [x] Research plan written (`docs/plan.md`)
- [x] URL regimes verified for all four eras
- [x] `fetch_pilot.py` and `ocr_triage.py` written
- [ ] Pilot PDFs in `corpus/raw/<year>/` (manual browser download, or allowlist bis.org)
- [ ] Manifest with SHA-256 and page counts
- [ ] OCR triage run; verdict per file
- [ ] Drafting-language check 1931 (EN vs FR)
- [ ] Segmentation prototype on 2005 (chapter files) and 1961 (scan)
- [ ] First crosswalk draft from the five tables of contents
- [ ] Gate decision: OCR usable? crosswalk workable? language scope?

## Decisions pending from the owner

1. English only, or EN + FR for the 1931–1960s originals?
2. LLM-assisted coding in the book, or in a companion working paper?
3. Corpus end date: through AER 2026, or a fixed cut?

## Blocked

- Downloads from bis.org (see DECISIONS ADR-003).

## Next phases

See `docs/plan.md` §7.
