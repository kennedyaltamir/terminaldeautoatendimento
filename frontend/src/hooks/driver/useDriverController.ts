/**
 * MODULE: LOGISTICS_CONTROLLER
 * VERSION: 3.2.0 (Debug Enabled)
 * DNA_ID: MF-DRIVER-CTRL-V3-2
 * Objective: Export setState for Oracle Debug HUD and fix state persistence.
 */
import { useState, useCallback, useEffect } from 'react';
import { Order } from '@/types';
import { getKitchenOrders, dispatchOrder, updateOrderStatus } from '@/lib/api';
import { toast } from 'sonner';

export type DriverState = 
  | 'IDLE'              
  | 'EN_ROUTE'          
  | 'WAITING_CUSTOMER'  
  | 'COMPLETING';       

export function useDriverController(slug: string) {
  const [state, setState] = useState<DriverState>('IDLE');
  const [orders, setOrders] = useState<Order[]>([]);
  const [activeOrder, setActiveOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [waitingTimer, setWaitingTimer] = useState<number | null>(null);

  // --- PERSISTÊNCIA ---
  useEffect(() => {
    const savedOrder = localStorage.getItem('mesaflow_driver_active_order');
    const savedState = localStorage.getItem('mesaflow_driver_state');
    if (savedOrder && savedState) {
      setActiveOrder(JSON.parse(savedOrder));
      setState(savedState as DriverState);
    }
  }, []);

  useEffect(() => {
    if (activeOrder) {
      localStorage.setItem('mesaflow_driver_active_order', JSON.stringify(activeOrder));
      localStorage.setItem('mesaflow_driver_state', state);
    } else {
      localStorage.removeItem('mesaflow_driver_active_order');
      localStorage.removeItem('mesaflow_driver_state');
    }
  }, [activeOrder, state]);

  const fetchQueue = useCallback(async () => {
    try {
      const allOrders = await getKitchenOrders(slug);
      if (state !== 'IDLE') return;
      const deliveryOrders = allOrders.filter(o => 
        o.order_type === 'delivery' && o.status === 'ready'
      );
      setOrders(deliveryOrders);
    } catch (e) {
      console.error("[DriverController] Sync Error");
    } finally {
      setLoading(false);
    }
  }, [slug, state]);

  const acceptOrder = async (order: Order) => {
    setActiveOrder(order);
    setState('EN_ROUTE');
    try {
      await dispatchOrder(order.id, 999);
    } catch (e) {
      toast.warning("Modo Offline: Rota salva no dispositivo.");
    }
  };

  const reportArrival = () => {
    setState('WAITING_CUSTOMER');
    setWaitingTimer(Date.now());
  };

  const completeDelivery = async (code?: string) => {
    if (!activeOrder) return { success: false };
    try {
      await updateOrderStatus(slug, activeOrder.id, 'delivered');
      setActiveOrder(null);
      setState('IDLE');
      setWaitingTimer(null);
      return { success: true };
    } catch (e) {
      toast.error("Erro ao finalizar.");
      return { success: false };
    }
  };

  useEffect(() => {
    fetchQueue();
    const interval = setInterval(fetchQueue, 15000);
    return () => clearInterval(interval);
  }, [fetchQueue]);

  return {
    state,
    setState, // 🛡️ FIX: Exportando o setter para o Debug HUD
    orders,
    activeOrder,
    loading,
    waitingTimer,
    actions: {
      refresh: fetchQueue,
      acceptOrder,
      reportArrival,
      completeDelivery
    }
  };
}