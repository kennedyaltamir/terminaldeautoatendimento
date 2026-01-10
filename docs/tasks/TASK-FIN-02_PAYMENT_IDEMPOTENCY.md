# DOMAIN: FINTECH
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-FIN-02
TITLE: Payment Webhook Idempotency & Double-Credit Protection
OWNER: Executor Kernel
PRIORITY: CRÍTICA (FINANCIAL INTEGRITY)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema processa Webhooks do Mercado Pago e Stripe para confirmar pagamentos.
- **Risco Financeiro:** Atualmente, a lógica de confirmação não possui uma trava de idempotência rigorosa em nível de transação. Se um provedor enviar o mesmo Webhook múltiplas vezes (devido a retries de rede), o sistema pode processar a lógica de cashback ou liberar o pedido repetidamente.
- Não há registro de "Transações Processadas" para evitar re-processamento de um ID que já foi concluído.
- Isso é um falha grave de integridade para sistemas que lidam com dinheiro real.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação de uma tabela de controle de idempotência no banco de dados.
- Verificação obrigatória do ID da transação externa antes de qualquer alteração de estado financeiro.
- Garantia de que a lógica de "Sucesso de Pagamento" (liberação de KDS + crédito de Cashback) ocorra exatamente uma vez por pagamento.
- Resiliência: se o Webhook falhar no meio, ele deve ser capaz de retomar sem duplicar benefícios.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Criação do modelo `PaymentTransaction` em `app/models.py`.
- Implementação do serviço de idempotência em `app/services/payment_service.py`.
- Refatoração dos Webhooks em `app/routers/webhooks.py` para usar a trava.
- Script de validação de duplicidade.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Estorno automático de pagamentos duplicados no gateway (foco na proteção interna).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Banco de Dados: PostgreSQL (via SQLAlchemy).
- Integridade: Uso de `unique_constraint` no par (provider, external_id).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/models.py`
- `app/routers/webhooks.py`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/models.py` (Atualizado).
- `app/services/payment_service.py` (Atualizado).
- `app/routers/webhooks.py` (Hardened).
- `scripts/production/verify_payment_idempotency.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] Tentativa de processar o mesmo ID de transação duas vezes retorna "Processed" sem alterar dados.
- [x] Cashback é creditado apenas uma vez.
- [x] O status do pedido não "pisca" ou gera logs duplicados em retries.
- [x] Script de validação simula 2 chamadas idênticas e confirma o bloqueio da segunda.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/verify_payment_idempotency.py`
RESULTADO_ESPERADO: "Idempotency Check Passed: Double-payment blocked."

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter mudanças no `webhooks.py` e remover tabela nova.
