"use client";
import { useState } from "react";
import { Lock, Key, ArrowRight, Loader2 } from "lucide-react";
import { joinTable } from "@/lib/api";
import { toast } from "sonner";

export default function BlockedTableScreen({ 
  customerName, 
  tableId, 
  slug, 
  qrToken,
  onSuccess 
}: { 
  customerName: string, 
  tableId: string, 
  slug: string, 
  qrToken: string,
  onSuccess: (token: string) => void
}) {
  const [pin, setPin] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPinInput, setShowPinInput] = useState(false);

  const handleRecover = async () => {
    if (pin.length < 10) return toast.error("Token deve ter 10 dígitos");

    setLoading(true);
    try {
      const session = await joinTable(slug, parseInt(tableId), qrToken, customerName, pin);
      toast.success("Acesso recuperado!");
      onSuccess(session.session_token);
    } catch (e: any) {
      toast.error(e.message || "Token incorreto");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 text-center text-white">
      <div className="w-24 h-24 bg-red-500/20 rounded-full flex items-center justify-center mb-6 animate-pulse">
        <Lock size={48} className="text-red-500" />
      </div>

      <h1 className="text-3xl font-bold mb-2">Mesa Ocupada</h1>
      <p className="text-gray-400 text-lg mb-8">
        Esta mesa está sendo usada por <span className="text-white font-bold">{customerName}</span>.
      </p>

      {!showPinInput ? (
        <div className="space-y-4 w-full max-w-xs">
          <button 
            onClick={() => setShowPinInput(true)}
            className="w-full bg-gray-800 border border-gray-700 hover:bg-gray-700 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-colors"
          >
            <Key size={18} /> Tenho o Token de Acesso
          </button>
          <p className="text-xs text-gray-500">
            Se você é {customerName} e saiu sem querer, peça o Token ao garçom.
          </p>
        </div>
      ) : (
        <div className="w-full max-w-xs animate-in slide-in-from-bottom-4">
          <label className="block text-sm font-bold text-gray-400 mb-2">Digite o Token de 10 dígitos</label>
          <div className="flex gap-2">
            <input 
              type="tel" 
              maxLength={10}
              className="flex-1 bg-gray-800 border border-gray-600 rounded-xl p-3 text-center text-white text-xl font-mono tracking-widest focus:ring-2 focus:ring-orange-500 outline-none"
              placeholder="0000000000"
              value={pin}
              onChange={e => setPin(e.target.value)}
              autoFocus
            />
            <button 
              onClick={handleRecover}
              disabled={loading || pin.length < 10}
              className="bg-orange-600 text-white px-4 rounded-xl font-bold hover:bg-orange-700 disabled:opacity-50 transition-colors"
            >
              {loading ? <Loader2 className="animate-spin" /> : <ArrowRight />}
            </button>
          </div>
          <button 
            onClick={() => setShowPinInput(false)}
            className="text-sm text-gray-500 mt-4 hover:text-white underline"
          >
            Cancelar
          </button>
        </div>
      )}
    </div>
  );
}
