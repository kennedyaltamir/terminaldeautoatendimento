import { useEffect, useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db, PendingOrder } from '@/lib/db';
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
        
        // Se for erro de validação (400/422), marca como erro para intervenção manual
        // Se for erro de rede (500 ou fetch fail), mantém como pending para tentar depois
        const isValidationError = error.message && (error.message.includes("Estoque") || error.message.includes("fechado"));
        
        if (isValidationError) {
          await db.pendingOrders.update(order.id!, {
            status: 'error',
            errorMessage: error.message || "Erro desconhecido"
          });
        } else {
          // Apenas incrementa retry, mantém pending
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

  useEffect(() => {
    // 1. Event Listeners de Rede
    const handleOnline = () => {
      toast.info("Conexão restaurada. Sincronizando...");
      syncNow();
    };

    window.addEventListener('online', handleOnline);

    // 2. Polling de Segurança (a cada 30s tenta enviar se tiver algo)
    const interval = setInterval(() => {
      if (navigator.onLine && pendingCount > 0) {
        syncNow();
      }
    }, 30000);

    return () => {
      window.removeEventListener('online', handleOnline);
      clearInterval(interval);
    };
  }, [pendingCount]);

  return {
    pendingCount,
    errorCount,
    isSyncing,
    syncNow
  };
}