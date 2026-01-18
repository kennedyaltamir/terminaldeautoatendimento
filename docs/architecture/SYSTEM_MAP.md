# 🗺️ Mapa de Arquitetura MesaFlow OS

```mermaid
graph TD
    subgraph "Client Layer"
        PWA[PWA Cliente - Next.js]
        APP[Super App - React Native]
        ADMIN[Painel Admin - Next.js]
    end

    subgraph "Communication"
        WS[WebSocket Server - Redis Pub/Sub]
        API[FastAPI Gateway - REST]
    end

    subgraph "Logic Layer"
        SVC[Order/Payment Services]
        LEDGER[Financial Ledger L7]
        IA[AI Prediction Engine]
    end

    subgraph "Persistence"
        DB[(PostgreSQL - RLS Enforced)]
        CACHE[(Redis - Cache & Session)]
    end

    PWA --> API
    APP --> API
    ADMIN --> API
    
    API --> WS
    API --> SVC
    SVC --> LEDGER
    SVC --> DB
    SVC --> CACHE
    IA --> DB
```

## Pontos de Integração Externa
- **Mercado Pago:** Pix e Split de Pagamento.
- **Stripe:** SaaS Billing e Assinaturas.
- **FocusNFe:** Emissão de documentos fiscais.
- **Evolution API:** Notificações transacionais WhatsApp.

