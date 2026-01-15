# ⏪ Plano de Rollback: TASK-FIN-03

## 1. Procedimento
- Reverter `app/services/payment_service.py` para a versão sem cálculo de `application_fee`.
- Zerar o campo `marketplace_fee_percentage` no banco de dados para evitar cobranças indevidas.
