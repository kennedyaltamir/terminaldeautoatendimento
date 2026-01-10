import { OrdersService } from './orders.service';
import { useOrdersStore } from '../store/orders.store';
import { logger } from './logger.service';

const TAG = 'SyncService';

export const OrdersSyncService = {
  /**
   * Realiza uma sincronização completa dos pedidos.
   * Usado na inicialização e após reconexão do WebSocket.
   */
  async performFullSync(slug: string) {
    const store = useOrdersStore.getState();
    store.setSyncing(true);

    logger.info(TAG, `Iniciando Full Sync para ${slug}`);

    try {
      const orders = await OrdersService.getActiveOrders(slug);
      store.setOrders(orders);
      store.updateSLAs(Date.now());
      logger.info(TAG, `Sincronização concluída. ${orders.length} pedidos carregados.`);
      return true;
    } catch (e) {
      logger.error(TAG, 'Falha catastrófica no Full Sync', e);
      return false;
    } finally {
      // Pequeno delay para evitar flicker na UI
      setTimeout(() => store.setSyncing(false), 500);
    }
  },

  /**
   * Busca um pedido específico para adicionar ou atualizar na lista.
   * Usado quando chega um evento 'new_order' via socket.
   */
  async fetchAndAddOrder(slug: string, orderId: string) {
    logger.debug(TAG, `Buscando detalhes do novo pedido: ${orderId}`);
    try {
      // Nota: Idealmente teríamos um endpoint GET /orders/:id, mas usamos a lista por enquanto
      // para garantir consistência com o filtro de KDS do backend.
      const orders = await OrdersService.getActiveOrders(slug);
      const target = orders.find((o: any) => o.id === orderId);

      if (target) {
        useOrdersStore.getState().addOrUpdateOrder(target);
        logger.info(TAG, `Pedido ${orderId} injetado na lista.`);
      } else {
        logger.warn(TAG, `Pedido ${orderId} não encontrado no fetch de segurança.`);
      }
    } catch (e) {
      logger.error(TAG, `Erro ao sincronizar pedido individual ${orderId}`, e);
    }
  }
};
