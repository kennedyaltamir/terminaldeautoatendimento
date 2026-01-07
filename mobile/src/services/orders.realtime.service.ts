import { ENV } from '../config/env';
import { RealtimeEvent } from '../types/realtime.events';
import { ReconnectPolicy } from './realtime.reconnect.policy';
import { useOrdersStore } from '../store/orders.store';
import { logger } from './logger.service';

const TAG = 'RealtimeService';

export const OrdersRealtimeService = {
  socket: null as WebSocket | null,
  currentSlug: null as string | null,
  currentToken: null as string | null,

  connect(slug: string, token: string, onEvent: (data: RealtimeEvent) => void, onReconnect?: () => void) {
    this.currentSlug = slug;
    this.currentToken = token;

    if (this.socket) {
      this.socket.close(1000, "Reconnecting");
    }

    const url = `${ENV.WS_URL}/${slug}?token=${token}`;
    logger.info(TAG, `Iniciando conexão WebSocket para ${slug}`);
    
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      logger.info(TAG, 'Conexão estabelecida com sucesso.');
      useOrdersStore.getState().setSocketStatus(true);
      ReconnectPolicy.reset();
      if (onReconnect) onReconnect();
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as RealtimeEvent;
        logger.debug(TAG, `Evento recebido: ${data.type}`, data);
        onEvent(data);
      } catch (e) {
        logger.error(TAG, 'Falha ao processar mensagem do socket', e);
      }
    };

    this.socket.onclose = (event) => {
      logger.warn(TAG, `Conexão encerrada. Código: ${event.code}, Razão: ${event.reason}`);
      useOrdersStore.getState().setSocketStatus(false);
      
      if (event.code !== 1000 && ReconnectPolicy.canRetry) {
        const delay = ReconnectPolicy.getNextDelay();
        if (delay) {
          logger.info(TAG, `Agendando reconexão em ${delay}ms...`);
          setTimeout(() => {
            this.connect(slug, token, onEvent, onReconnect);
          }, delay);
        }
      }
    };

    this.socket.onerror = (error) => {
      logger.error(TAG, 'Erro crítico no WebSocket', error);
      useOrdersStore.getState().setSocketStatus(false);
      try {
        this.socket?.close();
      } catch (e) {}
    };
  },

  disconnect() {
    if (this.socket) {
      logger.info(TAG, 'Desconectando WebSocket voluntariamente.');
      this.socket.close(1000, "Normal Closure");
      this.socket = null;
    }
    useOrdersStore.getState().setSocketStatus(false);
  }
};
