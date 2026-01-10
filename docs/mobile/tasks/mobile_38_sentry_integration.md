# DOMAIN: MOBILE
# 📱 Task 38: Integração Nativa com Sentry (Observabilidade)

## 1. Contexto
Implementação da camada de telemetria para captura de erros em produção. O objetivo é garantir que falhas silenciosas (crashes nativos ou exceções JS não tratadas) sejam reportadas para a equipe de engenharia.

## 2. Decisões Técnicas
- **SDK Híbrido:** Utilização do `@sentry/react-native` que captura tanto erros da camada JavaScript quanto sinais de falha nativa (SIGSEGV, ANR) no Android/iOS.
- **Logger Proxy:** O `LoggerService` foi promovido a um proxy inteligente. Além de imprimir no console (Logcat), ele agora despacha eventos de nível `WARN` e `ERROR` para o Sentry, incluindo breadcrumbs para contexto.
- **Configuração Condicional:** O Sentry só é inicializado se a variável `EXPO_PUBLIC_SENTRY_DSN` estiver presente e (por padrão) se não estiver em modo `__DEV__`. Isso evita poluição de cotas durante o desenvolvimento local.
- **ADB Bridge:** Criação de uma ferramenta de diagnóstico (`mobile_diagnostics.py`) que permite visualizar os logs estruturados do aplicativo em tempo real no terminal, filtrando o ruído do Logcat padrão.

## 3. Arquivos Afetados
- `mobile/package.json` (Dependência)
- `mobile/app.json` (Plugin Expo)
- `mobile/src/config/sentry.ts` (Inicialização)
- `mobile/App.tsx` (Wrap)
- `mobile/src/services/logger.service.ts` (Integração)
- `scripts/functional/mobile_diagnostics.py` (Ferramenta)

## 4. Próximos Passos
- Validar a captura de erros forçando uma exceção controlada.
- Configurar o upload de Source Maps no EAS Build para desofuscar stack traces.

---
*Fase 12 — Janeiro de 2026*
