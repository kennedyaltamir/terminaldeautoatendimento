# DOMAIN: OPERATIONS
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-OPS-06
TITLE: Robust Background Processing (Celery + Redis)
OWNER: Executor Kernel
PRIORITY: ALTA (RELIABILITY)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema utiliza `BackgroundTasks` do FastAPI para tarefas assíncronas (Webhooks, E-mails, Logs).
- **Risco Crítico:** Essas tarefas residem na memória do processo web. Se o container reiniciar (deploy, crash, OOM), as tarefas pendentes são perdidas irreversivelmente.
- Não há mecanismo de **Retry** persistente (apenas retries em memória que morrem com o processo).
- Em um cenário "Real Production", a perda de um Webhook de pagamento ou nota fiscal é inaceitável.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação do **Celery** como motor de filas distribuídas, utilizando o Redis existente como Broker.
- Separação de responsabilidades: Processo Web (API) apenas enfileira; Processo Worker executa.
- Migração do `WebhookDispatcher` para uma Task Celery com política de retry exponencial persistente.
- Configuração do serviço de Worker no `render.yaml`.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Instalação de `celery` e `redis` (lib python).
- Configuração do `app/core/celery_app.py`.
- Criação de tasks em `app/tasks/webhooks.py`.
- Refatoração do `app/services/webhook_dispatcher.py` para chamar a task Celery.
- Atualização do `render.yaml` para incluir o serviço Worker.
- Script de validação de enfileiramento.

### EXCLUI
- Migração de todas as tarefas do sistema (foco inicial em Webhooks como prova de conceito crítica).
- Dashboard do Celery (Flower) em produção (por segurança).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Broker: Redis (já configurado no projeto).
- Serialização: JSON.
- Concorrência: `gevent` ou `prefork` (usaremos prefork padrão por estabilidade).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `REDIS_URL` no ambiente.
- `app/services/webhook_dispatcher.py`.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `requirements.txt` (Atualizado).
- `app/core/celery_app.py`.
- `app/tasks/webhooks.py`.
- `render.yaml` (Atualizado).
- `scripts/production/verify_celery_worker.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Celery App inicializa e conecta ao Redis.
- [x] WebhookDispatcher enfileira task em vez de executar diretamente.
- [x] Worker consome a task e executa a lógica de envio.
- [x] Script de validação confirma o fluxo (Producer -> Queue).

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_celery_worker.py`
RESULTADO_ESPERADO: "Celery Integration Verified: Task queued successfully."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `app/services/webhook_dispatcher.py`.
- Remover `app/core/celery_app.py` e `app/tasks`.
- Remover worker do `render.yaml`.
