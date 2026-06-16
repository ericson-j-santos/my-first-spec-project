# Project Structure

## Organization Philosophy

Clear separation between framework metadata (`.sdd/settings/`), persistent project knowledge (`.sdd/steering/`), and feature contracts (`.sdd/specs/`). AI agent instructions live in agent-specific files at the repo root.

## Directory Patterns

### Steering — Project Memory
**Location**: `.sdd/steering/`  
**Purpose**: Persistent AI context loaded on every session — what the project is, how it's built, what the conventions are  
**Core files**: `product.md`, `tech.md`, `structure.md` plus optional custom files for specialized concerns (e.g., `api-standards.md`, `security.md`)

### Feature Specs
**Location**: `.sdd/specs/{feature-name}/`  
**Purpose**: Formal contract for a single feature — one directory per feature, independent lifecycle  
**Contents**: `spec.json` (metadata + language), `requirements.md`, `design.md`, `tasks.md`  
**Example**: `.sdd/specs/backlog-redmine-sync/requirements.md`

### Agent Commands
**Location**: `.claude/commands/sdd/` and `.gemini/commands/sdd/`  
**Purpose**: Agent-specific implementations of SDD slash commands; both implement the same phase protocol  
**Note**: Don't document agent tooling internals in steering — they're framework plumbing

### SDD Framework Metadata
**Location**: `.sdd/settings/`  
**Purpose**: Rules and templates consumed by commands; not project knowledge — not documented in steering

## Naming Conventions

- **Feature dirs**: `kebab-case` (e.g., `backlog-redmine-sync`, `pipeline-encoding-fix`)
- **Custom steering files**: `kebab-case.md` (e.g., `api-standards.md`, `deployment.md`)
- **Agent commands**: `sdd:{verb}-{noun}` (e.g., `/sdd:spec-init`, `/sdd:validate-design`)

## Code Organization Principles

- Steering captures patterns, not file trees — one annotated example beats a 50-line path list
- Specs are scoped to one feature; cross-cutting concerns go in steering or custom steering files
- External project repos own their implementation; this repo owns only their specs

---
_Document patterns, not file trees. New files following patterns shouldn't require steering updates_
