# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 6.0 — Total Coverage (Web & Mobile)
**Status:** SELADO

Este documento é o contrato final de comportamento. Nenhuma tela deve divergir destas especificações.

## 1. Módulo Público & Cliente
- [x] [**Cardápio PWA**](./pages/PUBLIC_MENU.md) — `/[slug]/menu`
- [x] [**Totem & Offline**](./pages/PUBLIC_KIOSK_OFFLINE.md) — `/[slug]/kiosk` | `/offline`
- [x] [**Monitor Público**](./pages/KITCHEN_MONITOR.md) — `/[slug]/monitor`
- [x] [**Trust Center**](./pages/TRUST_CENTER.md) — `/trust`

## 2. Módulo Administrativo (Web)
- [x] [**Login & Registro**](./pages/ADMIN_LOGIN.md) — `/admin/login` | `/register`
- [x] [**Dashboard BI**](./pages/ADMIN_DASHBOARD.md) — `/admin/[slug]/dashboard`
- [x] [**Auditoria & Marketing**](./pages/ADMIN_FINANCE_MARKETING.md) — `/audit/financial` | `/marketing`
- [x] [**Equipe & Perfil**](./pages/ADMIN_TEAM_PROFILE.md) — `/team` | `/profile`
- [x] [**Faturamento SaaS**](./pages/ADMIN_SETTINGS_BILLING.md) — `/settings/billing`
- [x] [**Configurações Gerais**](./pages/ADMIN_GENERAL_SETTINGS.md) — `/settings`
- [x] [**Feature Flags**](./pages/ADMIN_SETTINGS_FEATURES.md) — `/settings/features`

## 3. Módulo Operacional (Mobile App)
- [x] [**Auth & Cozinha**](./pages/MOBILE_AUTH_KDS.md) — `LoginScreen` | `OrdersScreen`
- [x] [**Fluxo do Garçom**](./pages/MOBILE_WAITER_FLOW.md) — `WaiterTables` | `OrderEntry` | `Payment`
- [x] [**Logística & Hardware**](./pages/MOBILE_LOGISTICS_TOOLS.md) — `DriverDashboard` | `PrinterDebug`

---
*Nota: 100% das rotas mapeadas e documentadas.*
