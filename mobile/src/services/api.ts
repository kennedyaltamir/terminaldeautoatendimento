import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { ENV } from '../config/env';
import { SecureAuthStorage } from './auth/storage';
import { AuthClient } from './auth/client';

/**
 * @file api.ts
 * @description Instância central do Axios com gerenciamento determinístico de sessão.
 */

export const api = axios.create({
  baseURL: ENV.API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) prom.reject(error);
    else prom.resolve(token);
  });
  failedQueue = [];
};

api.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    const token = await SecureAuthStorage.getAccessToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // 1. Quando o token NÃO será renovado:
    // - Se o erro não for 401.
    // - Se a requisição já for uma tentativa de retry.
    // - Se o backend estiver offline (error.response é undefined).
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      })
        .then((token) => {
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${token}`;
          }
          return api(originalRequest);
        })
        .catch((err) => Promise.reject(err));
    }

    originalRequest._retry = true;
    isRefreshing = true;

    try {
      const refreshToken = await SecureAuthStorage.getRefreshToken();
      
      // 2. Quando a sessão deve morrer sem retry:
      // - Ausência de Refresh Token no storage.
      if (!refreshToken) {
        throw new Error('Sessão inválida: Refresh Token ausente.');
      }

      const { access_token, refresh_token } = await AuthClient.refresh(refreshToken);
      
      await SecureAuthStorage.saveTokens({
        accessToken: access_token,
        refreshToken: refresh_token,
      });

      processQueue(null, access_token);
      
      if (originalRequest.headers) {
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
      }
      return api(originalRequest);

    } catch (refreshError: any) {
      // 3. Comportamento diante de Refresh Token inválido ou expirado:
      // - Limpeza total e rejeição da fila.
      processQueue(refreshError, null);
      await SecureAuthStorage.clear();
      
      // O erro é propagado para a Store, que transitará para 'unauthenticated'
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);
