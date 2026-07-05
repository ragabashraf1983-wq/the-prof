# Repository Analysis — Deep-Research-skills

- **Repository URL:** https://github.com/ragabashraf1983-wq/Deep-Research-skills
- **Repository purpose:** Two-phase deep research skill set with search modules and JSON validation.

## Main modules/files

- **Top-level files/directories:** LICENSE, README.md, README.zh.md, agents, agents-codex, scripts, skills, tests, workflow.png
- **Packaging/config files:** No packaging/build config detected.
- **Significant research/agent/provider files discovered:**
- `skills`
- `agents-codex`
- `agents`
- `agents/web-search-agent.md`
- `agents-codex/web-researcher.toml`
- `agents-codex/web-search-modules`
- `agents/web-search-modules`
- `agents/web-search-opencode.md`
- `skills/research-codex-en`
- `skills/research-codex-zh`
- `skills/research-en`
- `skills/research-zh`
- `skills/research-codex-en/research-add-fields`
- `skills/research-codex-en/research-add-items`
- `skills/research-codex-en/research-deep`
- `skills/research-codex-en/research-report`
- `skills/research-codex-en/research`
- `skills/research-codex-zh/research-add-fields`
- `skills/research-codex-zh/research-add-items`
- `skills/research-codex-zh/research-deep`

## Useful architecture

Clean two-phase skill decomposition and modular search-agent setup.

## Useful prompts

Research / deep / report skill prompts provide compact phase framing.

## Useful agent logic

Web researcher agent + modules; clear separation of concerns.

## Useful research workflow logic

Outline generation before deep investigation, then report generation.

## Useful provider/API logic

Search backend selection notes are useful.

## Useful UI/dashboard ideas

None.

## Useful storage/export logic

YAML/JSON validation helper concept for structured intermediates.

## Useful tests

Codex install smoke test and JSON validation helper.

## Dependencies

No explicit dependencies observed in the shallow scan.

## Risks

- Portable methodology, lightweight code.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- MIT license.

## What to reuse directly

- Outline + deep-investigation split, search-module separation, JSON validation helper idea.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Workflow-shaping reference for HITL/autonomous research stages.
- Desktop workflow and local schemas.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Host-specific skill installation scripts.
- Tool-host installation specifics.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
