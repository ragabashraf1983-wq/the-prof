# Extraction Plan

## Extraction policy

- Prefer **rewrite** over blind copy.
- Use **adaptation** only when a source module is small, clear, permissively licensed, and aligned with the Windows desktop target.
- Do **not** import web UI stacks, cloud-first assumptions, unsafe browser automation, or live credentials.
- Preserve attribution in docs where ideas or small logic patterns are reused.

## Planned extraction matrix

| Source repository | Useful source files/modules | Target location in The Prof | Action | Reason | Dependency impact | Test requirement |
|---|---|---|---|---|---|---|
| `the-prof` | `TheProf_logo.png`, repo root | `the_prof/app/assets/` | Adapt | Use logo if present; fallback theme if absent | None | UI should load with or without logo |
| `deep-research` | `src/deep-research.ts`, `src/prompt.ts` | `the_prof/core/workflow_engine.py`, `the_prof/research/source_search.py` | Rewrite | Best minimal iterative research loop; TS must become Python and audit-aware | Low | Workflow recursion and stage progression tests |
| `local-deep-researcher` | `src/ollama_deep_researcher/graph.py`, `prompts.py`, configuration concepts | `the_prof/providers/local_ollama.py`, `the_prof/research/source_search.py`, `the_prof/agents/skills/*.yaml` | Rewrite | Strong local LLM loop; avoid LangGraph dependency | Low | Ollama detection test, prompt output fallback test |
| `AutoResearchClaw` | `researchclaw/literature/verify.py`, `prompts.default.yaml`, selected memory/pipeline concepts | `the_prof/research/citation_validator.py`, `the_prof/agents/skills/`, `the_prof/core/integrity_governor.py` | Adapt + Rewrite | Best citation verification and prompt externalization patterns | Low | DOI/title verification tests, prompt loading tests |
| `council-of-high-intelligence` | `configs/auto-route-defaults.yaml`, provider slot examples, deliberation protocol | `the_prof/providers/provider_router.py`, `the_prof/agents/agent_selector.py`, `the_prof/app/ui/pages/council_page.py` | Rewrite | Good fallback ordering and structured debate concept | Low | Fallback-order test, debate transcript generation test |
| `Research-Paper-Writing-Skills` | `research-paper-writing/SKILL.md`, references ideas | `the_prof/agents/skills/reviewer_*.yaml`, `the_prof/agents/skills/markdown_typesetter.yaml` | Rewrite | Strong claim-evidence and section-review discipline; needs product-specific wording | None | Skill schema validation test |
| `research-skills` | `research-proposal/`, `skills/survey-*`, `references/` role split | `the_prof/agents/skills/principal_investigator.yaml`, `the_prof/agents/skills/literature_reviewer.yaml`, workflow stage templates | Rewrite | Good proposal/survey task decomposition; license unclear in snapshot | None | Scope-to-agent selection tests |
| `academic-research-skills` | agent markdowns, claim-audit/integrity concepts | `the_prof/core/integrity_governor.py`, `the_prof/research/claim_ledger.py`, `the_prof/agents/skills/*.yaml` | Rewrite only | Excellent integrity logic, but noncommercial content should not be copied verbatim | None | Claim traceability tests |
| `academic-research-skills-codex` | packaging/manifest concepts | `the_prof/agents/registry.py`, `the_prof/config/skill_registry.json` | Rewrite only | Useful for skill packaging ideas, not code import | None | Skill discovery test |
| `AI-Research-SKILLs` | category organization, autoresearch templates | `the_prof/agents/skills/`, `docs/` | Rewrite | Helps organize many skill files cleanly | None | Skill loading smoke test |
| `Deep-Research-skills` | two-phase research skill flow, JSON validation helper ideas | `the_prof/core/workflow_engine.py`, `the_prof/core/task_graph.py` | Rewrite | Useful for outline-then-deep-research sequencing | None | Structured intermediate validation test |
| `gpt-researcher` | planner/executor/publisher concept, parsing utilities, report structure | `the_prof/core/workflow_engine.py`, `the_prof/research/source_audit.py`, `the_prof/research/claim_ledger.py` | Rewrite | Rich but too large for direct reuse; keep only architecture and parsing ideas | Low | Report generation tests |
| `local-deep-research` | provider/settings taxonomy, security/provider tests, model settings concepts | `the_prof/providers/`, `the_prof/app/ui/pages/settings_page.py`, `the_prof/apis/api_registry.py` | Rewrite | Strong product engineering reference; desktop implementation must remain lighter | Medium | Settings serialization test, provider usage test |
| `Auto-claude-code-research-in-sleep` | research-wiki idea, citation-audit skill, governance patterns | `the_prof/memory/brain_manager.py`, `the_prof/brain/brain.md`, `the_prof/research/source_audit.py` | Rewrite | Excellent memory/audit discipline; host-specific packaging not needed | None | Brain import/export and audit-trail tests |
| `public-apis` | curated research/public data API entries, validation ideas | `the_prof/apis/imported_sources/public_apis_seed.json` | Adapt | Seed API registry with filtered research/public data sources | None | API registry import test |
| `public-api-lists` | machine-readable catalog ideas, validation scripts concepts | `the_prof/apis/imported_sources/public_api_lists_seed.json`, `the_prof/apis/api_tester.py` | Adapt + Rewrite | Good metadata structure for registry fields | None | Registry normalization test |
| `free-llm-api-resources` | provider names/limits/free-vs-trial metadata | `the_prof/apis/imported_sources/free_llm_resources_seed.json`, `the_prof/providers/provider_usage.py` | Adapt | Best legitimate free-provider metadata source | None | Seed import test |
| `free-llm-api-keys` | endpoint patterns only | `docs/provider_notes.md` | Ignore as runtime source | Live shared keys must not be redistributed or trusted | None | None |
| `API-mega-list` | broad API categories | `docs/future_api_backlog.md` | Ignore for v1 runtime | Too noisy and broad for first release | None | None |
| `AI-Researcher` | idea/plan/survey/memory taxonomy | `the_prof/agents/skills/`, `docs/architecture_notes.md` | Rewrite | Valuable conceptual model, but codebase is too large and domain-heavy | None | Agent taxonomy sanity test |

