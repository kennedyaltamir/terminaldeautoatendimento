/**
 * MESAFLOW OS - WAITER OPERATIONAL CONTROLLER
 * -----------------------------------------------------------------------------
 * Versão: 2.2.1 (Sovereign Gold Master - Consolidated & Null-Safe)
 * Data: 30 de Janeiro de 2026
 * Status: REVISADO, CORRIGIDO E SELADO PARA PRODUÇÃO
 * 
 * DNA_ID: MF-WAITER-CTRL-V2-2-1-GOLD
 * 
 * Objetivo: 
 * 1. Gerenciar estados das mesas com ordenação por prioridade tática.
 * 2. Garantir acesso seguro ao WebSocketContext (Fix TS2339).
 * 3. Prover ritos de abertura e fechamento de mesa com feedback visual.
 * 4. Manter suporte a filtros de salão e métricas em tempo real.
 */

import { useState, useCallback, useEffect, useMemo } from 'react';
import { TableDashboard } from '@/types';
import { getTablesDashboard, openTable, closeTable } from '@/lib/api';
import { toast } from 'sonner';
import { useWebSocketContext } from '@/context/WebSocketContext';

export type WaiterMode = 'VIEW' | 'ACTION' | 'SELECTION';
export type WaiterFilter = 'ALL' | 'MY_TABLES' | 'ALERTS';

export function useWaiterController(slug: string) {
  // 🛡️ Acesso ao contexto com proteção contra retorno nulo
  const context = useWebSocketContext();
  
  const [tables, setTables] = useState<TableDashboard[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<WaiterFilter>('ALL');

  // --- 1. DATA SYNC (Sincronização com Ordenação Tática) ---
  const fetchTables = useCallback(async (silent = false) => {
    if (!silent) setLoading(true);
    try {
      const data = await getTablesDashboard();
      
      // 🧠 ORDENAÇÃO INTELIGENTE: Alertas > Pagamento > Ocupadas > Livres
      // Garante que o garçom veja o que exige ação imediata no topo.
      const sorted = data.sort((a: TableDashboard, b: TableDashboard) => {
        const getScore = (t: TableDashboard) => {
          if (t.status === 'alert') return 3;
          if (t.status === 'payment') return 2;
          if (t.status === 'occupied') return 1;
          return 0;
        };
        return getScore(b) - getScore(a) || a.table_number - b.table_number;
      });
      
      setTables(sorted);
    } catch (e) {
      console.error("[WaiterController] Sync Error:", e);
      toast.error("Erro ao atualizar mapa de mesas.");
    } finally {
      if (!silent) setLoading(false);
    }
  }, []);

  // --- 2. REAL-TIME REACTION (WebSocket & Haptics) ---
  useEffect(() => {
    // 🛡️ FIX TS2339: Guard clause para garantir que o contexto existe
    if (context?.lastMessage) {
      const type = context.lastMessage.type;
      
      if (['table_update', 'order_update', 'waiter_call', 'payment_confirmed'].includes(type)) {
        // 📳 FEEDBACK HÁPTICO: Vibra em chamados críticos (Mesa chamando ou conta)
        if ((type === 'waiter_call' || type === 'payment_confirmed') && 
            typeof navigator !== 'undefined' && navigator.vibrate) {
          navigator.vibrate([200, 100, 200]);
        }
        
        fetchTables(true); // Atualização silenciosa
      }
    }
  }, [context?.lastMessage, fetchTables]);

  // --- 3. OPERATIONAL ACTIONS ---

  const handleOpenTable = async (tableId: number, customerName: string) => {
    try {
      await openTable(tableId, customerName);
      toast.success(`Mesa ${tableId} aberta para ${customerName}`);
      await fetchTables(true);
      return true;
    } catch (e) {
      toast.error("Falha ao abrir mesa. Verifique a conexão.");
      return false;
    }
  };

  const handleQuickClose = async (tableId: number) => {
    // Rito de confirmação para evitar encerramento acidental
    if (!confirm(`Confirmar fechamento da Mesa ${tableId} em DINHEIRO?`)) return;
    
    const toastId = toast.loading("Processando fechamento...");
    try {
      await closeTable(tableId, 'cash');
      toast.success("Mesa encerrada e liberada.", { id: toastId });
      await fetchTables(true);
    } catch (e) {
      toast.error("Erro ao fechar mesa.", { id: toastId });
    }
  };

  // --- 4. COMPUTED DATA (Memos para Performance) ---

  const filteredTables = useMemo(() => {
    return tables.filter(t => {
      if (filter === 'ALERTS') return t.status === 'alert' || t.status === 'payment';
      // MY_TABLES: Implementação futura baseada no ID do colaborador logado
      return true;
    });
  }, [tables, filter]);

  const stats = useMemo(() => ({
    total: tables.length,
    occupied: tables.filter(t => t.status === 'occupied' || t.status === 'alert' || t.status === 'payment').length,
    alerts: tables.filter(t => t.status === 'alert').length,
    revenue: tables.reduce((acc, t) => acc + (t.active_session?.total_spent || 0), 0)
  }), [tables]);

  // --- 5. INITIALIZATION ---
  useEffect(() => { 
    fetchTables(); 
  }, [fetchTables]);

  return {
    tables: filteredTables,
    stats,
    loading,
    filter,
    setFilter,
    isConnected: context?.isConnected ?? false,
    actions: {
      refresh: () => fetchTables(true),
      openTable: handleOpenTable,
      quickClose: handleQuickClose
    }
  };
}