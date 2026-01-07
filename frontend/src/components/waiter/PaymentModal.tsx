"use client";

import { useState, useEffect } from "react";
import { X, Banknote, CreditCard, QrCode, CheckCircle2, Loader2, Calculator, Smartphone, Copy, Edit2, Split } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { closeTable, payTableSession } from "@/lib/api";
import { toast } from "sonner";
import ChangeCalculator from "./ChangeCalculator";
import { QRCodeSVG } from "qrcode.react";
import { openCashDrawer } from "@/lib/printer/driver";

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  tableId: number;
  tableName: string;
  totalAmount: number;
  onSuccess: () => void;
  isPartial?: boolean;
}

export default function PaymentModal({ isOpen, onClose, tableId, tableName, totalAmount, onSuccess, isPartial = false }: PaymentModalProps) {
  const [method, setMethod] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showCalculator, setShowCalculator] = useState(false);
  const [cashReceived, setCashReceived] = useState<number | null>(null);
  const [pixData, setPixData] = useState<any>(null);

  const [tipMode, setTipMode] = useState<'percent' | 'fixed'>('percent');
  const [tipValue, setTipValue] = useState(10);
  const [isEditingTip, setIsEditingTip] = useState(false);

  useEffect(() => {
    if (!isOpen) {
        setMethod(null);
        setPixData(null);
        setCashReceived(null);
        setTipValue(10);
        setTipMode('percent');
        setIsEditingTip(false);
    }
  }, [isOpen]);

  const subtotal = totalAmount;
  
  const tipAmount = (!isPartial && tipMode === 'percent')
    ? (subtotal * (tipValue / 100)) 
    : (!isPartial ? tipValue : 0);
    
  const finalTotal = subtotal + tipAmount;

  const handleConfirm = async () => {
    if (!method) return;

    if (method === 'cash' && cashReceived === null) {
      setShowCalculator(true);
      return;
    }

    setLoading(true);
    try {
      if (isPartial) {
        await payTableSession(tableId, finalTotal, method);
        toast.success(`Pagamento de R$ ${finalTotal.toFixed(2)} registrado!`);
      } else {
        const res = await closeTable(tableId, method, tipAmount);
        if (method === 'pix' && res.pix_data) {
            setPixData(res.pix_data);
            toast.success("QR Code Pix gerado!");
            setLoading(false);
            return;
        }
        toast.success("Mesa finalizada com sucesso!");
      }
      
      // GAVETA DE DINHEIRO
      if (method === 'cash') {
        openCashDrawer();
        toast.info("Abrindo gaveta...");
      }
      
      onSuccess();
      onClose();
    } catch (e: any) {
      toast.error(e.message || "Erro ao processar pagamento");
    } finally {
      setLoading(false);
    }
  };

  const handleFinalizeAfterPix = () => {
    toast.success("Pagamento confirmado pelo staff!");
    onSuccess();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose} title={isPartial ? `Pagamento Parcial: ${tableName}` : `Fechar Conta: ${tableName}`}>
        <div className="space-y-6">
          {pixData ? (
            <div className="text-center space-y-6 animate-in zoom-in">
                <div className="bg-gray-900 p-4 rounded-2xl inline-block border-4 border-orange-500 shadow-xl">
                    <QRCodeSVG value={pixData.qr_code} size={200} />
                </div>
                <div>
                    <p className="text-gray-400 text-xs font-bold uppercase mb-2">Valor do Pix</p>
                    <p className="text-3xl font-black text-white">R$ {finalTotal.toFixed(2)}</p>
                </div>
                <button 
                    onClick={() => { navigator.clipboard.writeText(pixData.qr_code); toast.success("Copiado!"); }}
                    className="w-full bg-gray-800 text-gray-300 py-3 rounded-xl font-bold flex items-center justify-center gap-2 border border-gray-700"
                >
                    <Copy size={18} /> Copiar Código Pix
                </button>
                <button 
                    onClick={handleFinalizeAfterPix}
                    className="w-full bg-green-600 text-white py-4 rounded-xl font-black text-lg shadow-lg shadow-green-900/20"
                >
                    Confirmar Recebimento
                </button>
            </div>
          ) : (
            <>
              <div className="bg-gray-900 p-6 rounded-2xl shadow-inner space-y-4">
                <div className="flex justify-between text-gray-400 text-sm">
                    <span>{isPartial ? "Valor Selecionado" : "Subtotal"}</span>
                    <span>R$ {subtotal.toFixed(2)}</span>
                </div>

                {!isPartial && (
                    <>
                        <div className="flex justify-between items-center text-gray-400 text-sm border-b border-gray-700 pb-4">
                            <div className="flex items-center gap-2">
                                <span>Serviço ({tipMode === 'percent' ? `${tipValue}%` : 'Fixo'})</span>
                                <button onClick={() => setIsEditingTip(!isEditingTip)} className="bg-gray-800 p-1 rounded hover:bg-gray-700 text-orange-500">
                                    <Edit2 size={12} />
                                </button>
                            </div>
                            <span className="text-orange-400">+ R$ {tipAmount.toFixed(2)}</span>
                        </div>

                        {isEditingTip && (
                            <div className="bg-gray-800 p-3 rounded-lg animate-in slide-in-from-top-2">
                                <div className="flex gap-2 mb-2">
                                    <button onClick={() => { setTipMode('percent'); setTipValue(10); }} className={`flex-1 py-1 text-xs rounded ${tipMode === 'percent' && tipValue === 10 ? 'bg-orange-600 text-white' : 'bg-gray-700 text-gray-300'}`}>10%</button>
                                    <button onClick={() => { setTipMode('percent'); setTipValue(12); }} className={`flex-1 py-1 text-xs rounded ${tipMode === 'percent' && tipValue === 12 ? 'bg-orange-600 text-white' : 'bg-gray-700 text-gray-300'}`}>12%</button>
                                    <button onClick={() => { setTipMode('percent'); setTipValue(0); }} className={`flex-1 py-1 text-xs rounded ${tipValue === 0 ? 'bg-red-600 text-white' : 'bg-gray-700 text-gray-300'}`}>0%</button>
                                </div>
                                <div className="flex items-center gap-2">
                                    <span className="text-xs text-gray-500">Outro:</span>
                                    <input 
                                        type="number" 
                                        className="bg-gray-900 border border-gray-600 rounded px-2 py-1 text-white text-sm w-20"
                                        value={tipValue}
                                        onChange={(e) => setTipValue(Number(e.target.value))}
                                    />
                                    <select 
                                        className="bg-gray-900 border border-gray-600 rounded px-2 py-1 text-white text-sm"
                                        value={tipMode}
                                        onChange={(e) => setTipMode(e.target.value as any)}
                                    >
                                        <option value="percent">%</option>
                                        <option value="fixed">R$</option>
                                    </select>
                                </div>
                            </div>
                        )}
                    </>
                )}

                <div className="flex justify-between items-end pt-2">
                    <span className="text-gray-400 text-xs font-bold uppercase tracking-widest mb-1">Total a Pagar</span>
                    <p className="text-4xl font-black text-white">R$ {finalTotal.toFixed(2)}</p>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                {[
                  { id: 'cash', label: 'Dinheiro', icon: Banknote, color: 'text-green-500' },
                  { id: 'card', label: 'Cartão', icon: CreditCard, color: 'text-blue-500' },
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

              {method === 'cash' && cashReceived !== null && (
                 <div className="bg-green-50 border border-green-200 p-4 rounded-xl text-center animate-in slide-in-from-top-2">
                    <p className="text-xs text-gray-500 font-bold uppercase">Troco a devolver</p>
                    <p className="font-black text-2xl text-green-700">R$ {(cashReceived - finalTotal).toFixed(2)}</p>
                 </div>
              )}

              <button
                disabled={!method || loading}
                onClick={handleConfirm}
                className={`w-full text-white py-4 rounded-xl font-bold text-lg shadow-lg flex items-center justify-center gap-2 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed ${isPartial ? 'bg-blue-600 hover:bg-blue-700' : 'bg-orange-600 hover:bg-orange-700'}`}
              >
                {loading ? <Loader2 className="animate-spin" /> : isPartial ? <Split size={24} /> : <CheckCircle2 size={24} />}
                {method === 'pix' ? 'Gerar QR Code' : isPartial ? 'Pagar Parcial' : 'Finalizar Mesa'}
              </button>
            </>
          )}
        </div>
      </Modal>

      <ChangeCalculator 
        isOpen={showCalculator} 
        onClose={() => setShowCalculator(false)} 
        totalAmount={finalTotal} 
        onConfirm={(received) => { setCashReceived(received); setShowCalculator(false); }} 
      />
    </>
  );
}
