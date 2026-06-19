# Plano de Implementação

## Template de Tarefas

Use o padrão que melhor se encaixa na divisão do trabalho:

### Apenas tarefa principal

- [ ] {{NÚMERO}}. {{DESCRIÇÃO_DA_TAREFA}}{{MARCADOR_PARALELO}}
  - {{DETALHE_1}} _(Inclua detalhes apenas quando necessário. Se a tarefa for autoexplicativa, omita os itens.)_
  - _Requisitos: {{IDS_REQUISITOS}}_

### Estrutura de tarefa principal + subtarefa

- [ ] {{NÚMERO_PRINCIPAL}}. {{RESUMO_TAREFA_PRINCIPAL}}
- [ ] {{NÚMERO_PRINCIPAL}}.{{SUB_NÚMERO}} {{DESCRIÇÃO_SUBTAREFA}}{{SUB_MARCADOR_PARALELO}}
  - {{DETALHE_1}}
  - {{DETALHE_2}}
  - _Requisitos: {{IDS_REQUISITOS}}_ _(Apenas IDs; não adicione descrições ou parênteses.)_

> **Marcador de paralelo**: Adicione ` (P)` apenas às tarefas que podem ser executadas em paralelo. Omitir o marcador ao rodar em modo `--sequential`.
>
> **Cobertura de testes opcional**: Quando uma subtarefa for trabalho de teste postergável vinculado a critérios de aceite, marque o checkbox como `- [ ]*` e explique os requisitos referenciados nos detalhes.
