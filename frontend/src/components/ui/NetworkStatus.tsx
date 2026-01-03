"use client";

import { useState, useEffect } from "react";
import { WifiOff, Wifi } from "lucide-react";

export default function NetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);
  const [showBackOnline, setShowBackOnline] = useState(false);

  useEffect(() => {
    // Definir estado inicial (apenas no cliente)
    setIsOnline(navigator.onLine);

    const handleOnline = () => {
      setIsOnline(true);
      setShowBackOnline(true);
      setTimeout(() => setShowBackOnline(false), 3000); // Esconde msg de "Voltou" após 3s
    };

    const handleOffline = () => {
      setIsOnline(false);
    };

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  if (!isOnline) {
    return (
      <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-[100] bg-gray-900 text-white px-4 py-2 rounded-full shadow-lg flex items-center gap-2 text-sm font-bold animate-in slide-in-from-bottom-2">
        <WifiOff size={16} className="text-red-500" />
        <span>Sem conexão. Tentando reconectar...</span>
      </div>
    );
  }

  if (showBackOnline) {
    return (
      <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-[100] bg-green-600 text-white px-4 py-2 rounded-full shadow-lg flex items-center gap-2 text-sm font-bold animate-in slide-in-from-bottom-2 fade-out duration-1000">
        <Wifi size={16} />
        <span>Conexão restaurada!</span>
      </div>
    );
  }

  return null;
}