/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Indicador de Status de Rede e Sincronização Offline.
 * VERSION: 1.2.0 (Production Hardened)
 */
"use client";
import { useState, useEffect } from "react";
import { WifiOff, Wifi, RefreshCw, AlertTriangle, Trash2 } from "lucide-react";
import { useOfflineSync } from "@/hooks/useOfflineSync";
import { cn } from "@/lib/utils";

export default function NetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);
  const { pendingCount, errorCount, isSyncing, syncNow, clearQueue } = useOfflineSync();

  useEffect(() => {
    setIsOnline(navigator.onLine);
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  if (!isOnline) {
    return (
      <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-[100] bg-gray-900 text-white px-4 py-2 rounded-full shadow-lg flex items-center gap-3 text-sm font-bold animate-in slide-in-from-bottom-2 border border-red-500">
        <WifiOff size={16} className="text-red-500" />
        <span>Modo Offline</span>
        {pendingCount > 0 && (
          <span className="bg-red-600 text-white text-xs px-2 py-0.5 rounded-full">
            {pendingCount} na fila
          </span>
        )}
      </div>
    );
  }

  if (pendingCount > 0 || errorCount > 0) {
    return (
      <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-[100] flex items-center gap-2">
        <div 
          className={cn(
            "bg-white text-gray-900 px-4 py-2 rounded-full shadow-xl flex items-center gap-3 text-sm font-bold border cursor-pointer hover:bg-gray-50 transition-colors",
            errorCount > 0 ? "border-red-200" : "border-orange-200"
          )}
          onClick={() => syncNow()}
        >
          {isSyncing ? (
            <RefreshCw size={16} className="text-blue-500 animate-spin" />
          ) : errorCount > 0 ? (
            <AlertTriangle size={16} className="text-red-500" />
          ) : (
            <Wifi size={16} className="text-orange-500" />
          )}
          <div className="flex flex-col leading-none">
            <span>{isSyncing ? "Sincronizando..." : "Sincronização Pendente"}</span>
            <span className="text-[10px] text-gray-500 font-normal mt-0.5">
              {pendingCount} aguardando • {errorCount} erros
            </span>
          </div>
        </div>
        
        {errorCount > 0 && (
          <button 
            onClick={(e) => { e.stopPropagation(); clearQueue(); }}
            className="bg-red-100 text-red-600 p-2.5 rounded-full shadow-lg hover:bg-red-200 transition-colors border border-red-200"
            title="Limpar Fila de Erros"
          >
            <Trash2 size={16} />
          </button>
        )}
      </div>
    );
  }

  return null;
}
