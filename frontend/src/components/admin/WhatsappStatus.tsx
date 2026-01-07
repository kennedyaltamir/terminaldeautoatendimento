"use client";

import { useState, useEffect } from "react";
import { MessageSquare, RefreshCw, CheckCircle2, XCircle, Loader2, AlertCircle } from "lucide-react";
import { getWhatsappStatus } from "@/lib/api";
import Skeleton from "@/components/ui/Skeleton";

export default function WhatsappStatus() {
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const checkStatus = async () => {
    try {
      const data = await getWhatsappStatus();
      setStatus(data.status);
      setError(false);
    } catch (e) {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 10000); // Polling a cada 10s
    return () => clearInterval(interval);
  }, []);

  if (loading) return <Skeleton className="w-full h-24 rounded-2xl" />;

  const isConnected = status === "open";

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6 shadow-xl">
      <div className="flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="flex items-center gap-4">
          <div className={`p-4 rounded-2xl ${isConnected ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
            <MessageSquare size={32} />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Status do WhatsApp</h3>
            <div className="flex items-center gap-2 mt-1">
              {isConnected ? (
                <span className="flex items-center gap-1.5 text-green-500 text-sm font-bold">
                  <CheckCircle2 size={16} /> Conectado
                </span>
              ) : (
                <span className="flex items-center gap-1.5 text-red-500 text-sm font-bold">
                  <XCircle size={16} /> Desconectado
                </span>
              )}
              <span className="text-gray-500 text-xs">• Atualizado agora</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          {!isConnected && (
            <div className="flex-1 md:flex-none bg-yellow-900/20 border border-yellow-800 p-3 rounded-xl flex items-center gap-2 text-yellow-200 text-xs">
              <AlertCircle size={16} className="shrink-0" />
              <span>As notificações automáticas estão pausadas.</span>
            </div>
          )}
          <button 
            onClick={() => { setLoading(true); checkStatus(); }}
            className="bg-gray-700 hover:bg-gray-600 text-white p-3 rounded-xl transition-colors"
            title="Recarregar Status"
          >
            <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
          </button>
        </div>
      </div>
    </div>
  );
}
