"use client";
import React, { useState } from "react";
import { 
  CreditCard, Banknote, QrCode, 
  CheckCircle2, Loader2, ArrowRight, ArrowLeft
} from "lucide-react";
import Modal from "@/components/ui/Modal";
import { formatCurrency, cn } from "@/lib/utils";
import { payTableSession } from "@/lib/api";
import { toast } from "sonner";
import { CartItem } from "@/types"; 
import ChangeCalculator from "./ChangeCalculator";

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  tableId: number;
  tableName?: string;
  totalAmount: number;
  items?: CartItem[]; 
  onSuccess: () => void;
}

export default function PaymentModal({ 
  isOpen, 
  onClose, 
  tableId, 
  tableName, 
  totalAmount, 
  items,
  onSuccess 
}: PaymentModalProps) {
  const [method, setMethod] = useState<'cash' | 'card' | 'pix' | null>(null);
  const [loading, setLoading] = useState(false);
  const [showCalculator, setShowCalculator] = useState(false);

  const handlePayment = async (receivedAmount?: number) => {
    if (!method) return;
    setLoading(true);
    try {
      await payTableSession(tableId, receivedAmount || totalAmount, method);
      // 🛡️ FIX: Removido log de auditoria residual
      toast.success("Pagamento registrado!");
      onSuccess();
      onClose();
    } catch (e) {
      toast.error("Erro ao processar pagamento.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <Modal 
      isOpen={isOpen} 
      onClose={onClose} 
      title={`Pagamento: ${tableName || `Mesa ${tableId}`}`}
    >
      <div className="space-y-6">
        <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 text-center">
          <p className="text-xs text-slate-500 font-black uppercase tracking-widest mb-1">Total a Receber</p>
          <p className="text-4xl font-black text-white">{formatCurrency(totalAmount)}</p>
        </div>

        <div className="grid grid-cols-1 gap-3">
          <button 
            onClick={() => { setMethod('cash'); setShowCalculator(true); }}
            className="flex items-center justify-between p-5 bg-slate-800 hover:bg-slate-700 rounded-2xl border border-slate-700 transition-all group"
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-emerald-500/10 text-emerald-500 rounded-xl group-hover:scale-110 transition-transform">
                <Banknote size={24} />
              </div>
              <span className="font-bold text-white">Dinheiro</span>
            </div>
            <ArrowRight size={20} className="text-slate-600" />
          </button>

          <button 
            onClick={() => setMethod('card')}
            className={cn(
              "flex items-center justify-between p-5 bg-slate-800 hover:bg-slate-700 rounded-2xl border border-slate-700 transition-all group",
              method === 'card' && "border-blue-500 ring-1 ring-blue-500"
            )}
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-500/10 text-blue-500 rounded-xl group-hover:scale-110 transition-transform">
                <CreditCard size={24} />
              </div>
              <span className="font-bold text-white">Cartão</span>
            </div>
            <ArrowRight size={20} className="text-slate-600" />
          </button>

          <button 
            onClick={() => setMethod('pix')}
            className={cn(
              "flex items-center justify-between p-5 bg-slate-800 hover:bg-slate-700 rounded-2xl border border-slate-700 transition-all group",
              method === 'pix' && "border-purple-500 ring-1 ring-purple-500"
            )}
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-500/10 text-purple-500 rounded-xl group-hover:scale-110 transition-transform">
                <QrCode size={24} />
              </div>
              <span className="font-bold text-white">Pix</span>
            </div>
            <ArrowRight size={20} className="text-slate-600" />
          </button>
        </div>

        {method && method !== 'cash' && (
          <button 
            onClick={() => handlePayment()}
            disabled={loading}
            className="w-full py-5 bg-orange-600 hover:bg-orange-500 text-white rounded-2xl font-black uppercase tracking-widest shadow-xl transition-all flex items-center justify-center gap-3"
          >
            {loading ? <Loader2 className="animate-spin" /> : <CheckCircle2 />}
            Confirmar Recebimento
          </button>
        )}
      </div>

      <ChangeCalculator 
        isOpen={showCalculator}
        onClose={() => setShowCalculator(false)}
        totalAmount={totalAmount}
        onConfirm={(received) => handlePayment(received)}
      />
    </Modal>
  );
}
