# 📱 Matriz de Consistência Offline-First (Mobile POS)
**Versão:** 10.0.1-AUTO | **Domínio:** MOBILE | **Status:** ACTIVE

## 1. Edge-cases de Inconsistência
| Cenário | Risco | Mitigação L10 |
| :--- | :--- | :--- |
| **Venda sem Estoque** | Estoque negativo no servidor | Reserva de estoque "otimista" via WebSocket (se disponível) |
| **Preço Desatualizado** | Venda por valor menor | Validação de `price_version` no momento do Sync |
| **Duplo Pagamento** | Registro duplicado no Ledger | Idempotência via `client_generated_uuid` |

## 2. Reconciliação Inteligente
- **Timestamp Authority:** O servidor é a autoridade final. Se um dado local for mais antigo que o dado do servidor, o local é descartado (Server-Wins).
- **Conflict Resolution:** Para configurações de perfil, o sistema utiliza **CRDTs (Conflict-free Replicated Data Types)** simplificados para garantir que mudanças em campos diferentes não se sobrescrevam.

## 3. Indicadores de Risco Financeiro
- `offline_transaction_volume_brl`: Valor total pendente de sincronização.
- `sync_latency_minutes`: Tempo médio entre a criação do pedido e a chegada no servidor.
- `failed_sync_retry_count`: Alerta se um pedido falhar no sync > 3 vezes.

