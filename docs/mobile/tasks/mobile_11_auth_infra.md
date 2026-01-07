# 📱 Task 11: Infraestrutura de Autenticação Mobile

## 1. Contexto
Implementação da camada de rede e segurança para o App Mobile, focando na persistência de tokens JWT e na renovação automática (Refresh Token) com controle de concorrência.

## 2. Diagrama de Sequência: Refresh Token Lock (Implementado)
O sistema garante que apenas uma chamada de refresh seja feita, enfileirando requisições paralelas.

```text
App (Axios)              MesaFlow API
    |                         |
    |---(1) Req A (Expired)-->|
    |                         |
    |<--(2) 401 Unauthorized--|
    |                         |
    |---(3) Inicia Refresh--->| (Lock: isRefreshing = true)
    |                         |
    |---(4) Req B (Expired)-->|
    |                         |
    |<--(5) 401 Unauthorized--|
    |                         |
    |---(6) Req B aguarda ----| (Fila: failedQueue)
    |                         |
    |<--(7) Novos Tokens -----| (Unlock: isRefreshing = false)
    |                         |
    |---(8) Req A (Retry)---->| (Usa novo token)
    |---(9) Req B (Retry)---->| (Usa novo token)
```

## 3. Decisões Técnicas
- **Persistência:** `expo-secure-store` via `AuthStoragePort`.
- **Concorrência:** Fila de promessas no interceptor do Axios (`api.ts`).
- **Segurança:** Falha no refresh é um estado terminal. O storage é limpo e o erro é propagado.
- **Desacoplamento:** A infraestrutura não conhece a UI. Redirecionamentos de login devem ser tratados por Hooks de aplicação.

## 4. Arquivos Afetados
- `mobile/src/types/auth.ts`
- `mobile/src/config/env.ts`
- `mobile/src/services/auth/storage.ts`
- `mobile/src/services/api.ts`
- `mobile/src/services/auth/client.ts`
