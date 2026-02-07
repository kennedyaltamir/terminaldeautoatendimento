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
  
  // Callbacks mantidos para reconexão
  _onEvent: null as ((data: RealtimeEvent) => void) | null,
  _onReconnect: null as (() => void) | null,

  connect(
    slug: string, 
    token: string, 
    onEvent: (data: RealtimeEvent) => void, 
    onReconnect?: () => void
  ) {
    this.currentSlug = slug;
    this.currentToken = token;
    this._onEvent = onEvent;
    this._onReconnect = onReconnect;

    if (this.socket) {
      logger.info(TAG, 'Fechando conexão anterior para reconectar...');
      this.socket.close(1000, "Reconnecting");
    }

    const url = `${ENV.WS_URL}/${slug}?token=${token}`;
    logger.info(TAG, `Iniciando conexão WebSocket para ${slug}`);

    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      logger.info(TAG, 'Conexão estabelecida com sucesso (OPEN).');
      useOrdersStore.getState().setSocketStatus(true);
      
      // Se houve falha anterior, significa que é uma reconexão
      if (ReconnectPolicy.retryCount > 0 && this._onReconnect) {
        logger.info(TAG, 'Reconexão detectada. Disparando sincronização...');
        this._onReconnect();
      }
      
      ReconnectPolicy.reset();
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as RealtimeEvent;
        logger.debug(TAG, `Evento recebido: ${data.type}`, data);
        if (this._onEvent) this._onEvent(data);
      } catch (e) {
        logger.error(TAG, 'Falha ao processar mensagem do socket', e);
      }
    };

    this.socket.onclose = (event) => {
      logger.warn(TAG, `Conexão encerrada. Código: ${event.code}, Razão: ${event.reason}`);
      useOrdersStore.getState().setSocketStatus(false);

      // Código 1000 = Fechamento normal (logout ou sair da tela)
      if (event.code !== 1000 && ReconnectPolicy.canRetry) {
        const delay = ReconnectPolicy.getNextDelay();
        if (delay) {
          logger.info(TAG, `Agendando reconexão em ${delay}ms...`);
          setTimeout(() => {
            if (this.currentSlug && this.currentToken && this._onEvent) {
              this.connect(this.currentSlug, this.currentToken, this._onEvent, this._onReconnect);
            }
          }, delay);
        }
      }
    };

    this.socket.onerror = (error) => {
      logger.error(TAG, 'Erro crítico no WebSocket', error);
      // O onError geralmente é seguido pelo onClose, onde a reconexão acontece
    };
  },

  disconnect() {
    if (this.socket) {
      logger.info(TAG, 'Desconectando WebSocket voluntariamente.');
      this.socket.close(1000, "Normal Closure");
      this.socket = null;
    }
    this.currentSlug = null;
    this.currentToken = null;
    this._onEvent = null;
    this._onReconnect = null;
    useOrdersStore.getState().setSocketStatus(false);
  }
};
