# Repository Analysis — local-deep-research

- **Repository URL:** https://github.com/ragabashraf1983-wq/local-deep-research
- **Repository purpose:** Large local-first research product with provider abstractions, search stack, and extensive tests.

## Main modules/files

- **Top-level files/directories:** .file-whitelist.txt, .github, .gitignore, .gitleaks.toml, .gitleaksignore, .grype.yaml, .hadolint.yaml, .nvmrc, .pre-commit-config.yaml, .pre-commit-hooks, .safety-policy.yml, .semgrep, .trivyignore, .yamllint.yaml, .zap, CONTRIBUTING.md, Dockerfile, LICENSE, MANIFEST.in, README.md
- **Packaging/config files:** pyproject.toml, package.json, Dockerfile, docker-compose.yml
- **Significant research/agent/provider files discovered:**
- `tests/performance/relevance_filter/eval_prompt.py`
- `src/local_deep_research/advanced_search_system/tools/fetch/prompts.py`
- `cookiecutter-docker/hooks/pre_prompt.py`
- `changelog.d/+collection-exclude-from-agent.feature.md`
- `tests/security/test_collection_agent_enabled.py`
- `tests/strategies/test_langgraph_agent_strategy.py`
- `tests/strategies/test_langgraph_subagent_context.py`
- `tests/web_search_engines/test_engine_user_agents.py`
- `tests/js/components/progress-agent-thinking.test.js`
- `src/local_deep_research/database/migrations/versions/0012_add_collection_agent_enabled.py`
- `src/local_deep_research/advanced_search_system/strategies/langgraph_agent_strategy.py`
- `tests/llm_providers`
- `tests/test_llm_provider_integration.py`
- `tests/config/test_context_window_provider.py`
- `tests/embeddings/test_base_provider.py`
- `tests/llm/providers`
- `tests/llm/test_provider_base_url_ssrf.py`
- `tests/llm_providers/test_base_provider_keys.py`
- `tests/llm_providers/test_ollama_provider.py`
- `tests/llm_providers/test_providers_high_value.py`

## Useful architecture

Strong reference for separating provider layer, search services, settings, and tests in a local-first product.

## Useful prompts

Prompt fragments around search/fetch summarization are informative but too coupled to its stack.

## Useful agent logic

LangGraph/search strategies and provider abstractions are useful patterns.

## Useful research workflow logic

Deep research lifecycle, scheduler, history, and research library components.

## Useful provider/API logic

Best reference for provider settings taxonomy, availability tests, and secure egress thinking.

## Useful UI/dashboard ideas

Settings-heavy control panels and provider options, though web-oriented.

## Useful storage/export logic

Encrypted/local DB, settings JSON, backup concerns, library/download management.

## Useful tests

Extensive provider, security, settings, and research API tests.

## Dependencies

--version, ., @fortawesome/fontawesome-free, @vitest/coverage-v8, Pillow, X.Y.Z, aiohttp, alembic, apprise, apscheduler, arxiv, authors, beautifulsoup4, bootstrap, bootstrap-icons, branch, build-backend, cachetools, category, chart.js, chartjs-adapter-date-fns, chartjs-plugin-annotation, check_untyped_defs, classifiers, click, cookiecutter, crawl4ai, cryptography, datasets, date, date-fns, defusedxml, dependencies, description, dev, directory, disallow_untyped_defs, distribution, dompurify, duckduckgo-search

## Risks

- Too large to vendor; selective adaptation only.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- MIT license.

## What to reuse directly

- Provider configuration shape, settings taxonomy, security test ideas, search-service decomposition.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Architecture reference for local-first configuration, provider registry patterns, and security hardening.
- Desktop-friendly settings, provider registry, and search pipeline.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Flask/web UI, heavy database/search stack, and cloud-first optional subsystems.
- Flask frontend, heavy DB/search engine integrations, and unrelated features (news, accessibility suites, etc.).
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
