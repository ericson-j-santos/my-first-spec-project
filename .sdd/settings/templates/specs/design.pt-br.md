# Template de Documento de Design

---

**Propósito**: Fornecer detalhes suficientes para garantir consistência na implementação entre diferentes desenvolvedores, prevenindo desvios de interpretação.

**Abordagem**:

- Inclua seções essenciais que informam diretamente as decisões de implementação
- Omitir seções opcionais, a menos que sejam críticas para evitar erros de implementação
- Ajuste o nível de detalhe à complexidade da feature
- Prefira diagramas e tabelas a textos longos

## **Atenção**: Aproximar-se de 1000 linhas indica complexidade excessiva da feature e pode exigir simplificação do design.

> As seções podem ser reordenadas (ex: trazer Rastreabilidade de Requisitos para cima ou mover Modelos de Dados para perto da Arquitetura) quando isso melhorar a clareza. Dentro de cada seção, mantenha o fluxo **Resumo → Escopo → Decisões → Impactos/Riscos** para facilitar a revisão.

## Visão Geral

2-3 parágrafos no máximo
**Propósito**: Esta feature entrega [valor específico] para [usuários alvo].
**Usuários**: [Grupos de usuários alvo] utilizarão para [fluxos específicos].
**Impacto** (se aplicável): Altera o [estado atual do sistema] por meio de [modificações específicas].

### Objetivos

- Objetivo principal 1
- Objetivo principal 2
- Critérios de sucesso

### Não-Objetivos

- Funcionalidades explicitamente excluídas
- Considerações futuras fora do escopo atual
- Pontos de integração adiados

## Arquitetura

> Consulte notas detalhadas de descoberta em `research.md` apenas como referência; mantenha o design.md autoexplicativo para revisores, registrando todas as decisões e contratos aqui.
> Registre decisões-chave em texto e deixe os diagramas mostrarem detalhes estruturais—evite repetir a mesma informação em prosa.

### Análise da Arquitetura Existente (se aplicável)

Ao modificar sistemas existentes:

- Padrões e restrições atuais de arquitetura
- Limites de domínio existentes a serem respeitados
- Pontos de integração que devem ser mantidos
- Dívida técnica tratada ou contornada

### Padrão de Arquitetura & Mapa de Fronteiras

**RECOMENDADO**: Inclua diagrama Mermaid mostrando o padrão de arquitetura escolhido e os limites do sistema (obrigatório para features complexas, opcional para adições simples)

**Integração Arquitetural**:

- Padrão selecionado: [nome e breve justificativa]
- Limites de domínio/feature: [como responsabilidades são separadas para evitar conflitos]
- Padrões existentes preservados: [listar padrões principais]
- Justificativa de novos componentes: [por que cada um é necessário]
- Conformidade com steering: [princípios mantidos]

### Stack Tecnológica

| Camada                   | Escolha / Versão | Papel na Feature | Observações |
| ------------------------ | ---------------- | ---------------- | ----------- |
| Frontend / CLI           |                  |                  |             |
| Backend / Serviços       |                  |                  |             |
| Dados / Armazenamento    |                  |                  |             |
| Mensageria / Eventos     |                  |                  |             |
| Infraestrutura / Runtime |                  |                  |             |

> Mantenha a justificativa concisa aqui e, quando necessário detalhar (trade-offs, benchmarks), adicione um resumo curto e referência para a seção de Referências de Apoio e para o `research.md`.

## Fluxos do Sistema

Inclua apenas os diagramas necessários para explicar fluxos não triviais. Use sintaxe Mermaid pura. Padrões comuns:

- Sequência (interações entre múltiplas partes)
- Processo / estado (lógica de ramificação ou ciclo de vida)
- Fluxo de dados/eventos (pipelines, mensageria assíncrona)

Omitir esta seção para mudanças CRUD simples.

> Descreva decisões de fluxo (ex: condições de bloqueio, tentativas) brevemente após o diagrama, sem repetir cada passo.

## Rastreabilidade de Requisitos

Use esta seção para features complexas ou sensíveis a compliance, onde requisitos abrangem múltiplos domínios. Mapeamentos 1:1 simples podem usar apenas a tabela de resumo de Componentes.

Mapeie cada ID de requisito (ex: `2.1`) para os elementos de design que o realizam.

| Requisito | Resumo | Componentes | Interfaces | Fluxos |
| --------- | ------ | ----------- | ---------- | ------ |
| 1.1       |        |             |            |        |
| 1.2       |        |             |            |        |

> Omitir esta seção apenas quando um único componente satisfaz um único requisito sem preocupações cruzadas.

## Componentes e Interfaces

Forneça um resumo rápido antes dos detalhes por componente.

- Resumos podem ser em tabela ou lista compacta. Exemplo de tabela:
  | Componente | Domínio/Camada | Intenção | Cobertura Req | Dependências-Chave (P0/P1) | Contratos |
  |------------|----------------|----------|---------------|----------------------------|-----------|
  | ExemploComponente | UI | Exibe XYZ | 1, 2 | GameProvider (P0), MapPanel (P1) | Serviço, Estado |
- Apenas componentes que introduzem novos limites (ex: hooks de lógica, integrações externas, persistência) exigem blocos detalhados. Componentes de apresentação simples podem usar apenas a linha de resumo e uma breve Nota de Implementação.
