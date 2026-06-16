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

```text
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

```text
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

## Guia para quem não conhece SDD

**O problema que o SDD resolve:** quando você pede para uma IA escrever código diretamente, ela toma decisões de design sem avisar e o resultado pode não ser o que você queria. Depois fica difícil saber "por que foi feito assim?"

**A ideia central:** antes de escrever código, você formaliza o QUE quer (requisitos) e COMO vai ser feito (design), com aprovação humana entre cada etapa. A IA só implementa depois que você aprovou o plano.

### O fluxo em linguagem simples

```text
1. /sdd:spec-init "o que você quer fazer"
   → Cria uma pasta para essa funcionalidade

2. /sdd:spec-requirements {nome-da-funcionalidade}
   → IA gera o documento "O QUE o sistema deve fazer" (sem código)
   → VOCÊ revisa e aprova (ou pede ajustes)

3. /sdd:spec-design {nome}
   → IA gera o documento "COMO vai ser feito" (arquitetura, componentes)
   → VOCÊ revisa e aprova

4. /sdd:spec-tasks {nome}
   → IA gera a lista de tarefas de implementação
   → VOCÊ revisa e aprova

5. /sdd:spec-impl {nome}
   → Agora sim: IA escreve o código seguindo tudo que foi aprovado
```

### Analogia do dia a dia

Pense como uma construção: você não pede para um pedreiro começar a construir sem plantas. O SDD é o processo de fazer as plantas (requisitos e design) antes de pegar a ferramenta. A IA é o pedreiro; você é o arquiteto que aprova cada planta.

### Onde ficam os arquivos

```text
.sdd/specs/nome-da-funcionalidade/
  spec.json         ← estado atual (em qual fase está)
  requirements.md   ← O QUE deve fazer (você aprova)
  design.md         ← COMO vai ser feito (você aprova)
  tasks.md          ← lista de tarefas (você aprova)
  research.md       ← anotações de pesquisa da IA (leitura opcional)
```

### Specs em andamento

| Funcionalidade | Fase atual | Próxima ação |
| --- | --- | --- |
| `pipeline-encoding-fix` | design gerado | Revisar `design.md` e aprovar → `/sdd:spec-tasks pipeline-encoding-fix` |
| `backlog-redmine-sync` | inicializado | `/sdd:spec-requirements backlog-redmine-sync` |
| `ai-metrics-incident-report` | inicializado | `/sdd:spec-requirements ai-metrics-incident-report` |

---

_Repositório: `ericson-j-santos/my-first-spec-project` · Branch: `master`_
