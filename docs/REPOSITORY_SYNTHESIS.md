# Repository Synthesis

## Scope of study

Studied repositories:

1. the-prof
2. free-llm-api-keys
3. free-llm-api-resources
4. local-deep-research
5. gpt-researcher
6. deep-research
7. local-deep-researcher
8. AI-Researcher
9. public-apis
10. public-api-lists
11. API-mega-list
12. council-of-high-intelligence
13. AutoResearchClaw
14. Auto-claude-code-research-in-sleep
15. academic-research-skills
16. AI-Research-SKILLs
17. academic-research-skills-codex
18. Research-Paper-Writing-Skills
19. Deep-Research-skills
20. research-skills

## Executive synthesis

No single source repository can be adopted wholesale for The Prof.

The best implementation strategy is a **hybrid architecture**:

- **Workflow core:** `deep-research` + `local-deep-researcher`
- **Audit/integrity discipline:** `AutoResearchClaw` + `academic-research-skills`
- **Agent/council structure:** `council-of-high-intelligence` + `research-skills` + `academic-research-skills`
- **Writing/review skill design:** `Research-Paper-Writing-Skills` + `research-skills`
- **Provider/API registry design:** `local-deep-research`, `free-llm-api-resources`, `public-api-lists`, `public-apis`
- **Memory/knowledge discipline:** `Auto-claude-code-research-in-sleep`, `AI-Researcher`, `AutoResearchClaw`

That combination preserves the local-first Windows-desktop target and avoids importing web-dashboard, cloud-first, or host-specific assumptions.

---

## Best research workflow foundation

### Best overall foundation

**Primary choice:** `deep-research` + `local-deep-researcher`

### Why

- `deep-research` provides the cleanest small iterative model:
  - generate query
  - search
  - summarize
  - reflect
  - recurse
  - report
- `local-deep-researcher` provides the most relevant **local LLM** version of that loop:
  - Ollama-first
  - local model routing
  - query/summarize/reflect prompts
  - lightweight configuration

### What to adopt

- depth/breadth iterative logic from `deep-research`
- local model loop from `local-deep-researcher`
- project-file output discipline from the user's spec

### What not to adopt

- Node/Express implementation from `deep-research`
- LangGraph runtime dependency chain from `local-deep-researcher`
- web UI assumptions from either repo

---

## Best agent/council structure

### Best strategy layer

**Primary choice:** `academic-research-skills` + `research-skills` + `council-of-high-intelligence`

### Why

- `academic-research-skills` has the strongest role definitions for integrity-sensitive academic tasks.
- `research-skills` has a clean research-survey/proposal agent split.
- `council-of-high-intelligence` has a compact and effective structured-disagreement protocol.

### Decision for The Prof

Use a **bounded agent registry** with:

- strategy/executive agents
- research and prior-art agents
- drafting/editorial agents
- adversarial reviewers
- optional council debate stage only when beneficial

### Resulting The Prof pattern

- not all agents run every time
- workflow engine selects only relevant agents
- council stage is used for conflict resolution, novelty pressure-testing, and review

---

## Best skill/prompt structure

### Best prompt/skill reference set

**Primary choice:** `AutoResearchClaw` + `Research-Paper-Writing-Skills` + `Deep-Research-skills` + `AI-Research-SKILLs`

### Why

- `AutoResearchClaw` demonstrates prompt externalization with a customizable YAML file.
- `Research-Paper-Writing-Skills` offers compact writing guidance with claim-evidence checks.
- `Deep-Research-skills` cleanly separates phases and uses structured outputs.
- `AI-Research-SKILLs` demonstrates scalable skill organization by category.

### Decision for The Prof

Implement editable skill files per agent with:

- role
- bounded task
- allowed actions
- prohibited actions
- hallucination controls
- input schema
- output schema
- review requirements

Store them locally under `the_prof/agents/skills/`.

---

## Best provider/API structure

### Best provider architecture reference

**Primary choice:** `local-deep-research` + `free-llm-api-resources` + `council-of-high-intelligence`

### Why

- `local-deep-research` has the strongest provider/settings discipline.
- `free-llm-api-resources` is a better source of legitimate free/trial provider metadata than `free-llm-api-keys`.
- `council-of-high-intelligence` has useful provider-slot and auto-routing concepts.

### Decision for The Prof

Implement:

- local Ollama provider
- generic OpenAI-compatible provider
- named wrappers for OpenAI/Anthropic/Kimi/GLM
- browser-login adapter stub disabled by default
- provider router with fallback order
- provider tester and usage logging

### Registry source priorities

