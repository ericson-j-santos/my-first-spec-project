# Pesquisa e Decisões de Design — pipeline-encoding-fix

---

## Resumo

- **Feature**: `pipeline-encoding-fix`
- **Escopo de Discovery**: Extension (sistema existente — ReqSys v2 Enterprise)
- **Principais Achados**:
  - As strings em `pipeline.py` já aparecem em UTF-8 correto no arquivo lido em 14/06/2026; o problema original foi corrigido ou é intermitente por encoding do editor. A correção é **preventiva**: sem CI e sem testes de conteúdo, o bug pode reaparecer.
  - Python 3.12 usa UTF-8 como encoding de source por padrão — nenhuma declaração `# -*- coding: utf-8 -*-` é necessária.
  - `test_pipeline.py` (existente) verifica `status_code == 409` para flag desabilitada, mas **não verifica o conteúdo do campo `detail`** — mojibake passaria nos testes atuais.
  - `grep` com padrões de bytes de mojibake UTF-8-em-Latin-1 (`Ã§`, `Ã£`, `Ã©`) é suficiente para detecção no CI; nenhuma biblioteca externa necessária.

---

## Research Log

### Análise das strings existentes em pipeline.py

- **Contexto**: Verificar se strings já contêm mojibake ou se o arquivo já foi corrigido.
- **Fonte**: Leitura direta do arquivo `backend/app/api/pipeline.py` (reqsys-live local).
- **Achados**:
  - Linha 137: `'Integração GitHub→Redmine desabilitada por feature flag.'` — UTF-8 correto.
  - Linha 178: mesma string, também correta.
  - Sem ocorrências de `Ã§`, `Ã£o`, `Ã©` no arquivo atual.
- **Implicações**: O defeito imediato pode não existir no estado atual do arquivo local. O design deve focar em prevenção (CI + testes de conteúdo) para garantir que o problema não reapareça após futuras edições com editor mal configurado.

### Cobertura de testes atual

- **Contexto**: `test_pipeline.py` (existente) cobre os endpoints com flag desabilitada?
- **Achados**:
  - `test_listar_issues_github_feature_flag_desabilitada`: verifica apenas `resp.status_code == 409`. Não verifica `resp.json()["detail"]`.
  - `test_publicar_redmine_com_github_flag_desabilitada`: mesmo padrão — só status code.
- **Implicações**: Os dois testes existentes passariam mesmo com `detail` contendo `'IntegraÃ§Ã£o'`. O design deve adicionar classe `TestEncodingRegressao` com assertions no conteúdo do `detail`.

### Python 3.12 e encoding UTF-8

- **Contexto**: Verificar se Python 3.12 garante UTF-8 por padrão sem configuração extra.
- **Achados**:
  - Python 3.0+ usa UTF-8 como encoding padrão de source code (PEP 3120).
  - Em containers Linux (Fly.io usa Debian/Ubuntu), `PYTHONIOENCODING` e `LANG` podem influenciar saída de stdout/stderr, mas FastAPI/uvicorn serializa JSON explicitamente em UTF-8 via `json.dumps(ensure_ascii=False)` ou similar.
  - O container Fly.io do ReqSys não define `PYTHONIOENCODING` no `fly.toml`; é recomendável adicionar `PYTHONIOENCODING=utf-8` como medida defensiva.
- **Implicações**: O problema de encoding é de **source file**, não de runtime. Garantir que o editor salve em UTF-8 sem BOM e que o CI valide isso é suficiente.

### Abordagem CI para detecção de mojibake

- **Contexto**: Qual é a forma mais simples e confiável de detectar mojibake em CI sem dependências extras?
- **Alternativas avaliadas**:
  - `grep -rn --include="*.py" -P "[\xC3][\x83-\xBF]" backend/app/api/` — padrão de bytes Perl regex (requer `grep -P`)
  - `grep -rn --include="*.py" -E "Ã§|Ã£|Ã©|Ã¡|Ã\xba" backend/app/api/` — padrão de strings literais (mais legível)
  - Python script com `chardet` para detectar encoding de arquivos
- **Selecionado**: `grep -rn` com padrões de strings literais de mojibake (`Ã§`, `Ã£`, `Ã©`).
- **Rationale**: Sem dependências extras; padrões literais são imediatamente compreensíveis; grep está disponível em todos os runners GitHub Actions.
- **Limitação**: Não detecta mojibake de outros encodings (ex: Latin-2); aceitável para o contexto do projeto.

---

## Avaliação de Padrões de Arquitetura

| Opção | Descrição | Vantagens | Riscos/Limitações |
|---|---|---|---|
| Correção + CI grep | Fix source + grep no CI | Simples, zero dependências, falha rápida | Cobre apenas padrões Latin-1→UTF-8 conhecidos |
| Python chardet no CI | Detecta encoding do arquivo automaticamente | Mais robusto | Requer `pip install chardet`, mais lento, overkill |
| Pre-commit hook local | Bloqueia no commit do dev | Mais rápido (local) | Depende de setup do dev; não protege CI remoto |

**Selecionado**: Correção + CI grep (opção 1). Complementar com pre-commit hook fica fora do escopo desta spec.

---

## Decisões de Design

### Decisão: Adicionar assertions de conteúdo nos testes de feature flag

- **Contexto**: Testes existentes verificam status code 409 mas não o campo `detail`.
- **Alternativas**:
  1. Modificar testes existentes — risco de conflito com responsabilidade original do teste
  2. Nova classe `TestEncodingRegressao` — separação clara de responsabilidades
- **Selecionado**: Nova classe `TestEncodingRegressao` em `test_pipeline.py`.
- **Rationale**: Não polui testes existentes; nomeação clara indica propósito.
- **Trade-offs**: Duplica algumas chamadas de endpoints; aceitável dado o objetivo de isolamento.

### Decisão: Escopo do CI grep

- **Contexto**: Onde aplicar a verificação de encoding?
- **Alternativas**:
  1. Todo o repo (`backend/`) — mais abrangente
  2. Somente `backend/app/api/` — escopo da spec
- **Selecionado**: `backend/app/api/` com flag `--include="*.py"`.
- **Rationale**: Escopo conservador alinhado à spec; pode ser expandido em spec futura.
- **Follow-up**: Verificar se `github_redmine.py` (em `services/`) também deve ser incluído — as strings nele são em inglês, mas verificar encoding é inócuo.

---

## Riscos e Mitigações

- **Risco**: `pipeline.py` local já está correto, mas a versão no Fly.io pode estar defasada → mitigar com verificação de deploy (item 1 do brief ReqSys)
- **Risco**: Editor futuro salvar com Latin-1 por acidente → mitigado pelo CI grep
- **Risco**: `PYTHONIOENCODING` não setado no container Fly.io pode causar problemas de saída em logs → mitigar adicionando `PYTHONIOENCODING=utf-8` ao `fly.toml` (fora do escopo desta spec)

---

## Referências

- [PEP 3120 — Using UTF-8 as the default source encoding](https://peps.python.org/pep-3120/) — confirma UTF-8 padrão no Python 3
- [FastAPI Response encoding](https://fastapi.tiangolo.com/tutorial/response-model/) — FastAPI usa `json.dumps` com `ensure_ascii=False` para respostas JSON por padrão quando configurado com `JSONResponse`
- [GitHub Actions — jobs steps](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) — sintaxe de steps de CI
