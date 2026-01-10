// DOMAIN: MOBILE
// LAST_MODIFIED: 2026-01-10 01:55:00
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { ENV } from '../config/env';
import { SecureAuthStorage } from './auth/storage';
import { AuthClient } from './auth/client';
import { useAuthStore } from '../store/auth.store';

/**
 * Instância central do Axios com gerenciamento determinístico de sessão.
 * Implementa Fila de Espera para Refresh Token e Retries Automáticos.
 */

export const api = axios.create({
  baseURL: ENV.API_URL,
  timeout: 10000,
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

    // 1. Condições para NÃO tentar o retry:
    // - Erro não é 401 (Unauthorized)
    // - A requisição já é uma tentativa de retry (_retry: true)
    // - O backend está inacessível (sem response)
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    // 2. Se já houver um processo de refresh em andamento, enfileira esta requisição
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

    // 3. Inicia o processo de Refresh Token
    originalRequest._retry = true;
    isRefreshing = true;

    try {
      const refreshToken = await SecureAuthStorage.getRefreshToken();
      
      if (!refreshToken) {
        throw new Error('Sessão expirada: Refresh Token ausente.');
      }

      // Chama o cliente de autenticação para renovar os tokens
      const { access_token, refresh_token } = await AuthClient.refresh(refreshToken);
      
      // Persiste os novos tokens
      await SecureAuthStorage.saveTokens({
        accessToken: access_token,
        refreshToken: refresh_token,
      });

      // Libera a fila de espera com o novo token
      processQueue(null, access_token);
      
      if (originalRequest.headers) {
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
      }
      
      // Executa a requisição original novamente
      return api(originalRequest);

    } catch (refreshError: any) {
      // 4. Falha Crítica no Refresh:
      // - Limpa a fila com erro
      // - Limpa o storage local
      // - Força o logout na Store global para redirecionar a UI
      processQueue(refreshError, null);
      await SecureAuthStorage.clear();
      await useAuthStore.getState().logout();
      
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default api;
