# 📖 Dicionário de Páginas e Telas (Ecossistema Completo)
**Versão:** 3.0 — Omniscience Edition
**Total de Rotas:** 34

Este documento mapeia a intenção, elementos e comportamento de cada rota para eliminar o retrabalho.

---

## 1. Módulo Público (Cliente Final)

### 1.1 Landing Page (`/`)
- **Intenção:** Conversão de leads e vendas SaaS.
- **Elementos:** Hero Video, Calculadora de ROI, FAQ, Lead Capture.
- **Comportamento:** Scroll-reveal, animações Framer Motion.

### 1.2 Cardápio Digital (`/[slug]/menu`)
- **Intenção:** Interface principal de venda.
- **Elementos:** CategoryNav, ProductCards, FloatingCart, SearchBar.
- **Comportamento:** Offline-first (Dexie), WebSocket para status de pedido.
- **API:** `GET /api/[slug]/menu`, `POST /api/[slug]/orders`.

### 1.3 Totem de Autoatendimento (`/[slug]/kiosk`)
- **Intenção:** Tela de atração para terminais físicos.
- **Elementos:** Vídeo em loop, Botão "Toque para começar".
- **Comportamento:** Reseta para esta tela após 60s de inatividade.

### 1.4 Monitor Público de Senhas (`/[slug]/monitor`)
- **Intenção:** Exibição de status de retirada para o salão.
- **Elementos:** Colunas "Preparando" e "Pronto".
- **Comportamento:** Read-only, atualização via WebSocket, alerta sonoro.

### 1.5 Trust Center (`/trust`, `/trust/status`, `/trust/security`)
- **Intenção:** Transparência técnica para clientes Enterprise.
- **Elementos:** Health Indicators, Security Badges.
- **API:** `GET /api/health`.

### 1.6 Offline Page (`/offline`)
- **Intenção:** Fallback visual para perda total de rede.

---

## 2. Módulo Administrativo (Gestão & Auth)

### 2.1 Login (`/admin/login`)
- **Elementos:** EmailInput, PasswordInput (com toggle), GoogleLogin.
- **Comportamento:** Redireciona para dashboard se token for válido.

### 2.2 Registro (`/admin/register`)
- **Elementos:** Multi-step form, SlugValidator.
- **Comportamento:** Cria tenant e primeira mesa automaticamente.

### 2.3 Dashboard de BI (`/admin/[slug]/dashboard`)
- **Elementos:** KPI Cards, Recharts (Vendas/Hora, Top Produtos).
- **API:** `GET /api/admin/metrics`.

### 2.4 Gestão de Cardápio (`/admin/[slug]/menu`)
- **Elementos:** CategoryAccordion, ProductForm, ImageUpload.
- **Comportamento:** Invalida cache do Redis ao salvar.

### 2.5 Gestão de Mesas (`/admin/[slug]/tables`)
- **Elementos:** TableGrid, QR Generator, PositionEditor.
- **Comportamento:** Drag & Drop para layout do salão.

### 2.6 Auditoria Financeira (`/admin/[slug]/audit/financial`)
- **Elementos:** LedgerTable, ReconciliationPanel.
- **Comportamento:** Read-only, valida Hash Chain.

### 2.7 Configurações de Faturamento (`/admin/[slug]/settings/billing`)
- **Elementos:** PlanSelector, StripePortalButton.
- **Comportamento:** Bloqueia features se fatura estiver atrasada.

### 2.8 Funcionalidades Beta (`/admin/[slug]/settings/features`)
- **Elementos:** FeatureToggles.
- **Comportamento:** Apenas acessível via Impersonation (Suporte).

---

## 3. Módulo Operacional (KDS & POS)

### 3.1 Monitor de Cozinha (`/admin/[slug]/kitchen`)
- **Elementos:** OrderCards, StationFilter, BumpBar Shortcuts.
- **Comportamento:** WebSocket `new_order`, Alerta sonoro, Timer de SLA.

### 3.2 App do Garçom (`/admin/[slug]/waiter`)
- **Elementos:** TableSelector, ServiceRequestAlerts.
- **Comportamento:** Vibração ao receber chamado de mesa.

### 3.3 POS de Lançamento (`/admin/[slug]/waiter/pos/[tableId]`)
- **Elementos:** QuickSearch, Cart, PaymentModal.
- **Comportamento:** Impressão Bluetooth nativa (ESC/POS).

### 3.4 App do Entregador (`/admin/[slug]/driver`)
- **Elementos:** DeliveryList, MapView, POD (Proof of Delivery).
- **Comportamento:** Captura GPS em background.

---
*Nota: Para especificações de elementos e APIs de cada rota, consulte os arquivos em `docs/technical/pages/*.md`.*