1. `free-llm-api-resources`
2. `public-api-lists`
3. `public-apis`
4. curated subset from `API-mega-list`
5. explicit opt-in manual user additions

### Explicit rejection

Do **not** ingest or redistribute live keys from `free-llm-api-keys`.

---

## Best citation/source-validation logic

### Best reference

**Primary choice:** `AutoResearchClaw`

### Why

Its citation verification module is the most directly applicable engineering asset:

- arXiv lookup
- Crossref DOI lookup
- title similarity checks
- suspicious/hallucinated classification

### Reinforcement reference

`academic-research-skills` adds stronger provenance and claim-audit thinking.

### Decision for The Prof

Implement:

- source registry
- citation validator
- claim ledger
- source audit report
- final integrity report

With the rule:

- if support is absent, output `Do not know.`

---

## Best automation logic

### Best reference mix

- `AutoResearchClaw` for stage pipeline and test coverage
- `deep-research` for recursive iteration
- `gpt-researcher` for planner/execution/publisher decomposition

### Decision for The Prof

Use a **staged workflow engine** rather than a free-form agent swarm.

Benefits:

- easier testing
- easier audit trail generation
- clearer user-facing progress UI
- simpler Windows packaging

---

## Best local-first design ideas

### Best reference mix

- `local-deep-research`
- `local-deep-researcher`
- `Auto-claude-code-research-in-sleep`

### Decision for The Prof

Adopt these local-first principles:

- local projects as human-readable folders
- local `brain.md` as authoritative portable memory
- local-first provider routing with Ollama preferred
- no hidden server requirement
- user-visible logs for online activity
- offline-capable conservative mode

---

## Useful duplicated functionality

Duplicated functionality found across the study set:

- query -> search -> summarize -> reflect loops
- multi-agent writer/reviewer patterns
- skill-folder packaging conventions
- provider wrappers and model settings
- literature/source tracking
- markdown report generation
- local memory/wiki concepts

### Integration rule

Where multiple repos duplicate the same concept, prefer:

1. smallest understandable implementation
2. local-first implementation
3. audit-friendly implementation
4. permissive license implementation

---

## Obsolete, weak, or non-fit code

The following categories are non-fit for v1 and should be excluded:

- web dashboards/frontends from `gpt-researcher`, `local-deep-research`, `AI-Researcher`
- broad benchmark payloads from `AI-Researcher` and `AutoResearchClaw`
- cloud-first orchestration assumptions
- host-specific skill installers and plugin wrappers
- browser automation that could conflict with provider terms
- live public keys from `free-llm-api-keys`
- huge unfiltered API catalogs from `API-mega-list`

---

## Licensing and reuse constraints

### Safe direct-reuse candidates

Mostly permissive-license references:

- `AutoResearchClaw` (MIT)
- `deep-research` (MIT)
- `local-deep-researcher` (MIT)
- `Research-Paper-Writing-Skills` (MIT)
- `Deep-Research-skills` (MIT)
- `AI-Research-SKILLs` (MIT)
- `public-apis` (MIT)
- `public-api-lists` (MIT)
- `council-of-high-intelligence` (MIT)
- `gpt-researcher` (Apache-2.0)

### Rewrite-only references

Due to license or packaging concerns:

- `academic-research-skills` (CC BY-NC 4.0)
- `academic-research-skills-codex` (CC BY-NC 4.0)
- repositories with no clear license in the observed snapshot should be treated as idea sources only

---

## Integration priorities

### Priority 1 — Must implement immediately

1. Desktop shell in PySide6
2. Project creation and local folder output
3. Workflow engine
4. Agent registry and editable skill files
5. Brain memory system
6. Source registry and claim ledger
7. Citation validator
8. Ollama provider adapter
9. Provider fallback router
10. Markdown output generation

### Priority 2 — Important for practical use

1. API registry importer/tester
2. Council debate view
3. Provider usage/logging UI
4. Memory import/export
5. Integrity reports

### Priority 3 — Deferred or minimal in v1

1. broad online provider support beyond generic wrappers
2. advanced data experiment execution
3. non-Markdown export formats
4. browser-login automation beyond a disabled stub

---

## Final synthesis decision

The Prof should be implemented as a **desktop-native, staged, local-first academic research workbench** with:

- the iterative research core of `deep-research` / `local-deep-researcher`
- the audit rigor of `AutoResearchClaw` / `academic-research-skills`
- the proposal and survey role logic of `research-skills`
- the editorial discipline of `Research-Paper-Writing-Skills`
- the debate pattern of `council-of-high-intelligence`
- the provider/API registry discipline of `local-deep-research` and public API catalogs

This is the most compatible path with the user’s non-negotiable constraints and the Windows ZIP-distributable target.
