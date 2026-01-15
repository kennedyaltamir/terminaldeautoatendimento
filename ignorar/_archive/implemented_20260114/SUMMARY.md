# 📘 MesaFlow: Relatório Técnico Consolidado

**Versão:** 2.3.0 (Enterprise Ready)
**Data:** 05/01/2026

Este documento resume toda a arquitetura, funcionalidades e decisões técnicas implementadas no projeto. Use-o como base de conhecimento para manutenção e expansão.

---

## 1. Arquitetura do Sistema

### Backend (API)
- **Framework:** FastAPI (Python 3.11+).
- **Banco de Dados:** PostgreSQL com SQLAlchemy Async (ORM).
- **Real-time:** WebSockets gerenciados via Redis Pub/Sub (escalável) com fallback para memória local.
- **Segurança:**
    - Autenticação JWT (Access + Refresh Tokens).
    - Rate Limiting (SlowAPI) por IP.
    - Isolamento Multi-tenant (Row-Level Security via `company_id`).
    - Sanitização de Inputs (Anti-XSS).

### Frontend (Cliente)
- **Framework:** Next.js 14 (App Router).
- **Estilização:** Tailwind CSS + Framer Motion.
- **Estado:** React Context API + Dexie.js (IndexedDB para modo offline).
- **PWA:** Manifesto configurado para instalação (Add to Home Screen).

---

## 2. Módulos Funcionais

### 🍔 Cardápio Digital (Cliente Final)
- **Acesso:** Via QR Code (Mesa) ou Link Direto (Delivery/Kiosk).
- **Features:**
    - Carrinho persistente.
    - Personalização de itens (Adicionais/Opções).
    - Checkout transparente (Pix/Cartão).
    - **Modo Kiosk:** Interface de totem com proteção de inatividade e tela de atração.

### 👨‍🍳 KDS (Kitchen Display System)
- **Interface:** Tela de produção para tablets.
- **Features:**
    - SLA Visual (Cores mudam com o tempo).
    - Setorização (Filtros para Bar, Cozinha, Sobremesa).
    - Gestão de Estoque Rápida (Regra 86).
    - Recall de pedidos finalizados.

### 📱 App do Garçom (Mobile POS)
- **Interface:** Otimizada para celulares da equipe.
- **Features:**
    - Mapa de Mesas em tempo real.
    - Lançamento de pedidos (Staff Override).
    - Transferência e Junção de Mesas.
    - Fechamento de conta com calculadora de troco.
    - **SmartPOS:** Integração via Deep Link com maquininhas Stone/PagSeguro.

### 🛵 Logística & Delivery
- **Interface:** Painel de Despacho e App do Entregador.
- **Features:**
    - Atribuição de entregadores.
    - Rastreamento GPS em tempo real (Relay via WebSocket).
    - Proof of Delivery (Código de confirmação).

---

## 3. Motor Financeiro (Fintech)

### 💳 Pagamentos
- **Split de Pagamento:** Integração Mercado Pago (OAuth). O valor é dividido na fonte entre o Restaurante e a Plataforma (SaaS).
- **Assinaturas:** Integração Stripe (Checkout/Portal). Controla o acesso aos recursos Pro/Enterprise automaticamente.

### 🤝 Fidelidade
- **Cashback:** Carteira digital vinculada ao telefone do cliente. Crédito automático após pagamento confirmado.

### 🧾 Fiscal
- **NFC-e:** Módulo de emissão fiscal integrado (Adapter Pattern).
- **Status:** Interface de histórico com status da nota e links para PDF/XML.

---

## 4. Inteligência & Dados

### 🧠 Marketing & IA
- **Upselling:** Motor de recomendação que analisa histórico de vendas ("Quem comprou X levou Y").
- **Automação:** Disparo de mensagens WhatsApp (API Evolution) para status de pedido e estoque baixo.

### 🏢 Franquias
- **Dashboard Multi-loja:** Visão consolidada de faturamento e pedidos para donos de redes.

---

## 5. Infraestrutura & DevOps

- **Docker:** Containerização otimizada (Multi-stage build).
- **Scripts:** Automação de setup, seed, migração e testes (`scripts/`).
- **Testes:** Suíte completa com Pytest (Backend) e Playwright (E2E Frontend).



# 📘 MesaFlow: Relatório Técnico Consolidado

**Versão:** 2.3.0 (Enterprise Ready)
**Data:** 05/01/2026

Este documento resume toda a arquitetura, funcionalidades e decisões técnicas implementadas no projeto. Use-o como base de conhecimento para manutenção e expansão.

---

## 1. Arquitetura do Sistema

### Backend (API)
- **Framework:** FastAPI (Python 3.11+).
- **Banco de Dados:** PostgreSQL com SQLAlchemy Async (ORM).
- **Real-time:** WebSockets gerenciados via Redis Pub/Sub (escalável) com fallback para memória local.
- **Segurança:**
    - Autenticação JWT (Access + Refresh Tokens).
    - Rate Limiting (SlowAPI) por IP.
    - Isolamento Multi-tenant (Row-Level Security via `company_id`).
    - Sanitização de Inputs (Anti-XSS).

### Frontend (Cliente)
- **Framework:** Next.js 14 (App Router).
- **Estilização:** Tailwind CSS + Framer Motion.
- **Estado:** React Context API + Dexie.js (IndexedDB para modo offline).
- **PWA:** Manifesto configurado para instalação (Add to Home Screen).

---

## 2. Módulos Funcionais

