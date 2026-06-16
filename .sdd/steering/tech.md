# Technology Stack

## Architecture

Methodology-first: no application code lives here. This repository provides the SDD framework (commands, templates, rules) that AI agents execute when specifying features in **external** project repositories.

## Core Technologies

- **AI Agents**: Claude Code (`.claude/commands/sdd/`) and Gemini (`.gemini/commands/sdd/`)
- **CI**: GitHub Actions — validates SDD structural conventions on every push
- **Spec format**: Markdown artifacts + `spec.json` (metadata, language config)

## SDD Phase Protocol

Each phase produces an artifact; human approval is required before the next phase starts:

| Phase | Command | Output artifact |
|---|---|---|
| 0 (optional) | `/sdd:steering` | `.sdd/steering/*.md` |
| 1a | `/sdd:spec-init "desc"` | `.sdd/specs/{feature}/spec.json` |
| 1b | `/sdd:spec-requirements {feature}` | `requirements.md` |
| 1c (optional) | `/sdd:validate-gap {feature}` | gap analysis report |
| 1d | `/sdd:spec-design {feature} [-y]` | `design.md` |
| 1e (optional) | `/sdd:validate-design {feature}` | design review report |
| 1f | `/sdd:spec-tasks {feature} [-y]` | `tasks.md` |
| 2 | `/sdd:spec-impl {feature} [tasks]` | implementation |

## Key Technical Decisions

- **`-y` flag** fast-tracks a phase past human review — use intentionally, not as default
- **Language**: Spec artifacts use the language set in `spec.json`; steering files default to English
- **Steering vs Specs**: Steering = project-wide memory (global, persistent); Specs = scoped feature contracts
- **Validation commands** (`validate-gap`, `validate-design`, `validate-impl`) are optional but recommended for existing codebases

---
_Document standards and patterns, not every dependency_
