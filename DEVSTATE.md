# DEVSTATE

## Project

**Name:** The Prof  
**Target platform:** Windows desktop, local-first, ZIP-extract-and-run  
**Primary stack:** Python + PySide6  
**Current date baseline:** 2026-07-05

---

## Phase status

### Phase 1 — Repository Intelligence

- [x] Created `DEVSTATE.md`
- [x] Created `docs/repo_analysis/`
- [x] Inspected all listed repositories
- [x] Wrote one analysis file per repository
- [x] Wrote `docs/REPOSITORY_SYNTHESIS.md`
- [x] Wrote `docs/EXTRACTION_PLAN.md`
- [x] Identified reusable workflows, skills, prompts, agents, provider logic, source-audit logic, memory logic, and automation logic
- [x] Recorded risks, licensing constraints, and reuse/rewrite decisions

**Phase 1 status:** Complete

### Phase 2 — Architecture From Existing Assets

- [x] Created repository structure
- [x] Implemented core models/config/state
- [x] Implemented memory system
- [x] Implemented provider system
- [x] Implemented research/audit modules
- [x] Implemented agent registry and skill files

**Phase 2 status:** Complete

### Phase 3 — Working Desktop Application

- [x] Built PySide6 desktop shell
- [x] Implemented dark UI
- [x] Implemented project creation/intake
- [x] Implemented dynamic setup questions
- [x] Implemented workflow engine
- [x] Implemented Markdown output pipeline
- [x] Implemented source audit
- [x] Implemented claim ledger
- [x] Implemented Brain page and memory import/export support
- [x] Implemented Provider usage and API Registry views
- [x] Implemented settings and skill editor
- [x] Implemented packaging scripts
- [x] Wrote README

**Phase 3 status:** Complete

### Phase 4 — Verification

- [x] Compiled all Python modules successfully
- [x] Launched the PySide6 app in offscreen mode successfully
- [x] Created test Gap Analysis project
- [x] Created test Research Proposal project
- [x] Verified final Markdown output generation
- [x] Verified source audit generation
- [x] Verified claim ledger generation
- [x] Verified memory usage report generation
- [x] Verified provider fallback behavior (`ollama` -> `rules`)
- [x] Verified no secrets were committed in source files
- [x] Created portable ZIP package script and tested ZIP creation
- [ ] Windows EXE build executed on Windows

**Phase 4 status:** Substantially complete; Windows-native EXE packaging still needs execution on Windows itself.

---

## Architecture decisions from study phase

### Selected foundations

- **Iterative workflow foundation:** `deep-research` + `local-deep-researcher`
- **Integrity/audit discipline:** `AutoResearchClaw` + `academic-research-skills` concepts
- **Proposal/survey role design:** `research-skills`
- **Editorial review patterns:** `Research-Paper-Writing-Skills`
- **Council debate structure:** `council-of-high-intelligence`
- **Provider/API registry discipline:** `local-deep-research`, `free-llm-api-resources`, `public-api-lists`, `public-apis`
- **Memory/brain inspiration:** `Auto-claude-code-research-in-sleep`, `AI-Researcher`, `AutoResearchClaw`

### Key constraints preserved

- No web UI
- Local-first by default
- No hidden external calls
- No fabricated citations or claims
- Missing verification must be marked exactly: `Do not know.`
- `brain.md` remains the authoritative portable memory file

---

## Verified implementation outputs

### Desktop/UI

- Main window with dark theme
- Sidebar navigation
- Home page
- New Project page
- Project Dashboard with tabs
- Brain page
- Settings page
- Agent Skills editor
- Live log panel

### Core project outputs

- `final_output.md`
- `source_audit.md`
- `claim_ledger.md`
- `integrity_report.md`
- `memory_report.md`

### Tested project runs

- Gap Analysis smoke project
- Research Proposal smoke project

### Packaging/runtime assets

- `start_the_prof.bat`
- `build_windows_zip.bat`
- `build_windows_exe.bat`
- `scripts/package_portable_zip.py`
- `dist/the-prof-portable.zip`

---

## Current limitations

1. The deterministic rules provider is intentionally conservative and not a substitute for a strong local LLM.
2. The EXE build pathway is prepared but not executed inside a real Windows runtime from this environment.
3. Citation verification is good for Crossref/OpenAlex/arXiv flows but not yet exhaustive across all scholarly providers.
4. Browser-login provider support remains a disabled stub by design.

---

## Immediate recommended next action for end user

1. Run `start_the_prof.bat` on a Windows machine.
2. Optionally install and start Ollama locally.
3. Open The Prof and create a real project.
4. If desired, run `build_windows_exe.bat` on Windows to create `TheProf.exe`.
