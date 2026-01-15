# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 4.0 — Total Specification
**Status:** ATIVO (Contrato de Comportamento)

Este documento detalha as 34 rotas do ecossistema. Nenhuma alteração de UI deve divergir destas especificações sem atualização prévia deste dicionário.

---

## 1. Módulo Público (Cliente Final)

### 1.1 Landing Page (`/`)
- **Elementos:** Hero Video, ROI Calculator, Lead Capture, FAQ.
- **Comportamento:** Scroll-reveal. O botão "Começar" leva ao `/admin/register`.
- **API:** `POST /api/leads` (Captura de e-mail).

### 1.2 Cardápio Digital (`/[slug]/menu`)
- **Elementos:** CategoryNav (Sticky), ProductGrid, FloatingCart, SearchBar.
- **Comportamento:** Ao clicar no produto, abre `ProductModal`. Se `?table=X`, ativa modo salão.
- **API:** `GET /api/[slug]/menu`, `POST /api/[slug]/orders`.

### 1.3 Totem de Autoatendimento (`/[slug]/kiosk`)
- **Elementos:** Vídeo de fundo, Botão gigante "Toque para Iniciar".
- **Comportamento:** Bloqueia gestos de navegação do browser. Reseta após 60s.

### 1.4 Monitor Público (`/[slug]/monitor`)
- **Elementos:** Duas colunas (Preparando | Pronto).
- **Comportamento:** Atualização via WebSocket. Toca "ding.mp3" quando um pedido entra em "Pronto".

### 1.5 Trust Center (`/trust`, `/status`, `/security`)
- **Elementos:** Badges de conformidade, Gráfico de Uptime.
- **API:** `GET /api/health`.

### 1.6 Offline Fallback (`/offline`)
- **Elementos:** Ilustração de desconexão, Botão "Tentar Novamente".

---

## 2. Módulo Administrativo (Gestão)

### 2.1 Login & Registro (`/admin/login`, `/admin/register`)
- **Elementos:** AuthInput, GoogleButton, SlugValidator.
- **Comportamento:** Validação de força de senha em tempo real.

### 2.2 Dashboard BI (`/admin/[slug]/dashboard`)
- **Elementos:** KPI Cards (Faturamento, Ticket Médio), Gráficos Recharts.
- **API:** `GET /api/admin/metrics`.

### 2.3 Histórico de Vendas (`/admin/[slug]/dashboard/history`)
- **Elementos:** Tabela paginada, Filtro por Status/Data.
- **API:** `GET /api/admin/[slug]/history`.

### 2.4 Gestão de Cardápio (`/admin/[slug]/menu`)
- **Elementos:** CategoryAccordion, ProductForm, ImageUpload (S3/Local).
- **Comportamento:** Invalida cache do cardápio público ao salvar.

### 2.5 Gestão de Estoque (`/admin/[slug]/inventory`)
- **Elementos:** Tabela de Ingredientes, Alerta de Nível Crítico.
- **API:** `GET /api/admin/inventory/ingredients`.

### 2.6 Mapa de Mesas (`/admin/[slug]/tables`)
- **Elementos:** Canvas interativo, Gerador de QR Code PDF.
- **Comportamento:** Drag & Drop para posicionar mesas.

### 2.7 Gestão de Equipe (`/admin/[slug]/team`)
- **Elementos:** Lista de Funcionários, Seletor de Role (Kitchen, Waiter, Driver).

### 2.8 Marketing & Promoções (`/admin/[slug]/marketing`)
- **Elementos:** CouponCreator, CampaignStats.

### 2.9 Auditoria Financeira (`/admin/[slug]/audit/financial`)
- **Elementos:** LedgerTable, IntegrityBadge.
- **Comportamento:** Valida Hash Chain do banco em tempo real.

### 2.10 Faturamento SaaS (`/admin/[slug]/settings/billing`)
- **Elementos:** PlanCards, StripePortalLink.

### 2.11 Feature Flags (`/admin/[slug]/settings/features`)
- **Elementos:** Toggles de funcionalidades Beta.
- **Segurança:** Apenas acessível via Impersonation.

---

## 3. Módulo Operacional (KDS & POS)

### 3.1 Monitor de Cozinha (`/admin/[slug]/kitchen`)
- **Elementos:** OrderCards, StationFilter (Cozinha/Bar), Timer de SLA.
- **Comportamento:** WebSocket `order_update`.

### 3.2 Expedição (`/admin/[slug]/expeditor`)
- **Elementos:** Lista de conferência de itens.
- **Comportamento:** Botão "Despachar" dispara notificação ao cliente.

### 3.3 App do Garçom (`/admin/[slug]/waiter`)
- **Elementos:** Grid de Mesas, Notificações de Chamado.

### 3.4 POS de Lançamento (`/admin/[slug]/waiter/pos/[tableId]`)
- **Elementos:** QuickSearch, Carrinho, PaymentModal (Pix/Dinheiro).
- **Comportamento:** Impressão Bluetooth nativa.

### 3.5 App do Entregador (`/admin/[slug]/driver`)
- **Elementos:** Rota no Mapa, Botão "Entregue", Validador de Código.

---
*Documentação completa das 34 rotas selada.*
