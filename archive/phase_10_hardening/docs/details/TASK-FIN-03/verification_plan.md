# 🧪 Plano de Verificação: TASK-FIN-03

## 1. Critérios de Sucesso (DoD)
- [ ] Teste unitário prova que um pedido de R$ 100,00 gera um split de R$ 2,50.
- [ ] Log de transação no banco de dados registra o valor da taxa retida.
- [ ] Webhook de teste do Stripe altera o `plan_tier` da empresa com sucesso.

## 2. Procedimento de Teste
1. Executar `pytest scripts/scripts/tests/test_payment_split.py`.
2. Simular um pagamento via script e verificar o campo `marketplace_fee` no banco.
3. Validar se o cálculo de centavos está exato (sem erros de float).
