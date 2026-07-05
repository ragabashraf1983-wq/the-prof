# Repository Analysis — academic-research-skills

- **Repository URL:** https://github.com/ragabashraf1983-wq/academic-research-skills
- **Repository purpose:** Comprehensive academic research skill suite with strong integrity gates and claim-audit design.

## Main modules/files

- **Top-level files/directories:** .claude, .claude-plugin, .command-invariants.toml, .gitattributes, .github, .gitignore, .gitleaks.toml, CHANGELOG.md, CITATION.cff, CONTRIBUTING.md, LICENSE, MODE_REGISTRY.md, NOTICE.md, POSITIONING.md, QUICKSTART.md, README.ja-JP.md, README.ko-KR.md, README.md, README.zh-CN.md, README.zh-TW.md
- **Packaging/config files:** pyproject.toml
- **Significant research/agent/provider files discovered:**
- `scripts/check_judge_prompt_version.py`
- `scripts/test_check_judge_prompt_version.py`
- `skills`
- `scripts/_skill_lint.py`
- `agents`
- `academic-paper-reviewer/agents`
- `academic-paper/agents`
- `academic-pipeline/agents`
- `agents/report_compiler_agent.md`
- `agents/research_architect_agent.md`
- `agents/synthesis_agent.md`
- `deep-research/agents`
- `scripts/check_agents_mirror_sync.py`
- `scripts/test_check_agents_mirror_sync.py`
- `shared/agents`
- `tests/fixtures/v3_6_7_pattern_eval/integration/chapter_level_run/round_1/report_compiler_agent`
- `tests/fixtures/v3_6_7_pattern_eval/integration/chapter_level_run/round_1/research_architect_agent`
- `tests/fixtures/v3_6_7_pattern_eval/integration/chapter_level_run/round_1/synthesis_agent`
- `tests/fixtures/v3_6_7_pattern_eval/integration/chapter_level_run/round_2/report_compiler_agent`
- `tests/fixtures/v3_6_7_pattern_eval/integration/chapter_level_run/round_2/research_architect_agent`

## Useful architecture

Best normative design for integrity gates, provenance, and agent schemas.

## Useful prompts

Many agent markdown files provide strong role framing.

## Useful agent logic

Pipeline orchestrator, integrity verifier, claim-ref alignment auditor, source verification agent, reviewer agents.

## Useful research workflow logic

Deep research, paper writing, review, temporal verification, trust provenance.

## Useful provider/API logic

Cross-model verification ideas only; local-first The Prof should keep providers thinner.

## Useful UI/dashboard ideas

No desktop UI, but the stage/state vocabulary is very useful.

## Useful storage/export logic

Extensive artifact and audit discipline.

## Useful tests

Claim-audit pipeline tests and many consistency scripts.

## Dependencies

pythonpath

## Risks

- Rewrite concepts into original code and local skill files.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- CC BY-NC 4.0; do not directly copy substantial content into a general software repo.

## What to reuse directly

- Agent schemas, integrity gates, temporal verification and provenance concepts.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Best integrity-policy reference, but not for direct code vendoring.
- Agent roles, integrity rules, and audit requirements into original The Prof skill files and code.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Claude-plugin packaging, optional PDF/DOCX export stack, noncommercial-licensed content.
- Claude/plugin-specific packaging and optional DOCX/PDF pathways for v1.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
