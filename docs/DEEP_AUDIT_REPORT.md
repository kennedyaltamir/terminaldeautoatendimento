# 🛡️ Relatório de Auditoria Profunda MesaFlow

**Data:** 05/01/2026 16:37:52
**Ambiente:** http://localhost:3000

## ⚠️ 81 Inconsistências Detectadas

### `/hamburgueria-ze/menu`
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/delivery. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:300:90)
    at renderWithHooks (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:9745:28)
    at mountIndeterminateComponent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:14632:25)
    at beginWork$1 (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:15936:32)
    at beginWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:22789:28)
    at performUnitOfWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21852:24)
    at workLoopConcurrent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21840:17)
    at renderRootConcurrent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21808:25)
    at performConcurrentWorkOnRoot (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:20841:48)
    at workLoop (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:200:48)
    at flushWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:178:28)
    at MessagePort.performWorkUntilDeadline (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:416:35)
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

### `/hamburgueria-ze/kiosk`
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/delivery. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:300:90)
    at renderWithHooks (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:9745:28)
    at mountIndeterminateComponent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:14632:25)
    at beginWork$1 (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:15936:32)
    at beginWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:22789:28)
    at performUnitOfWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21852:24)
    at workLoopConcurrent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21840:17)
    at renderRootConcurrent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21808:25)
    at performConcurrentWorkOnRoot (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:20841:48)
    at workLoop (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:200:48)
    at flushWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:178:28)
    at MessagePort.performWorkUntilDeadline (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:416:35)
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

### `/admin/hamburgueria-ze/dashboard`
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/delivery. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:300:90)
    at renderWithHooks (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:9745:28)
    at mountIndeterminateComponent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:14632:25)
    at beginWork$1 (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:15936:32)
    at beginWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:22789:28)
    at performUnitOfWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21852:24)
    at workLoopConcurrent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21840:17)
    at renderRootConcurrent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21808:25)
    at performConcurrentWorkOnRoot (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:20841:48)
    at workLoop (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:200:48)
    at flushWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:178:28)
    at MessagePort.performWorkUntilDeadline (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:416:35)
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

### `/admin/hamburgueria-ze/menu`
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/delivery. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at InnerLayoutRouter (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/layout-router.js:300:90)
    at renderWithHooks (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:9745:28)
    at mountIndeterminateComponent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:14632:25)
    at beginWork$1 (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:15936:32)
    at beginWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:22789:28)
    at performUnitOfWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21852:24)
    at workLoopConcurrent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21840:17)
    at renderRootConcurrent (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:21808:25)
    at performConcurrentWorkOnRoot (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/react-dom/cjs/react-dom.development.js:20841:48)
    at workLoop (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:200:48)
    at flushWork (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:178:28)
    at MessagePort.performWorkUntilDeadline (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/compiled/scheduler/cjs/scheduler.development.js:416:35)
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

### `/admin/hamburgueria-ze/tables`
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)

### `/admin/hamburgueria-ze/inventory`
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)

### `/admin/hamburgueria-ze/marketing`
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)

### `/admin/hamburgueria-ze/team`
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)

### `/admin/hamburgueria-ze/history`
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)

### `/admin/hamburgueria-ze/settings`
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)

### `/admin/hamburgueria-ze/kitchen`
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [CONSOLE] Failed to load resource: the server responded with a status of 404 (Not Found)
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error
- [CONSOLE] Failed to fetch RSC payload for http://localhost:3000/admin/hamburgueria-ze/settings. Falling back to browser navigation. TypeError: Failed to fetch
    at fetchServerResponse (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/fetch-server-response.js:54:27)
    at fastRefreshReducerImpl (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/reducers/fast-refresh-reducer.js:29:67)
    at clientReducer (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/router-reducer/router-reducer.js:41:67)
    at Object.action (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:149:55)
    at runAction (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:47:38)
    at runRemainingActions (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:30:13)
    at handleResult (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/shared/lib/router/action-queue.js:65:9)

### `/admin/hamburgueria-ze/waiter`
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

Import trace for requested module:
./src/app/admin/[slug]/counter/page.tsx
- [NAVIGATION_FAIL] Page.goto: net::ERR_ABORTED at http://localhost:3000/admin/hamburgueria-ze/waiter
Call log:
  - navigating to "http://localhost:3000/admin/hamburgueria-ze/waiter", waiting until "domcontentloaded"

- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

### `/admin/hamburgueria-ze/counter`
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

### `/admin/hamburgueria-ze/delivery`
- [CONSOLE] Failed to load resource: the server responded with a status of 500 (Internal Server Error)
- [CRASH] Module build failed (from ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js):
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────


Caused by:
    Syntax Error
- [CONSOLE] ./src/app/admin/[slug]/counter/page.tsx
Error: 
  × Unexpected eof
     ╭─[C:\Users\Kennedy Oliveira\Desktop\terminaldeautoatendimento\frontend\src\app\admin\[slug]\counter\page.tsx:296:1]
 296 │     // O teste real de binário é complexo no E2E, validamos a intenção
 297 │   });
 298 │ });
     ╰────

Caused by:
    Syntax Error

