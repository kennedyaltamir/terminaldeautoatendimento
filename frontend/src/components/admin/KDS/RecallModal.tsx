/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.0.1 (Type Hardening)
 * DNA_ID: MF-KDS-RECALL-V1-FIX
 * Objective: Resolver erro TS2339 garantindo que o campo finished_at seja reconhecido.
 */
"use client";

import { useState, useEffect } from "react";
import { Order } from "@/types";
import { getRecentCompletedOrders, updateOrderStatus } from "@/lib/api";
import Modal from "@/components/ui/Modal";
import { Loader2, Undo2, Clock,CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

// 🛡️ Interface estendida para o contexto tático do KDS
interface TacticalOrder extends Order {
  finished_at?: string | Date | null;
}

interface RecallModalProps {
  isOpen: boolean;
  onClose: () => void;
  slug: string;
  onRestore: () => void;
}

export default function RecallModal({ isOpen, onClose, slug, onRestore }: RecallModalProps) {
  const [orders, setOrders] = useState<TacticalOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [restoringId, setRestoringId] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      getRecentCompletedOrders(slug)
        .then((data) => setOrders(data as TacticalOrder[]))
        .catch(() => toast.error("Erro ao carregar histórico recente"))
        .finally(() => setLoading(false));
    }
  }, [isOpen, slug]);

  const handleRestore = async (order: TacticalOrder) => {
    setRestoringId(order.id);
    try {
      await updateOrderStatus(slug, order.id, 'preparing');
      toast.success(`Pedido #${order.id.slice(0,4)} restaurado!`);
      onRestore();
      onClose();
    } catch (e) {
      toast.error("Falha ao restaurar pedido.");
    } finally {
      setRestoringId(null);
    }
  };

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Histórico Recente (Recall)">
      <div className="space-y-4">
        <div className="bg-blue-900/20 border border-blue-800 p-4 rounded-xl flex gap-3">
          <Undo2 className="text-blue-400 shrink-0" size={20} />
          <p className="text-xs text-blue-200 leading-relaxed">
            Use esta tela para recuperar pedidos que foram marcados como "Pronto" ou "Entregue" acidentalmente nas últimas 2 horas.
          </p>
        </div>

        {loading ? (
          <div className="py-10 flex justify-center"><Loader2 className="animate-spin text-slate-500" /></div>
        ) : orders.length === 0 ? (
          <div className="py-10 text-center text-slate-500 text-sm">Nenhum pedido finalizado recentemente.</div>
        ) : (
          <div className="max-h-[50vh] overflow-y-auto space-y-2 pr-2 custom-scrollbar">
            {orders.map(order => (
              <div key={order.id} className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex justify-between items-center group hover:border-slate-700 transition-all">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-black text-white text-lg">#{order.id.slice(0,4).toUpperCase()}</span>
                    <span className="text-xs font-bold text-slate-500 uppercase">{order.customer_name}</span>
                  </div>
                  <div className="flex items-center gap-2 mt-1 text-[10px] text-slate-400">
                    <Clock size={10} /> 
                    {/* 🛡️ FIX: finished_at agora é reconhecido via TacticalOrder */}
                    Finalizado às {order.finished_at ? new Date(order.finished_at).toLocaleTimeString() : '---'}
                  </div>
                </div>
                
                <button
                  onClick={() => handleRestore(order)}
                  disabled={restoringId === order.id}
                  className="bg-slate-800 hover:bg-blue-600 text-slate-300 hover:text-white px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all flex items-center gap-2 disabled:opacity-50"
                >
                  {restoringId === order.id ? <Loader2 size={14} className="animate-spin" /> : <Undo2 size={14} />}
                  Restaurar
                </button>
              </div>
            ))}
          </div>
        )}
        
        <div className="pt-4 border-t border-slate-800">
          <button onClick={onClose} className="w-full py-3 bg-slate-800 text-slate-300 rounded-xl font-bold text-xs hover:bg-slate-700">
            Fechar
          </button>
        </div>
      </div>
    </Modal>
  );
}