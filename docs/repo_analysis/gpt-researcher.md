# Repository Analysis — gpt-researcher

- **Repository URL:** https://github.com/ragabashraf1983-wq/gpt-researcher
- **Repository purpose:** Mature deep-research system with planner/execution/publisher architecture and strong report generation.

## Main modules/files

- **Top-level files/directories:** .claude, .codex-plugin, .cursorignore, .cursorrules, .dockerignore, .env.example, .github, .gitignore, .mcp.json, .python-version, .vscode, CODE_OF_CONDUCT.md, CONTRIBUTING.md, CURSOR_RULES.md, Dockerfile, Dockerfile.fullstack, LICENSE, PR_pr_feat-anthropic-real-usage-cost-tracking.md, PR_pr_fix-brave-snippet-bypasses-scraper.md, Procfile
- **Packaging/config files:** pyproject.toml, requirements.txt, setup.py, Dockerfile, docker-compose.yml
- **Significant research/agent/provider files discovered:**
- `gpt_researcher/prompts.py`
- `docs/docs/examples/custom_prompt.py`
- `.claude/references/prompts.md`
- `skills`
- `gpt_researcher/skills`
- `gpt_researcher/scraper/browser/processing/scrape_skills.py`
- `docs/docs/gpt-researcher/gptr/claude-skill.md`
- `multi_agents`
- `multi_agents_ag2`
- `gpt_researcher/agent.py`
- `multi_agents/agent.py`
- `multi_agents/agents`
- `multi_agents_ag2/agents`
- `tests/test_agent_discovery.py`
- `tests/test_multi_agents_plan_revisions.py`
- `tests/test_new_agents.py`
- `gpt_researcher/actions/agent_creator.py`
- `frontend/nextjs/public/img/agents`
- `docs/static/img/multi-agent.png`
- `docs/docs/gpt-researcher/multi_agents`

## Useful architecture

Planner -> execution agents -> publisher/reporter architecture is directly relevant to The Prof.

## Useful prompts

Prompt and parsing conventions for research/deep research are useful.

## Useful agent logic

Multi-agent decomposition, researcher memory, and conductor/retriever split.

## Useful research workflow logic

Question generation, source gathering, summarization, aggregation, report writing.

## Useful provider/API logic

LLM provider abstraction patterns and model-specific configuration.

## Useful UI/dashboard ideas

Research sidebar/content layout ideas, but not the web implementation.

## Useful storage/export logic

Research history and memory layers are relevant conceptual inputs.

## Useful tests

Agent discovery, parsing, deep-research, quick search, logging tests.

## Dependencies

Elovic, PyMuPDF, SQLAlchemy, addopts, aiofiles, aiohappyeyeballs, aiohttp, aiosignal, annotated-types, anyio, arxiv, asyncio_fixture_loop_scope, asyncio_mode, attrs, authors, backoff, beautifulsoup4, brotli, build-backend, certifi, cffi, chardet, charset-normalizer, click, colorama, cryptography, cssselect2, dataclasses-json, ddgs, dependencies, description, dev, distro, docopt, duckduckgo-search, duckduckgo_search, email, emoji, extras, fastapi

## Risks

- Useful concepts are portable; large web product is not.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- Apache-2.0 license.

## What to reuse directly

- Planner/execution/publisher workflow, response parsing hardening, local/web report structure.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Research orchestration and robust parsing reference.
- Provider routing, report generation, and project storage to fit local-first desktop usage.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Web frontend, MCP server, full-stack deployment assumptions, and image generation extras.
- Next.js/fastapi frontend stack and remote-first deployment pieces.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
