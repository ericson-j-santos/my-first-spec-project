# Desenvolvimento Guiado por Especificação Assistido por IA

Implementação de Spec Driven Development agnóstica de ferramenta de IA

## Contexto do Projeto

### Caminhos

- Steering: `.sdd/steering/`
- Specs: `.sdd/specs/`

### Steering vs Especificação

**Steering** (`.sdd/steering/`) - Guia a IA com regras e contexto globais do projeto
**Specs** (`.sdd/specs/`) - Formaliza o processo de desenvolvimento para features individuais

### Especificações Ativas

- Verifique `.sdd/specs/` para especificações ativas
- Use `/sdd:spec-status [nome-da-feature]` para checar o progresso

## Diretrizes de Desenvolvimento

- Pense em inglês, gere respostas em inglês. Todo conteúdo Markdown gravado nos arquivos do projeto (ex: requirements.md, design.md, tasks.md, research.md, relatórios de validação) DEVE ser escrito no idioma alvo configurado para esta especificação (veja spec.json.language).

## Workflow Mínimo

- Fase 0 (opcional): `/sdd:steering`, `/sdd:steering-custom`
- Fase 1 (Especificação):
  - `/sdd:spec-init "descrição"`
  - `/sdd:spec-requirements {feature}`
  - `/sdd:validate-gap {feature}` (opcional: para código legado)
  - `/sdd:spec-design {feature} [-y]`
  - `/sdd:validate-design {feature}` (opcional: revisão de design)
  - `/sdd:spec-tasks {feature} [-y]`
- Fase 2 (Implementação): `/sdd:spec-impl {feature} [tasks]`
  - `/sdd:validate-impl {feature}` (opcional: após implementação)
- Checagem de progresso: `/sdd:spec-status {feature}` (use a qualquer momento)

## Regras de Desenvolvimento

- Workflow de aprovação em 3 fases: Requisitos → Design → Tarefas → Implementação
- Revisão humana obrigatória em cada fase; use `-y` apenas para fast-track intencional
- Mantenha o steering atualizado e verifique alinhamento com `/sdd:spec-status`
- Siga as instruções do usuário à risca e, dentro desse escopo, aja de forma autônoma: colete o contexto necessário e complete o trabalho solicitado de ponta a ponta nesta execução, perguntando apenas quando informações essenciais estiverem faltando ou as instruções forem criticamente ambíguas.

## Configuração de Steering

- Carregue todo o `.sdd/steering/` como memória do projeto
- Arquivos padrão: `product.md`, `tech.md`, `structure.md`
- Arquivos customizados são suportados (gerenciados via `/sdd:steering-custom`)
