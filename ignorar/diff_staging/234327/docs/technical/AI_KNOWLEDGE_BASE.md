# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-14 23:42:00
# 🧠 AI Knowledge Base & Learned Patterns
> **System Memory:** Este arquivo registra aprendizados, correções de padrão e regras implícitas descobertas durante a operação.
> **Usage:** Deve ser consultado antes de tarefas complexas para evitar regressão.

---

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
