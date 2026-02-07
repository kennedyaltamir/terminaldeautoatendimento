/**
 * MESAFLOW OS - KDS SOVEREIGN CONTROLLER
 * -----------------------------------------------------------------------------
 * Versão: 18.5.0 (Sovereign Gold Master - Final Consolidated)
 * Data: 30 de Janeiro de 2026
 * Status: REVISADO, CORRIGIDO E SELADO PARA PRODUÇÃO
 * 
 * DNA_ID: MF-KDS-CONTROLLER-V18-5-GOLD
 * 
 * Objetivo: 
 * 1. Unificar a FSM atômica com o motor de BI (Pace Engine).
 * 2. Corrigir erros de assinatura de dispatch (TS2554) e tipagem de parâmetros.
 * 3. Garantir integridade total do rito de finalização (Anti-Bumerangue).
 * 4. Manter suporte a Product 86, Recall, Gestão de Áudio e Logs SRE.
 */

import { useState, useCallback, useEffect, useMemo } from 'react';
import { useKdsFsm } from '@/hooks/useKdsFsm';
import { useKdsSocket } from './useKdsSocket';
import { audioManager } from '@/lib/kds/audio-engine';
import { kdsLogger } from '@/lib/kds/logger';
import { getKitchenOrders, updateOrderStatus, updateProduct } from '@/lib/api';
import { toast } from 'sonner';
import { Order } from '@/types';

// Interface estendida para suportar campos de auditoria temporal do KDS
interface TacticalOrder extends Order {
  finished_at?: string | Date | null;
}

