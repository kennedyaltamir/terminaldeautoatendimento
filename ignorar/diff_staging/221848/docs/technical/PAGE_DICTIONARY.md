# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 11.0 — Visual & Interactive Specification
**Status:** ATIVO

Este documento detalha as 34 rotas do ecossistema. Nenhuma alteração de UI deve divergir destas especificações.

---

## 1. Módulo Público (Cliente Final)

### 1.1 Landing Page (`/`)
- **Intenção:** Conversão de leads e vendas SaaS.
- **Demo:** `[🎥 VIDEO_DEMO_LP_01.mp4]`
- **Comportamento:** Scroll-reveal. O botão "Começar" leva ao `/admin/register`.

### 1.2 Cardápio Digital (`/[slug]/menu`)
- **Intenção:** Interface principal de venda.
- **Demo:** `[🎥 VIDEO_DEMO_MENU_01.mp4]`
- **Comportamento:** Ao clicar no produto, abre `ProductModal`. Se `?table=X`, ativa modo salão.

### 1.3 Totem de Autoatendimento (`/[slug]/kiosk`)
- **Intenção:** Tela de atração para terminais físicos.
- **Demo:** `[🎥 VIDEO_DEMO_KIOSK_01.mp4]`
- **Comportamento:** Bloqueia gestos de navegação do browser. Reseta após 60s.

---

## 2. Módulo Administrativo (Gestão)

### 2.1 Dashboard BI (`/admin/[slug]/dashboard`)
- **Intenção:** Visão geral do negócio.
- **Demo:** `[🎥 VIDEO_DEMO_DASH_01.mp4]`
- **API:** `GET /api/admin/metrics`.

### 2.2 Gestão de Cardápio (`/admin/[slug]/menu`)
- **Intenção:** Gestão de Itens.
- **Demo:** `[🎥 VIDEO_DEMO_MENU_MGMT_01.mp4]`
- **Comportamento:** Invalida cache do cardápio público ao salvar.

---

## 3. Módulo Operacional (KDS & POS)

### 3.1 Monitor de Cozinha (`/admin/[slug]/kitchen`)
- **Intenção:** Produção.
- **Demo:** `[🎥 VIDEO_DEMO_KDS_01.mp4]`
- **Comportamento:** WebSocket `order_update`.

### 3.2 App do Garçom (`/admin/[slug]/waiter`)
- **Intenção:** Atendimento.
- **Demo:** `[🎥 VIDEO_DEMO_WAITER_01.mp4]`
- **Comportamento:** Vibração ao receber chamado de mesa.

---
*Nota: Os vídeos de demonstração devem ser gravados em 720p, sem áudio, com duração máxima de 10s e armazenados em `docs/assets/demos/`.*
