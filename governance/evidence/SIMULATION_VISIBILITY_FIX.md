# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 08:50:00
# 🩺 Relatório de Correção: Visibilidade de Status de Pedido

## 1. Problema Identificado
A simulação de entrega falhava porque o cliente não conseguia visualizar o status "Pronto". A investigação revelou que o componente `OrderStatusView.tsx` ocultava o rastreamento para pedidos com pagamento pendente.

## 2. Ações Executadas
- **Frontend:** O stepper de status foi movido para fora do bloco condicional `isPaid`. Agora, o cliente pode acompanhar o progresso da cozinha mesmo antes da confirmação financeira (essencial para pagamentos offline/entrega).
- **Backend:** Adicionado endpoint `PATCH /api/admin/orders/{id}/payment` para permitir que o staff confirme pagamentos manualmente via painel administrativo.
- **Automação:** O script `delivery_realtime_simulation.py` foi atualizado para confirmar o pagamento durante o setup, garantindo que o ambiente de teste reflita um cenário de produção real.

## 3. Veredito
O sistema agora é mais transparente para o usuário final e mais testável para a equipe de QA.

---
*MesaFlow Kernel L6 — Engineered for Stability.*

