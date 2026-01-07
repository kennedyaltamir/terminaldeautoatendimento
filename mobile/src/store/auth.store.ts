import { create } from 'zustand';
import { AuthState, AuthErrorType } from '../types/auth.types';
import { SecureAuthStorage } from '../services/auth/storage';
import { AuthClient } from '../services/auth/client';
import { JwtService } from '../services/auth/jwt';
import { NotificationsService } from '../services/notifications.service';
import { logger } from '../services/logger.service';

/**
 * useAuthStore: Gerencia a validade da sessão e o registro de dispositivos.
 * Evoluído na Missão 31 para integrar Push Notifications.
 */

const TAG = 'AuthStore';

interface ExtendedAuthState extends AuthState {
  accessToken: string | null;
  fcmToken: string | null;
  setupNotifications: () => Promise<void>;
}

export const useAuthStore = create<ExtendedAuthState>((set, get) => ({
  status: 'idle',
  user: null,
  error: null,
  accessToken: null,
  fcmToken: null,

  hydrate: async () => {
    if (get().status !== 'idle') return;
    set({ status: 'hydrating' });

    try {
      const accessToken = await SecureAuthStorage.getAccessToken();
      const refreshToken = await SecureAuthStorage.getRefreshToken();

      if (!accessToken || !refreshToken) {
        set({ status: 'unauthenticated', accessToken: null });
        return;
      }

      set({ status: 'checking_expiry' });
      const isExpired = JwtService.isTokenExpired(accessToken);

      if (!isExpired) {
        set({ status: 'authenticated', accessToken });
        get().setupNotifications();
        return;
      }

      try {
        const data = await AuthClient.refresh(refreshToken);
        await SecureAuthStorage.saveTokens({
          accessToken: data.access_token,
          refreshToken: data.refresh_token,
        });
        set({ status: 'authenticated', accessToken: data.access_token });
        get().setupNotifications();
      } catch {
        await SecureAuthStorage.clear();
        set({ status: 'unauthenticated', accessToken: null });
      }
    } catch (e) {
      set({ status: 'unauthenticated', accessToken: null });
    }
  },

  login: async (credentials) => {
    set({ status: 'hydrating', error: null });
    try {
      const data = await AuthClient.login(credentials);
      await SecureAuthStorage.saveTokens({
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
      });
      set({ status: 'authenticated', accessToken: data.access_token, error: null });
      get().setupNotifications();
    } catch (error: any) {
      set({ 
        status: 'unauthenticated', 
        accessToken: null,
        error: { 
          type: AuthErrorType.INVALID_CREDENTIALS, 
          message: error.response?.data?.detail || 'Credenciais inválidas' 
        } 
      });
      throw error;
    }
  },

  setupNotifications: async () => {
    try {
      const token = await NotificationsService.registerForPushNotifications();
      if (token) {
        set({ fcmToken: token });
        await NotificationsService.syncTokenWithBackend(token);
      }
    } catch (e) {
      logger.error(TAG, 'Erro no setup de notificações', e);
    }
  },

  logout: async () => {
    const { fcmToken } = get();
    if (fcmToken) {
      await NotificationsService.unregisterDevice(fcmToken);
    }
    await SecureAuthStorage.clear();
    set({ status: 'unauthenticated', user: null, accessToken: null, fcmToken: null, error: null });
    logger.info(TAG, 'Sessão encerrada e dispositivo desvinculado.');
  },
}));
