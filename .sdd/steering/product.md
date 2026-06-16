# Product Overview

Multi-project SDD coordination lab. This repository is the operational base for applying Spec-Driven Development across a portfolio of Python/FastAPI + Vue 3 projects, using AI assistants (Claude Code, Gemini) as specification partners.

## Core Capabilities

- Structured specification workflow with human-approval gates between phases
- AI-agnostic: same SDD workflow runs on Claude Code and Gemini via their respective command systems
- Cross-project coordination: one lab manages specs for multiple external codebases
- Gap analysis support for adding specs to already-existing code
- CI validation of SDD structural conventions

## Target Use Cases

- Specifying new features for any coordinated project **before** writing implementation code
- Producing a formal paper trail (requirements → design → tasks) that survives model or team changes
- Gap analysis when retrofitting specs onto an existing codebase

## Value Proposition

Prevents AI-generated code drift by formalizing intent before implementation. Each feature has traceable artifacts that answer "why was this built this way?" independently of who (or which model) built it.

## Coordinated Projects

| Project | Stack | Status |
|---|---|---|
| ReqSys v2 Enterprise | FastAPI + Vue 3 + SQLite/SQL Server | Active |
| AI Metrics Backend | FastAPI + SQLite | Active |
| AI Metrics Frontend | Vue 3 + Vuetify + Vitest | Active |
| Teams Outbox v2 | FastAPI + SQL Server + Vue 3 | Stable |
| Pipeline Redmine | Python CLI | Stable |

---
_Focus on patterns and purpose, not exhaustive feature lists_
