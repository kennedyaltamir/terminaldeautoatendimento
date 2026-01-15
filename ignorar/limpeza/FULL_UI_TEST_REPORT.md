# 🛡️ Relatório de Teste de Interface Abrangente (UI Stress Test v2)
**Data:** 10/01/2026 18:12:15
**Duração:** 0:00:13.813119
**Total de Interações:** 29
**Total de Erros:** 4

## 📹 Evidência em Vídeo
Os vídeos da execução foram salvos em `docs/reports/videos/`.

## 🚨 Erros Críticos Encontrados
- **CONSOLE**: error: Erro de conexão com API: TypeError: Failed to fetch
    at fetchClient (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:102:26)
    at getDashboardMetrics (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:340:23)
    at fetchMetrics (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/dashboard/page.tsx:97:93)
    at eval (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/dashboard/page.tsx:112:9)
    at commitHookEffectListMount (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21102:23)
    at commitHookPassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23154:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23259:11)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23370:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23370:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23370:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23370:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23370:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23370:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23370:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
    at commitPassiveMountOnFiber (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23256:9)
    at recursivelyTraversePassiveMountEffects (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:23237:7)
- **CONSOLE**: error: Erro ao carregar métricas: ApiError: Servidor indisponível. Verifique sua conexão.
    at fetchClient (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:108:15)
    at async getDashboardMetrics (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:340:17)
    at async fetchMetrics (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/dashboard/page.tsx:97:26)
- **NETWORK**: 403 http://127.0.0.1:8000/api/admin/delivery/orders
- **CONSOLE**: error: Failed to load resource: the server responded with a status of 403 (Forbidden)

## 📝 Log de Interações
| Página | Elemento / Ação | Resultado | Detalhes |
|---|---|---|---|
| Login | `Formulário` | ✅ SUCCESS | Autenticação realizada |
| 03_Dashboard | `Dashboard` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 03_Dashboard | `7 Dias` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 03_Dashboard | `Carregamento` | ✅ SUCCESS | Página renderizada |
| 04_Menu_Admin | `1 Inputs Detectados` | ❌ INFO | Campos de formulário presentes |
| 04_Menu_Admin | `Cardápio` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 04_Menu_Admin | `Abrir` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 04_Menu_Admin | `Categoria` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 04_Menu_Admin | `Carregamento` | ✅ SUCCESS | Página renderizada |
| 05_Mesas_Admin | `Mesas` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 05_Mesas_Admin | `Nova Mesa` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 05_Mesas_Admin | `Carregamento` | ✅ SUCCESS | Página renderizada |
| 06_Estoque | `1 Inputs Detectados` | ❌ INFO | Campos de formulário presentes |
| 06_Estoque | `Estoque` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 06_Estoque | `Novo Ingrediente` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 06_Estoque | `Carregamento` | ✅ SUCCESS | Página renderizada |
| 07_Equipe | `1 Inputs Detectados` | ❌ INFO | Campos de formulário presentes |
| 07_Equipe | `Equipe` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 07_Equipe | `Adicionar Membro` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 07_Equipe | `Carregamento` | ✅ SUCCESS | Página renderizada |
| 08_Configuracoes | `11 Inputs Detectados` | ❌ INFO | Campos de formulário presentes |
| 08_Configuracoes | `Config` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 08_Configuracoes | `Salvar Alterações` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 08_Configuracoes | `Geral & Marca` | ✅ SUCCESS | Elemento interativo (Hover OK) |
| 08_Configuracoes | `Carregamento` | ✅ SUCCESS | Página renderizada |
| 09_KDS_Cozinha | `Carregamento` | ✅ SUCCESS | Página renderizada |
| 10_App_Garcom | `1 Inputs Detectados` | ❌ INFO | Campos de formulário presentes |
| 10_App_Garcom | `Carregamento` | ✅ SUCCESS | Página renderizada |
| 11_Delivery_Admin | `Carregamento` | ✅ SUCCESS | Página renderizada |
