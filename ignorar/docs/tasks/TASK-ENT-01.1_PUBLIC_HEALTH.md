# DOMAIN: BACKEND
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-ENT-01.1
TITLE: Public Health Endpoint (Root Level)
OWNER: Executor Kernel
PRIORITY: ALTA (ENTERPRISE)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O endpoint de verificação de saúde existe apenas em `/api/health`.
- Ferramentas de monitoramento externas (Load Balancers, UptimeRobot) e o próprio Trust Center (em configurações agnósticas de base path) frequentemente buscam `/health` na raiz.
- A ausência deste endpoint gera falsos positivos de indisponibilidade em dashboards de status e dificulta a configuração de Probes em Kubernetes/Render.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O backend responde requisições `GET /health` com o mesmo payload e lógica de `/api/health`.
- A compatibilidade com `/api/health` é mantida para clientes legados.
- O Trust Center e monitores externos conseguem validar a saúde do sistema sem depender do prefixo de API.
- A implementação utiliza "Dual Binding" (mesma função para múltiplas rotas) para evitar duplicação de lógica.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Modificação do `app/main.py` para expor a rota `/health`.
- Script de validação `scripts/production/verify_public_health.py`.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Alterações na lógica interna de verificação (DB/Redis).
- Alterações no Frontend (o frontend já consome a variável de ambiente correta).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Framework: FastAPI.
- Método: Decorator stacking.
- Segurança: O endpoint deve ser público (sem Auth), mas não deve expor stack traces ou dados sensíveis.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/main.py` (Versão com Hardening de Segurança e Observabilidade).

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/main.py` atualizado.
- Script de validação.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] `GET /health` retorna 200 OK e JSON de status.
- [x] `GET /api/health` continua retornando 200 OK.
- [x] Ambos os endpoints retornam a mesma estrutura de dados (`status`, `services`).

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_public_health.py`
RESULTADO_ESPERADO: "Health Check Dual-Binding Verified: OK."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `app/main.py` para remover o decorator `/health`.