/**
 * 🧠 MESAFLOW OS — KDS FINITE STATE MACHINE HOOK
 * Domain: Production Logic / State Management
 * Version: 2.3.0 (Diamond Hardened - Type Safe)
 * DNA_ID: MF-KDS-FSM-V23-GOLD
 */
"use client";

import { useReducer, useCallback, useRef } from 'react';
import { Order } from '@/types';

// --- 1. CONTRATOS DE ESTADO ---
interface KdsState {
  orders: Order[];
  isSaturationMode: boolean;
  /** 🛡️ MÁSCARA ATÔMICA: IDs protegidos contra re-renderização bumerangue */
  pendingBumpIds: Set<string>;
}

type KdsAction = 
  | { type: 'SET_ORDERS'; payload: Order[] }
  | { type: 'BUMP_START'; orderId: string }
  | { type: 'BUMP_COMMIT'; orderId: string }
  | { type: 'BUMP_ROLLBACK'; orderId: string }
  | { type: 'CHECK_SATURATION' };

// --- 2. REDUCER DETERMINÍSTICO ---
function kdsReducer(state: KdsState, action: KdsAction): KdsState {
  switch (action.type) {
    case 'SET_ORDERS':
      // Filtra o payload do servidor removendo IDs que o operador já "limpou" localmente
      const filteredPayload = action.payload.filter((o: Order) => !state.pendingBumpIds.has(o.id));
      return { ...state, orders: filteredPayload };

    case 'BUMP_START': {
      const newSet = new Set(state.pendingBumpIds);
      newSet.add(action.orderId);
      return { 
        ...state, 
        pendingBumpIds: newSet,
        orders: state.orders.filter((o: Order) => o.id !== action.orderId) 
      };
    }

    case 'BUMP_COMMIT':
    case 'BUMP_ROLLBACK': {
      const cleanupSet = new Set(state.pendingBumpIds);
      cleanupSet.delete(action.orderId);
      return { ...state, pendingBumpIds: cleanupSet };
    }

    case 'CHECK_SATURATION':
      return { ...state, isSaturationMode: state.orders.length > 15 };

    default:
      return state;
  }
}

// --- 3. HOOK SOBERANO ---
export function useKdsFsm() {
  const [state, dispatch] = useReducer(kdsReducer, {
    orders: [],
    isSaturationMode: false,
    // 🛡️ FIX TS2769: Inicialização explícita para evitar Set<unknown>
    pendingBumpIds: new Set<string>()
  });

  const activeTimers = useRef<Record<string, ReturnType<typeof setTimeout>>>({});

  const calculateComplexity = useCallback((order: Order): number => {
    if (!order.items) return 0;
    return order.items.reduce((acc, item) => {
      let score = item.product.station === 'kitchen' ? 3 : 1;
      if (item.notes) score += 2;
      return acc + (score * item.quantity);
    }, 0);
  }, []);

  const bumpOrder = useCallback((orderId: string, apiCall: () => Promise<void>) => {
    dispatch({ type: 'BUMP_START', orderId });

    activeTimers.current[orderId] = setTimeout(async () => {
      try {
        await apiCall();
        dispatch({ type: 'BUMP_COMMIT', orderId });
      } catch (e) {
        console.error(`🚨 [FSM] Falha no commit do pedido ${orderId}`);
        dispatch({ type: 'BUMP_ROLLBACK', orderId });
      } finally {
        delete activeTimers.current[orderId];
      }
    }, 5000);
  }, []);

  const cancelUndo = useCallback((orderId: string) => {
    if (activeTimers.current[orderId]) {
      clearTimeout(activeTimers.current[orderId]);
      delete activeTimers.current[orderId];
      dispatch({ type: 'BUMP_ROLLBACK', orderId });
      return true;
    }
    return false;
  }, []);

  return { 
    state, 
    dispatch, 
    calculateComplexity, 
    bumpOrder, 
    cancelUndo 
  };
}
