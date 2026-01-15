
# 👁️ Guia de Telemetria Mobile (Sentry)

**Status:** OBRIGATÓRIO PARA PRODUÇÃO
**Nível:** L5 Observability

Este documento orienta a obtenção e configuração das credenciais de telemetria exigidas pela Apple e Google para aplicativos Enterprise.

## 1. Obtenção de Credenciais

1.  Acesse [sentry.io](https://sentry.io).
2.  Crie um novo projeto:
    *   **Plataforma:** React Native
    *   **Nome:** `mesaflow-mobile`
3.  Vá em **Settings > Client Keys (DSN)**.
4.  Copie o valor do DSN (ex: `https://examplePublicKey@o0.ingest.sentry.io/0`).

## 2. Configuração de Ambiente

Adicione a variável no seu arquivo `.env` local e nos Segredos do EAS (Expo Application Services).

```ini
# mobile/.env
EXPO_PUBLIC_SENTRY_DSN=https://seu-dsn-aqui@sentry.io/123456
```

## 3. Validação de Instalação

O projeto já possui as dependências configuradas:
- `@sentry/react-native`
- `expo-application`
- `expo-constants`
- `expo-device`

## 4. Checklist de Validação (Antes do Lock)

- [ ] DSN configurado no `.env`.
- [ ] `initSentry()` chamado no `App.tsx`.
- [ ] Interceptor do Axios configurado para capturar erros 4xx/5xx.
- [ ] Teste de Crash realizado (usando `CrashTester.tsx`).

## 5. Política de Privacidade (Store)

Ao usar Sentry, você deve declarar na App Store / Google Play:
- **Coleta de Dados:** Sim.
- **Tipo:** Crash Logs, Performance Data.
- **Vínculo:** Não vinculado ao usuário (se anonimizado) ou Vinculado (se enviar User ID).
- **Rastreamento:** Não (apenas diagnóstico).

---
*MesaFlow Kernel Governance*

