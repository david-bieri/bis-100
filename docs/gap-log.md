# BIS corpus pilot — gap log (for the skill-builder gap test)

Mirror of the Claude project doc `bis-pilot-gap-log.md`; the project copy is canonical until the repo takes over.

Format: `date · phase · what happened · what the skill should encode`.

## Entries

- 2026-11-25 · acquire · Cloud workspace cannot reach bis.org (egress allowlist). → *Skill: institutional sites are usually off the allowlist; plan the fetch route before writing a downloader.*
- 2026-11-25 · acquire · Test command refused for putting the owner's e-mail in a User-Agent. → *Skill: generic client name in UA; ask before sending a real contact address.*
- 2026-11-25 · acquire · Folder access cannot be requested by Claude; owner adds the folder via the desktop app. → *Skill: step 1 is "confirm a connected folder exists"; name the target repo folder.*
- 2026-11-25 · acquire · Device shell is behind the same allowlist. Routes: owner downloads in browser, or org owner allowlists `www.bis.org`. → *Skill: offer both routes with a ready URL list; allowlist is the only scalable route.*
- 2026-11-25 · acquire · URL regimes reverse-engineered; first guess for 2018+ was wrong (correct: `publications/aer-YYYY.pdf`, `publications/annual-report-YYYY.pdf`). Modern listing pages serve only the activities extract for pre-2018 years. → *Skill: `references/url-patterns.md` per institution; verify one URL per regime before writing the manifest.*
- 2026-11-25 · acquire · Pre-1997 scans "scanned but searchable": OCR layer of unknown quality. → *Skill: ship per-page triage and gate re-OCR on its verdicts.*
- 2026-11-25 · structure · Workspace lacked PyMuPDF; Tesseract 5 present (eng, fra, deu). → *Skill: toolchain check as step 0.*
- 2026-11-25 · repo · Repo had to be scaffolded to the owner's house conventions (CLAUDE.md, README, PROGRESS, DECISIONS, SESSION_NOTES) before any corpus work. → *Skill: `serial-corpus` ships a repo template with these files and the corpus layout; `core:session-handover` owns SESSION_NOTES.*

## Open gaps to watch

- Segmentation of scans from TOC + running headers.
- How many crosswalk categories survive the 1930s structure.
- Codebook drift between hand-coded batches.
