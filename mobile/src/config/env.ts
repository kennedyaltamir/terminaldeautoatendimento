
/**
 * MESAFLOW NATIVE - ENVIRONMENT CONFIGURATION
 * Domain: MOBILE / INFRA
 * Security Level: HIGH
 */

// Variáveis injetadas pelo Expo (EAS Build ou .env local)
const RAW_API_URL = process.env.EXPO_PUBLIC_API_URL;
const RAW_WS_URL = process.env.EXPO_PUBLIC_WS_URL;
const RAW_ENV = process.env.EXPO_PUBLIC_ENV;

// Validação de Produção
const isProduction = !__DEV__ || RAW_ENV === 'production';

// Hard Gate: Em produção, variáveis são obrigatórias.
if (isProduction) {
  if (!RAW_API_URL || !RAW_WS_URL) {
    throw new Error(
      '[FATAL] Variáveis de ambiente críticas ausentes em produção. ' +
      'Verifique EXPO_PUBLIC_API_URL e EXPO_PUBLIC_WS_URL no EAS.'
    );
  }
  
  // Bloqueio de HTTP em Produção (Compliance Google Play / App Store)
  if (RAW_API_URL.startsWith('http://') || RAW_WS_URL.startsWith('ws://')) {
    throw new Error(
      '[SECURITY] Uso de protocolo inseguro (HTTP/WS) detectado em produção. ' +
      'Obrigatório uso de HTTPS/WSS.'
    );
  }
}

// Fallback Seguro (Apenas Desenvolvimento)
const getDevFallback = (key: string, value: string | undefined, fallback: string) => {
  if (value) return value;
  if (__DEV__) {
    console.warn(`[ENV] Variável ${key} não definida. Usando fallback de desenvolvimento: ${fallback}`);
    return fallback;
  }
  return ''; // Retorna vazio em prod para falhar graciosamente ou ser pego pelo check acima
};

export const ENV = {
  API_URL: getDevFallback('EXPO_PUBLIC_API_URL', RAW_API_URL, 'http://localhost:8000/api'),
  WS_URL: getDevFallback('EXPO_PUBLIC_WS_URL', RAW_WS_URL, 'ws://localhost:8000/ws'),
  ENVIRONMENT: RAW_ENV || 'development',
  VERSION: '1.0.0', // Sincronizar com app.json via script de build se necessário
  
  // Feature Flags de Ambiente
  ENABLE_LOGS: __DEV__ || process.env.EXPO_PUBLIC_ENABLE_LOGS === 'true',
};

// Log de Inicialização (Sanitizado)
if (__DEV__) {
  console.log('[ENV] Configuração carregada:', {
    env: ENV.ENVIRONMENT,
    api: ENV.API_URL,
    ws: ENV.WS_URL
  });
}

