"use client";

import { WifiOff, RefreshCw } from "lucide-react";

export default function OfflinePage() {
  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 text-center text-white">
      <div className="w-24 h-24 bg-gray-800 rounded-full flex items-center justify-center mb-6 animate-pulse">
        <WifiOff size={40} className="text-red-500" />
      </div>
      <h1 className="text-3xl font-bold mb-2">Sem Conexão</h1>
      <p className="text-gray-400 mb-8 max-w-xs">
        Você está offline. Verifique sua internet para continuar recebendo pedidos.
      </p>
      <button 
        onClick={() => window.location.reload()}
        className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-3 rounded-xl font-bold flex items-center gap-2 transition-colors"
      >
        <RefreshCw size={20} /> Tentar Novamente
      </button>
    </div>
  );
}