# 🗺️ Mapa de Dependências e Integrações Externas
**Versão:** 5.0.1-SEQ | **Domínio:** INFRASTRUCTURE

## 1. Diagrama de Dependências Internas

```mermaid
graph TD
    subgraph "API Layer"
        R_AUTH[auth.py]
        R_ORD[admin_delivery.py]
        R_PUB[public/orders.py]
    end

    subgraph "Service Layer"
        S_ORD[order_service.py]
        S_PAY[payment_service.py]
        S_LED[ledger_service.py]
        S_REC[reconciliation_service.py]
    end

    subgraph "Persistence"
        M_ORD[models/orders.py]
        M_FIN[models/fintech.py]
        DB[(PostgreSQL RLS)]
    end

    subgraph "Async Tasks"
        T_WH[tasks/webhooks.py]
        T_FIS[tasks/fiscal.py]
    end

    R_ORD --> S_ORD
    S_ORD --> S_LED
    S_LED --> M_FIN
    S_PAY --> S_LED
    S_ORD --> T_WH
    M_FIN --> DB
    M_ORD --> DB
```

## 2. Catálogo de Integrações Externas

| Provedor | Endpoint | Função | Timeout | Fallback |
| :--- | :--- | :--- | :---: | :--- |
| **Mercado Pago** | `/v1/payments` | Pix/Cartão | 10s | Pix Estático (Manual) |
| **Stripe** | `/v1/checkout` | SaaS Billing | 15s | Grace Period (3 dias) |
| **FocusNFe** | `/v2/nfce` | Fiscal | 30s | Contingência Offline (Dexie) |
| **Evolution API** | `/message/send` | WhatsApp | 5s | Log Silencioso (Fail-Open) |

### 2.1. Resiliência de Integração
- **Circuit Breaker:** Ativo para FocusNFe e Mercado Pago. Se 20 erros ocorrerem em 60s, o circuito abre por 30s.
- **Idempotência:** Chave `X-Idempotency-Key` enviada em todos os POSTs externos.

