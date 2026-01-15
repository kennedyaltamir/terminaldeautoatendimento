# 🕵️ Relatório de Comportamento de UI (L6 - Full Coverage)
**Data:** 2026-01-15T04:52:10.982004

## 1. Resumo dos Cenários
| Cenário | Status | Passos |
| :--- | :---: | :--- |
| 1. Login Admin | ✅ PASS | 3 |
| 2. Onboarding & Dashboard | ✅ PASS | 4 |
| 3. Gestão de Cardápio | ❌ FAIL | 0 |
| 4. Gestão de Mesas | ✅ PASS | 0 |
| 5. KDS (Cozinha) | ❌ FAIL | 0 |
| 6. Garçom (POS) | ❌ FAIL | 1 |
| 7. Estoque | ❌ FAIL | 1 |
| 8. Configurações | ✅ PASS | 2 |
| 9. Menu Público (Cliente) | ❌ FAIL | 0 |

## 2. Erros Capturados
```text
CONSOLE: Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/dashboard. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:58:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:33:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:150:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:56:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:66:9)
SCENARIO 3. Gestão de Cardápio: Elemento não visível: button:has-text('Criar Categoria')
HTTP 404: http://127.0.0.1:8000/api/admin/tables/dashboard
CONSOLE: Failed to load resource: the server responded with a status of 404 (Not Found)
CONSOLE: [TablesPage] Fetch Error: ApiError: Not Found
    at fetchClient (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:154:15)
    at async getTablesDashboard (webpack-internal:///(app-pages-browser)/./src/lib/api.ts:477:17)
    at async eval (webpack-internal:///(app-pages-browser)/./src/app/admin/[slug]/tables/page.tsx:54:26)
SCENARIO 5. KDS (Cozinha): Elemento não visível: button[title='Tela Cheia']
HTTP 404: http://127.0.0.1:8000/api/admin/tables/dashboard
CONSOLE: Failed to load resource: the server responded with a status of 404 (Not Found)
SCENARIO 6. Garçom (POS): Elemento não visível: button:has-text('Ocupada')
SCENARIO 7. Estoque: Elemento não visível: button:has-text('Cancelar')
SCENARIO 9. Menu Público (Cliente): Elemento não visível: div[role='button']:has-text('X-Bacon')
```

## 3. Detalhamento
### 1. Login Admin
- ✅ input[name='email']
- ✅ input[name='password']
- ✅ button[type='submit']

### 2. Onboarding & Dashboard
- ✅ text=Faturamento
- ✅ text=Ticket Médio
- ✅ Filtro Hoje
- ✅ Filtro 7 Dias

### 3. Gestão de Cardápio
> 🚨 **Erro:** Elemento não visível: button:has-text('Criar Categoria')


### 4. Gestão de Mesas

### 5. KDS (Cozinha)
> 🚨 **Erro:** Elemento não visível: button[title='Tela Cheia']


### 6. Garçom (POS)
> 🚨 **Erro:** Elemento não visível: button:has-text('Ocupada')

- ✅ Filtro Livre

### 7. Estoque
> 🚨 **Erro:** Elemento não visível: button:has-text('Cancelar')

- ✅ button:has-text('Novo Ingrediente')

### 8. Configurações
- ✅ input[name='name']
- ✅ button:has-text('Salvar Alterações')

### 9. Menu Público (Cliente)
> 🚨 **Erro:** Elemento não visível: div[role='button']:has-text('X-Bacon')


