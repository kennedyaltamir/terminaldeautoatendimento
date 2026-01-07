import { create } from 'zustand';
import { AuthState, AuthErrorType } from '../types/auth.types';
import { SecureAuthStorage } from '../services/auth/storage';
import { AuthClient } from '../services/auth/client';
import { JwtService } from '../services/auth/jwt';
import { NotificationsService } from '../services/notifications.service';
import { logger } from '../services/logger.service';

/**
 * useAuthStore: Gerencia a validade da sessão e o registro de dispositivos.
 * Atualizado na Missão 14A para endurecimento semântico e telemetria de erro.
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
      const isValid = JwtService.validateClaims(accessToken);

      if (!isExpired && isValid) {
        const claims = JwtService.getClaims(accessToken);
        set({ 
          status: 'authenticated', 
          accessToken,
          user: claims ? { email: claims.sub, role: claims.role, company_id: claims.company_id } : null
        });
        get().setupNotifications();
        return;
      }

      try {
        const data = await AuthClient.refresh(refreshToken);
        
        if (!JwtService.validateClaims(data.access_token)) {
          throw new Error('INVALID_REFRESH_TOKEN_PAYLOAD');
        }

        await SecureAuthStorage.saveTokens({
          accessToken: data.access_token,
          refreshToken: data.refresh_token,
        });

        const newClaims = JwtService.getClaims(data.access_token);
        set({ 
          status: 'authenticated', 
          accessToken: data.access_token,
          user: newClaims ? { email: newClaims.sub, role: newClaims.role, company_id: newClaims.company_id } : null
        });
        get().setupNotifications();
      } catch (e) {
        logger.error(TAG, 'Falha na revalidação da sessão. Forçando logout.', e);
        await SecureAuthStorage.clear();
        set({ status: 'unauthenticated', accessToken: null, user: null });
      }
    } catch (e) {
      set({ status: 'unauthenticated', accessToken: null });
    }
  },

  login: async (credentials) => {
    set({ status: 'hydrating', error: null });
    try {
      const data = await AuthClient.login(credentials);
      
      // Validação Semântica Imediata pós-login
      if (!JwtService.validateClaims(data.access_token)) {
        logger.error(TAG, 'Token recebido falhou na validação de claims obrigatórias.');
        throw new Error('O servidor retornou um token sem contexto operacional.');
      }

      await SecureAuthStorage.saveTokens({
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
      });

      const claims = JwtService.getClaims(data.access_token);
      set({ 
        status: 'authenticated', 
        accessToken: data.access_token, 
        user: claims ? { email: claims.sub, role: claims.role, company_id: claims.company_id } : null,
        error: null 
      });
      get().setupNotifications();
      logger.info(TAG, `Login bem sucedido: ${credentials.email}`);
    } catch (error: any) {
      // Telemetria de Erro para Logcat
      const errorMessage = error.response?.data?.detail || error.message || 'Falha na autenticação';
      logger.error(TAG, `Erro no login: ${errorMessage}`, error);

      set({ 
        status: 'unauthenticated', 
        accessToken: null,
        error: { 
          type: AuthErrorType.INVALID_CREDENTIALS, 
          message: errorMessage
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
