# 📱 Task 21: SLA Engine & Prioridade Operacional

## 1. Contexto
Elevação do KDS Mobile para um sistema de decisão por prioridade temporal. O tempo passa a ser um dado de domínio processado centralmente.

## 2. Arquitetura do Global Clock
Introduzimos o `GlobalClockService` (Singleton) que emite pulsos de tempo sincronizados. 
- **Benefício**: Evita que cada card de pedido tenha seu próprio timer (`setInterval`), economizando bateria e memória.
- **Acoplamento**: A `OrdersStore` assina o clock para recalcular métricas de SLA e reordenar a lista.

## 3. SLA Engine & Priority Score
Lógica determinística para classificar pedidos:
- **OK**: > 50% do tempo restante.
- **WARNING**: <= 50% do tempo restante.
- **CRITICAL**: <= 20% do tempo restante.
- **BREACHED**: Tempo esgotado (Prioridade máxima).

A lista de pedidos é ordenada dinamicamente pelo `priorityScore`, garantindo que o que é urgente apareça primeiro.

## 4. Dívida Técnica Resolvida
- [x] Removidos cálculos de tempo do render da `OrdersScreen`.
- [x] Centralizada a fonte de verdade temporal (`Date.now()` isolado).

---
*Fase 10 — Janeiro de 2026*
