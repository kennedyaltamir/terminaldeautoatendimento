"use client";
/**
 * DOMAIN: FRONTEND
 * COMPONENT: PublicMonitorView
 * OBJECTIVE: Exibição pública de pedidos (KDS Viewer) com proteção contra Hydration Mismatch.
 * STATUS: HARDENED (L6)
 */
import React, { useEffect, useState, useRef, useCallback } from "react";
import { getPublicMonitorOrders } from "@/lib/api";
import { useWebSocket } from "@/hooks/useWebSocket";
import { motion, AnimatePresence } from "framer-motion";
import { Clock, ChefHat, CheckCircle2, AlertCircle } from "lucide-react";

interface MonitorOrder {
  id: string;
  display_id: string;
  status: string;
  customer_name: string | null;
}

export default function PublicMonitorView({ slug }: { slug: string }) {
  // STATE: Inicialização segura
  const [orders, setOrders] = useState<MonitorOrder[]>([]);
  const [time, setTime] = useState<string | null>(null); // Null inicial para evitar mismatch
  const [error, setError] = useState<boolean>(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // FETCH: Busca de dados com tratamento de erro robusto
  const fetchOrders = useCallback(async () => {
    try {
      const data = await getPublicMonitorOrders(slug);
      if (Array.isArray(data)) {
        setOrders(data);
        setError(false);
      } else {
        console.warn("[Monitor] Formato de dados inválido recebido:", data);
        setOrders([]);
      }
    } catch (e) {
      console.error("[Monitor] Erro de conexão:", e);
      setError(true);
    }
  }, [slug]);

  // EFFECT: Relógio e Polling
  useEffect(() => {
    fetchOrders();
    
    // Relógio (Client-side only para evitar mismatch)
    const updateClock = () => {
      setTime(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    };
    
    // Primeira execução imediata no cliente
    updateClock();
    const timer = setInterval(updateClock, 1000);

    // Polling de segurança (caso WS falhe)
    const polling = setInterval(fetchOrders, 15000);

    return () => {
      clearInterval(timer);
      clearInterval(polling);
    };
  }, [fetchOrders]);

  // WEBSOCKET: Atualização em tempo real
  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "new_order") {
      // Toca som apenas se houver um pedido pronto novo
      if (data.status === "ready" && audioRef.current) {
        // 🛡️ FIX: console.log -> console.warn para erros de autoplay
        audioRef.current.play().catch((err) => console.warn("Autoplay bloqueado:", err));
      }
      fetchOrders();
    }
  });

  // FILTROS: Memorização implícita via renderização
  const preparing = orders.filter(o => ["pending", "preparing", "accepted"].includes(o.status));
  const ready = orders.filter(o => o.status === "ready");

  return (
    <div className="h-screen flex flex-col bg-gray-950 text-white font-sans overflow-hidden selection:bg-orange-500 selection:text-white">
      <audio ref={audioRef} src="/notification.mp3" preload="auto" />
      
      {/* HEADER */}
      <header className="p-6 md:p-8 bg-gray-900 border-b border-gray-800 flex justify-between items-center shadow-lg z-10">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg shadow-orange-900/20">
            <ChefHat size={40} className="text-white" />
          </div>
          <div>
            <h1 className="text-3xl md:text-4xl font-black tracking-tighter uppercase leading-none">
              Acompanhe seu Pedido
            </h1>
            <p className="text-gray-500 text-sm font-bold tracking-widest uppercase mt-1">
              Status em Tempo Real
            </p>
          </div>
        </div>
        <div className="text-right min-w-[150px]">
          {/* Renderização condicional segura para evitar Hydration Mismatch */}
          {time ? (
            <p className="text-4xl md:text-5xl font-mono font-bold text-gray-400 animate-in fade-in">
              {time}
            </p>
          ) : (
            <div className="h-12 w-32 bg-gray-800 rounded-lg animate-pulse" />
          )}
        </div>
      </header>

      {/* MAIN CONTENT */}
      <div className="flex-1 flex relative">
        {error && (
          <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-red-900/80 text-white px-6 py-2 rounded-full flex items-center gap-2 text-sm font-bold backdrop-blur-md z-50">
            <AlertCircle size={16} /> Tentando reconectar...
          </div>
        )}

        {/* COLUNA: PREPARANDO */}
        <div className="flex-1 border-r border-gray-800 bg-gray-900/30 flex flex-col">
          <div className="p-6 bg-gray-900/50 border-b border-gray-800 flex items-center gap-3 sticky top-0 z-10">
            <Clock size={28} className="text-orange-500" />
            <h2 className="text-2xl font-black uppercase text-orange-500 tracking-wide">Preparando</h2>
            <span className="bg-gray-800 text-gray-400 px-3 py-1 rounded-full text-xs font-bold ml-auto">
              {preparing.length}
            </span>
          </div>
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 overflow-y-auto content-start">
            <AnimatePresence mode="popLayout">
              {preparing.map((order) => (
                <motion.div
                  key={order.id}
                  layout
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.5 }}
                  className="bg-gray-800/50 border border-gray-700 p-6 rounded-3xl flex flex-col items-center justify-center relative overflow-hidden group"
                >
                  <span className="text-4xl md:text-5xl font-black text-gray-300 group-hover:text-white transition-colors">
                    {order.display_id}
                  </span>
                  <span className="text-xs text-gray-500 mt-2 font-bold uppercase truncate w-full text-center group-hover:text-orange-400 transition-colors">
                    {order.customer_name || "Cliente"}
                  </span>
                </motion.div>
              ))}
            </AnimatePresence>
            {preparing.length === 0 && !error && (
              <div className="col-span-full text-center py-20 text-gray-600 font-medium">
                A cozinha está aguardando novos pedidos.
              </div>
            )}
          </div>
        </div>

        {/* COLUNA: PRONTO */}
        <div className="flex-1 bg-green-950/5 flex flex-col">
          <div className="p-6 bg-green-900/10 border-b border-green-900/20 flex items-center gap-3 sticky top-0 z-10">
            <CheckCircle2 size={28} className="text-green-500" />
            <h2 className="text-2xl font-black uppercase text-green-500 tracking-wide">Pronto</h2>
            <span className="bg-green-900/30 text-green-400 px-3 py-1 rounded-full text-xs font-bold ml-auto">
              {ready.length}
            </span>
          </div>
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-2 gap-6 overflow-y-auto content-start">
            <AnimatePresence mode="popLayout">
              {ready.map((order) => (
                <motion.div
                  key={order.id}
                  layout
                  initial={{ scale: 0.8, opacity: 0, y: 20 }}
                  animate={{ scale: 1, opacity: 1, y: 0 }}
                  exit={{ scale: 1.1, opacity: 0 }}
                  transition={{ type: "spring", stiffness: 300, damping: 25 }}
                  className="bg-green-600 p-8 rounded-[2.5rem] shadow-[0_10px_40px_rgba(22,163,74,0.3)] flex flex-col items-center justify-center border-4 border-green-400 relative overflow-hidden"
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-0 animate-pulse" />
                  <span className="text-6xl md:text-8xl font-black text-white drop-shadow-md relative z-10">
                    {order.display_id}
                  </span>
                  <span className="text-base md:text-lg text-green-100 mt-2 font-black uppercase truncate w-full text-center relative z-10">
                    {order.customer_name || "Cliente"}
                  </span>
                </motion.div>
              ))}
            </AnimatePresence>
             {ready.length === 0 && !error && (
              <div className="col-span-full flex flex-col items-center justify-center py-20 text-green-800/30">
                <CheckCircle2 size={64} className="mb-4" />
                <p className="font-black uppercase text-lg">Tudo Entregue</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* FOOTER */}
      <footer className="p-4 bg-orange-600 text-white text-center shadow-[0_-10px_40px_rgba(234,88,12,0.3)] z-20">
        <p className="text-lg md:text-2xl font-bold animate-pulse flex items-center justify-center gap-3">
          <span className="bg-white text-orange-600 px-2 py-0.5 rounded text-sm font-black">DICA</span>
          Por favor, retire seu pedido no balcão ao visualizar seu número em verde.
        </p>
      </footer>
    </div>
  );
}
