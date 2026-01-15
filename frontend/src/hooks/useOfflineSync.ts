// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-10 16:15:00
import { useEffect, useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '@/lib/db';
import { createOrder } from '@/lib/api';
import { toast } from 'sonner';

export function useOfflineSync() {
  const [isSyncing, setIsSyncing] = useState(false);

  // Monitora a tabela local reativamente
  const pendingCount = useLiveQuery(() => db.pendingOrders.where('status').equals('pending').count()) || 0;
  const errorCount = useLiveQuery(() => db.pendingOrders.where('status').equals('error').count()) || 0;

  const syncNow = async () => {
    if (isSyncing || !navigator.onLine) return;

    const pendingOrders = await db.pendingOrders
      .where('status')
      .equals('pending')
      .toArray();

    if (pendingOrders.length === 0) return;

    setIsSyncing(true);
    let successCount = 0;

    for (const order of pendingOrders) {
      try {
        await createOrder(order.slug, order.payload);
        // Sucesso: Remove da fila
        await db.pendingOrders.delete(order.id!);
        successCount++;
      } catch (error: any) {
        console.error("Erro na sincronização:", error);
        
        // Se for erro de regra de negócio (400) ou validação (422)
        // Marcamos como erro para parar o loop de retry automático
        const isFatalError = error.status === 400 || error.status === 422;
        
        if (isFatalError) {
          await db.pendingOrders.update(order.id!, {
            status: 'error',
            errorMessage: error.message || "Erro de validação"
          });
          toast.error(`Falha no pedido offline: ${error.message}`, {
            description: "O pedido foi movido para a lista de erros."
          });
        } else {
          // Erro de rede ou servidor: Incrementa retry e tenta depois
          await db.pendingOrders.update(order.id!, {
            retryCount: (order.retryCount || 0) + 1
          });
        }
      }
    }

    setIsSyncing(false);
    if (successCount > 0) {
      toast.success(`${successCount} pedidos sincronizados! ☁️`);
    }
  };

  const clearQueue = async () => {
    if (confirm("Deseja limpar todos os pedidos pendentes (incluindo erros)?")) {
      await db.pendingOrders.clear();
      toast.success("Fila offline limpa.");
    }
  };

  useEffect(() => {
    const handleOnline = () => {
      syncNow();
    };
    window.addEventListener('online', handleOnline);
    
    return () => window.removeEventListener('online', handleOnline);
  }, [pendingCount]);

  return {
    pendingCount,
    errorCount,
    isSyncing,
    syncNow,
    clearQueue
  };
}