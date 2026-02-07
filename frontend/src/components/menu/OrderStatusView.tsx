/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 14.3.0 (Diamond Correction)
 * DNA_ID: MF-ORDER-STATUS-V14-3
 * Objective: Resolve TS2322 by removing 'duration' prop and aligning with TrackingMap v17 interface.
 */
"use client";

import React, { useState, useEffect } from "react";
import { 
  Clock, ChefHat, CheckCircle2, MapPin, Plus, Bike, 
  PartyPopper, DollarSign, Info
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import dynamic from "next/dynamic";

// --- LIBS & UTILS ---
import { Order } from "@/types";
import { useWebSocket } from "@/hooks/useWebSocket";
import { cn, formatCurrency } from "@/lib/utils";
import { fetchRoute } from "@/lib/routing";

// Carregamento dinâmico do mapa
const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { 
  ssr: false,
  loading: () => (
    <div className="w-full h-80 bg-slate-100 rounded-[2.5rem] flex items-center justify-center text-slate-300 font-black uppercase text-[10px] tracking-widest animate-pulse border-2 border-dashed border-slate-200">
      CARREGANDO MAPA DE RASTREIO...
    </div>
  )
});

interface OrderStatusViewProps {
  order: Order;
  onNewOrder: () => void;
  primaryColor: string;
}

