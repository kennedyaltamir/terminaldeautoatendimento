/**
 * Configurações de ambiente para o App Mobile.
 */

const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api';

/**
 * Deriva a URL de WebSocket a partir da API_URL.
 * Substitui o protocolo e remove o sufixo /api se presente.
 */
const WS_URL = API_URL.replace('http', 'ws').replace('/api', '/ws');

export const ENV = {
  API_URL,
  WS_URL,
  IS_PROD: !__DEV__,
};

if (!API_URL) {
  console.warn('⚠️ EXPO_PUBLIC_API_URL não definida. Usando fallback localhost.');
}
