# Repository Analysis — AI-Researcher

- **Repository URL:** https://github.com/ragabashraf1983-wq/AI-Researcher
- **Repository purpose:** Large autonomous scientific innovation platform with many agents, memories, and benchmarks.

## Main modules/files

- **Top-level files/directories:** .env.template, .gitignore, Communication.md, README.md, assets, benchmark, benchmark_collection, docker, examples, global_state.py, main_ai_researcher.py, paper_agent, pyproject.toml, research_agent, setup.cfg, web_ai_researcher.py
- **Packaging/config files:** pyproject.toml, setup.cfg
- **Significant research/agent/provider files discovered:**
- `benchmark_collection/prompts`
- `paper_agent/gnn/writing_templates/abstract/prompt_tuning_for_graph_neural_networks_abstract_template.txt`
- `paper_agent/gnn/writing_templates/introduction/prompt_tuning_for_graph_neural_networks_introduction_template.txt`
- `paper_agent/gnn/writing_templates/methodology/prompt_tuning_for_graph_neural_networks_methodology_template.txt`
- `paper_agent/gnn/writing_templates/preliminaries/prompt_tuning_for_graph_neural_networks_preliminaries_template.txt`
- `benchmark/process/dataset_candidate/diffu_flow/metaprompt.py`
- `benchmark/process/dataset_candidate/gnn/metaprompt.py`
- `benchmark/process/dataset_candidate/reasoning/metaprompt.py`
- `benchmark/process/dataset_candidate/recommendation/metaprompt.py`
- `benchmark/process/dataset_candidate/vq/metaprompt.py`
- `benchmark/process/dataset_candidate/reasoning/math_reasoning/prompts.py`
- `paper_agent`
- `research_agent`
- `assets/researchagent.svg`
- `research_agent/inno/agents`
- `research_agent/inno/agents/inno_agent`
- `research_agent/inno/agents/inno_agent/idea_agent.py`
- `research_agent/inno/agents/inno_agent/judge_agent.py`
- `research_agent/inno/agents/inno_agent/ml_agent.py`
- `research_agent/inno/agents/inno_agent/plan_agent.py`

## Useful architecture

Rich multi-stage scientific research architecture with dedicated idea/plan/survey/memory submodules.

## Useful prompts

Many metaprompt templates for innovation and paper sections.

## Useful agent logic

Idea agent, judge agent, survey agent, plan agent, prepare agent, and memory modules.

## Useful research workflow logic

Concept intake, survey, innovation, implementation, evaluation, paper drafting.

## Useful provider/API logic

Implicit LLM integration patterns but not a clean local-first provider layer.

## Useful UI/dashboard ideas

Large web GUI exists conceptually, but The Prof should stay desktop only.

## Useful storage/export logic

Multiple memory classes and benchmark/result folders.

## Useful tests

Benchmark examples and experimental outputs rather than compact unit tests.

## Dependencies

build-backend, requires

## Risks

- Too large and specialized for first The Prof version.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- No license file detected in the shallow metadata snapshot; verify upstream before any direct reuse.

## What to reuse directly

- Idea/plan/survey agent roles, memory categories, benchmark artifacts for inspiration.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- High-level agent taxonomy and long-horizon pipeline reference.
- All concrete implementations to remove cloud/benchmark heaviness and preserve local-first scope.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Heavy benchmark data, large experimental code, browser/web assumptions, and domain-specific code runners.
- Heavy domain-specific experiment code and large benchmark payloads.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
