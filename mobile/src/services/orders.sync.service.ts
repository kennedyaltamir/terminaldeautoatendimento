import { OrdersService } from './orders.service';
import { useOrdersStore } from '../store/orders.store';
import { logger } from './logger.service';

const TAG = 'SyncService';

export const OrdersSyncService = {
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
      setTimeout(() => store.setSyncing(false), 500);
    }
  },

  async fetchAndAddOrder(slug: string, orderId: string) {
    logger.debug(TAG, `Buscando detalhes do novo pedido: ${orderId}`);
    try {
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
