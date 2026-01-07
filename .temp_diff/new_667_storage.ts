import * as SecureStore from 'expo-secure-store';
import { AuthTokens } from '../../types/auth';

/**
 * AuthStoragePort: Contrato para persistência de credenciais.
 */
export interface AuthStoragePort {
  saveTokens(tokens: AuthTokens): Promise<void>;
  getAccessToken(): Promise<string | null>;
  getRefreshToken(): Promise<string | null>;
  clear(): Promise<void>;
}

/**
 * SecureAuthStorage: Implementação utilizando hardware-backed storage.
 * CORREÇÃO MISSÃO 14A: Chaves normalizadas para conformidade com Android/iOS.
 * Proibido usar ":" ou "@".
 */
const KEYS = {
  ACCESS: 'mesaflow_access_token',
  REFRESH: 'mesaflow_refresh_token',
};

export const SecureAuthStorage: AuthStoragePort = {
  async saveTokens(tokens: AuthTokens): Promise<void> {
    await SecureStore.setItemAsync(KEYS.ACCESS, tokens.accessToken);
    await SecureStore.setItemAsync(KEYS.REFRESH, tokens.refreshToken);
  },

  async getAccessToken(): Promise<string | null> {
    return await SecureStore.getItemAsync(KEYS.ACCESS);
  },

  async getRefreshToken(): Promise<string | null> {
    return await SecureStore.getItemAsync(KEYS.REFRESH);
  },

  async clear(): Promise<void> {
    await SecureStore.deleteItemAsync(KEYS.ACCESS);
    await SecureStore.deleteItemAsync(KEYS.REFRESH);
  }
};
