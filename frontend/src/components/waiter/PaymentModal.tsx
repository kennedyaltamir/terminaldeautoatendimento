"use client";

import { useState, useEffect } from "react";
import { X, Banknote, CreditCard, QrCode, CheckCircle2, Loader2, Calculator, Smartphone } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { closeTable } from "@/lib/api";
import { toast } from "sonner";
import ChangeCalculator from "./ChangeCalculator";
import { generatePaymentIntent, detectSmartPOS, PaymentScheme } from "@/lib/smartpos";

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  tableId: number;
  tableName: string;
  totalAmount: number;
  onSuccess: () => void;
}

export default function PaymentModal({ isOpen, onClose, tableId, tableName, totalAmount, onSuccess }: PaymentModalProps) {
  const [method, setMethod] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showCalculator, setShowCalculator] = useState(false);
  const [cashReceived, setCashReceived] = useState<number | null>(null);
  const [smartPosType, setSmartPosType] = useState<PaymentScheme | null>(null);

  useEffect(() => {
    if (isOpen) {
      setSmartPosType(detectSmartPOS());
    }
  }, [isOpen]);

  const handleConfirm = async () => {
    if (!method) return;
    
    // Se for dinheiro e não calculou troco, abre a calculadora
    if (method === 'cash' && cashReceived === null) {
      setShowCalculator(true);
      return;
    }

    // Se for SmartPOS, abre o app de pagamento
    if (smartPosType && method === 'card') {
      const intentUrl = generatePaymentIntent({
        scheme: smartPosType,
        amount: totalAmount,
        type: 'credit', // Default, poderia ser selecionável
        orderId: `MESA-${tableId}`
      });
      window.location.href = intentUrl;
      // Não fecha a mesa automaticamente, espera o garçom confirmar que passou
      return;
    }

    setLoading(true);
    try {
      await closeTable(tableId, method);
      toast.success("Mesa finalizada com sucesso!");
      onSuccess();
      onClose();
    } catch (e) {
      toast.error("Erro ao fechar mesa");
    } finally {
      setLoading(false);
    }
  };

  const handleCalculatorConfirm = (received: number) => {
    setCashReceived(received);
    setShowCalculator(false);
    // Auto-confirma após calcular o troco
    setTimeout(() => handleConfirm(), 500); 
  };

  if (!isOpen) return null;

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} title={`Fechar Conta: ${tableName}`}>
        <div className="space-y-6">
          <div className="bg-gray-900 p-6 rounded-2xl text-center shadow-inner">
            <p className="text-gray-400 text-xs font-bold uppercase tracking-widest mb-1">Total a Receber</p>
            <p className="text-4xl font-black text-white">R$ {totalAmount.toFixed(2)}</p>
          </div>

          <div className="grid grid-cols-3 gap-3">
            {[
              { id: 'cash', label: 'Dinheiro', icon: Banknote, color: 'text-green-500' },
              { id: 'card', label: smartPosType ? 'Maquininha' : 'Cartão', icon: smartPosType ? Smartphone : CreditCard, color: 'text-blue-500' },
              { id: 'pix', label: 'Pix', icon: QrCode, color: 'text-purple-500' },
            ].map((m) => (
              <button
                key={m.id}
                onClick={() => { setMethod(m.id); setCashReceived(null); }}
                className={`flex flex-col items-center justify-center p-4 rounded-xl border-2 transition-all active:scale-95 ${method === m.id ? 'border-orange-500 bg-orange-50 shadow-md ring-2 ring-orange-200' : 'border-gray-100 bg-white text-gray-400 hover:bg-gray-50'}`}
              >
                <m.icon size={28} className={method === m.id ? 'text-orange-600' : m.color} />
                <span className={`text-xs font-bold mt-2 uppercase ${method === m.id ? 'text-orange-700' : ''}`}>{m.label}</span>
              </button>
            ))}
          </div>

          {method === 'cash' && (
            <div className="bg-green-50 border border-green-200 p-4 rounded-xl flex items-center justify-between animate-in slide-in-from-top-2">
              <div className="flex items-center gap-3">
                <div className="bg-green-100 p-2 rounded-full text-green-600">
                  <Calculator size={20} />
                </div>
                <div>
                  <p className="text-sm font-bold text-green-800">Troco</p>
                  <p className="text-xs text-green-600">Calcular troco para o cliente</p>
                </div>
              </div>
              {cashReceived !== null ? (
                 <div className="text-right">
                    <p className="text-xs text-gray-500">Recebido: R$ {cashReceived.toFixed(2)}</p>
                    <p className="font-bold text-green-700">Troco: R$ {(cashReceived - totalAmount).toFixed(2)}</p>
                 </div>
              ) : (
                <button onClick={() => setShowCalculator(true)} className="text-xs bg-green-600 text-white px-3 py-1.5 rounded-lg font-bold hover:bg-green-700">
                  Abrir
                </button>
              )}
            </div>
          )}

          <button
            disabled={!method || loading}
            onClick={handleConfirm}
            className="w-full bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold text-lg shadow-lg flex items-center justify-center gap-2 transition-all active:scale-95"
          >
            {loading ? <Loader2 className="animate-spin" /> : <CheckCircle2 size={24} />}
            {method === 'cash' && cashReceived === null ? 'Calcular & Fechar' : (smartPosType && method === 'card' ? 'Abrir Pagamento' : 'Finalizar Mesa')}
          </button>
        </div>
      </Modal>

      <ChangeCalculator 
        isOpen={showCalculator} 
        onClose={() => setShowCalculator(false)} 
        totalAmount={totalAmount} 
        onConfirm={handleCalculatorConfirm} 
      />
    </>
  );
}