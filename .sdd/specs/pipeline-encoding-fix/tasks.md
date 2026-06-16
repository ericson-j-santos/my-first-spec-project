# Plano de Implementação — pipeline-encoding-fix

## Visão Geral

3 tarefas principais · 6 sub-tarefas · Tarefas 2 e 3 executáveis em paralelo após conclusão da tarefa 1

---

- [ ] 1. Auditar e corrigir strings em português no módulo pipeline

- [ ] 1.1 Inspecionar todos os literais em português em pipeline.py e github_redmine.py
  - Abrir cada arquivo e listar todas as strings literais que contenham caracteres especiais (ç, ã, é, á, ú, etc.)
  - Comparar com a saída esperada: `'Integração GitHub→Redmine desabilitada por feature flag.'`
  - Registrar qualquer ocorrência de sequências `Ã§`, `Ã£`, `Ã©`, `Ã¡`, `Ãº` como defeito
  - Se o arquivo estiver correto, documentar que o estado atual é válido (sem alteração necessária)
  - _Requirements: 1.1, 1.2_

- [ ] 1.2 Garantir que a serialização JSON retorna Content-Type com charset=utf-8
  - Verificar se o FastAPI/uvicorn inclui `charset=utf-8` no `Content-Type` da resposta JSON
  - Se ausente, configurar `JSONResponse` com `media_type="application/json; charset=utf-8"` ou via middleware
  - _Requirements: 2.3, 2.4_

---

- [ ] 2. (P) Criar testes de regressão de encoding em test_pipeline.py

- [ ] 2.1 (P) Implementar TestEncodingRegressao com testes de conteúdo do campo detail
  - Adicionar classe `TestEncodingRegressao` em `tests/test_pipeline.py`
  - Implementar teste que chama `POST /v1/integracoes/github/issues` com flag desabilitada e asserta que `resp.json()["detail"]` contém `'Integração'` sem mojibake
  - Implementar teste equivalente para `POST /v1/backlog/publicar-redmine/1` com `use_github_import=True` e flag desabilitada
  - Usar `monkeypatch.setattr("app.api.pipeline.github_redmine_import_enabled", lambda: False)` para isolar
  - _Requirements: 2.1, 2.2, 3.1, 3.4_

- [ ] 2.2 (P) Adicionar testes de decodificação UTF-8 e Content-Type
  - Implementar teste que chama `POST /v1/integracoes/github/issues` (flag OFF) e verifica que `json.loads(resp.text)` completa sem `UnicodeDecodeError`
  - Implementar teste que verifica que `resp.headers["content-type"]` contém `utf-8` em qualquer endpoint do pipeline
  - _Requirements: 2.3, 3.2, 3.3_

---

- [ ] 3. (P) Adicionar step anti-mojibake ao CI do reqsys-v2-enterprise-real

- [ ] 3.1 (P) Inserir step de grep antes dos testes no job backend-test do ci.yml
  - Adicionar step `Verificar encoding UTF-8 (anti-mojibake)` no job `backend-test`, imediatamente antes do step `Run tests with coverage`
  - O step usa `grep -rn --include="*.py" -E "Ã§|Ã£|Ã©|Ã¡|Ãº" app/api/ app/services/` e sai com `exit 1` se encontrar ocorrências
  - A saída do grep já imprime `arquivo:linha:conteúdo`, satisfazendo o requisito de localização exata
  - Se nenhum mojibake for encontrado, o step imprime "OK" e continua para os testes
  - _Requirements: 1.3, 2.4, 4.1, 4.2, 4.3_
