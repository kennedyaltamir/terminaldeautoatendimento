import { api } from './api';
import { useWaiterStore } from '../store/waiter.store';
import { useSessionStore } from '../store/session.store';
import { logger } from './logger.service';

/**
 * WaiterSyncService: Responsável por processar a fila de pedidos offline.
 */

const TAG = 'WaiterSyncService';

export const WaiterSyncService = {
  isProcessing: false,

  async processQueue() {
    if (this.isProcessing) return;
    
    const { pendingQueue, removeFromQueue } = useWaiterStore.getState();
    const { slug } = useSessionStore.getState();

    if (pendingQueue.length === 0 || !slug) return;

    this.isProcessing = true;
    logger.info(TAG, `Iniciando sincronização de ${pendingQueue.length} pedidos pendentes...`);

    for (const order of pendingQueue) {
      try {
        await api.post(`/${slug}/orders`, order.payload);
        removeFromQueue(order.id);
        logger.info(TAG, `Pedido offline ${order.id} sincronizado com sucesso.`);
      } catch (e) {
        logger.error(TAG, `Falha ao sincronizar pedido ${order.id}. Aguardando próxima janela.`, e);
        break; // Interrompe o loop se a rede ainda estiver instável
      }
    }

    this.isProcessing = false;
  }
};
