# my-first-spec-project

> Laboratório de **Desenvolvimento Guiado por Especificação (SDD)** — metodologia agnóstica de IA para desenvolvimento orientado por especificações formais.

---

## O que é este repositório?

Este repositório serve como **ponto de coordenação** de projetos desenvolvidos com a metodologia SDD, usando Gemini/Copilot como assistentes de especificação. Veja [GEMINI.pt-br.md](./GEMINI.pt-br.md) para o guia completo da metodologia.

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
Fase 0 (opcional): /sdd:steering
Fase 1 (Especificação):
  /sdd:spec-init "descrição"
  /sdd:spec-requirements {feature}
  /sdd:spec-design {feature} [-y]
  /sdd:spec-tasks {feature} [-y]
Fase 2 (Implementação):
  /sdd:spec-impl {feature} [tasks]
  /sdd:spec-status {feature}
```

## Estrutura

```
.sdd/
  specs/        ← especificações individuais de features
  steering/     ← contexto e regras globais do projeto
GEMINI.pt-br.md ← guia da metodologia SDD
scripts/sdd_status.py ← valida os metadados e gera o dashboard
.gemini/        ← configurações do Gemini
.github/
  workflows/
    ci.yml      ← validação da estrutura SDD
```

## Specs em andamento

| Funcionalidade | Fase atual | Próxima ação |
| --- | --- | --- |
| `ai-metrics-incident-report` | inicializado | `/sdd:spec-requirements ai-metrics-incident-report` |
| `autenticacao-de-usuarios` | design gerado · bloqueado | Os documentos atuais descrevem exportação em PDF; substituir ou renomear antes de aprovar |
| `backlog-redmine-sync` | inicializado | `/sdd:spec-requirements backlog-redmine-sync` |
| `exemplo-feature` | design gerado · requer revisão | Revisar requisitos e design legados antes de gerar tarefas |
| `pipeline-encoding-fix` | implementado | Validar a implementação e manter a spec sincronizada |

O arquivo [`sdd-dashboard.html`](./sdd-dashboard.html) é gerado de forma determinística a partir dos cinco `spec.json`. Use `python scripts/sdd_status.py --check` para validar os metadados e detectar divergências.

---

_Repositório: `ericson-j-santos/my-first-spec-project` · Branch: `master`_
