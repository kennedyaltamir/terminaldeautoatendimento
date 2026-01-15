
import axios, { AxiosError } from 'axios';
import { ENV } from '../config/env';
import { useAuthStore } from '../store/auth.store';

export const api = axios.create({
  baseURL: ENV.API_URL,
  timeout: 10000,
});

// 🛡️ L6 QA SHIELD: Intercepta chamadas e injeta Mocks se o backend estiver offline ou em modo QA
api.interceptors.request.use(async (config) => {
  const isQaMode = useAuthStore.getState().isQaMode;
  
  if (isQaMode) {
    config.adapter = async (cfg) => {
      console.log(`[L6_QA_SHIELD] Mocking: ${cfg.method?.toUpperCase()} ${cfg.url}`);
      return {
        data: getMockData(cfg.url || ''),
        status: 200,
        statusText: 'OK',
        headers: {},
        config: cfg,
      };
    };
  }
  return config;
});

const getMockData = (url: string) => {
  if (url.includes('/tables/dashboard')) {
    return [
      { id: 1, table_number: 1, status: 'free', active_session: null },
      { id: 2, table_number: 2, status: 'occupied', active_session: { customer_name: 'QA L6 User', total_spent: 150.00 } }
    ];
  }
  return {};
};

export default api;

