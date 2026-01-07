import { api } from './api';

/**
 * OrdersService: Consumidor de API parametrizado.
 * O slug deve ser passado explicitamente em cada chamada para garantir isolamento.
 */
export const OrdersService = {
  async getActiveOrders(slug: string) {
    // Rota protegida por JWT e filtrada por SLUG no backend
    const response = await api.get(`/admin/${slug}/orders`);
    return response.data;
  },

  async updateStatus(orderId: string, nextStatus: string) {
    const response = await api.patch(`/admin/orders/${orderId}`, {
      status: nextStatus
    });
    return response.data;
  }
};
