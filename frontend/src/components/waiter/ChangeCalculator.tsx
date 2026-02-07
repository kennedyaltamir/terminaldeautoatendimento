"use client";
/**
 * DOMAIN: FRONTEND
 * FILE: src/components/waiter/ChangeCalculator.tsx
 * OBJECTIVE: Interface numérica para cálculo rápido de troco em dispositivos touch.
 */
import { useState, useEffect } from "react";
import { Delete, Check, X } from "lucide-react";
import { formatCurrency } from "@/lib/utils";
import Modal from "@/components/ui/Modal";

interface ChangeCalculatorProps {
  isOpen: boolean;
  onClose: () => void;
  totalAmount: number;
  onConfirm: (received: number) => void;
}

export default function ChangeCalculator({ isOpen, onClose, totalAmount, onConfirm }: ChangeCalculatorProps) {
  const [input, setInput] = useState("");
  
  // Sugestões inteligentes de pagamento (ex: se total é 45, sugere 50 e 100)
  const suggestions = [
    Math.ceil(totalAmount / 10) * 10,
    Math.ceil(totalAmount / 50) * 50,
    Math.ceil(totalAmount / 100) * 100
  ].filter((v, i, a) => v >= totalAmount && a.indexOf(v) === i); // Remove duplicatas e valores menores

  useEffect(() => {
    if (isOpen) setInput("");
  }, [isOpen]);

  const handlePress = (val: string) => {
    if (val === "." && input.includes(".")) return;
    // Limita casas decimais
    if (input.includes(".") && input.split(".")[1].length >= 2) return;
    setInput(prev => prev + val);
  };

  const handleDelete = () => {
    setInput(prev => prev.slice(0, -1));
  };

  const handleConfirm = () => {
    const val = parseFloat(input);
    if (!isNaN(val) && val >= totalAmount) {
      onConfirm(val);
    }
  };

  const received = parseFloat(input) || 0;
  const change = received - totalAmount;
  const isSufficient = received >= totalAmount;

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Calculadora de Troco">
      <div className="space-y-6">
        {/* Display */}
        <div className="bg-slate-100 p-4 rounded-2xl text-right border-2 border-slate-200">
          <p className="text-xs text-slate-500 font-bold uppercase mb-1">Valor Recebido</p>
          <div className={`text-4xl font-black tracking-tight ${isSufficient ? 'text-slate-900' : 'text-red-500'}`}>
            R$ {input || "0,00"}
          </div>
        </div>

        {/* Info de Troco */}
        <div className="flex justify-between items-center px-2">
          <div className="text-left">
            <p className="text-xs text-slate-400 font-bold uppercase">Total da Conta</p>
            <p className="text-lg font-bold text-slate-700">{formatCurrency(totalAmount)}</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-slate-400 font-bold uppercase">Troco</p>
            <p className={`text-2xl font-black ${change >= 0 ? 'text-green-600' : 'text-slate-300'}`}>
              {change >= 0 ? formatCurrency(change) : "---"}
            </p>
          </div>
        </div>

        {/* Sugestões Rápidas */}
        <div className="flex gap-2">
          <button 
            onClick={() => setInput(totalAmount.toString())}
            className="flex-1 py-2 bg-blue-50 text-blue-700 rounded-lg text-xs font-bold border border-blue-100 hover:bg-blue-100"
          >
            Exato
          </button>
          {suggestions.map(s => (
            <button 
              key={s}
              onClick={() => setInput(s.toString())}
              className="flex-1 py-2 bg-slate-50 text-slate-700 rounded-lg text-xs font-bold border border-slate-200 hover:bg-slate-100"
            >
              {formatCurrency(s)}
            </button>
          ))}
        </div>

        {/* Teclado Numérico */}
        <div className="grid grid-cols-3 gap-3">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(num => (
            <button
              key={num}
              onClick={() => handlePress(num.toString())}
              className="h-14 bg-white border border-slate-200 rounded-xl text-2xl font-bold text-slate-700 shadow-sm active:bg-slate-50 active:scale-95 transition-all"
            >
              {num}
            </button>
          ))}
          <button onClick={() => handlePress(".")} className="h-14 bg-slate-50 border border-slate-200 rounded-xl text-2xl font-bold text-slate-500">.</button>
          <button onClick={() => handlePress("0")} className="h-14 bg-white border border-slate-200 rounded-xl text-2xl font-bold text-slate-700 shadow-sm active:bg-slate-50">0</button>
          <button onClick={handleDelete} className="h-14 bg-red-50 border border-red-100 rounded-xl flex items-center justify-center text-red-500 active:bg-red-100">
            <Delete size={24} />
          </button>
        </div>

        {/* Ações */}
        <div className="flex gap-3 pt-2">
          <button onClick={onClose} className="flex-1 py-4 rounded-xl font-bold text-slate-500 hover:bg-slate-100">
            Cancelar
          </button>
          <button 
            onClick={handleConfirm}
            disabled={!isSufficient}
            className="flex-[2] bg-green-600 disabled:bg-slate-300 text-white py-4 rounded-xl font-black uppercase tracking-widest shadow-lg active:scale-95 transition-all flex items-center justify-center gap-2"
          >
            <Check size={20} /> Confirmar
          </button>
        </div>
      </div>
    </Modal>
  );
}
