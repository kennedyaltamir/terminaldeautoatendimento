import { create } from 'zustand';
import { api } from '../services/api';
import { logger } from '../services/logger.service';

/**
 * WaiterStore: Gerencia o estado do fluxo de atendimento (Mobile POS).
 */

const TAG = 'WaiterStore';

export interface CartItem {
  productId: number;
  name: string;
  price: number;
  quantity: number;
}

export interface ServiceRequest {
  id: number;
  table: number;
  service_type: string;
  notes?: string;
  status: 'pending' | 'resolved';
}

export interface PaymentData {
  qrCode: string;
  totalAmount: number;
  method: string;
}

export interface PendingOrder {
  id: string;
  payload: any;
  createdAt: number;
}

export interface WaiterState {
  selectedTableId: number | null;
  selectedTableNumber: number | null;
  activeSessionToken: string | null;
  cart: CartItem[];
  serviceRequests: ServiceRequest[];
  pendingQueue: PendingOrder[];
  isSubmitting: boolean;
  lastSubmittedOrder: any | null;
  paymentData: PaymentData | null;
  
  // Actions - Contexto
  selectTable: (id: number | null, num: number | null) => void;
  setSession: (token: string | null) => void;
  
  // Actions - Carrinho
  addToCart: (product: { id: number; name: string; price: number }) => void;
  removeFromCart: (productId: number) => void;
  updateQuantity: (productId: number, delta: number) => void;
  clearCart: () => void;
  
  // Actions - Chamados
  addServiceRequest: (event: any) => void;
  resolveRequest: (id: number) => Promise<void>;
  setInitialRequests: (reqs: ServiceRequest[]) => void;
  
  // Actions - Pagamento
  initiatePayment: (slug: string, method: string) => Promise<boolean>;
  clearPayment: () => void;
  
  // Actions - API & Offline
  submitOrder: (slug: string) => Promise<{ success: boolean; offline: boolean }>;
  removeFromQueue: (orderId: string) => void;
  
  // Getters
  getCartTotal: () => number;
  resetWaiterFlow: () => void;
}

export const useWaiterStore = create<WaiterState>((set, get) => ({
  selectedTableId: null,
  selectedTableNumber: null,
  activeSessionToken: null,
  cart: [],
  serviceRequests: [],
  pendingQueue: [],
  isSubmitting: false,
  lastSubmittedOrder: null,
  paymentData: null,

  selectTable: (id, num) => set({ selectedTableId: id, selectedTableNumber: num }),
  setSession: (token) => set({ activeSessionToken: token }),

  addToCart: (product) => {
    const { cart } = get();
    const existing = cart.find(item => item.productId === product.id);
    if (existing) {
      set({ cart: cart.map(item => item.productId === product.id ? { ...item, quantity: item.quantity + 1 } : item) });
    } else {
      set({ cart: [...cart, { productId: product.id, name: product.name, price: product.price, quantity: 1 }] });
    }
  },

  removeFromCart: (productId) => set((state) => ({ cart: state.cart.filter(item => item.productId !== productId) })),

  updateQuantity: (productId, delta) => {
    const { cart } = get();
    set({
      cart: cart.map(item => {
        if (item.productId === productId) {
          const newQty = Math.max(0, item.quantity + delta);
          return { ...item, quantity: newQty };
        }
        return item;
      }).filter(item => item.quantity > 0)
    });
  },

  clearCart: () => set({ cart: [] }),

  setInitialRequests: (reqs) => set({ serviceRequests: reqs }),

  addServiceRequest: (event) => {
    const { serviceRequests } = get();
    if (!serviceRequests.find(r => r.id === event.id)) {
      const newRequest: ServiceRequest = {
        id: event.id,
        table: event.table,
        service_type: event.service_type,
        notes: event.notes,
        status: 'pending'
      };
      set({ serviceRequests: [newRequest, ...serviceRequests] });
      logger.info(TAG, `Novo chamado adicionado: Mesa ${event.table}`);
    }
  },

  resolveRequest: async (id) => {
    set({ serviceRequests: get().serviceRequests.filter(r => r.id !== id) });
  },

  initiatePayment: async (slug, method) => {
    const { selectedTableId } = get();
    if (!selectedTableId) return false;
    set({ isSubmitting: true });
    try {
      const response = await api.post(`/admin/tables/${selectedTableId}/close`, { payment_method: method });
      if (method === 'pix' && response.data.pix_data) {
        set({ paymentData: { qrCode: response.data.pix_data.qr_code, totalAmount: response.data.total_amount || 0, method: 'pix' } });
      }
      return true;
    } catch (e) {
      logger.error(TAG, 'Erro ao iniciar pagamento', e);
      return false;
    } finally {
      set({ isSubmitting: false });
    }
  },

  clearPayment: () => set({ paymentData: null }),

  submitOrder: async (slug: string) => {
    const { cart, selectedTableId, isSubmitting } = get();
    if (isSubmitting || cart.length === 0) return { success: false, offline: false };
    const payload = {
      table_id: selectedTableId,
      qr_token: "staff-override",
      order_type: "dine_in",
      customer_name: "Atendimento Garçom",
      items: cart.map(item => ({ product_id: item.productId, quantity: item.quantity, notes: "" }))
    };
    set({ isSubmitting: true });
    try {
      const response = await api.post(`/${slug}/orders`, payload);
      set({ lastSubmittedOrder: { ...response.data, items: cart }, cart: [] });
      return { success: true, offline: false };
    } catch (e: any) {
      if (!e.response || e.response.status >= 500) {
        const offlineOrder: PendingOrder = { id: Math.random().toString(36).substr(2, 9), payload, createdAt: Date.now() };
        set({ pendingQueue: [...get().pendingQueue, offlineOrder], cart: [] });
        return { success: true, offline: true };
      }
      return { success: false, offline: false };
    } finally {
      set({ isSubmitting: false });
    }
  },

  removeFromQueue: (orderId) => set((state) => ({ pendingQueue: state.pendingQueue.filter(o => o.id !== orderId) })),
  getCartTotal: () => get().cart.reduce((acc, item) => acc + (item.price * item.quantity), 0),
  resetWaiterFlow: () => set({ selectedTableId: null, selectedTableNumber: null, activeSessionToken: null, cart: [], isSubmitting: false, lastSubmittedOrder: null, paymentData: null }),
}));
