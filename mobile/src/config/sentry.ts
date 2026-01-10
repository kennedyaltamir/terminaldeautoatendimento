import * as Sentry from '@sentry/react-native';

/**
 * Inicializa o Sentry para captura de erros nativos e JS.
 * A inicialização é condicional para evitar ruído em ambiente de desenvolvimento,
 * a menos que explicitamente forçada.
 */
export const initSentry = () => {
  const dsn = process.env.EXPO_PUBLIC_SENTRY_DSN;
  const isDev = __DEV__;

  // Em produção, o DSN é obrigatório. Em dev, é opcional.
  if (dsn && (!isDev || process.env.EXPO_PUBLIC_FORCE_SENTRY === 'true')) {
    Sentry.init({
      dsn: dsn,
      debug: isDev, // Debug apenas em dev
      tracesSampleRate: 1.0, // Ajustar para produção (ex: 0.2)
      _experiments: {
        profilesSampleRate: 1.0,
      },
    });
    console.log('[Sentry] Inicializado com sucesso.');
  } else {
    console.log('[Sentry] Inicialização pulada (Ambiente Dev ou DSN ausente).');
  }
};