### 🍔 Cardápio Digital (Cliente Final)
- **Acesso:** Via QR Code (Mesa) ou Link Direto (Delivery/Kiosk).
- **Features:**
    - Carrinho persistente.
    - Personalização de itens (Adicionais/Opções).
    - Checkout transparente (Pix/Cartão).
    - **Modo Kiosk:** Interface de totem com proteção de inatividade e tela de atração.

### 👨‍🍳 KDS (Kitchen Display System)
- **Interface:** Tela de produção para tablets.
- **Features:**
    - SLA Visual (Cores mudam com o tempo).
    - Setorização (Filtros para Bar, Cozinha, Sobremesa).
    - Gestão de Estoque Rápida (Regra 86).
    - Recall de pedidos finalizados.

### 📱 App do Garçom (Mobile POS)
- **Interface:** Otimizada para celulares da equipe.
- **Features:**
    - Mapa de Mesas em tempo real.
    - Lançamento de pedidos (Staff Override).
    - Transferência e Junção de Mesas.
    - Fechamento de conta com calculadora de troco.
    - **SmartPOS:** Integração via Deep Link com maquininhas Stone/PagSeguro.

### 🛵 Logística & Delivery
- **Interface:** Painel de Despacho e App do Entregador.
- **Features:**
    - Atribuição de entregadores.
    - Rastreamento GPS em tempo real (Relay via WebSocket).
    - Proof of Delivery (Código de confirmação).

---

## 3. Motor Financeiro (Fintech)

### 💳 Pagamentos
- **Split de Pagamento:** Integração Mercado Pago (OAuth). O valor é dividido na fonte entre o Restaurante e a Plataforma (SaaS).
- **Assinaturas:** Integração Stripe (Checkout/Portal). Controla o acesso aos recursos Pro/Enterprise automaticamente.

### 🤝 Fidelidade
- **Cashback:** Carteira digital vinculada ao telefone do cliente. Crédito automático após pagamento confirmado.

### 🧾 Fiscal
- **NFC-e:** Módulo de emissão fiscal integrado (Adapter Pattern).
- **Status:** Interface de histórico com status da nota e links para PDF/XML.

---

## 4. Inteligência & Dados

### 🧠 Marketing & IA
- **Upselling:** Motor de recomendação que analisa histórico de vendas ("Quem comprou X levou Y").
- **Automação:** Disparo de mensagens WhatsApp (API Evolution) para status de pedido e estoque baixo.

### 🏢 Franquias
- **Dashboard Multi-loja:** Visão consolidada de faturamento e pedidos para donos de redes.

---

## 5. Infraestrutura & DevOps

- **Docker:** Containerização otimizada (Multi-stage build).
- **Scripts:** Automação de setup, seed, migração e testes (`scripts/`).
- **Testes:** Suíte completa com Pytest (Backend) e Playwright (E2E Frontend).
# 📘 MesaFlow: Relatório Técnico Consolidado v2.3.5

**Status:** Enterprise Ready (Green Build)
**Data:** 05/01/2026

## 1. Arquitetura de Segurança
- **Isolamento Multi-tenant:** Row-Level Security (RLS) via `company_id` em todas as tabelas.
- **Token de Acesso (PIN):** Sistema de 10 dígitos numéricos para recuperação de sessão de mesa, visível para staff e gestores.
- **RBAC:** Controle de acesso baseado em funções (Owner, Manager, Cashier, Kitchen, Driver) com redirecionamento automático no nível de Layout.

## 2. Operação Real-time
- **WebSockets:** Implementados sobre Redis Pub/Sub para sincronização instantânea entre Cliente, Garçom e Cozinha.
- **KDS Setorizado:** Filtros por estação (Bar/Cozinha) com persistência de preferência no navegador.

## 3. Fintech & SaaS
- **Split de Pagamento:** Integração Mercado Pago para divisão de receita na fonte.
- **Assinaturas:** Motor Stripe para gestão de planos Free/Pro.
- **Fidelidade:** Sistema de Cashback automático vinculado ao telefone do cliente.

## 4. Infraestrutura
- **Database:** PostgreSQL (Neon.tech) com suporte a GUIDs compatíveis com SQLite.
- **Cache:** Redis Layer 2 para otimização de leitura do cardápio público.
- **Deploy:** Orquestração via Docker e suporte a PaaS (Render/Vercel).
# 📘 MesaFlow: Relatório Técnico Consolidado v2.3.5

**Status:** Enterprise Ready (Green Build)
**Data:** 05/01/2026

## 1. Arquitetura de Segurança
- **Isolamento Multi-tenant:** Row-Level Security (RLS) via `company_id` em todas as tabelas.
- **Token de Acesso (PIN):** Sistema de 10 dígitos numéricos para recuperação de sessão de mesa, visível para staff e gestores.
- **RBAC:** Controle de acesso baseado em funções (Owner, Manager, Cashier, Kitchen, Driver) com redirecionamento automático no nível de Layout.

## 2. Operação Real-time
- **WebSockets:** Implementados sobre Redis Pub/Sub para sincronização instantânea entre Cliente, Garçom e Cozinha.
- **KDS Setorizado:** Filtros por estação (Bar/Cozinha) com persistência de preferência no navegador.

## 3. Fintech & SaaS
- **Split de Pagamento:** Integração Mercado Pago para divisão de receita na fonte.
- **Assinaturas:** Motor Stripe para gestão de planos Free/Pro.
- **Fidelidade:** Sistema de Cashback automático vinculado ao telefone do cliente.

## 4. Infraestrutura
- **Database:** PostgreSQL (Neon.tech) com suporte a GUIDs compatíveis com SQLite.
- **Cache:** Redis Layer 2 para otimização de leitura do cardápio público.
- **Deploy:** Orquestração via Docker e suporte a PaaS (Render/Vercel).
