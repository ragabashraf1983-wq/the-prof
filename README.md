# The Prof

The Prof is a **local-first Windows desktop application** for autonomous academic research production.

It helps a researcher:

- enter a topic
- choose a research or writing scope
- answer setup questions
- run a staged autonomous workflow
- inspect sources, claims, memory usage, and integrity reports
- produce final **Markdown** outputs with audit trails

The first version is intentionally conservative:

- local-first by default
- no web UI
- no hidden telemetry
- no fabricated citations or claims
- unsupported content must be marked exactly as `Do not know.`

---

## Current implemented features

### Study and documentation phase

This repository includes the full mandatory repository study output:

- `docs/repo_analysis/*.md`
- `docs/REPOSITORY_SYNTHESIS.md`
- `docs/EXTRACTION_PLAN.md`
- `DEVSTATE.md`

### Desktop application

Implemented with **Python + PySide6**.

Main capabilities:

- dark desktop UI with logo in the home/sidebar surfaces
- scrollable project creation form that works on smaller screens
- topic intake
- scope selection
- dynamic setup question prompt
- local project folder generation
- staged workflow engine
- agent registry with editable YAML skill files
- local `brain.md` memory system
- source registry
- claim ledger
- source audit
- integrity report
- provider router with Ollama, many OpenAI-compatible APIs, Google AI Studio, Anthropic, and rule-based fallback
- Providers page for enabling LLMs, saving local API keys, adding custom providers, and switching local/API/paid/browser-login modes
- API registry seed importer/tester plus manual API record entry
- final Markdown output generation

### Current scopes supported in working form

- Gap Analysis
- Research Proposal
- Literature Review
- Review Paper
- Conference Paper
- Journal Article
- Research Idea Discovery
- Research Question Development
- Systematic Review Plan
- Scoping Review Plan

### Provider support

Implemented adapters and built-in provider profiles:

- Ollama local provider
- generic OpenAI-compatible provider
- OpenAI, OpenRouter, Groq, Mistral, Cerebras, Hugging Face, SambaNova, DeepSeek, Together, Fireworks, Perplexity, NVIDIA NIM, GitHub Models
- Google AI Studio wrapper
- Anthropic wrapper
- Kimi wrapper
- GLM wrapper
- custom OpenAI-compatible provider entry from the UI
- browser-login stub (disabled by default and only for manual user login; it must not bypass site rules)
- built-in deterministic fallback provider

### Brain memory

Files used by the memory subsystem:

- `brain/brain.md`
- `brain/brain_index.json`
- `brain/references.bib`
- `brain/reference_notes.md`
- `brain/memory_log.md`
- `brain/pending_verification.md`
- `brain/rejected_claims.md`

---

## Run from source

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch the desktop app

```bash
python main.py
```

---

## Windows launch

For Windows users, the repository includes:

- `start_the_prof.bat`
- `build_windows_zip.bat`
- `build_windows_exe.bat`

### Start on Windows

Double-click:

```text
start_the_prof.bat
```

Behavior:

- creates `.venv` if missing
- installs requirements on first run
- launches The Prof desktop window
- writes a startup log to `the_prof_startup.log`
- pauses on failure so the error does not disappear immediately

### If nothing happens on Windows

Check these first:

1. Make sure **Python 3.11+** is installed.
2. Re-run `start_the_prof.bat`.
3. If it fails, open:

```text
the_prof_startup.log
```

4. If needed, run manually from Command Prompt inside the folder:

```bat
start_the_prof.bat
```

---

## Create a portable ZIP package

```bash
python scripts/package_portable_zip.py
```

Or on Windows:

```text
build_windows_zip.bat
```

Output:

```text
dist/the-prof-portable.zip
```

---

## Build a Windows EXE

On Windows:

```text
build_windows_exe.bat
```

This uses PyInstaller to build:

```text
dist/TheProf/TheProf.exe
```

Note: the EXE build script is provided, but the EXE build itself should be run and verified on Windows.

---

## Application structure

```text
the_prof/
  app/
  core/
  agents/
  providers/
  research/
  memory/
  apis/
brain/
projects/
exports/
storage/
docs/
tests/
```

---

## Output files per project

Each project creates human-readable artifacts under `projects/<project_id>/`:

- `project.yaml`
- `intake.md`
- `workflow_plan.md`
- `selected_agents.md`
- `provider_log.md`
- `source_registry.md`
- `claim_ledger.md`
- `memory_usage.md`
- `agent_outputs/`
- `reviews/`
- `drafts/`
- `logs/`
- `final/final_output.md`
- `final/source_audit.md`
- `final/integrity_report.md`
- `final/memory_report.md`

---

## Testing completed

The following were tested in the development environment:

### Core tests

```bash
python -m unittest tests/test_workflow_smoke.py -v
```

Covered:

- local-only Gap Analysis workflow
- local-only Research Proposal workflow
- final Markdown generation
- source audit generation
- claim ledger generation
- memory report generation

### End-to-end smoke run

```bash
python scripts/smoke_test.py
```

This creates:

- one tested Gap Analysis project
- one tested Research Proposal project

### Desktop launch smoke test

The PySide6 application was launched in offscreen mode successfully during development.

---

## Known limitations in this version

- The UI is working but intentionally minimal.
- Review/debate generation falls back to the deterministic local rules provider when Ollama or online LLMs are unavailable.
- Citation validation is conservative and currently strongest for Crossref/OpenAlex/arXiv-derived records.
- Browser-login providers are stubbed and disabled by default.
- PDF/DOCX/LaTeX/BibTeX export is not a core output pathway in v1.
- The Windows EXE build script is prepared, but must be executed and verified on Windows.

---

## Security and integrity rules

- No secrets are stored in source files.
- Local secrets are stored under `storage/secrets/`.
- `brain.md` never stores API keys.
- Hidden telemetry is not used.
- Unsupported claims must be written as `Do not know.`
- Final outputs include source and integrity artifacts.

---

## Recommended next steps

1. Run `start_the_prof.bat` on Windows and verify the desktop shell there.
2. Connect a local Ollama model for richer agent review behavior.
3. Add additional source providers such as Europe PMC or Semantic Scholar.
4. Expand the skill editor with structured forms.
5. Add stronger claim-level citation alignment checks.

---

## License and attribution notes

This repository contains original integration code for The Prof plus study documentation about the analyzed repositories.

Third-party repository ideas were selectively studied and adapted according to:

- `docs/repo_analysis/`
- `docs/REPOSITORY_SYNTHESIS.md`
- `docs/EXTRACTION_PLAN.md`
