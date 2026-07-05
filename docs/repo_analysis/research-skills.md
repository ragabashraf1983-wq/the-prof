# Repository Analysis — research-skills

- **Repository URL:** https://github.com/ragabashraf1983-wq/research-skills
- **Repository purpose:** Academic workflow skill collection including multi-agent survey and proposal writing.

## Main modules/files

- **Top-level files/directories:** .gitignore, README.md, agents-config, medical-imaging-review, paper-slide-deck, references, research-proposal, skills
- **Packaging/config files:** No packaging/build config detected.
- **Significant research/agent/provider files discovered:**
- `paper-slide-deck/references/base-prompt.md`
- `skills`
- `agents-config`
- `research-proposal`

## Useful architecture

Simple multi-agent survey system specialized for literature reviews and proposals.

## Useful prompts

Proposal-writing and survey-role guides are valuable references.

## Useful agent logic

Survey director, literature scout, paper analyst, survey writer, quality editor.

## Useful research workflow logic

Proposal intake, literature strategy, outline, drafting, quality review.

## Useful provider/API logic

Zotero MCP references are useful conceptually but not core for v1.

## Useful UI/dashboard ideas

No app UI; content suggests what setup questions matter.

## Useful storage/export logic

References folder and agent-config split are easy to map to The Prof skills.

## Useful tests

None notable.

## Dependencies

No explicit dependencies observed in the shallow scan.

## Risks

- Good content model; direct code reuse depends on upstream license verification.
- Additional risk: dependencies and examples in this repo are often broader than The Prof needs; over-importing would increase maintenance cost.

## Licensing/attribution notes if available

- No explicit license detected in snapshot; use as inspiration and rewrite.

## What to reuse directly

- Research proposal structure, survey director/scout/analyst/writer/editor role split.
- Decision reason: selective reuse saves time only when it does not import unsafe assumptions, excessive dependencies, or licensing problems.

## What to rewrite

- Proposal and survey-agent role reference.
- All content into original local-first workflows and editable skills.
- Decision reason: The Prof is a Windows desktop, local-first, audit-heavy application, so most source material must be translated into a simpler and more controlled architecture.

## What to ignore

- Single-tool installation details and domain-specific slide generation extras.
- Slide-deck subsystem and external MCP assumptions for the first version.
- Decision reason: these parts do not improve the first working desktop version, or they conflict with the non-negotiable constraints.
