# 🕵️ Relatório de Auditoria Sistêmica (Full Coverage)
**Data:** 2026-01-15T04:01:17.687106
**Páginas Auditadas:** 38
**Total de Elementos Interativos:** 610

## 1. Matriz de Status
| Rota | Status | Botões | Links | Inputs | Erros |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `/` | ✅ 200 | 19 | 26 | 5 | 0 |
| `/[slug]/kiosk` | ✅ 200 | 0 | 0 | 0 | 0 |
| `/[slug]/menu` | ✅ 200 | 6 | 0 | 1 | 0 |
| `/[slug]/monitor` | ⚠️ 200 | 0 | 0 | 0 | 3 |
| `/admin/[slug]/audit` | ⚠️ 200 | 2 | 12 | 1 | 4 |
| `/admin/[slug]/audit/financial` | ✅ 200 | 4 | 12 | 0 | 0 |
| `/admin/[slug]/counter` | ✅ 200 | 2 | 12 | 0 | 0 |
| `/admin/[slug]/dashboard` | ✅ 200 | 6 | 12 | 0 | 0 |
| `/admin/[slug]/dashboard/history` | ✅ 200 | 14 | 12 | 0 | 0 |
| `/admin/[slug]/delivery` | ✅ 200 | 3 | 12 | 0 | 0 |
| `/admin/[slug]/driver` | ✅ 200 | 6 | 12 | 0 | 0 |
| `/admin/[slug]/expeditor` | ✅ 200 | 2 | 12 | 0 | 0 |
| `/admin/[slug]/franchise` | ✅ 200 | 2 | 13 | 0 | 0 |
| `/admin/[slug]/history` | ✅ 200 | 24 | 12 | 0 | 0 |
| `/admin/[slug]/inventory` | ✅ 200 | 7 | 12 | 1 | 0 |
| `/admin/[slug]/kitchen` | ✅ 200 | 2 | 12 | 0 | 0 |
| `/admin/[slug]/marketing` | ✅ 200 | 5 | 13 | 1 | 0 |
| `/admin/[slug]/menu` | ✅ 200 | 24 | 13 | 1 | 0 |
| `/admin/[slug]/profile` | ✅ 200 | 3 | 12 | 3 | 0 |
| `/admin/[slug]/settings` | ✅ 200 | 40 | 12 | 11 | 0 |
| `/admin/[slug]/settings/billing` | ✅ 200 | 5 | 12 | 0 | 0 |
| `/admin/[slug]/settings/features` | ⚠️ 200 | 4 | 1 | 0 | 20 |
| `/admin/[slug]/tables` | ⚠️ 200 | 3 | 12 | 0 | 3 |
| `/admin/[slug]/team` | ✅ 200 | 8 | 12 | 1 | 0 |
| `/admin/[slug]/waiter` | ⚠️ 200 | 8 | 15 | 1 | 2 |
| `/admin/[slug]/waiter/orders` | ✅ 200 | 2 | 15 | 1 | 0 |
| `/admin/[slug]/waiter/pos/[tableId]` | ✅ 200 | 11 | 12 | 3 | 0 |
| `/admin/[slug]/waiter/pos/quick` | ✅ 200 | 9 | 12 | 2 | 0 |
| `/admin/forgot-password` | ✅ 200 | 1 | 1 | 1 | 0 |
| `/admin/login` | ✅ 200 | 2 | 3 | 2 | 0 |
| `/admin/payment/callback` | ✅ 200 | 1 | 0 | 0 | 0 |
| `/admin/register` | ✅ 200 | 2 | 2 | 6 | 0 |
| `/admin/reset-password` | ✅ 200 | 0 | 0 | 0 | 0 |
| `/admin/support` | ✅ 200 | 2 | 0 | 2 | 0 |
| `/offline` | ✅ 200 | 1 | 0 | 0 | 0 |
| `/trust` | ✅ 200 | 0 | 7 | 0 | 0 |
| `/trust/security` | ✅ 200 | 0 | 7 | 0 | 0 |
| `/trust/status` | ✅ 200 | 0 | 5 | 0 | 0 |

