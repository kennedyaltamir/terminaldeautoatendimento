"use client";

import { useState, useEffect } from "react";
import { X, DollarSign, Clock, CheckCircle2, AlertCircle, Receipt, ArrowRight } from "lucide-react";
import { getSessionDetails } from "@/lib/api";
import { TableSession } from "@/types";
import Modal from "@/components/ui/Modal";
import { formatCurrency } from "@/lib/utils";

interface BillAuditModalProps {
  isOpen: boolean;
  onClose: () => void;
  sessionId: number;
  tableName: string;
  onPayRequest?: (amount: number) => void;
}

export default function BillAuditModal({ isOpen, onClose, sessionId, tableName, onPayRequest }: BillAuditModalProps) {
  const [session, setSession] = useState<TableSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen && sessionId) {
      setLoading(true);
      getSessionDetails(sessionId)
        .then(setSession)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [isOpen, sessionId]);

  const subtotal = session ? Number(session.total_spent) : 0;
  const serviceFee = subtotal * 0.10;
  const total = subtotal + serviceFee;

  const handleCobrar = () => {
    if (onPayRequest) {
      onPayRequest(total);
    }
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Conferência: ${tableName}`}>
      {loading ? (
        <div className="p-12 text-center space-y-4">
          <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-slate-500 font-bold animate-pulse">Sincronizando comanda...</p>
        </div>
      ) : session ? (
        <div className="space-y-6">
          <div className="bg-slate-50 dark:bg-slate-900/50 p-4 rounded-2xl border border-slate-100 dark:border-slate-800 max-h-[40vh] overflow-y-auto custom-scrollbar">
            {session.orders.length === 0 ? (
              <p className="text-center py-8 text-slate-400 italic text-sm">Nenhum item lançado.</p>
            ) : (
              session.orders.map((order) => (
                <div key={order.id} className="mb-6 last:mb-0 border-b border-slate-200 dark:border-slate-800 pb-4 last:border-0 last:pb-0">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-tighter">#{order.id.slice(0,6)}</span>
                    <span className={cn(
                      "text-[10px] font-black px-2 py-0.5 rounded uppercase",
                      order.status === 'delivered' ? 'bg-emerald-100 text-emerald-700' : 'bg-orange-100 text-orange-700'
                    )}>
                      {order.status}
                    </span>
                  </div>
                  {order.items.map((item, i) => (
                    <div key={i} className="flex justify-between text-sm mb-2">
                      <div className="flex gap-2">
                        <span className="font-black text-orange-600">{item.quantity}x</span>
                        <span className="text-slate-700 dark:text-slate-300 font-medium">{item.product.name}</span>
                      </div>
                      <span className="font-bold text-slate-900 dark:text-white">{formatCurrency(item.product.price * item.quantity)}</span>
                    </div>
                  ))}
                </div>
              ))
            )}
          </div>

          <div className="space-y-3 pt-2">
            <div className="flex justify-between text-sm text-slate-500 font-bold uppercase tracking-widest">
              <span>Subtotal</span>
              <span>{formatCurrency(subtotal)}</span>
            </div>
            <div className="flex justify-between text-sm text-slate-500 font-bold uppercase tracking-widest">
              <span>Serviço (10%)</span>
              <span className="text-emerald-600">+ {formatCurrency(serviceFee)}</span>
            </div>
            <div className="flex justify-between items-end pt-4 border-t border-slate-100 dark:border-slate-800">
              <span className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Total Geral</span>
              <span className="text-3xl font-black text-slate-900 dark:text-white">{formatCurrency(total)}</span>
            </div>
          </div>

          <div className="flex gap-3">
            <button 
              type="button"
              onClick={onClose} 
              className="flex-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 py-4 rounded-2xl font-black uppercase text-xs hover:bg-slate-200 transition-all"
            >
              Voltar
            </button>
            <button 
              type="button"
              onClick={handleCobrar}
              className="flex-[2] bg-emerald-600 text-white py-4 rounded-2xl font-black uppercase text-xs flex items-center justify-center gap-2 shadow-lg shadow-emerald-900/20 hover:bg-emerald-700 active:scale-95 transition-all"
            >
              <DollarSign size={18} /> Iniciar Cobrança
            </button>
          </div>
        </div>
      ) : (
        <div className="p-12 text-center space-y-4">
          <AlertCircle size={48} className="text-red-500 mx-auto" />
          <p className="text-slate-500 font-bold">Falha ao carregar comanda.</p>
          <button onClick={onClose} className="text-orange-500 font-bold underline">Tentar novamente</button>
        </div>
      )}
    </Modal>
  );
}

