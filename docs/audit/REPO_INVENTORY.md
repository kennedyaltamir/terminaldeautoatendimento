[[MESAFLOW_BEGIN:docs/audit/REPO_INVENTORY.md]]
# 📦 Inventário Técnico do Repositório MesaFlow OS

**Data de Geração:** 2026-01-08
**Versão do Kernel:** 6.3
**Escopo:** Mapeamento integral de módulos, serviços e fronteiras arquiteturais.

---

## 1. Visão Geral da Arquitetura

O MesaFlow OS opera sob uma arquitetura **Monolito Modular Híbrido**, composta por três grandes domínios de aplicação interconectados:

1.  **Backend (API Gateway & Core Logic):** Python/FastAPI.
2.  **Frontend (Web Client & Admin):** Next.js/React.
3.  **Mobile (Native Operations):** React Native/Expo.

A persistência é garantida por **PostgreSQL** (Dados Relacionais) e **Redis** (Cache & Pub/Sub).

---

## 2. Mapeamento de Domínios

### 🧠 Backend (`app/`)
Responsável pela regra de negócio, segurança, persistência e orquestração de eventos.

*   **Core Framework:** FastAPI, Uvicorn.
*   **Database Layer:** SQLAlchemy (Async), Alembic (Migrations).
*   **Entrypoint:** `app/main.py` (Configuração de App, CORS, Sentry, Rotas).

#### Módulos de Serviço (`app/services/`)
| Serviço | Responsabilidade | Dependências |
| :--- | :--- | :--- |
| `payment_service.py` | Orquestração de pagamentos e cálculo de Split. | PaymentFactory, Models |
| `stock_service.py` | Gestão de estoque, baixa de ficha técnica e Regra 86. | WhatsAppService, Models |
| `ifood_service.py` | Integração com iFood (Polling/Ingestão). | HTTPX, Models |
| `webhook_dispatcher.py` | Envio de Webhooks de saída (Outbound). | HTTPX, HMAC |
| `whatsapp_service.py` | Integração com Evolution API para mensagens. | HTTPX |
| `stripe_service.py` | Gestão de assinaturas SaaS (Billing). | Stripe SDK |
| `loyalty_service.py` | Cálculo e crédito de Cashback. | Models |
| `recommendation_service.py` | Motor de IA para Upselling (Market Basket). | SQLAlchemy |
| `audit_service.py` | Registro de logs de auditoria imutáveis. | Models |
| `feature_flag_service.py` | Gestão de toggles de funcionalidades. | Redis, Models |
| `fiscal/` | Módulo Fiscal (Adapter Pattern). | FocusNFeProvider, MockProvider |

#### Controladores (`app/routers/`)
*   **Auth:** `auth.py` (JWT, Google OAuth).
*   **Public:** `public.py` (Cardápio, Check-in).
*   **Admin:** `admin.py`, `admin_*.py` (Gestão segmentada: menu, tables, inventory, employees, billing, delivery, audit, fiscal, financial, marketing, franchise, integrations, features).
*   **Webhooks:** `webhooks.py` (Inbound: Stripe, MP, Fiscal).
*   **Payments:** `payments.py` (Simulação/Processamento).

---

### 🎨 Frontend (`frontend/`)
Aplicação Web SPA/SSR para clientes finais e gestores.

*   **Framework:** Next.js 14 (App Router).
*   **Estilo:** Tailwind CSS.
*   **Estado Global:** React Context (`CartContext`, `WebSocketContext`, `LanguageContext`).
*   **Offline/Local:** Dexie.js (IndexedDB Wrapper).

#### Estrutura de Rotas (`src/app/`)
*   **Público:**
    *   `[slug]/menu`: Cardápio Digital (PWA).
    *   `[slug]/kiosk`: Modo Totem (Kiosk).
    *   `page.tsx`: Landing Page Institucional.
*   **Administrativo (`admin/[slug]/`):**
    *   `dashboard`: BI e Métricas.
    *   `kitchen`: KDS (Kitchen Display System).
    *   `waiter`: App do Garçom (Mobile Web).
    *   `delivery`: Gestão de Logística.
    *   `counter`: PDV de Balcão.
    *   `settings`: Configurações Gerais.
    *   `inventory`, `menu`, `tables`, `team`, `history`, `audit`, `marketing`, `franchise`.

#### Bibliotecas Core (`src/lib/`)
*   `api.ts`: Cliente HTTP (Fetch Wrapper).
*   `auth.ts`: Gestão de Tokens (LocalStorage).
*   `db.ts`: Schema do Banco Local (Offline).
*   `printer/`: Drivers de impressão (ESC/POS, ZPL).
*   `smartpos.ts`: Integração com maquininhas (Stone/PagSeguro).

---

### 📱 Mobile (`mobile/`)
Aplicativo Nativo para operação de alta performance (Garçom/KDS).

*   **Framework:** React Native (Expo SDK 54).
*   **Estado:** Zustand.
*   **Navegação:** React Navigation.

#### Camadas
*   **Store:** `auth.store.ts`, `orders.store.ts`, `session.store.ts`, `settings.store.ts`, `waiter.store.ts`.
*   **Services:** `api.ts`, `auth/`, `realtime/`, `sync/`, `alerts/`.
*   **UI Foundation:** `src/ui/` (Design System Nativo).
*   **Screens:** `auth/`, `orders/` (KDS), `waiter/` (POS).

---

## 3. Infraestrutura & DevOps (`scripts/`)

Automação e manutenção do ciclo de vida do software.

*   **Setup:** `check_env.py`, `verify_installation.py`, `mobile_doctor.py`.
*   **Maintenance:** `seed.py` (Dados de teste), `update_db_*.py` (Migrações manuais), `fix_*.py` (Correções).
*   **Functional:** Scripts de teste manual e simulação (`simular_pagamento.py`, `test_whatsapp_real.py`).
*   **Security:** `security_audit.py`.
*   **Validation:** `verify_TASK-*.py` (Proof of Work).
*   **Tests:** Suíte Pytest (`scripts/tests/`).

---

## 4. Documentação (`docs/`)

A fonte da verdade do projeto.

*   **Governance:** `governance/` (Protocolos, Leis, Perfis de IA).
*   **Technical:** `technical/` (API Reference, ERD, Troubleshooting).
*   **Tasks:** `tasks/` (Logs de execução de tarefas).
*   **Manuals:** `manuals/` (Guias de usuário).
*   **Reports:** `reports/` (Relatórios de auditoria e incidentes).

---

## 5. Fronteiras de Integração

*   **Pagamentos:** Mercado Pago (Split), Stripe (SaaS).
*   **Mensageria:** Evolution API (WhatsApp).
*   **Fiscal:** Focus NFe.
*   **Delivery:** iFood (Polling).
*   **Hardware:** Impressoras Térmicas (RawBT/Network), SmartPOS (Deep Link).