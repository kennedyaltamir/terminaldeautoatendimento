"use client";

import { useState, useEffect } from "react";
import { Calculator, ArrowRight, Delete, Banknote } from "lucide-react";
import Modal from "@/components/ui/Modal";

interface ChangeCalculatorProps {
  isOpen: boolean;
  onClose: () => void;
  totalAmount: number;
  onConfirm: (received: number) => void;
}

export default function ChangeCalculator({ isOpen, onClose, totalAmount, onConfirm }: ChangeCalculatorProps) {
  const [receivedString, setReceivedString] = useState("");
  
  // Resetar ao abrir
  useEffect(() => {
    if (isOpen) setReceivedString("");
  }, [isOpen]);

  if (!isOpen) return null;

  const handleNumberClick = (num: string) => {
    setReceivedString(prev => prev + num);
  };

  const handleBackspace = () => {
    setReceivedString(prev => prev.slice(0, -1));
  };

  const handleQuickAdd = (amount: number) => {
    setReceivedString(amount.toString());
  };

  const receivedVal = parseFloat(receivedString.replace(",", ".")) || 0;
  const change = receivedVal - totalAmount;
  const isSufficient = change >= 0;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Calculadora de Troco">
      <div className="space-y-6">
        <div className="text-center bg-gray-50 p-4 rounded-xl border border-gray-200">
          <p className="text-gray-500 text-xs font-bold uppercase tracking-widest mb-1">Total da Conta</p>
          <p className="text-3xl font-black text-gray-900">R$ {totalAmount.toFixed(2)}</p>
        </div>

        <div>
          <label className="block text-xs font-bold text-gray-500 uppercase mb-2">Valor Recebido</label>
          <div className="relative">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 font-bold">R$</span>
            <input 
              type="number" 
              readOnly
              className={`w-full bg-white border-2 rounded-xl py-4 pl-12 pr-4 text-2xl font-bold outline-none transition-colors ${isSufficient ? 'border-green-500 text-green-600' : 'border-gray-300 text-gray-900'}`}
              placeholder="0.00"
              value={receivedString}
            />
            {receivedString && (
              <button onClick={handleBackspace} className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-red-500 p-2">
                <Delete size={24} />
              </button>
            )}
          </div>
        </div>

        {/* Sugestões de Notas */}
        <div className="grid grid-cols-4 gap-2">
          {[10, 20, 50, 100].map(val => (
            <button 
              key={val}
              onClick={() => handleQuickAdd(val)}
              className="bg-green-50 hover:bg-green-100 border border-green-200 text-green-700 font-bold py-2 rounded-lg text-sm flex flex-col items-center"
            >
              <span className="text-[10px] opacity-70">Nota</span>
              R$ {val}
            </button>
          ))}
        </div>

        {/* Teclado Numérico */}
        <div className="grid grid-cols-3 gap-2">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, '.', 0].map((key) => (
            <button
              key={key}
              onClick={() => handleNumberClick(key.toString())}
              className="bg-gray-100 hover:bg-gray-200 text-gray-900 font-bold py-4 rounded-xl text-xl active:scale-95 transition-transform"
            >
              {key}
            </button>
          ))}
          <button 
            onClick={() => setReceivedString("")}
            className="bg-red-100 hover:bg-red-200 text-red-600 font-bold py-4 rounded-xl text-sm uppercase"
          >
            Limpar
          </button>
        </div>

        {/* Resultado do Troco */}
        <div className={`p-4 rounded-xl text-center transition-all duration-300 ${isSufficient ? 'bg-green-600 text-white shadow-lg scale-105' : 'bg-gray-200 text-gray-400'}`}>
          <p className="text-xs font-bold uppercase mb-1 opacity-80">{isSufficient ? "Troco a Devolver" : "Faltam"}</p>
          <p className="text-3xl font-black">R$ {Math.abs(change).toFixed(2)}</p>
        </div>

        <button
          disabled={!isSufficient}
          onClick={() => onConfirm(receivedVal)}
          className="w-full bg-gray-900 hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold text-lg shadow-xl flex items-center justify-center gap-2 transition-all"
        >
          Confirmar Pagamento <ArrowRight size={20} />
        </button>
      </div>
    </Modal>
  );
}