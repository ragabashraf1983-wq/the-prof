# Repository Analysis — deep-research

- **Repository URL:** https://github.com/ragabashraf1983-wq/deep-research
- **Repository purpose:** Minimal TypeScript deep-research loop emphasizing depth/breadth recursion.

## Main modules/files

- **Top-level files/directories:** .env.example, .gitignore, .nvmrc, .prettierignore, Dockerfile, LICENSE, README.md, docker-compose.yml, package-lock.json, package.json, prettier.config.mjs, report.md, src, tsconfig.json
- **Packaging/config files:** package.json, Dockerfile, docker-compose.yml
- **Significant research/agent/provider files discovered:**
- `src/prompt.ts`
- `src/ai/providers.ts`
- `src/deep-research.ts`
- `src/ai/text-splitter.test.ts`

## Useful architecture

The cleanest minimal recursive search architecture among studied repos.

## Useful prompts

Short prompt set appropriate for query/reflection/report cycles.

## Useful agent logic

Single-agent iterative refinement rather than large councils.

## Useful research workflow logic

Depth/breadth recursion, parallel search batches, markdown report output.

## Useful provider/API logic

Simple ai-sdk provider split; concept only.

## Useful UI/dashboard ideas

None needed; CLI/API oriented.

## Useful storage/export logic

Markdown report output and lightweight state passing.

## Useful tests

Text-splitter tests only; limited but useful for robustness mindset.

## Dependencies

@ai-sdk/fireworks, @ai-sdk/openai, @ianvs/prettier-plugin-sort-imports, @mendable/firecrawl-js, @types/cors, @types/express, @types/lodash-es, @types/node, @types/uuid, ai, cors, express, js-tiktoken, lodash-es, p-limit, prettier, tsx, typescript, uuid, zod

## Risks

- Rewrite in Python instead of porting TypeScript verbatim.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- MIT license.

## What to reuse directly

- Depth/breadth stage design, parallel search idea, concise prompt flow.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Best small conceptual foundation for iterative search/reflection loop.
- Python implementation with stronger audit and memory layers.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Express API wrapper and Node-specific implementation details.
- Express API server and TS-specific utilities.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
