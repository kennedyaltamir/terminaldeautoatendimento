# 🚀 MesaFlow: Master Project Context & Architecture

**Versão:** 1.0 (Consolidada)
**Data de Referência:** Janeiro de 2026
**Status:** Fase 10 (Mobile & Deep Tech) em andamento.

---

## 1. Visão Geral do Produto
O **MesaFlow** é um ecossistema SaaS B2B Enterprise projetado para orquestrar operações em ambientes de alto tráfego (Restaurantes, Hotéis, Estádios e Eventos). 

### Diferencial Estratégico: Arquitetura Híbrida
O sistema permite que o **Autoatendimento** (Cliente via QR Code/PWA) e a **Operação Assistida** (Staff via Mobile POS) coexistam na mesma comanda em tempo real, eliminando fricções de pagamento e anotação.

---

## 2. Stack Tecnológica (The Engine)

### 🧠 Backend (API Gateway & Business Logic)
- **Framework:** Python 3.11+ com FastAPI (Async/Await).
- **ORM:** SQLAlchemy 2.0 com suporte a `GUID` híbrido (compatibilidade SQLite/PostgreSQL).
- **Banco de Dados:** PostgreSQL (Neon.tech) com isolamento Multi-tenant (RLS).
- **Real-time:** WebSockets sobre Redis Pub/Sub para escalabilidade horizontal.
- **Segurança:** JWT com Rotação de Refresh Tokens e Rate Limiting (SlowAPI).

### 🎨 Frontend Web (Admin & Customer PWA)
- **Framework:** Next.js 14 (App Router) + TypeScript.
- **Estilização:** Tailwind CSS + ShadcnUI + Framer Motion.
- **Offline-First:** Dexie.js (IndexedDB) para sincronização de pedidos e notas fiscais.

### 📱 Mobile (Native Experience)
- **Framework:** React Native com Expo (Managed Workflow).
- **Estado:** Zustand (Global) + React Query (Server State).
- **Segurança:** Expo SecureStore (Hardware-backed encryption).

---

## 3. Módulos e Funcionalidades (Esmiuçados)

### 3.1 Core Operacional
- **Engenharia de Cardápio:** Categorias agendadas, produtos com variações complexas e adicionais.
- **Gestão de Mesas:** Mapa de sala visual, abertura/fechamento, transferência e junção (merge) de comandas.
- **KDS (Kitchen Display System):** Monitor de produção setorizado (Bar/Cozinha) com SLA visual por cores e alertas sonoros.
- **Modo Expedidor:** Tela de conferência e montagem de bandejas.

### 3.2 Fintech & SaaS
- **Split de Pagamento:** Integração Mercado Pago OAuth. A comissão do SaaS é retida na fonte.
- **Assinaturas:** Motor Stripe para planos Free/Pro com bloqueio automático de recursos.
- **Fidelidade:** Sistema de Cashback automático vinculado ao telefone do cliente.

### 3.3 Fiscal & Legal (Fase 9)
- **Homologação SEFAZ:** Emissão real de NFC-e via FocusNFe em ambiente de produção.
- **Contingência Offline:** Capacidade de emitir notas sem internet e sincronizar automaticamente via worker local.
- **Salvaguardas:** Trava de segurança dupla para evitar ativação acidental de produção.

### 3.4 Governança & Suporte
- **Tenant Impersonation (God Mode):** Permite que o suporte acesse qualquer conta de cliente com log de auditoria imutável.
- **Feature Flags:** Sistema de Canary Release para ativar funcionalidades Beta por tenant via UI administrativa.

### 3.5 Logística & Delivery
- **App do Entregador:** PWA com rastreamento GPS em tempo real e Proof of Delivery (POD).
- **Middleware iFood:** Serviço de polling para ingestão automática de pedidos de marketplaces externos.

---

## 4. Estado Atual: Domínio Mobile (Fase 10)

O desenvolvimento mobile seguiu o princípio de **Infraestrutura Primeiro**:

1.  **Setup:** Repositório Expo inicializado com TypeScript estrito.
2.  **Auth Infra:** Cliente Axios isolado com interceptores de segurança.
3.  **Refresh Lock:** Lógica de semáforo que impede múltiplas chamadas de refresh de token simultâneas.
4.  **Application Layer:** Store global (Zustand) implementada com ciclo de vida de sessão (Cold Start/Hydration).
5.  **Fail Secure:** O app identifica o estado de autenticação antes de renderizar qualquer UI, garantindo que dados sensíveis nunca vazem.

---

## 5. Regras de Ouro para o Futuro (Governança v5.3)

1.  **Separação de Domínios:** Alterações em `mobile/`, `frontend/` e `app/` devem ser tratadas como contextos isolados.
2.  **Integridade Financeira:** Uso obrigatório de `Decimal` para qualquer cálculo monetário.
3.  **Documentação Contínua:** Toda task concluída deve gerar um log em `docs/tasks/` (Web/Back) ou `docs/mobile/tasks/` (Mobile).
4.  **Protocolo de Resposta:** Toda interação deve iniciar com `<Task_Classification>` e `<Domain>`.

---
*Este documento é a verdade absoluta do projeto MesaFlow até a data presente.*
