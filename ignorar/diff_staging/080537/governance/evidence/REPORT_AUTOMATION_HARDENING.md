# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 15:15:00
# 🛡️ Relatório de Endurecimento de Automação (QA-Standard)

## 1. Problema Identificado
Falha sistemática em testes E2E devido a seletores de interface ambíguos. O uso de `:has-text` causava colisões com múltiplos elementos no DOM, violando o `strict mode` do Playwright.

## 2. Padrão Adotado (MesaFlow QA-Gold)
Fica estabelecido o uso obrigatório de atributos de teste para elementos interativos:
- **Container:** `[data-testid="<contexto>.<entidade>.card"]`
- **Instância:** `[data-order-id="<uuid>"]`
- **Ação:** `[data-testid="<contexto>.<entidade>.<acao>"]`

## 3. Implementações Realizadas
- **Driver Dashboard:** Cards de pedido instrumentados com `delivery.order.card` e botões com `delivery.order.pickup`.
- **Customer View:** Stepper e Mapa instrumentados com prefixos `customer.order.*`.
- **Simulador:** Script atualizado para utilizar `get_by_test_id`, eliminando 100% das ambiguidades.

---
*Assinado: Optimus Kernel L6*
