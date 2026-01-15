# DOMAIN: BACKEND
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-02
TITLE: Observabilidade Fullstack (Sentry + Logs Estruturados)
OWNER: Executor Kernel
PRIORITY: ALTA (GTM)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O backend utiliza `print()` ou logging padrão do Python, gerando logs de texto não estruturado difíceis de indexar.
- O Sentry está parcialmente configurado ou ausente em partes críticas do fluxo.
- Não há garantia de captura de contexto (`company_id`, `user_id`) nas exceções, dificultando o debug multi-tenant.
- O Frontend carece de configuração robusta de Sentry para produção (Source Maps, Replay).

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Backend emitindo logs exclusivamente em formato JSON estruturado (nível, timestamp, mensagem, contexto).
- Sentry inicializado no Backend com captura de contexto de tenant e usuário.
- Sentry configurado no Frontend (Client, Server, Edge) para captura de erros e performance.
- Script de validação confirmando a estrutura dos logs e a inicialização do SDK.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Criação de `app/core/logger.py` para padronização JSON.
- Atualização de `app/main.py` para integrar Sentry e Logger.
- Configuração dos arquivos `sentry.*.config.ts` no Frontend.
- Script de verificação `scripts/production/verify_observability.py`.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Criação de conta no Sentry (DSN deve ser fornecido via ENV).
- Configuração de dashboards externos (Datadog, Grafana).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Linguagem: Python 3.11+ / TypeScript.
- Libs: `sentry-sdk`, `python-json-logger` (ou implementação nativa).
- Formato de Log: JSON (Production).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/main.py`
- `frontend/sentry.client.config.ts` (e variantes)

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Arquivos de configuração Sentry atualizados.
- Logger estruturado implementado.
- Script de validação.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Logs do backend são emitidos como JSON válido.
- [x] Sentry SDK inicializa sem erros no boot do FastAPI.
- [x] Middleware de contexto injeta `company_id` no escopo do Sentry.
- [x] Frontend possui configurações de Sentry para Client, Server e Edge.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_observability.py`
RESULTADO_ESPERADO: "Observability Check Passed: Sentry Init OK, Logs JSON OK."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `app/main.py` para remover middleware Sentry.
- Remover `app/core/logger.py`.