## Concrete extraction decisions

### Copy/adapt candidates

These are the only areas where limited close adaptation is justified:

1. citation verification strategy inspired by `AutoResearchClaw`
2. provider-slot/fallback configuration shape inspired by `council-of-high-intelligence`
3. selected public/provider metadata records from list repositories after normalization
4. logo asset handling from target repo

### Rewrite candidates

Most of the system must be rewritten into original code:

- desktop UI
- workflow engine
- project storage
- memory manager
- claim ledger
- integrity governor
- agent registry
- provider router
- API registry importer/tester
- proposal/gap-analysis/report generation

### Ignore candidates

- all web frontends
- all Docker-only deployment assumptions
- all host-specific slash-command installers
- experimental sandboxes unrelated to first release
- live/free public keys and shared secrets
- giant benchmark corpora and unrelated datasets

## Dependency impact summary

### Dependencies to keep small and explicit

Planned first-version runtime:

- `PySide6`
- `requests`
- `PyYAML`

Optional future-only dependencies are intentionally deferred.

### Dependencies explicitly avoided in v1

- LangGraph
- FastAPI/Flask server stacks
- Node/Electron
- heavyweight vector DBs
- browser automation frameworks
- cloud SDK sprawl where a generic OpenAI-compatible adapter is sufficient

## Required validation after extraction

1. app launches in a desktop window
2. project creation writes required files
3. gap analysis workflow completes
4. research proposal workflow completes
5. markdown output exists
6. source audit exists
7. claim ledger exists
8. memory usage report exists
9. `brain.md` import/export works
10. provider router falls back cleanly when Ollama is unavailable
11. no secrets appear in repo files or logs

## Implementation order derived from extraction plan

1. repo study docs complete
2. project skeleton and local file layout
3. core models and settings
4. memory system
5. provider system
6. research/source/citation modules
7. agent registry and skill files
8. workflow engine
9. desktop UI
10. packaging scripts
11. tests and smoke runs
