// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-10 15:20:00
"use client";
import React, { useEffect, useState, useRef, useCallback } from "react";
import { getPublicMonitorOrders } from "@/lib/api";
import { useWebSocket } from "@/hooks/useWebSocket";
import { motion, AnimatePresence } from "framer-motion";
import { Clock, ChefHat, CheckCircle2, Volume2 } from "lucide-react";

interface MonitorOrder {
  id: string;
  display_id: string;
  status: string;
  customer_name: string | null;
}

export default function PublicMonitorView({ slug }: { slug: string }) {
  const [orders, setOrders] = useState<MonitorOrder[]>([]);
  const [time, setTime] = useState(new Date());
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const fetchOrders = useCallback(async () => {
    try {
      const data = await getPublicMonitorOrders(slug);
      setOrders(data);
    } catch (e) {
      console.error("Erro ao carregar monitor:", e);
    }
  }, [slug]);

  useEffect(() => {
    fetchOrders();
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, [fetchOrders]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "new_order") {
      if (data.status === "ready" && audioRef.current) {
        audioRef.current.play().catch(() => {});
      }
      fetchOrders();
    }
  });

  const preparing = orders.filter(o => o.status === "pending" || o.status === "preparing" || o.status === "accepted");
  const ready = orders.filter(o => o.status === "ready");

  return (
    <div className="h-screen flex flex-col bg-gray-950 text-white font-sans overflow-hidden">
      <audio ref={audioRef} src="/notification.mp3" preload="auto" />
      
      {/* HEADER */}
      <header className="p-8 bg-gray-900 border-b border-gray-800 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg">
            <ChefHat size={40} />
          </div>
          <h1 className="text-4xl font-black tracking-tighter uppercase">Acompanhe seu Pedido</h1>
        </div>
        <div className="text-right">
          <p className="text-5xl font-mono font-bold text-gray-400">
            {time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <div className="flex-1 flex">
        {/* PREPARANDO */}
        <div className="flex-1 border-r border-gray-800 p-8">
          <div className="flex items-center gap-3 mb-8 text-orange-500">
            <Clock size={32} />
            <h2 className="text-3xl font-black uppercase">Preparando</h2>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <AnimatePresence>
              {preparing.map((order) => (
                <motion.div
                  key={order.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, scale: 0.5 }}
                  className="bg-gray-900/50 border border-gray-800 p-6 rounded-3xl flex flex-col items-center justify-center"
                >
                  <span className="text-5xl font-black text-gray-300">{order.display_id}</span>
                  <span className="text-sm text-gray-500 mt-2 font-bold uppercase truncate w-full text-center">
                    {order.customer_name || "Cliente"}
                  </span>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>

        {/* PRONTO */}
        <div className="flex-1 p-8 bg-green-950/10">
          <div className="flex items-center gap-3 mb-8 text-green-500">
            <CheckCircle2 size={32} />
            <h2 className="text-3xl font-black uppercase">Pronto para Retirada</h2>
          </div>
          <div className="grid grid-cols-2 gap-6">
            <AnimatePresence>
              {ready.map((order) => (
                <motion.div
                  key={order.id}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ 
                    scale: [1, 1.05, 1],
                    opacity: 1 
                  }}
                  transition={{ 
                    scale: { repeat: Infinity, duration: 2 },
                    opacity: { duration: 0.5 }
                  }}
                  className="bg-green-600 p-8 rounded-[2.5rem] shadow-[0_0_40px_rgba(34,197,94,0.3)] flex flex-col items-center justify-center border-4 border-green-400"
                >
                  <span className="text-7xl font-black text-white drop-shadow-lg">{order.display_id}</span>
                  <span className="text-lg text-green-100 mt-3 font-black uppercase truncate w-full text-center">
                    {order.customer_name || "Cliente"}
                  </span>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* FOOTER */}
      <footer className="p-6 bg-orange-600 text-white text-center">
        <p className="text-2xl font-bold animate-pulse">
          Por favor, retire seu pedido no balcão ao visualizar seu número em verde.
        </p>
      </footer>
    </div>
  );
}
