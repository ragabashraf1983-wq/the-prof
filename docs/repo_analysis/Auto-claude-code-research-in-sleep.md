# Repository Analysis — Auto-claude-code-research-in-sleep

- **Repository URL:** https://github.com/ragabashraf1983-wq/Auto-claude-code-research-in-sleep
- **Repository purpose:** ARIS methodology and research-wiki/audit oriented skill collection.

## Main modules/files

- **Top-level files/directories:** .env.example, .gitattributes, .github, .gitignore, AGENT_GUIDE.md, CONTRIBUTING.md, CONTRIBUTING_CN.md, LICENSE, README.md, README_CN.md, SETUP_GUIDE.md, SETUP_GUIDE_CN.md, aris-monitor, assets, community_papers, docs, mcp-servers, skills, templates, tests
- **Packaging/config files:** No packaging/build config detected.
- **Significant research/agent/provider files discovered:**
- `tests/test_mainline_large_payload_prompts.py`
- `skills`
- `skills/skills-codex-claude-review`
- `skills/skills-codex-gemini-review`
- `skills/skills-codex`
- `tests/test_codex_skill_mirror.py`
- `tools/check_skills_inventory.py`
- `tools/convert_skills_to_llm_chat.py`
- `tools/lint_skills_helpers.sh`
- `skills/shared-references/skill-governance.md`
- `.github/workflows/check-skills-inventory.yml`
- `.github/workflows/lint-skills-helpers.yml`
- `docs/tutorials/agent_foundations_tutorial.html`
- `docs/tutorials/agent_foundations_tutorial.md`
- `docs/tutorials/agent_foundations_tutorial.review.json`
- `docs/tutorials/agent_foundations_tutorial_en.html`
- `docs/tutorials/agent_foundations_tutorial_en.md`
- `docs/tutorials/agentic_rl_tutorial.html`
- `docs/tutorials/agentic_rl_tutorial.md`
- `docs/tutorials/agentic_rl_tutorial.review.json`

## Useful architecture

Methodology-first repo emphasizing audited output and research wiki memory.

## Useful prompts

Skill governance and citation-audit instructions are useful references.

## Useful agent logic

Research review/refine/wikis rather than app runtime agents.

## Useful research workflow logic

Research pipeline + refine + review loops with audit traces.

## Useful provider/API logic

Provider use is host-tool specific and not directly portable.

## Useful UI/dashboard ideas

ARIS monitor is interesting, but The Prof only needs a simpler live status pane.

## Useful storage/export logic

Research wiki concept is directly relevant to brain.md and project logs.

## Useful tests

Good evidence/audit oriented tests.

## Dependencies

No explicit dependencies observed in the shallow scan.

## Risks

- Best used for process ideas, not runtime code.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- MIT license.

## What to reuse directly

- Research-wiki idea, citation-audit skill, skill governance, tests around evidence capture.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Research-wiki memory and audit discipline reference.
- Memory files and audit trail into the_prof/brain and project outputs.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Host-specific Claude/Codex automation packaging and non-desktop tooling.
- Claude/Codex adaptation layers and unrelated multimedia expansions.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
