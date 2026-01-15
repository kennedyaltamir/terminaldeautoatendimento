# 📊 Diagramas de Fluxo e Sequência (Mermaid)
**Domínio:** ARCHITECTURE / DOCUMENTATION
**Status:** ATIVO

Este documento centraliza a lógica visual dos processos críticos do MesaFlow OS.

---

## 1. Fluxo de Pagamento Pix (Split Automático)
Este diagrama descreve a interação entre o Cliente, Backend, Mercado Pago e o Ledger Financeiro.

```mermaid
sequenceDiagram
    participant C as Cliente (PWA)
    participant B as Backend (FastAPI)
    participant MP as Mercado Pago API
    participant L as Ledger (L7)
    participant K as KDS (WebSocket)

    C->>B: POST /orders (Finalizar com Pix)
    B->>MP: POST /v1/payments (com application_fee)
    MP-->>B: 201 Created (QR Code + ID)
    B-->>C: Exibe QR Code
    Note over MP,B: Aguardando Webhook...
    MP->>B: POST /webhooks/mercadopago (Status: approved)
    B->>B: register_transaction_idempotent()
    B->>L: create_entry(CREDIT, amount, hash_chain)
    B->>K: broadcast(order_update: paid)
    K-->>K: Toca Alerta Sonoro
```

---

## 2. Ingestão de Pedidos iFood (Hub Bridge)
Fluxo de captura de pedidos externos para o monitor de cozinha unificado.

```mermaid
graph TD
    IF[iFood API] -->|Webhook| WH[webhooks_ifood.py]
    WH -->|Verify Signature| HMAC{HMAC-SHA256 OK?}
    HMAC -->|Não| ERR[403 Forbidden]
    HMAC -->|Sim| BG[process_event_background]
    BG -->|Fetch Details| IF
    IF -->> BG: Order JSON
    BG -->|Map Products| DB[(PostgreSQL)]
    BG -->|Broadcast| WS[WebSocket Manager]
    WS -->|Notify| KDS[Monitor de Cozinha]
```

---

## 3. Ciclo de Vida do Token (Auth Hardening)
```mermaid
stateDiagram-v2
    [*] --> Login
    Login --> Authenticated: JWT Issued
    Authenticated --> Request: Bearer Token
    Request --> Authenticated: 200 OK
    Request --> Expired: 401 Unauthorized
    Expired --> Refresh: POST /auth/refresh
    Refresh --> Authenticated: New Pair
    Refresh --> Login: Invalid/Expired Refresh
```
