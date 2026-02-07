import { useEffect, useState } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '@/lib/db';
import { emitFiscalDocument } from '@/lib/api';
import { toast } from 'sonner';

interface UseFiscalSyncProps {
  onSyncComplete?: () => void;
}

export function useFiscalSync({ onSyncComplete }: UseFiscalSyncProps = {}) {
  const [isSyncing, setIsSyncing] = useState(false);

  // Monitora a fila fiscal localmente
  const pendingItems = useLiveQuery(() => db.fiscalQueue.where('status').equals('pending').toArray()) || [];
  const errorCount = useLiveQuery(() => db.fiscalQueue.where('status').equals('error').count()) || 0;

  const syncFiscalQueue = async () => {
    if (isSyncing || !navigator.onLine || pendingItems.length === 0) return;

    setIsSyncing(true);
    let successCount = 0;

    for (const item of pendingItems) {
      try {
        // Tenta emitir no backend
        await emitFiscalDocument(item.orderId);
        
        // Sucesso: Remove da fila local
        await db.fiscalQueue.delete(item.id!);
        successCount++;
      } catch (error: any) {
        console.error(`[FiscalSync] Erro na nota ${item.orderId}:`, error);

        // Se for erro de validação (400/422), marca como erro para o usuário corrigir
        if (error.status === 400 || error.status === 422) {
          await db.fiscalQueue.update(item.id!, {
            status: 'error',
            errorMessage: error.message || "Erro de validação fiscal"
          });
        } else {
          // Erro de rede: Incrementa retry e tenta na próxima volta da internet
          await db.fiscalQueue.update(item.id!, {
            retryCount: (item.retryCount || 0) + 1
          });
        }
      }
    }

    setIsSyncing(false);
    
    if (successCount > 0) {
      toast.success(`${successCount} notas fiscais transmitidas! 🧾`);
      // Notifica o componente pai para atualizar a lista
      if (onSyncComplete) onSyncComplete();
    }
  };

  useEffect(() => {
    const handleOnline = () => {
      if (pendingItems.length > 0) {
        syncFiscalQueue();
      }
    };

    window.addEventListener('online', handleOnline);
    
    // Tenta sincronizar se houver itens e estiver online
    if (navigator.onLine && pendingItems.length > 0 && !isSyncing) {
      syncFiscalQueue();
    }

    return () => window.removeEventListener('online', handleOnline);
  }, [pendingItems.length, isSyncing]);

  return {
    pendingCount: pendingItems.length,
    errorCount,
    isSyncing,
    syncNow: syncFiscalQueue
  };
}
