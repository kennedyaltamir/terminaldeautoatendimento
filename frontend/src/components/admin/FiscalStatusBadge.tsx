"use client";

import { FileText, AlertCircle, CheckCircle2, Loader2, WifiOff, Clock } from "lucide-react";
import { useLiveQuery } from "dexie-react-hooks";
import { db } from "@/lib/db";
import { toast } from "sonner";

interface FiscalStatusBadgeProps {
  orderId: string;
  status: string;
  nfeUrl?: string | null;
  onEmit: () => void;
  loading: boolean;
  slug: string;
}

export default function FiscalStatusBadge({ orderId, status, nfeUrl, onEmit, loading, slug }: FiscalStatusBadgeProps) {
  // Verifica se este pedido específico está na fila de contingência
  const queuedItem = useLiveQuery(() => db.fiscalQueue.where('orderId').equals(orderId).first());

  const handleEmitClick = async () => {
    if (!navigator.onLine) {
      // Modo Contingência: Salva no Dexie
      try {
        const exists = await db.fiscalQueue.where('orderId').equals(orderId).first();
        if (exists) {
          toast.error("Esta nota já está na fila de espera.");
          return;
        }

        await db.fiscalQueue.add({
          orderId,
          slug,
          status: 'pending',
          createdAt: new Date(),
          retryCount: 0
        });

        toast.warning("Sem internet. Nota salva na fila de contingência.", {
          description: "Será enviada automaticamente assim que a rede voltar."
        });
      } catch (e) {
        toast.error("Erro ao salvar em contingência.");
      }
      return;
    }

    // Se estiver online, segue o fluxo normal
    onEmit();
  };

  if (loading) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-blue-100 text-blue-700">
        <Loader2 size={12} className="animate-spin" /> Processando
      </span>
    );
  }

  // Estado: Na Fila Offline
  if (queuedItem) {
    if (queuedItem.status === 'error') {
      return (
        <button 
          onClick={handleEmitClick}
          className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-red-100 text-red-700 border border-red-200"
          title={queuedItem.errorMessage}
        >
          <AlertCircle size={12} /> Erro na Fila
        </button>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-orange-100 text-orange-700 border border-orange-200">
        <Clock size={12} className="animate-pulse" /> Na Fila
      </span>
    );
  }

  if (status === 'emitted' && nfeUrl) {
    return (
      <a 
        href={nfeUrl} 
        target="_blank" 
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-green-100 text-green-700 hover:bg-green-200 transition-colors"
      >
        <CheckCircle2 size={12} /> NFC-e
      </a>
    );
  }

  if (status === 'error') {
    return (
      <button 
        onClick={handleEmitClick}
        className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-red-100 text-red-700 hover:bg-red-200 transition-colors border border-red-200"
      >
        <AlertCircle size={12} /> Erro (Reenviar)
      </button>
    );
  }

  if (status === 'processing') {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-yellow-100 text-yellow-700">
        <Loader2 size={12} className="animate-spin" /> Emitindo...
      </span>
    );
  }

  return (
    <button 
      onClick={handleEmitClick}
      className="inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors border border-gray-300"
    >
      {!navigator.onLine && <WifiOff size={10} className="text-orange-500" />}
      <FileText size={12} /> Emitir Nota
    </button>
  );
}
