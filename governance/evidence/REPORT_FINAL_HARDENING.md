# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 16:45:00
# 🛡️ Relatório de Hardening Logístico (Enterprise Standard)

## 1. Integridade Concorrente (Locks)
Implementado `with_for_update()` no banco de dados para os fluxos de despacho. 
- **Risco Mitigado:** Double-dispatch (dois entregadores coletando o mesmo pedido).
- **Consistência:** Um driver está agora limitado a 1 entrega ativa por vez em nível de transação SQL.

## 2. Segurança de Telemetria (Ownership)
O endpoint de GPS agora exige que o `current_user.id` seja idêntico ao `driver_id` do pedido.
- **Risco Mitigado:** Spoofing de localização por outros membros da equipe.

## 3. Eficiência de Bateria e Custo (ETA Model)
Introduzido o **Simple ETA Model (Haversine)** no backend.
- **Vantagem:** O cliente final recebe atualizações de chegada a cada GPS sem disparar requisições para APIs de roteamento externas.
- **Throttle:** 3 segundos de frequência mínima para economia de dados e energia.

## 4. Padronização WS v2
Eventos renomeados para o padrão de namespaces:
- `delivery.status`
- `delivery.location`

---
*MesaFlow Kernel L6 — Release Sealed.*

