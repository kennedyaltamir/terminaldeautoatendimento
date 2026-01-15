# 🚨 Relatório de Incidente: Erro de Await em Funções Síncronas e CORS

**Data:** 10 de Janeiro de 2026  
**Severidade:** ALTA  
**Status:** RESOLVIDO

## 1. Diagnóstico da Causa Raiz

### 1.1. TypeError no Cache (Backend)
O erro `TypeError: object dict can't be used in 'await' expression` ocorreu porque o decorador `@cache_response` estava tentando usar `await` em funções que não eram assíncronas (como o `get_menu` em alguns contextos).
- **Correção:** O decorador agora utiliza `inspect.iscoroutinefunction` para detectar se a função original é `async` ou não, tratando ambos os casos corretamente.

### 1.2. Bloqueio de CORS (Navegador)
O navegador bloqueou as requisições do Frontend (`localhost:3000`) para o Backend (`127.0.0.1:8000`).
- **Causa:** Embora apontem para a mesma máquina, `localhost` e `127.0.0.1` são considerados origens diferentes pelo navegador.
- **Correção:** Adicionado `http://127.0.0.1:3000` à lista de origens permitidas no middleware de CORS do FastAPI.

### 1.3. Persistência de Erro de Sintaxe (Frontend)
O arquivo `api.ts` continuava apresentando erros de múltiplos pontos (`......`).
- **Causa:** Falha na lógica de substituição do script de reparo anterior.
- **Correção:** Reescrita integral do arquivo `api.ts` com a sintaxe correta e atualização do script de reparo para ser idempotente e seguro.

## 2. Ações Realizadas
1.  Atualização do `app/core/cache.py` com suporte a funções híbridas (sync/async).
2.  Expansão da lista branca de CORS em `app/main.py`.
3.  Hardenização do log de erros no `app/services/ifood_service.py`.
4.  Correção definitiva do `frontend/src/lib/api.ts`.
