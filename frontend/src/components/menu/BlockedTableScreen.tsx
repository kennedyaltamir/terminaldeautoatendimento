"use client";
import { Lock } from "lucide-react";

export default function BlockedTableScreen({ customerName }: { customerName: string }) {
  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 text-center text-white">
      <div className="w-24 h-24 bg-red-500/20 rounded-full flex items-center justify-center mb-6 animate-pulse">
        <Lock size={48} className="text-red-500" />
      </div>
      <h1 className="text-3xl font-bold mb-2">Mesa Ocupada</h1>
      <p className="text-gray-400 text-lg">Esta mesa está sendo usada por <span className="text-white font-bold">{customerName}</span>.</p>
      <p className="text-sm text-gray-500 mt-8">Se esta é sua mesa, peça para {customerName} compartilhar o acesso ou chame o garçom.</p>
    </div>
  );
}