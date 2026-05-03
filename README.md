# my-first-spec-project

> Laboratório de **Spec-Driven Development (SDD)** — metodologia AI-agnóstica para desenvolvimento guiado por especificações formais.

---

## O que é este repositório?

Este repositório serve como **ponto de coordenação** de projetos desenvolvidos com metodologia SDD, usando Gemini/Copilot como assistentes de especificação. Veja [GEMINI.md](./GEMINI.md) para o guia completo da metodologia.

## Projetos relacionados

Este repositório coordena e documenta os seguintes projetos locais:

| Projeto              | Stack                               | Status     |
| -------------------- | ----------------------------------- | ---------- |
| ReqSys v2 Enterprise | FastAPI + Vue 3 + SQLite/SQL Server | ✅ Ativo   |
| AI Metrics Backend   | FastAPI + SQLite + Incidentes       | ✅ Ativo   |
| AI Metrics Frontend  | Vue 3 + Vuetify + Vitest            | ✅ Ativo   |
| Teams Outbox v2      | FastAPI + SQL Server + Vue 3        | ✅ Ativo   |
| Pipeline Redmine     | Python CLI                          | ✅ Estável |

## Workflow SDD resumido

```
Phase 0 (opcional): /sdd:steering
Phase 1 (Especificação):
  /sdd:spec-init "descrição"
  /sdd:spec-requirements {feature}
  /sdd:spec-design {feature} [-y]
  /sdd:spec-tasks {feature} [-y]
Phase 2 (Implementação):
  /sdd:spec-impl {feature} [tasks]
  /sdd:spec-status {feature}
```

## Estrutura

```
.sdd/
  specs/        ← specs individuais de features
  steering/     ← contexto e regras globais do projeto
GEMINI.md       ← guia da metodologia SDD
.gemini/        ← configurações do Gemini
.github/
  workflows/
    ci.yml      ← validação de estrutura SDD
```

---

_Repositório: `ericson-j-santos/my-first-spec-project` · Branch: `master`_
