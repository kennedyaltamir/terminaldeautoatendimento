# 🔐 Referência de Variáveis de Ambiente (.env)

Este documento descreve todas as variáveis de configuração suportadas pelo MesaFlow.
**Importante:** Nunca commite o arquivo `.env` real. Use `.env.example` como base.

## 1. Core & Banco de Dados
| Variável | Obrigatório | Descrição | Exemplo |
| :--- | :---: | :--- | :--- |
| `DATABASE_URL` | **SIM** | Connection string do PostgreSQL (Async). | `postgresql://user:pass@localhost:5432/db` |
| `REDIS_URL` | Não | URL do Redis para Cache e Pub/Sub. Se omitido, usa memória local. | `redis://localhost:6379/0` |
| `SECRET_KEY` | **SIM** | Chave para assinar tokens JWT. | `openssl rand -hex 32` |
| `ENVIRONMENT` | Não | `development` ou `production`. | `development` |

## 2. Frontend (Next.js)
| Variável | Obrigatório | Descrição | Exemplo |
| :--- | :---: | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | **SIM** | URL base da API Backend. | `http://localhost:8000/api` |
| `NEXT_PUBLIC_WS_URL` | **SIM** | URL base do WebSocket. | `ws://localhost:8000/ws` |
| `NEXT_PUBLIC_ROOT_DOMAIN` | Não | Domínio raiz para lógica de subdomínios. | `mesaflow.com.br` |

## 3. Integrações Financeiras
| Variável | Obrigatório | Descrição |
| :--- | :---: | :--- |
| `STRIPE_SECRET_KEY` | Não* | Chave secreta da API Stripe (SaaS Billing). |
| `STRIPE_WEBHOOK_SECRET` | Não* | Segredo para validar webhooks do Stripe. |
| `STRIPE_PRO_PRICE_ID` | Não* | ID do plano "Pro" no dashboard do Stripe. |
| `MP_APP_ID` | Não* | App ID do Mercado Pago (Split). |
| `MP_CLIENT_SECRET` | Não* | Client Secret do Mercado Pago (Split). |

*\*Obrigatório apenas se for ativar cobranças reais.*

## 4. Integrações de Terceiros
| Variável | Obrigatório | Descrição |
| :--- | :---: | :--- |
| `WHATSAPP_API_URL` | Não | URL da Evolution API ou similar. |
| `WHATSAPP_API_TOKEN` | Não | Token de autenticação da API de Zap. |
| `SENTRY_DSN_BACKEND` | Não | DSN do Sentry para logs do Python. |
| `NEXT_PUBLIC_SENTRY_DSN` | Não | DSN do Sentry para logs do React. |
