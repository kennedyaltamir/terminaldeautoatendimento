"use client";
/**
 * DOMAIN: FRONTEND
 * FILE: src/components/waiter/BillAuditModal.tsx
 * OBJECTIVE: Detalhamento da comanda antes do pagamento.
 */
import { useState, useEffect } from "react";
import { DollarSign, AlertCircle, Receipt, Clock } from "lucide-react";
import { getSessionDetails } from "@/lib/api";
import { TableSession } from "@/types";
import Modal from "@/components/ui/Modal";
import { formatCurrency, cn } from "@/lib/utils";
import Skeleton from "@/components/ui/Skeleton";

interface BillAuditModalProps {
  isOpen: boolean;
  onClose: () => void;
  sessionId: number;
  tableName: string;
  onPayRequest?: (amount: number) => void;
}

export default function BillAuditModal({ 
  isOpen, 
  onClose, 
  sessionId, 
  tableName, 
  onPayRequest 
}: BillAuditModalProps) {
  const [session, setSession] = useState<TableSession | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen && sessionId) {
      setLoading(true);
      getSessionDetails(sessionId.toString())
        .then(setSession)
        .catch(console.error)
        .finally(() => setLoading(false));
    } else {
      setSession(null);
    }
  }, [isOpen, sessionId]);

  // Cálculos
  const subtotal = session ? Number(session.total_spent) : 0;
  const serviceFee = subtotal * 0.10; // 10% padrão (pode vir do backend no futuro)
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
        <div className="p-6 space-y-4">
          <Skeleton className="w-full h-12 rounded-xl" />
          <Skeleton className="w-full h-32 rounded-xl" />
          <Skeleton className="w-full h-12 rounded-xl" />
        </div>
      ) : session ? (
        <div className="space-y-6">
          {/* Cabeçalho da Sessão */}
          <div className="flex items-center justify-between text-xs text-gray-500 px-1">
            <span className="flex items-center gap-1"><Clock size={12}/> {new Date(session.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
            <span className="font-bold uppercase">{session.customer_name}</span>
          </div>

          {/* Lista de Itens */}
          <div className="bg-slate-50 dark:bg-slate-900/50 p-4 rounded-2xl border border-slate-100 dark:border-slate-800 max-h-[40vh] overflow-y-auto custom-scrollbar">
            {session.orders.length === 0 ? (
              <p className="text-center text-gray-400 text-sm py-4">Nenhum pedido lançado.</p>
            ) : (
              session.orders.map((order) => (
                <div key={order.id} className="mb-4 last:mb-0 border-b border-slate-200 dark:border-slate-700 pb-4 last:border-0 last:pb-0">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-wider">#{order.id.slice(0,6)}</span>
                    <span className={cn(
                      "text-[10px] font-bold px-2 py-0.5 rounded uppercase",
                      order.status === 'delivered' ? 'bg-emerald-100 text-emerald-700' : 'bg-orange-100 text-orange-700'
                    )}>
                      {order.status}
                    </span>
                  </div>
                  {order.items.map((item, i) => (
                    <div key={i} className="flex justify-between text-sm mb-1">
                      <span className="text-slate-700 dark:text-slate-300 font-medium">
                        {item.quantity}x {item.product.name}
                      </span>
                      <span className="font-bold text-slate-900 dark:text-white">
                        {formatCurrency(item.product.price * item.quantity)}
                      </span>
                    </div>
                  ))}
                </div>
              ))
            )}
          </div>

          {/* Totais */}
          <div className="space-y-2 pt-2">
            <div className="flex justify-between text-sm text-gray-500">
              <span>Subtotal</span>
              <span>{formatCurrency(subtotal)}</span>
            </div>
            <div className="flex justify-between text-sm text-gray-500">
              <span>Serviço (10%)</span>
              <span>{formatCurrency(serviceFee)}</span>
            </div>
            <div className="flex justify-between items-end pt-2 border-t border-dashed border-gray-200">
              <span className="text-sm font-black text-slate-900 uppercase">Total Final</span>
              <span className="text-3xl font-black text-emerald-600">{formatCurrency(total)}</span>
            </div>
          </div>

          {/* Ação */}
          <button 
            onClick={handleCobrar}
            className="w-full bg-slate-900 hover:bg-slate-800 text-white py-4 rounded-xl font-black uppercase text-xs flex items-center justify-center gap-2 shadow-lg active:scale-95 transition-all"
          >
            <DollarSign size={18} /> Ir para Pagamento
          </button>
        </div>
      ) : (
        <div className="p-12 text-center flex flex-col items-center">
          <AlertCircle size={48} className="text-red-400 mb-4 opacity-50" />
          <p className="text-slate-500 font-bold">Falha ao carregar comanda.</p>
          <button onClick={onClose} className="mt-4 text-orange-600 font-bold text-sm hover:underline">Fechar</button>
        </div>
      )}
    </Modal>
  );
}
