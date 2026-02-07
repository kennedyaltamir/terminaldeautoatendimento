
import { create } from 'zustand';
import { api } from '../services/api';
import { logger } from '../services/logger.service';

interface Delivery {
  id: string;
  customer_name: string;
  delivery_address: string;
  total_amount: number;
  status: string;
}

interface LogisticsState {
  deliveries: Delivery[];
  isLoading: boolean;
  fetchDeliveries: () => Promise<void>;
}

export const useLogisticsStore = create<LogisticsState>((set) => ({
  deliveries: [],
  isLoading: false,
  fetchDeliveries: async () => {
    set({ isLoading: true });
    try {
      const res = await api.get('/admin/delivery/orders');
      set({ deliveries: res.data, isLoading: false });
    } catch (e) {
      set({ isLoading: false });
      logger.error('LOGISTICS_STORE', 'Falha ao buscar entregas', e);
    }
  }
}));

