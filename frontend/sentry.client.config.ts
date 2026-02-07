// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 00:07:00
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  // Ajuste de amostragem para produção
  // Em dev: 100% para debug. Em prod: 10% para economizar quota.
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
  // Captura de Replay (Vídeo da sessão)
  // Apenas em caso de erro para produção
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [
    Sentry.replayIntegration({
      maskAllText: true, // Privacidade: Mascara textos
      blockAllMedia: true, // Privacidade: Bloqueia imagens
    }),
  ],
  // Ambiente
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT || "production",
});

