# Repository Analysis — Research-Paper-Writing-Skills

- **Repository URL:** https://github.com/ragabashraf1983-wq/Research-Paper-Writing-Skills
- **Repository purpose:** Focused academic writing skill with section guides and claim-evidence mapping.

## Main modules/files

- **Top-level files/directories:** .gitignore, LICENSE, README.md, README_zh.md, research-paper-writing
- **Packaging/config files:** No packaging/build config detected.
- **Significant research/agent/provider files discovered:**
- `research-paper-writing/agents`
- `research-paper-writing`
- `research-paper-writing/references/does-my-writing-flow-source.md`

## Useful architecture

Small, focused skill package with references separated by section.

## Useful prompts

Section guides and claim-evidence map output contract are very reusable.

## Useful agent logic

Implicit editor/reviewer behavior rather than runtime code.

## Useful research workflow logic

Section drafting -> reverse outlining -> adversarial review -> claim-evidence check.

## Useful provider/API logic

None.

## Useful UI/dashboard ideas

Skill editor can expose these section rules cleanly.

## Useful storage/export logic

Reference markdown files map well to editable agent skills.

## Useful tests

None, but the package is easy to inspect.

## Dependencies

No explicit dependencies observed in the shallow scan.

## Risks

- Compact and useful to adapt into editable agent skills.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- MIT license.

## What to reuse directly

- Section-specific guidance, paragraph clarity checks, claim-evidence map output contract.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Writing-quality and self-review reference.
- The Prof-specific skill files and output contracts.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Single-host skill installation instructions.
- Host-specific installation text.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
