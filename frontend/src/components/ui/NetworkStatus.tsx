"use client";

import { useState, useEffect } from "react";
import { WifiOff, Wifi, RefreshCw, AlertTriangle } from "lucide-react";
import { useOfflineSync } from "@/hooks/useOfflineSync";

export default function NetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);
  const { pendingCount, errorCount, isSyncing, syncNow } = useOfflineSync();

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

  // Caso 1: Offline
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

  // Caso 2: Online com Pendências (Sincronizando ou Erro)
  if (pendingCount > 0 || errorCount > 0) {
    return (
      <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-[100] bg-white text-gray-900 px-4 py-2 rounded-full shadow-xl flex items-center gap-3 text-sm font-bold animate-in slide-in-from-bottom-2 border border-orange-200 cursor-pointer" onClick={syncNow}>
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
    );
  }

  return null;
}