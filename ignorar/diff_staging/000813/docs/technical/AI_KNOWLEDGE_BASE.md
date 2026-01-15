# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-15 00:07:00
# 🧠 AI Knowledge Base & Learned Patterns
> **System Memory:** Este arquivo registra aprendizados, correções de padrão e regras implícitas descobertas durante a operação.
> **Usage:** Deve ser consultado antes de tarefas complexas para evitar regressão.

---

## 2026-01-15 | TS_COMPILATION_FIX_SENTRY
- **Sintoma:** Erro de compilação `TS1005: '}' expected` em `sentry.client.config.ts`.
- **Causa:** O arquivo estava truncado (sem fechamento de objeto/função) e utilizava comentários de metadados com sintaxe incorreta (`#` em vez de `//`).
- **Ação:** Correção da sintaxe de comentários e fechamento adequado do bloco `Sentry.init({...});`.

## 2026-01-15 | FRONTEND_COMPILATION_CHECK
- **Contexto:** Correção de erro de sintaxe em `api.ts` aplicada.
- **Ação:** Criação de script de validação de compilação (`verify_frontend_compilation.py`) para garantir que não restam erros de TypeScript no projeto.

## 2026-01-15 | FISCAL_UI_DEPLOYED
- **Evento:** Implementação da interface de configuração fiscal (`FiscalSection`).
- **Status:** Código aplicado e auditado (412 elementos interativos detectados).
- **Fluxo:** O cliente agora possui autonomia para inserir credenciais da Focus NFe.

## 2026-01-15 | SYNTAX_ERROR_FIX
- **Sintoma:** Erro de compilação no Next.js (`Expected ';', '}' or <eof>`) no arquivo `src/lib/api.ts`.    
- **Causa Raiz:** O arquivo TypeScript continha cabeçalhos de metadados (`# DOMAIN: FRONTEND`) usando sintaxe de comentário Python/Shell (`#`) em vez de JavaScript/TypeScript (`//`).
- **Ação:** Correção da sintaxe de comentários para `//` no arquivo afetado.
- **Regra Aprendida:** Arquivos `.ts`, `.tsx`, `.js` devem usar `//` para metadados de governança.

## 2026-01-14 | FISCAL_INTEGRATION_VERIFIED
- **Evento:** Sucesso no `smoke_test_focus_nfe.py`.
- **Estado:** Credenciais da Focus NFe (Sandbox) validadas e funcionais.
- **Conclusão:** O ambiente de desenvolvimento está apto a emitir notas fiscais em modo de homologação.

## 2026-01-14 | GOVERNANCE_DRIFT_FIX
- **Sintoma:** O script `gov_04_registry_drift.py` falhava reportando "Evidence Missing".
- **Causa Raiz:** O arquivo `registry.xml` apontava para caminhos legados (`docs/audit/...`) enquanto os scripts geravam relatórios na nova estrutura canônica (`governance/evidence/...`).
- **Resolução:** Atualização dos atributos `evidence` no XML para refletir o caminho real.
- **Regra Aprendida:** Ao mover scripts ou relatórios, o `registry.xml` deve ser atualizado atomicamente na mesma transação.

## 2026-01-14 | COGNITIVE_CONSTITUTION_LOCATOR
- **Contexto:** O operador solicitou a localização das regras de resposta da IA.
- **Fato:** A "Constituição Cognitiva" reside em `governance/prompts/AI_COGNITIVE_PROFILE.xml`.
- **Protocolo:** O protocolo de atualização (como formatar XML) reside em `governance/protocols/UPDATE_EXECUTION_PROTOCOL.md`.

## 2026-01-14 | MEMORY_PERSISTENCE_RULE
- **Diretiva:** Toda resposta da IA deve gerar/atualizar este arquivo (`AI_KNOWLEDGE_BASE.md`) com novos conhecimentos adquiridos na interação.
- **Ação:** Inclusão deste arquivo no payload de resposta padrão quando houver aprendizado relevante.
