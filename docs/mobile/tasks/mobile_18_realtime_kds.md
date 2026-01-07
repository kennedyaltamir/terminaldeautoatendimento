# 📱 Task 18: Realtime Operacional (KDS Mobile)

## 1. Objetivo
Implementação da infraestrutura de comunicação em tempo real para o Monitor de Produção, garantindo latência sub-segundo na atualização de status e sincronia entre dispositivos nativos e web.

## 2. Arquitetura Refinada (v2.0)
- **Transporte (`OrdersRealtimeService`)**: Agora utiliza o `RealtimeEvent` type para normalizar a comunicação. O log de encerramento inclui o `code` do protocolo WebSocket.
- **Processamento (`OrdersStore`)**: Implementada lógica de merge com retornos de estado explícitos e guard clauses de segurança.
- **Isolamento**: A UI continua 100% isolada, consumindo apenas o estado reativo do Zustand.

## 3. Matriz de Eventos Documentada
- `new_order`: Notifica a existência de uma nova comanda. Exige sincronização via fetch se o payload for parcial.
- `order_update`: Atualiza o status atômico de um pedido existente na lista.
- `waiter_call`: Evento de sinalização sensorial (Pendente integração com sistema de som/vibração).

## 4. Dívida Técnica (Endurecida)
- **Reconnection Strategy**: Falta o loop de retry em caso de perda de sinal Wi-Fi.
- **Implicit Authentication**: A conexão do WebSocket confia na barreira do `AuthGate` mas não envia o Token JWT no handshake (Subprotocolo ou Query).

---
*Fase 10 — Janeiro de 2026*
