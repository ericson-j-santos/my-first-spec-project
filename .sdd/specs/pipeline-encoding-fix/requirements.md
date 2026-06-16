# Documento de Requisitos

## Descrição do Projeto (Input)

Corrigir o encoding quebrado em backend/app/api/pipeline.py (ReqSys v2 Enterprise). Strings como 'IntegraÃ§Ã£o' devem ser 'Integração'. O arquivo existe no repo reqsys-v2-enterprise-real e precisa ser corrigido antes do próximo deploy no Fly.io.

---

## Introdução

O módulo `backend/app/api/pipeline.py` do ReqSys v2 Enterprise (FastAPI, Python 3.12) contém strings literais em português usadas como mensagens de erro em respostas HTTP (`HTTPException.detail`) e textos de validação retornados pela API. Quando o arquivo foi editado com encoding incorreto, caracteres especiais do português foram corrompidos (mojibake), resultando em respostas malformadas para o cliente (ex: `'IntegraÃ§Ã£o'` em vez de `'Integração'`). Esta spec formaliza os requisitos para corrigir o estado atual e prevenir regressões futuras.

**Escopo**: `backend/app/api/pipeline.py` e eventuais arquivos `.py` relacionados com strings em português expostos via API.  
**Sistema referenciado nos critérios EARS**: ReqSys Pipeline.

---

## Requisitos

### Requisito 1: Corretude das strings literais em UTF-8

**Objetivo:** Como desenvolvedor do ReqSys, quero que todas as strings em português no código-fonte estejam em UTF-8 correto, para que as respostas da API nunca contenham caracteres corrompidos.

#### Critérios de Aceite — Requisito 1

1. The ReqSys Pipeline shall conter todas as strings literais com caracteres especiais do português (ç, ã, é, à, â, ê, í, ó, ô, ú, õ) codificadas corretamente em UTF-8 nos arquivos-fonte Python.
2. When um endpoint do pipeline retornar mensagem contendo caractere especial (ex: `'Integração'`), the ReqSys Pipeline shall serializar o caractere corretamente no corpo JSON da resposta HTTP, sem mojibake.
3. If uma string literal no código-fonte contiver sequência de bytes de mojibake (ex: `Ã§`, `Ã£o`, `Ã©`), the ReqSys Pipeline shall ser considerado em estado inválido e rejeitado pelo pipeline de qualidade.

---

### Requisito 2: Validação das respostas HTTP dos endpoints de integração

**Objetivo:** Como consumidor da API, quero receber mensagens de erro e textos de validação em português legível, para que o sistema seja utilizável sem necessidade de inspeção de logs.

#### Critérios de Aceite — Requisito 2

1. When `POST /v1/integracoes/github/issues` for chamado com a feature flag `ENABLE_GITHUB_REDMINE_IMPORT` desabilitada, the ReqSys Pipeline shall retornar campo `detail` contendo `'Integração GitHub→Redmine desabilitada por feature flag.'` sem caracteres corrompidos.
2. When `POST /v1/backlog/publicar-redmine/{id}` for chamado com `use_github_import=true` e feature flag desabilitada, the ReqSys Pipeline shall retornar a mesma mensagem corretamente codificada no JSON.
3. The ReqSys Pipeline shall retornar `Content-Type: application/json; charset=utf-8` em todos os endpoints do módulo pipeline.
4. If o campo `detail` de qualquer `HTTPException` lançada por `pipeline.py` contiver caracteres mojibake, the ReqSys Pipeline shall ser considerado com defeito e exigir correção antes do deploy.

---

### Requisito 3: Testes de regressão de encoding

**Objetivo:** Como desenvolvedor, quero testes automatizados que verifiquem a integridade das strings da API, para que encoding quebrado seja detectado antes do deploy em qualquer ambiente.

#### Critérios de Aceite — Requisito 3

1. When os testes de pipeline (`tests/test_pipeline.py`) forem executados, the ReqSys Pipeline shall validar que a resposta de `POST /v1/integracoes/github/issues` (com flag desabilitada) contém a string `Integração` sem caracteres corrompidos.
2. When os testes forem executados, the ReqSys Pipeline shall decodificar a resposta como UTF-8 e verificar que `json.loads(response.text)` não lança `UnicodeDecodeError`.
3. If qualquer teste de regressão de encoding falhar, the ReqSys Pipeline shall exibir no relatório do pytest a string recebida versus a esperada, facilitando diagnóstico.
4. The ReqSys Pipeline shall cobrir com testes ao menos os dois endpoints que retornam mensagens de erro em português: `/v1/integracoes/github/issues` e `/v1/backlog/publicar-redmine/{id}`.

---

### Requisito 4: Prevenção de regressão no CI/CD

**Objetivo:** Como mantenedor do projeto, quero que o pipeline de CI detecte e rejeite automaticamente código com mojibake, para que o problema não reapareça após edições futuras.

#### Critérios de Aceite — Requisito 4

1. When o CI executar no repositório `reqsys-v2-enterprise-real`, the ReqSys Pipeline shall verificar se arquivos `.py` em `backend/app/api/` contêm sequências de bytes características de mojibake UTF-8-em-Latin-1 (ex: `Ã§`, `Ã£`, `Ã©`, `Ã\xa3`).
2. If arquivos com mojibake forem detectados, the ReqSys Pipeline shall falhar o job de CI com mensagem indicando arquivo e linha problemáticos antes de executar os testes unitários.
3. The ReqSys Pipeline shall executar a verificação de encoding como etapa independente no CI, antes dos testes, para garantir falha rápida.

---

## Fora do Escopo

- Alterações de schema do banco de dados ou modelos SQLAlchemy
- Internacionalização (i18n) ou suporte a múltiplos idiomas
- Correção de encoding em módulos além de `pipeline.py` e seus imports diretos
- Mudanças na lógica de negócio dos endpoints

## Dependências

- Python 3.12 com codificação padrão UTF-8 (padrão desde Python 3.0)
- `PYTHONIOENCODING=utf-8` ou `LANG=C.UTF-8` no container Fly.io (verificar se necessário)
- Arquivo salvo com encoding UTF-8 sem BOM pelo editor/IDE
