# 🚨 Relatório de Incidente: Falha de Execução em Decoradores Híbridos

**Data:** 10 de Janeiro de 2026  
**Severidade:** ALTA (Crash de API)  
**Status:** RESOLVIDO

## 1. Diagnóstico da Causa Raiz

### 1.1. TypeError: object dict can't be used in 'await'
O erro ocorreu no arquivo `app/core/cache.py`. O decorador `@cache_response` estava tentando usar a palavra-chave `await` em uma função que, embora estivesse sendo tratada como assíncrona pelo sistema de tipos, retornava um dicionário síncrono (devido ao wrapping do `slowapi`).
- **Correção:** Alterada a lógica do decorador para utilizar `inspect.isawaitable()`. Agora o sistema executa a função e, somente se o retorno for uma promessa (corrotina), ele aplica o `await`. Isso garante compatibilidade total com funções `def` e `async def`.

### 1.2. Loop de Sincronização Offline (Mesa Fechada)
O Frontend estava tentando sincronizar pedidos de mesas que já haviam sido fechadas no servidor, resultando em erro 400 persistente.
- **Correção:** 
    1. Atualizado o hook `useOfflineSync.ts` para identificar erros de regra de negócio (400) e marcar o pedido como `error` imediatamente, interrompendo a tentativa automática.
    2. Adicionada funcionalidade de "Limpar Fila" no componente `NetworkStatus.tsx` para permitir que o usuário descarte pedidos que não podem mais ser processados.

## 2. Ações Realizadas
1.  Refatoração do `CacheService` para suporte a chamadas híbridas.
2.  Implementação de gestão de erros granulares na fila offline.
3.  Adição de controles de manutenção de banco local na UI.