## 2. Detalhamento de Anomalias
### 🚩 /[slug]/monitor
```text
- HTTP 404: http://127.0.0.1:8000/api/hamburgueria-ze/monitor
- CONSOLE: Failed to load resource: the server responded with a status of 404 (Not Found)
- CONSOLE: Erro ao carregar monitor: Error: Falha ao carregar monitor
    at getPublicMonitorOrders (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:175:24)
    at async eval (webpack-internal:///(app-pages-browser)/./src/components/menu/PublicMonitorView.tsx:32:26)
```
### 🚩 /admin/[slug]/audit
```text
- HTTP 401: http://127.0.0.1:8000/api/admin/company/me
- CONSOLE: Failed to load resource: the server responded with a status of 401 (Unauthorized)
- HTTP 401: http://127.0.0.1:8000/api/admin/audit?limit=50
- CONSOLE: Failed to load resource: the server responded with a status of 401 (Unauthorized)
```
### 🚩 /admin/[slug]/settings/features
```text
- CONSOLE: Warning: Cannot update a component (`%s`) while rendering a different component (`%s`). To locate the bad setState() call inside `%s`, follow the stack trace as described in https://reactjs.org/link/setstate-in-render%s HotReload FeaturesBetaPage FeaturesBetaPage 
    at FeaturesBetaPage (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/settings/features/page.tsx:41:136)
    at ClientPageRoot (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/client-page.js:14:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at main
    at MotionComponent (webpack-internal:///(app-pages-browser)/./node_modules/framer-motion/dist/es/motion/index.mjs:54:65)
    at PresenceChild (webpack-internal:///(app-pages-browser)/./node_modules/framer-motion/dist/es/components/AnimatePresence/PresenceChild.mjs:18:11)
    at AnimatePresence (webpack-internal:///(app-pages-browser)/./node_modules/framer-motion/dist/es/components/AnimatePresence/index.mjs:55:11)
    at div
    at WebSocketProvider (webpack-internal:///(app-pages-browser)/./src/context/WebSocketContext.tsx:15:11)
    at AdminLayout (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/layout.tsx:51:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:76:9)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at CartProvider (webpack-internal:///(app-pages-browser)/./src/context/CartContext.tsx:14:11)
    at LanguageProvider (webpack-internal:///(app-pages-browser)/./src/context/LanguageContext.tsx:16:11)
    at f (webpack-internal:///(app-pages-browser)/./node_modules/next-themes/dist/index.module.js:8:597)
    at $ (webpack-internal:///(app-pages-browser)/./node_modules/next-themes/dist/index.module.js:8:348)
    at Providers (webpack-internal:///(app-pages-browser)/./src/components/Providers.tsx:14:11)
    at body
    at html
    at RootLayout (Server)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:76:9)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at DevRootNotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/dev-root-not-found-boundary.js:33:11)
    at ReactDevOverlay (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/react-dev-overlay/app/ReactDevOverlay.js:87:9)
    at HotReload (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/react-dev-overlay/app/hot-reloader-client.js:321:11)
    at Router (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/app-router.js:207:11)
    at ErrorBoundaryHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:113:9)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at AppRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/app-router.js:585:13)
    at ServerRoot (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/app-index.js:112:27)
    at Root (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/app-index.js:117:11)
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CRASH: useFeatureFlags deve ser usado dentro de FeatureFlagProvider
- CONSOLE: The above error occurred in the <NotFoundErrorBoundary> component:

    at FeaturesBetaPage (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/settings/features/page.tsx:41:136)
    at ClientPageRoot (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/client-page.js:14:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at main
    at MotionComponent (webpack-internal:///(app-pages-browser)/./node_modules/framer-motion/dist/es/motion/index.mjs:54:65)
    at PresenceChild (webpack-internal:///(app-pages-browser)/./node_modules/framer-motion/dist/es/components/AnimatePresence/PresenceChild.mjs:18:11)
    at AnimatePresence (webpack-internal:///(app-pages-browser)/./node_modules/framer-motion/dist/es/components/AnimatePresence/index.mjs:55:11)
    at div
    at WebSocketProvider (webpack-internal:///(app-pages-browser)/./src/context/WebSocketContext.tsx:15:11)
    at AdminLayout (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/layout.tsx:51:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:243:11)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:76:9)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at LoadingBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:349:11)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at InnerScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:153:9)
    at ScrollAndFocusHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:228:11)
    at RenderFromTemplateContext (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/render-from-template-context.js:16:44)
    at OuterLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:370:11)
    at CartProvider (webpack-internal:///(app-pages-browser)/./src/context/CartContext.tsx:14:11)
    at LanguageProvider (webpack-internal:///(app-pages-browser)/./src/context/LanguageContext.tsx:16:11)
    at f (webpack-internal:///(app-pages-browser)/./node_modules/next-themes/dist/index.module.js:8:597)
    at $ (webpack-internal:///(app-pages-browser)/./node_modules/next-themes/dist/index.module.js:8:348)
    at Providers (webpack-internal:///(app-pages-browser)/./src/components/Providers.tsx:14:11)
    at body
    at html
    at RootLayout (Server)
    at RedirectErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:74:9)
    at RedirectBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/redirect-boundary.js:82:11)
    at NotFoundErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:76:9)
    at NotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/not-found-boundary.js:84:11)
    at DevRootNotFoundBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/dev-root-not-found-boundary.js:33:11)
    at ReactDevOverlay (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/react-dev-overlay/app/ReactDevOverlay.js:87:9)
    at HotReload (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/react-dev-overlay/app/hot-reloader-client.js:321:11)
    at Router (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/app-router.js:207:11)
    at ErrorBoundaryHandler (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:113:9)
    at ErrorBoundary (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/error-boundary.js:160:11)
    at AppRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/app-router.js:585:13)
    at ServerRoot (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/app-index.js:112:27)
    at Root (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/app-index.js:117:11)

React will try to recreate this component tree from scratch using the error boundary you provided, ReactDevOverlay.
```
### 🚩 /admin/[slug]/tables
```text
- HTTP 404: http://127.0.0.1:8000/api/admin/tables/dashboard
- CONSOLE: Failed to load resource: the server responded with a status of 404 (Not Found)
- CONSOLE: [TablesPage] Fetch Error: ApiError: Not Found
    at fetchClient (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:154:15)
    at async getTablesDashboard (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:477:17)
    at async eval (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/tables/page.tsx:54:26)
```
### 🚩 /admin/[slug]/waiter
```text
- HTTP 404: http://127.0.0.1:8000/api/admin/tables/dashboard
- CONSOLE: Failed to load resource: the server responded with a status of 404 (Not Found)
```
 