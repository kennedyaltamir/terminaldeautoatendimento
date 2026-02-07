"use client";

import { Wallet, ChevronRight } from "lucide-react";

interface WalletWidgetProps {
  balance: number;
  loyaltyPercent: number;
  customerPhone: string;
  onUseBalance: (use: boolean) => void;
  useBalance: boolean;
}

export default function WalletWidget({ balance, loyaltyPercent, customerPhone, onUseBalance, useBalance }: WalletWidgetProps) {
  if (!customerPhone || customerPhone.length < 8) {
    return (
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-4 rounded-xl text-white shadow-lg mb-6 animate-in fade-in">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 p-2 rounded-full">
            <Wallet size={20} />
          </div>
          <div className="flex-1">
            <p className="font-bold text-sm">Ganhe Cashback!</p>
            <p className="text-xs text-purple-100">Informe seu telefone no carrinho para ganhar {loyaltyPercent}% de volta.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-purple-100 p-4 rounded-xl shadow-sm mb-6 animate-in slide-in-from-top-2">
      <div className="flex justify-between items-center mb-3">
        <div className="flex items-center gap-2">
          <div className="bg-purple-100 p-2 rounded-full text-purple-600">
            <Wallet size={18} />
          </div>
          <div>
            <p className="text-xs text-gray-500 font-bold uppercase">Seu Saldo</p>
            <p className="text-xl font-black text-gray-900">R$ {Number(balance).toFixed(2)}</p>
          </div>
        </div>
        <div className="text-right">
          <span className="bg-purple-100 text-purple-700 text-xs font-bold px-2 py-1 rounded-full">
            {loyaltyPercent}% Cashback
          </span>
        </div>
      </div>

      {balance > 0 && (
        <label className="flex items-center justify-between bg-gray-50 p-3 rounded-lg cursor-pointer border border-gray-200 hover:border-purple-300 transition-colors">
          <span className="text-sm font-medium text-gray-700">Usar saldo neste pedido?</span>
          <div className="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" className="sr-only peer" checked={useBalance} onChange={(e) => onUseBalance(e.target.checked)} />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
          </div>
        </label>
      )}
    </div>
  );
}