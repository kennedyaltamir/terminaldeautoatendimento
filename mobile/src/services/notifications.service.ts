import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';
import { api } from './api';
import { logger } from './logger.service';

/**
 * NotificationsService: Gerencia o ciclo de vida de Push Notifications.
 * Integra o hardware do dispositivo com o serviço de mensageria do MesaFlow.
 */

const TAG = 'NotificationsService';

// Configuração de comportamento das notificações em primeiro plano
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export const NotificationsService = {
  /**
   * Solicita permissão e obtém o token FCM do dispositivo.
   */
  async registerForPushNotifications(): Promise<string | null> {
    try {
      const { status: existingStatus } = await Notifications.getPermissionsAsync();
      let finalStatus = existingStatus;

      if (existingStatus !== 'granted') {
        const { status } = await Notifications.requestPermissionsAsync();
        finalStatus = status;
      }

      if (finalStatus !== 'granted') {
        logger.warn(TAG, 'Permissão de notificação negada pelo usuário.');
        return null;
      }

      // Obtém o token para o projeto Expo
      const token = (await Notifications.getExpoPushTokenAsync()).data;
      logger.info(TAG, 'Token de notificação gerado com sucesso.');
      
      return token;
    } catch (e) {
      logger.error(TAG, 'Falha ao configurar notificações push', e);
      return null;
    }
  },

  /**
   * Envia o token para o backend MesaFlow para vincular ao usuário.
   */
  async syncTokenWithBackend(token: string) {
    try {
      await api.post('/auth/device', {
        fcm_token: token,
        device_name: `${Platform.OS} - ${Platform.Version}`,
        platform: Platform.OS
      });
      logger.info(TAG, 'Dispositivo registrado no backend MesaFlow.');
    } catch (e) {
      logger.error(TAG, 'Erro ao sincronizar token com backend', e);
    }
  },

  /**
   * Remove o token do backend (chamado no logout).
   */
  async unregisterDevice(token: string) {
    try {
      await api.delete(`/auth/device/${token}`);
      logger.info(TAG, 'Dispositivo removido do backend.');
    } catch (e) {
      logger.error(TAG, 'Erro ao remover dispositivo do backend', e);
    }
  }
};
