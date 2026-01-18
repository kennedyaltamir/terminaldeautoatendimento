# 💾 Estratégia de Persistência e Sincronização
**Versão:** 5.0.1-SEQ | **Domínio:** FRONTEND | MOBILE

## 1. Estados Persistidos (Client-Side)
| Store / DB | Tecnologia | Escopo | Risco de Inconsistência |
| :--- | :--- | :--- | :--- |
| **AuthStore** | SecureStore / LocalStorage | JWT & Roles | Baixo (Refresh Token resolve) |
| **CartStore** | LocalStorage | Itens do Carrinho | Médio (Preço pode mudar) |
| **PendingOrders** | Dexie.js (IndexedDB) | Fila Offline | Alto (Estoque pode acabar) |
| **FiscalQueue** | Dexie.js (IndexedDB) | Notas Pendentes | Baixo (Retry determinístico) |

## 2. Protocolo de Sincronização (Offline-First)
1. **Detecção:** `navigator.onLine` + WebSocket Heartbeat.
2. **Priorização:** Fila de Pedidos > Fila Fiscal.
3. **Reconciliação:** 
    - O cliente envia o `offline_id`.
    - O servidor verifica se o pedido já existe (Idempotência).
    - Se não existe, processa e retorna o `server_id`.
    - O cliente limpa o registro local.

## 3. Melhorias Propostas
- **Eager Validation:** Validar estoque via WebSocket assim que o cliente entra no checkout, antes do envio.
- **Conflict Resolution:** Implementar "Last-Write-Wins" com timestamp do servidor para configurações de perfil.