export function useKdsController(slug: string) {
  // Extração da FSM Soberana e seus métodos de controle
  const { 
    state: fsmState, 
    dispatch, 
    bumpOrder, 
    cancelUndo, 
    calculateComplexity 
  } = useKdsFsm();

  const [isSyncing, setIsSyncing] = useState(true);
  const [isRecallOpen, setIsRecallOpen] = useState(false);
  const [completedHistory, setCompletedHistory] = useState<TacticalOrder[]>([]);

  // --- 1. PACE ENGINE (Velocímetro de Produção) ---
  // Calcula o ritmo da cozinha baseado nos últimos 30 minutos de histórico real
  const productionPace = useMemo(() => {
    const now = Date.now();
    const thirtyMinsAgo = now - (30 * 60 * 1000);
    
    const recent = completedHistory.filter(o => {
      if (!o.finished_at) return false;
      const finishTime = new Date(o.finished_at).getTime();
      return finishTime > thirtyMinsAgo;
    });

    if (recent.length === 0) return { avgTime: 0, ordersPerHour: 0, count: 0 };

    const totalPrepTime = recent.reduce((acc, o) => {
      const start = new Date(o.created_at).getTime();
      const end = new Date(o.finished_at!).getTime();
      return acc + (end - start);
    }, 0);

    return {
      avgTime: Math.round((totalPrepTime / recent.length) / 60000),
      ordersPerHour: recent.length * 2, // Projeção para 60min
      count: recent.length
    };
  }, [completedHistory]);

  // --- 2. DATA SYNC (Sincronização de Snapshot) ---
  // Implementa o rito de atualização atômica alinhado com a FSM
  const syncSnapshot = useCallback(async () => {
    if (fsmState.orders.length === 0) setIsSyncing(true);
    try {
      const orders = await getKitchenOrders(slug);
      
      // 🛡️ FIX TS2554: Alinhado com a assinatura do Reducer (KdsAction)
      dispatch({ type: 'SET_ORDERS', payload: orders });
      dispatch({ type: 'CHECK_SATURATION' });
      
      // Atualiza histórico para o motor de Pace (Pedidos finalizados ou entregues)
      const completed = orders.filter(o => o.status === 'ready' || o.status === 'delivered');
      setCompletedHistory(completed as TacticalOrder[]);
      
      kdsLogger.log({ 
        domain: 'SYSTEM', 
        action: 'SNAPSHOT_SYNC', 
        meta: { count: orders.length, pace: productionPace.ordersPerHour } 
      });
    } catch (e) {
      kdsLogger.log({ domain: 'SYSTEM', action: 'SYNC_FAIL', severity: 'ERROR', meta: { error: e } });
      toast.error("Falha na sincronização com o servidor.");
    } finally {
      setIsSyncing(false);
    }
  }, [slug, dispatch, fsmState.orders.length, productionPace.ordersPerHour]);

  // --- 3. REAL-TIME GATEWAY ---
  const handleSocketEvent = useCallback((data: any) => {
    if (data.type === 'new_order') {
      audioManager.play('new_order');
      syncSnapshot();
    } else if (data.type === 'order_update') {
      // O Reducer da FSM filtrará bumerangues de IDs que estão em rito de finalização (pendingBumpIds)
      syncSnapshot();
    }
  }, [syncSnapshot]);

  const { status: connectionStatus } = useKdsSocket(slug, handleSocketEvent);

  // --- 4. OPERATIONAL ACTIONS (Hardened) ---

  // Rito 86: Esgotar produto instantaneamente no cardápio
  const exhaustProduct = async (productId: number, productName: string) => {
    const toastId = toast.loading(`Bloqueando ${productName}...`);
    try {
      await updateProduct(productId, { is_available: false });
      kdsLogger.log({ domain: 'USER_ACTION', action: 'PRODUCT_86', meta: { productId, productName } });
      toast.success(`${productName} esgotado no cardápio!`, { id: toastId });
      await syncSnapshot();
    } catch (e) {
      kdsLogger.log({ domain: 'SYSTEM', action: 'PRODUCT_86_FAIL', severity: 'ERROR', meta: { error: e } });
      toast.error("Erro ao bloquear produto.", { id: toastId });
    }
  };

  // Aceite de Pedido: Transição PENDING -> PREPARING
  const acceptOrder = async (order: Order) => {
    kdsLogger.log({ domain: 'USER_ACTION', action: 'ACCEPT_ORDER', orderId: order.id });
    try {
      await updateOrderStatus(slug, order.id, 'preparing');
      await syncSnapshot();
    } catch (e) { 
      kdsLogger.log({ domain: 'SYSTEM', action: 'ACCEPT_FAIL', severity: 'ERROR', orderId: order.id });
      toast.error("Falha ao aceitar pedido."); 
    }
  };

  // Finalização de Pedido: Transição PREPARING -> READY (Com rito de Undo)
  const completeOrder = async (order: Order) => {
    kdsLogger.log({ domain: 'USER_ACTION', action: 'COMPLETE_ORDER', orderId: order.id });
    audioManager.play('bump');
    
    // 🛡️ RITO ATÔMICO: O pedido some da UI instantaneamente via FSM (Optimistic)
    // e só volta se a API falhar após a janela de 5s de Undo.
    try {
      await bumpOrder(order.id, async () => {
        await updateOrderStatus(slug, order.id, 'ready');
      });
      toast.success(`Pedido #${order.id.slice(0,4)} finalizado.`);
    } catch (e) {
      kdsLogger.log({ domain: 'SYSTEM', action: 'BUMP_FAIL', severity: 'ERROR', orderId: order.id });
      toast.error("Erro ao salvar. O pedido retornou à fila.");
      syncSnapshot();
    }
  };

  // --- 5. LIFECYCLE ---
  useEffect(() => { 
    syncSnapshot(); 
  }, [syncSnapshot]);

  return {
    orders: fsmState.orders,
    uiMode: fsmState.isSaturationMode ? 'SATURATION' : 'NORMAL',
    connectionStatus,
    isSyncing,
    isRecallOpen,
    productionPace,
    actions: {
      acceptOrder,
      completeOrder,
      exhaustProduct,
      refresh: syncSnapshot,
      toggleMute: () => audioManager.toggleMute(),
      getMuteState: () => audioManager.getMuteState(),
      openRecall: () => setIsRecallOpen(true),
      closeRecall: () => setIsRecallOpen(false),
      cancelUndo // Permite que a UI ofereça o rito de "Desfazer"
    },
    helpers: { calculateComplexity }
  };
}