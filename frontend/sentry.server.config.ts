import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  
  // Amostragem de performance no servidor
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,

  // Ambiente
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT || "production",
});