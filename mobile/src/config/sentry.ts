
import * as Sentry from '@sentry/react-native';

/**
 * Inicializa o Sentry para captura de erros nativos e JS.
 * O DSN deve ser injetado via variável de ambiente EXPO_PUBLIC_SENTRY_DSN.
 */
export const initSentry = () => {
  const dsn = process.env.EXPO_PUBLIC_SENTRY_DSN;
  
  if (dsn) {
    Sentry.init({
      dsn: dsn,
      debug: __DEV__,
      environment: process.env.EXPO_PUBLIC_ENV || 'production',
      tracesSampleRate: 1.0,
    });
    console.log('[Sentry] Telemetria ativa.');
  } else {
    console.warn('[Sentry] DSN ausente. Telemetria desativada.');
  }
};

