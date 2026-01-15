# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-14 19:30:00

# 🗺️ Mapa de Infraestrutura

Visão lógica da distribuição dos serviços do MesaFlow OS.

```mermaid
graph TD
    subgraph "Client Layer"
        Browser[Navegador Web]
        MobileApp[App Android/iOS]
        Kiosk[Totem Touch]
    end

    subgraph "Edge / CDN"
        Vercel[Vercel Edge Network]
        Cloudflare[Cloudflare DNS/WAF]
    end

    subgraph "Application Layer (Render.com)"
        API[FastAPI Backend]
        Worker[Celery Worker]
    end

    subgraph "Data Layer"
        Neon[(Neon PostgreSQL)]
        Upstash[(Upstash Redis)]
        S3[AWS S3 / R2 Storage]
    end

    subgraph "External Services"
        Stripe[Stripe Gateway]
        MP[Mercado Pago]
        Wpp[Evolution API (WhatsApp)]
        Sentry[Sentry Observability]
    end

    %% Fluxos
    Browser -->|HTTPS| Vercel
    MobileApp -->|HTTPS/WSS| API
    Vercel -->|SSR Fetch| API
    
    API -->|SQL| Neon
    API -->|Pub/Sub| Upstash
    API -->|Upload| S3
    
    API -->|Webhooks| Stripe
    API -->|Webhooks| MP
    API -->|Logs| Sentry
    
    Worker -->|Async Tasks| Wpp
```

## Detalhes dos Serviços

| Componente | Provedor | Função | Tier |
| :--- | :--- | :--- | :--- |
| **Frontend** | Vercel | Hospedagem Next.js, Edge Functions, CDN. | Pro |
| **Backend** | Render | API Python, Workers, Cron Jobs. | Team |
| **Database** | Neon | Banco Relacional Serverless (Auto-scaling). | Launch |
| **Cache/WS** | Upstash | Redis Serverless para filas e real-time. | Pay-as-you-go |
| **Storage** | AWS S3 | Armazenamento de imagens de produtos. | Standard |

---
*Architecture Team*

