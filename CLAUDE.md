# bis-100 — Claude session context

Loaded at the start of every Claude Code session. Keep it short; detail lives in the files below.

## What this project is

Research repository for **Serial Reinvention: A Centenary History of the Bank for International Settlements** (target: BIS centenary, 2030). Two strands:

1. **Proposal** — the LaTeX book proposal (`proposal/`), with its figures and appendix tables.
2. **Corpus** — the full series of BIS Annual Reports 1931–2026 (and Annual Economic Reports 2018–), acquired, structured and analysed to trace the Economic Advisers' doctrinal lineages and Adviser–General Manager alignment in the Bank's own words.

**Owner:** David Bieri, Virginia Tech. Former BIS Adviser to the General Manager (Malcolm Knight era).
**Repo:** `bis-100` (private). Raw PDFs and derived text are **not** committed (see DECISIONS ADR-001).

## Read these before doing anything

1. `README.md` — layout, pipeline, how to run things
2. `PROGRESS.md` — what is done, what is next, what is blocked
3. `SESSION_NOTES.md` — handover from the last session (core:session-handover)
4. `docs/plan.md` — the content-analysis research plan (phases, analytical layers, gates)
5. `DECISIONS.md` — only when facing an architecture or method question

After reading, summarise status and proposed next steps; wait for confirmation before changing code or corpus files.

## Working rules

- Raw PDFs under `corpus/raw/` are immutable originals; never edit or re-save them.
- Every derived file traces back to `corpus/manifest.csv` by year and SHA-256.
- Judgement calls (chapter crosswalk, OCR choices, codebook changes) are logged in `docs/corpus-notes.md`, not left implicit in code.
- Skill-builder gap log: `docs/gap-log.md`. Add an entry whenever Claude had to be told something the eventual `research:serial-corpus` / `llm-content-coding` / `diachronic-text-analysis` skills should encode.
- bis.org is not on the network allowlist for Claude's shells; downloads happen in the owner's browser or after the host is allowlisted.
