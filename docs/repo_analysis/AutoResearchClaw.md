# Repository Analysis — AutoResearchClaw

- **Repository URL:** https://github.com/ragabashraf1983-wq/AutoResearchClaw
- **Repository purpose:** Autonomous research pipeline with prompts YAML, citation verification, skills, and many tests.

## Main modules/files

- **Top-level files/directories:** .claude, .gitignore, CONTRIBUTING.md, LICENSE, README.md, RESEARCHCLAW_AGENTS.md, RESEARCHCLAW_CLAUDE.md, config.researchclaw.example.yaml, docs, experiments, external, frontend-legacy, image, prompts.default.yaml, pyproject.toml, researchclaw, run_hep_pipeline.sh, scripts, sentinel.sh, tests
- **Packaging/config files:** pyproject.toml
- **Significant research/agent/provider files discovered:**
- `prompts.default.yaml`
- `researchclaw/prompts`
- `tests/test_hep_prompt_hygiene.py`
- `tests/test_prompt_adapter.py`
- `tests/test_rc_prompts.py`
- `researchclaw/domains/prompt_adapter.py`
- `experiments/arc_bench/scripts/prompts`
- `experiments/arc_bench/scripts/prompts/manual_strict_audit_prompt.md`
- `.claude/skills`
- `researchclaw/skills`
- `tests/test_skills_library.py`
- `tests/test_metaclaw_bridge/test_lesson_to_skill.py`
- `tests/test_metaclaw_bridge/test_skill_feedback.py`
- `tests/test_metaclaw_bridge/test_stage_skill_map.py`
- `researchclaw/metaclaw_bridge/lesson_to_skill.py`
- `researchclaw/metaclaw_bridge/skill_feedback.py`
- `researchclaw/metaclaw_bridge/stage_skill_map.py`
- `external/agents/Biology-Agent/skills`
- `external/agents/stat_research_agent/skills`
- `external/agents`

## Useful architecture

Most complete stage-based autonomous research pipeline in the study set.

## Useful prompts

External prompt YAML with stage blocks is highly reusable as a customization pattern.

## Useful agent logic

Multiple agents, domain adapters, benchmark/citation/decision agents.

## Useful research workflow logic

Idea -> literature -> code/experiment -> review/publish with HITL options.

## Useful provider/API logic

Config-driven provider setup and tests around providers.

## Useful UI/dashboard ideas

Legacy frontend exists, but the better input is workflow visibility and stage naming.

## Useful storage/export logic

Pipeline state, lessons/skills, memory, reports.

## Useful tests

Outstanding breadth: citation verify, memory, prompts, runner, literature, code agent tests.

## Dependencies

PyMuPDF, all, anthropic, arxiv, build-backend, crawl4ai, dependencies, description, dev, httpx, huggingface-hub, license, matplotlib, name, numpy, packages, pdf, pytest, pytest-asyncio, pyyaml, readme, requires, requires-python, researchclaw, rich, scholarly, scipy, tavily-python, text, version, web

## Risks

- Selective extraction/rewrite is worthwhile.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- MIT license.

## What to reuse directly

- Prompt externalization, staged pipeline, citation verification, memory patterns, tests.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Strongest engineering reference for audit-heavy autonomous research.
- Stage runner, memory, and desktop-specific orchestration.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Legacy frontend, domain-specific experiment sandboxes, huge optional execution stack.
- Legacy frontend, domain-specific sandboxes, and overly broad benchmark machinery.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
