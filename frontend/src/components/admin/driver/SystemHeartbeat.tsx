/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Visual log of system activity to reduce "waiting anxiety".
 */
"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Activity, ChefHat, CheckCircle2, ShoppingBag } from "lucide-react";

const MOCK_EVENTS = [
  { icon: ChefHat, text: "Cozinha iniciou Pedido #4829", color: "text-orange-500" },
  { icon: ShoppingBag, text: "Novo pedido delivery recebido", color: "text-blue-500" },
  { icon: CheckCircle2, text: "Motoboy João finalizou entrega", color: "text-emerald-500" },
  { icon: Activity, text: "Sincronizando rotas...", color: "text-slate-500" },
];

export default function SystemHeartbeat() {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      const randomEvent = MOCK_EVENTS[Math.floor(Math.random() * MOCK_EVENTS.length)];
      const eventWithId = { ...randomEvent, id: Date.now() };
      
      setEvents(prev => [eventWithId, ...prev].slice(0, 3)); // Mantém apenas os últimos 3
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-sm mx-auto mt-8">
      <div className="flex items-center gap-2 mb-3 opacity-50">
        <Activity size={12} className="text-emerald-500 animate-pulse" />
        <span className="text-[9px] font-black uppercase tracking-widest text-slate-500">Atividade da Rede</span>
      </div>
      
      <div className="space-y-2 relative h-24 overflow-hidden mask-linear-fade">
        <AnimatePresence mode="popLayout">
          {events.map((event) => (
            <motion.div
              key={event.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="flex items-center gap-3 text-xs font-mono text-slate-400"
            >
              <event.icon size={14} className={event.color} />
              <span>{event.text}</span>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {/* Gradiente de Fade Out na base */}
        <div className="absolute bottom-0 left-0 w-full h-8 bg-gradient-to-t from-black to-transparent pointer-events-none" />
      </div>
    </div>
  );
}

