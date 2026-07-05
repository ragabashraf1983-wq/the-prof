# Repository Analysis — council-of-high-intelligence

- **Repository URL:** https://github.com/ragabashraf1983-wq/council-of-high-intelligence
- **Repository purpose:** Multi-persona deliberation skill with provider auto-routing.

## Main modules/files

- **Top-level files/directories:** .DS_Store, .gitattributes, .github, .gstack, CHANGELOG.md, CLAUDE.md, CONTRIBUTING.md, LICENSE, README.md, SKILL.codex.md, SKILL.gemini.md, SKILL.md, agents, assets, configs, demos, install.sh, scripts
- **Packaging/config files:** No packaging/build config detected.
- **Significant research/agent/provider files discovered:**
- `agents`
- `configs/provider-model-slots.cursor.example.yaml`
- `configs/provider-model-slots.example.yaml`
- `configs/provider-model-slots.nim.example.yaml`
- `scripts/detect-providers.sh`
- `.github/workflows`

## Useful architecture

Deliberation protocol separated from provider routing/config.

## Useful prompts

Council skill and verdict template provide a compact debate scaffold.

## Useful agent logic

Independent-perspective discussion, dissent quotas, unresolved-question emphasis.

## Useful research workflow logic

Quick/duo/full debate modes and final verdict synthesis.

## Useful provider/API logic

Provider slot configs and provider detection script are very relevant.

## Useful UI/dashboard ideas

Council debate transcript and verdict panels.

## Useful storage/export logic

Session pack/verdict templates can inspire debate logging.

## Useful tests

Minimal, but scripts/configs are simple.

## Dependencies

No explicit dependencies observed in the shallow scan.

## Risks

- Adapt the debate mechanics, not the named personas.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- MIT license.

## What to reuse directly

- Structured disagreement protocol, provider-model slot config, auto-detection shell logic.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Council debate and provider slotting reference.
- Persona content and shell detection into Python.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Brand/persona content that does not map directly to academic research.
- Non-academic named personas as default system agents.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