export default function OrderStatusView({ order, onNewOrder, primaryColor }: OrderStatusViewProps) {
  const [localOrder, setLocalOrder] = useState<Order>(order);
  const [driverPos, setDriverPos] = useState<[number, number] | null>(null);
  const [routeData, setRouteData] = useState<any>(null);
  
  // Resolve slug safely for WebSocket context
  const slug = typeof window !== 'undefined' ? window.location.pathname.split('/')[1] : "";

  // --- SINCRONIZAÇÃO VIA WEBSOCKET ---
  useWebSocket(slug, (data: any) => {
    const incomingOrderId = data.order_id || data.payload?.order_id;
    
    if (incomingOrderId === localOrder.id) {
      if (data.type === "order_update" || data.type === "payment_confirmed") {
        const newStatus = data.status || data.new_status;
        const newPaymentStatus = data.type === "payment_confirmed" ? "paid" : (data.payment_status || localOrder.payment_status);
        
        setLocalOrder((prev: Order) => ({
          ...prev,
          status: newStatus || prev.status,
          payment_status: newPaymentStatus
        }));
        
        if (data.type === "payment_confirmed") {
          toast.success("Pagamento Confirmado!", {
            description: "Seu pedido foi enviado para a fila de produção.",
            icon: <CheckCircle2 className="text-emerald-500" />
          });
        }
      } 
      else if (data.type === "DELIVERY_LOCATION") {
        const lat = data.payload?.lat || data.lat;
        const lng = data.payload?.lng || data.lng;
        if (lat && lng) setDriverPos([lat, lng]);
      }
    }
  });

  // --- LÓGICA DE ROTEAMENTO ---
  useEffect(() => {
    if (localOrder.status === 'delivering' && driverPos) {
       fetchRoute(driverPos, [-19.22815, -44.94195]).then(setRouteData);
    }
  }, [localOrder.status, driverPos]);

  const steps = [
    { id: 'pending', label: 'Recebido', icon: Clock },
    { id: 'preparing', label: 'Cozinha', icon: ChefHat },
    { id: 'ready', label: 'Pronto', icon: CheckCircle2 },
    { id: 'delivering', label: 'Em Rota', icon: MapPin },
    { id: 'delivered', label: 'Finalizado', icon: PartyPopper },
  ];

  const visibleSteps = localOrder.order_type === 'delivery' 
    ? steps 
    : steps.filter(s => s.id !== 'delivering');

  const currentStepIndex = visibleSteps.findIndex(s => s.id === localOrder.status);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col pb-10 font-sans" data-testid="customer.order-view">
      {/* HEADER */}
      <div className="bg-white p-6 shadow-sm border-b border-slate-200">
        <h1 className="text-2xl font-black text-slate-900 tracking-tight">
          Olá, {localOrder.customer_name?.split(' ')[0] || 'Cliente'}!
        </h1>
        <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest mt-1">
          Acompanhamento do Pedido <span className="text-orange-600">#{localOrder.id.slice(0, 6)}</span>
        </p>
      </div>

      <div className="p-6 space-y-6 max-w-md mx-auto w-full">
        {/* CARD DE STATUS DE PAGAMENTO */}
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className={cn(
            "p-5 rounded-[2rem] border-2 flex items-center justify-between transition-all shadow-sm",
            localOrder.payment_status === 'paid' 
              ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-600" 
              : "bg-orange-500/10 border-orange-500/20 text-orange-600 animate-pulse"
          )}
        >
          <div className="flex items-center gap-3">
            <div className={cn("p-2 rounded-full", localOrder.payment_status === 'paid' ? "bg-emerald-500 text-white" : "bg-orange-500 text-white")}>
              <DollarSign size={18} />
            </div>
            <span className="font-black uppercase text-xs tracking-widest">
              {localOrder.payment_status === 'paid' ? "Pagamento Confirmado" : "Aguardando Pagamento"}
            </span>
          </div>
          {localOrder.payment_status === 'paid' && <CheckCircle2 size={20} />}
        </motion.div>

        {/* PROGRESS STEPPER */}
        <div className="bg-white p-8 rounded-[2.5rem] shadow-xl border border-slate-100" data-testid="customer.order.stepper">
          <div className="flex justify-between relative mb-10">
            <div className="absolute top-5 left-0 w-full h-1 bg-slate-100 -z-10 rounded-full" />
            <div 
              className="absolute top-5 left-0 h-1 bg-green-500 -z-10 rounded-full transition-all duration-1000" 
              style={{ width: `${Math.max(0, (currentStepIndex / (visibleSteps.length - 1)) * 100)}%` }}
            />
            {visibleSteps.map((step, idx) => (
              <div key={step.id} className="flex flex-col items-center gap-2 bg-white px-1">
                <div className={cn(
                  "w-10 h-10 rounded-full flex items-center justify-center transition-all duration-500",
                  idx <= currentStepIndex ? "bg-orange-600 text-white shadow-lg shadow-orange-200" : "bg-slate-100 text-slate-400"
                )}>
                  <step.icon size={18} className={cn(idx === currentStepIndex && "animate-bounce")} />
                </div>
                <span className={cn(
                  "text-[9px] font-black uppercase tracking-tighter",
                  idx === currentStepIndex ? "text-orange-600" : "text-slate-400"
                )}>{step.label}</span>
              </div>
            ))}
          </div>

          {/* CONTEÚDO DINÂMICO POR ESTADO */}
          <AnimatePresence mode="wait">
            {localOrder.status === 'delivered' ? (
              <motion.div key="delivered" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="py-10 text-center space-y-4">
                 <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-inner">
                    <PartyPopper size={40} />
                 </div>
                 <h2 className="text-2xl font-black text-slate-900">Bom apetite!</h2>
                 <p className="text-slate-500 text-sm font-medium">Seu pedido foi finalizado com sucesso.</p>
              </motion.div>
            ) : localOrder.status === 'delivering' ? (
              <motion.div key="delivering" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                <div className="bg-blue-600 text-white p-5 rounded-3xl flex items-center gap-4 shadow-lg">
                  <div className="bg-white/20 p-2 rounded-full animate-pulse"><Bike size={24} /></div>
                  <div>
                    <p className="font-black text-sm uppercase tracking-widest">Saiu para entrega!</p>
                    <p className="text-[10px] opacity-80 font-bold">Acompanhe o motorista no mapa abaixo.</p>
                  </div>
                </div>
                <div className="h-72 w-full rounded-[2rem] overflow-hidden shadow-inner border border-slate-200" data-testid="customer.order.map">
                  <TrackingMap 
                    driverPos={driverPos || [-19.22448, -44.93548]} 
                    clientPos={[-19.22815, -44.94195]} 
                    routeGeojson={routeData?.geometry}
                    mapMode="AUTO_FOLLOW"
                    onMapModeChange={() => {}}
                  />
                </div>
              </motion.div>
            ) : (
              <motion.div key="waiting" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="py-12 text-center space-y-4 bg-slate-50/50 rounded-3xl border border-dashed border-slate-200">
                 <ChefHat size={48} className="text-slate-200 mx-auto" />
                 <p className="text-slate-400 font-black text-[10px] uppercase tracking-[0.2em]">
                    {localOrder.status === 'ready' ? "Pedido pronto! Aguardando retirada." : "Estamos preparando seu pedido..."}
                 </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* INFO DE RETIRADA / LOCALIZAÇÃO */}
        <div className="bg-slate-900 p-6 rounded-[2rem] text-white border border-slate-800 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10"><Info size={40} /></div>
          <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest mb-2">Referência de Entrega</p>
          <p className="text-xl font-bold leading-tight">
            {localOrder.order_type === 'delivery' 
              ? localOrder.delivery_address 
              : (localOrder.pickup_note || "Retirada no Balcão")}
          </p>
        </div>

        <button 
          onClick={onNewOrder} 
          className="w-full py-5 rounded-2xl font-black uppercase text-xs tracking-widest text-white shadow-xl shadow-orange-900/20 flex items-center justify-center gap-2 active:scale-95 transition-all" 
          style={{ backgroundColor: primaryColor }}
        >
          <Plus size={20} /> Novo Pedido
        </button>
      </div>
    </div>
  );
}