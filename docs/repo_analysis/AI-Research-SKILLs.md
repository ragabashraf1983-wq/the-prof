# Repository Analysis — AI-Research-SKILLs

- **Repository URL:** https://github.com/ragabashraf1983-wq/AI-Research-SKILLs
- **Repository purpose:** Large MIT skills library for end-to-end AI research tasks.

## Main modules/files

- **Top-level files/directories:** .claude-plugin, .github, .gitignore, 0-autoresearch-skill, 01-model-architecture, 02-tokenization, 03-fine-tuning, 04-mechanistic-interpretability, 05-data-processing, 06-post-training, 07-safety-alignment, 08-distributed-training, 09-infrastructure, 10-optimization, 11-evaluation, 12-inference-serving, 13-mlops, 14-agents, 15-rag, 16-prompt-engineering
- **Packaging/config files:** package.json
- **Significant research/agent/provider files discovered:**
- `16-prompt-engineering`
- `07-safety-alignment/prompt-guard`
- `packages/ai-research-skills/src/prompts.js`
- `0-autoresearch-skill`
- `anthropic_official_docs/skills_overview.md`
- `docs/skills.png`
- `packages/ai-research-skills`
- `video-promo/ai-research-skills-promo`
- `0-autoresearch-skill/references/skill-routing.md`
- `.github/workflows/sync-skills.yml`
- `14-agents`
- `22-agent-native-research-artifact`
- `packages/ai-research-skills/src/agents.js`
- `14-agents/llamaindex/references/agents.md`
- `14-agents/langchain/references/agents.md`
- `0-autoresearch-skill/references/agent-continuity.md`
- `16-prompt-engineering/instructor/references/providers.md`
- `21-research-ideation`
- `21-research-ideation/brainstorming-research-ideas`
- `21-research-ideation/creative-thinking-for-research`

## Useful architecture

Category-based skill library organization is a strong reference for editable skill files.

## Useful prompts

Many skill prompts/references, especially autoresearch and ML paper writing sections.

## Useful agent logic

Skill routing and research manager ideas.

## Useful research workflow logic

Autoresearch plus writing/ideation loops.

## Useful provider/API logic

Little direct provider logic.

## Useful UI/dashboard ideas

None.

## Useful storage/export logic

Templates, references, and research-state YAML ideas.

## Useful tests

Skill inventory sync workflows.

## Dependencies

No explicit dependencies observed in the shallow scan.

## Risks

- Use its organizational approach more than its domain-specific content.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- MIT license.

## What to reuse directly

- Skill packaging patterns, category organization, autoresearch concept.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Agent skill taxonomy and skill-folder organization reference.
- Selected skill structures into academic-general agent skill files.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Model-training-specific skills irrelevant to academic writing v1.
- Training/infrastructure skills irrelevant to The Prof v1.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
