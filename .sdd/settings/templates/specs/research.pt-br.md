# Template de Pesquisa & Decisões de Design

---

**Propósito**: Registrar descobertas, investigações arquiteturais e justificativas que embasam o design técnico.

**Uso**:

- Registre atividades e resultados de pesquisa durante a fase de descoberta.
- Documente trade-offs de decisões de design que são detalhados demais para o `design.md`.
- Forneça referências e evidências para auditorias futuras ou reuso.

---

## Resumo

- **Feature**: `<nome-da-feature>`
- **Escopo da Descoberta**: Nova Feature / Extensão / Adição Simples / Integração Complexa
- **Principais Descobertas**:
  - Descoberta 1
  - Descoberta 2
  - Descoberta 3

## Log de Pesquisa

Documente etapas notáveis da investigação e seus resultados. Agrupe por tópico para facilitar a leitura.

### [Tópico ou Questão]

- **Contexto**: O que motivou esta investigação?
- **Fontes Consultadas**: Links, documentação, APIs, benchmarks
- **Descobertas**: Pontos resumidos das percepções
- **Implicações**: Como isso afeta arquitetura, contratos ou implementação

_Repita a subseção para cada tópico relevante._

## Avaliação de Padrões Arquiteturais

Liste padrões ou abordagens candidatos considerados. Use tabela quando útil.

| Opção     | Descrição                                                     | Pontos Fortes                   | Riscos / Limitações                       | Observações                        |
| --------- | ------------------------------------------------------------- | ------------------------------- | ----------------------------------------- | ---------------------------------- |
| Hexagonal | Abstração de portas e adaptadores ao redor do domínio central | Limites claros, núcleo testável | Exige construção da camada de adaptadores | Alinha com princípio X do steering |

## Decisões de Design

Registre decisões importantes que influenciam o `design.md`. Foque em escolhas com trade-offs relevantes.

### Decisão: `<Título>`

- **Contexto**: Problema ou requisito que motivou a decisão
- **Alternativas Consideradas**:
  1. Opção A — breve descrição
  2. Opção B — breve descrição
- **Abordagem Selecionada**: O que foi escolhido e como funciona
- **Justificativa**: Por que esta abordagem se encaixa no contexto do projeto
- **Trade-offs**: Benefícios vs. compromissos
- **Follow-up**: Itens a verificar durante implementação ou testes

_Repita a subseção para cada decisão._

## Riscos & Mitigações

- Risco 1 — Mitigação proposta
- Risco 2 — Mitigação proposta
- Risco 3 — Mitigação proposta

## Referências

Forneça links e citações canônicas (docs oficiais, padrões, ADRs, guias internos).

- [Título](https://exemplo.com) — breve nota sobre relevância
- ...
