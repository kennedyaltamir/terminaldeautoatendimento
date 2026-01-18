// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 21:45:00
"use client";
import { useState, useEffect } from "react";
import { DollarSign, AlertCircle } from "lucide-react";
import { getSessionDetails } from "@/lib/api";
import { TableSession } from "@/types";
import Modal from "@/components/ui/Modal";
import { formatCurrency, cn } from "@/lib/utils";

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
      getSessionDetails(sessionId.toString())
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
        <div className="p-12 text-center">
          <p className="text-slate-500 font-bold animate-pulse">Sincronizando comanda...</p>
        </div>
      ) : session ? (
        <div className="space-y-6">
          <div className="bg-slate-50 dark:bg-slate-900/50 p-4 rounded-2xl border border-slate-100 dark:border-slate-800 max-h-[40vh] overflow-y-auto">
            {session.orders.map((order) => (
              <div key={order.id} className="mb-6 last:mb-0 border-b border-slate-200 dark:border-slate-800 pb-4 last:border-0 last:pb-0">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-[10px] font-black text-slate-400 uppercase">#{order.id.slice(0,6)}</span>
                  <span className={cn(
                    "text-[10px] font-black px-2 py-0.5 rounded uppercase",
                    order.status === 'delivered' ? 'bg-emerald-100 text-emerald-700' : 'bg-orange-100 text-orange-700'
                  )}>
                    {order.status}
                  </span>
                </div>
                {order.items.map((item, i) => (
                  <div key={i} className="flex justify-between text-sm mb-2">
                    <span className="text-slate-700 dark:text-slate-300">{item.quantity}x {item.product.name}</span>
                    <span className="font-bold text-slate-900 dark:text-white">{formatCurrency(item.product.price * item.quantity)}</span>
                  </div>
                ))}
              </div>
            ))}
          </div>
          <div className="flex justify-between items-end pt-4 border-t border-slate-100 dark:border-slate-800">
            <span className="text-xs font-black text-slate-400 uppercase">Total Geral</span>
            <span className="text-3xl font-black text-slate-900 dark:text-white">{formatCurrency(total)}</span>
          </div>
          <button 
            onClick={handleCobrar}
            className="w-full bg-emerald-600 text-white py-4 rounded-2xl font-black uppercase text-xs flex items-center justify-center gap-2 shadow-lg"
          >
            <DollarSign size={18} /> Iniciar Cobrança
          </button>
        </div>
      ) : (
        <div className="p-12 text-center">
          <AlertCircle size={48} className="text-red-500 mx-auto" />
          <p className="text-slate-500 font-bold">Falha ao carregar comanda.</p>
        </div>
      )}
    </Modal>
  );
}

