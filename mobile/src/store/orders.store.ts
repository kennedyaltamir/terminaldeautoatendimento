import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { OrdersService } from '../services/orders.service';
import { RealtimeEvent } from '../types/realtime.events';
import { OrdersSLAService, SLAStatus } from '../services/orders.sla.service';
import { AlertsEngineService } from '../services/alerts/alerts.engine.service';
import { AlertsOutputService } from '../services/alerts/alerts.output.service';
import { useSettingsStore } from './settings.store';

interface OrderItem {
  quantity: number;
  product: { name: string };
}

export interface Order {
  id: string;
  status: string;
  customer_name: string;
  created_at: string;
  items: OrderItem[];
  table?: { table_number: number };
  elapsedTime?: string;
  remainingTime?: string;
  slaStatus?: SLAStatus;
  priorityScore?: number;
  lastAlertedStatus?: SLAStatus;
  lastAlertedAt?: number;
}

interface OrdersState {
  orders: Order[];
  isLoading: boolean;
  isSyncing: boolean;
  isSocketConnected: boolean;
  isHydrated: boolean;
  error: string | null;
  
  setOrders: (orders: Order[]) => void;
  setSyncing: (status: boolean) => void;
  setSocketStatus: (connected: boolean) => void;
  setHydrated: (status: boolean) => void;
  addOrUpdateOrder: (order: Order) => void;
  fetchOrders: (slug: string) => Promise<void>;
  advanceStatus: (orderId: string, currentStatus: string, slug: string) => Promise<void>;
  handleRealtimeEvent: (event: RealtimeEvent) => void;
  updateSLAs: (currentTimestamp: number) => void;
  evaluateAlerts: (currentTimestamp: number) => void;
}

export const useOrdersStore = create<OrdersState>()(
  persist(
    (set, get) => ({
      orders: [],
      isLoading: false,
      isSyncing: false,
      isSocketConnected: false,
      isHydrated: false,
      error: null,

      setOrders: (orders) => set({ orders, error: null }),
      setSyncing: (status) => set({ isSyncing: status }),
      setSocketStatus: (connected) => set({ isSocketConnected: connected }),
      setHydrated: (status) => set({ isHydrated: status }),

      addOrUpdateOrder: (order) => {
        const { orders } = get();
        const exists = orders.find(o => o.id === order.id);
        if (exists) {
          set({ orders: orders.map(o => o.id === order.id ? order : o) });
        } else {
          set({ orders: [order, ...orders] });
        }
        get().updateSLAs(Date.now());
      },

      fetchOrders: async (slug: string) => {
        set({ isLoading: true, error: null });
        try {
          const rawOrders = await OrdersService.getActiveOrders(slug);
          set({ orders: rawOrders, error: null });
          get().updateSLAs(Date.now());
          set({ isLoading: false });
        } catch (e: any) {
          set({ 
            error: 'Não foi possível conectar ao servidor. Exibindo dados locais.', 
            isLoading: false 
          });
        }
      },

      advanceStatus: async (orderId: string, currentStatus: string, slug: string) => {
        const nextStatusMap: Record<string, string> = {
          'pending': 'preparing',
          'preparing': 'ready',
          'ready': 'delivered'
        };

        const nextStatus = nextStatusMap[currentStatus];
        if (!nextStatus) return;

        const previousOrders = get().orders;
        set({
          orders: previousOrders.map(o => o.id === orderId ? { ...o, status: nextStatus } : o)
        });

        try {
          await OrdersService.updateStatus(orderId, nextStatus);
          get().updateSLAs(Date.now());
        } catch (e) {
          set({ orders: previousOrders, error: 'Falha ao atualizar status.' });
          setTimeout(() => set({ error: null }), 3000);
        }
      },

      handleRealtimeEvent: (event: RealtimeEvent) => {
        const { orders } = get();
        if (event.type === 'order_update') {
          const updated = orders.map(o => 
            o.id === event.order_id ? { ...o, status: event.status } : o
          );
          set({ orders: updated });
          get().updateSLAs(Date.now());
        }
      },

      updateSLAs: (currentTimestamp: number) => {
        const { orders } = get();
        if (orders.length === 0) return;

        const enrichedAndSorted = orders
          .map(order => {
            const metrics = OrdersSLAService.calculateMetrics(order, currentTimestamp);
            const remainingMinutes = Math.ceil(metrics.remainingSeconds / 60);
            
            return {
              ...order,
              elapsedTime: `${Math.floor(metrics.elapsedSeconds / 60)}m`,
              remainingTime: metrics.status === 'BREACHED' ? 'ATRASADO' : `${remainingMinutes}m`,
              slaStatus: metrics.status,
              priorityScore: metrics.priorityScore
            };
          })
          .sort((a, b) => b.priorityScore - a.priorityScore);

        set({ orders: enrichedAndSorted });
      },

      evaluateAlerts: (currentTimestamp: number) => {
        const { orders } = get();
        const { isSilentMode } = useSettingsStore.getState();

        const decisions = AlertsEngineService.decide(orders, currentTimestamp);
        if (decisions.length === 0) return;

        set((state) => ({
          orders: state.orders.map(order => {
            const decision = decisions.find(d => d.orderId === order.id);
            if (decision) {
              if (!isSilentMode) {
                AlertsOutputService.trigger(decision.status);
              }
              return { 
                ...order, 
                lastAlertedStatus: decision.status, 
                lastAlertedAt: currentTimestamp 
              };
            }
            return order;
          })
        }));
      }
    }),
    {
      name: 'mesaflow-orders-cache',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({ orders: state.orders }),
      onRehydrateStorage: () => (state) => {
        state?.setHydrated(true);
      }
    }
  )
);
