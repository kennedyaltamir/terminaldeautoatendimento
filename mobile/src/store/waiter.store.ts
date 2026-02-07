import { create } from 'zustand';
import { api } from '../services/api';
import { logger } from '../services/logger.service';

/**
 * WaiterStore: Gerencia o estado do fluxo de atendimento (Mobile POS).
 * Atualizado para suportar sincronização reativa de mesas.
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

export interface WaiterState {
  selectedTableId: number | null;
  selectedTableNumber: number | null;
  activeSessionToken: string | null;
  cart: CartItem[];
  serviceRequests: ServiceRequest[];
  isSubmitting: boolean;
  lastTableUpdate: number; // Timestamp para gatilho de UI
  
  // Actions
  selectTable: (id: number | null, num: number | null) => void;
  setSession: (token: string | null) => void;
  addToCart: (product: { id: number; name: string; price: number }) => void;
  updateQuantity: (productId: number, delta: number) => void;
  clearCart: () => void;
  addServiceRequest: (event: any) => void;
  resolveRequest: (id: number) => Promise<void>;
  triggerRefresh: () => void; // Sinaliza que as mesas mudaram
  resetWaiterFlow: () => void;
  getCartTotal: () => number;
  submitOrder: (slug: string) => Promise<{ success: boolean; offline: boolean }>;
}

export const useWaiterStore = create<WaiterState>((set, get) => ({
  selectedTableId: null,
  selectedTableNumber: null,
  activeSessionToken: null,
  cart: [],
  serviceRequests: [],
  isSubmitting: false,
  lastTableUpdate: Date.now(),

  selectTable: (id, num) => set({ selectedTableId: id, selectedTableNumber: num }),
  setSession: (token) => set({ activeSessionToken: token }),

  triggerRefresh: () => {
    logger.debug(TAG, 'Gatilho de atualização de mesas acionado.');
    set({ lastTableUpdate: Date.now() });
  },

  addToCart: (product) => {
    const { cart } = get();
    const existing = cart.find(item => item.productId === product.id);
    if (existing) {
      set({ cart: cart.map(item => item.productId === product.id ? { ...item, quantity: item.quantity + 1 } : item) });
    } else {
      set({ cart: [...cart, { productId: product.id, name: product.name, price: product.price, quantity: 1 }] });
    }
  },

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
    }
  },

  resolveRequest: async (id) => {
    set({ serviceRequests: get().serviceRequests.filter(r => r.id !== id) });
  },

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
      await api.post(`/${slug}/orders`, payload);
      set({ cart: [] });
      return { success: true, offline: false };
    } catch (e: any) {
      return { success: false, offline: false };
    } finally {
      set({ isSubmitting: false });
    }
  },

  getCartTotal: () => get().cart.reduce((acc, item) => acc + (item.price * item.quantity), 0),
  
  resetWaiterFlow: () => set({ 
    selectedTableId: null, 
    selectedTableNumber: null, 
    activeSessionToken: null, 
    cart: [], 
    isSubmitting: false 
  }),
}));
