// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 15:00:00
"use client";
import { 
  Clock, ChefHat, CheckCircle2, MapPin, Plus, Bike 
} from "lucide-react";
import { Order } from "@/types";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import dynamic from "next/dynamic";
import { fetchRoute } from "@/lib/routing";

const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { 
  ssr: false,
  loading: () => <div className="w-full h-80 bg-slate-100 rounded-[2.5rem] flex items-center justify-center text-slate-300 font-black uppercase text-xs tracking-widest animate-pulse">Iniciando GPS...</div>
});

export default function OrderStatusView({ order, onNewOrder, primaryColor }: { order: Order, onNewOrder: () => void, primaryColor: string }) {
  const [localStatus, setLocalStatus] = useState(order.status);
  const [driverPos, setDriverPos] = useState<[number, number] | null>(null);
  const [routeData, setRouteData] = useState<any>(null);
  const slug = typeof window !== 'undefined' ? window.location.pathname.split('/')[1] : "";

  useEffect(() => { setLocalStatus(order.status); }, [order.status]);

  useWebSocket(slug, (data) => {
    if (data.order_id === order.id || data.payload?.order_id === order.id) {
      if (data.type === "order_update") {
        setLocalStatus(data.status);
      } else if (data.type === "DELIVERY_LOCATION") {
        setDriverPos([data.payload.lat, data.payload.lng]);
      }
    }
  });

  useEffect(() => {
    if (localStatus === 'delivering' && driverPos) {
       fetchRoute(driverPos, [-19.22815, -44.94195]).then(setRouteData);
    }
  }, [localStatus, driverPos]);

  const steps = [
    { id: 'pending', label: 'Recebido', icon: Clock },
    { id: 'preparing', label: 'Cozinha', icon: ChefHat },
    { id: 'ready', label: 'Pronto', icon: CheckCircle2 },
    { id: 'delivering', label: 'Em Rota', icon: MapPin },
  ];
  
  const currentStepIndex = steps.findIndex(s => s.id === localStatus);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col pb-10 font-sans" data-testid="customer.order-view">
      <div className="bg-white p-6 shadow-sm border-b border-slate-200">
        <h1 className="text-2xl font-black text-slate-900 tracking-tight">Olá, {order.customer_name?.split(' ')[0] || 'Cliente'}!</h1>
        <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest mt-1">Acompanhamento do Pedido <span className="text-orange-600">#{order.id.slice(0, 6)}</span></p>
      </div>

      <div className="p-6 space-y-6 max-w-md mx-auto w-full">
        {/* PROGRESS STEPPER */}
        <div className="bg-white p-8 rounded-[2.5rem] shadow-xl border border-slate-100" data-testid="customer.order.stepper">
          <div className="flex justify-between relative mb-10">
            <div className="absolute top-1/2 left-0 w-full h-1 bg-slate-100 -z-10 -translate-y-1/2 rounded-full"></div>
            <div className="absolute top-1/2 left-0 h-1 bg-green-500 -z-10 -translate-y-1/2 rounded-full transition-all duration-1000" style={{ width: `${Math.max(0, (currentStepIndex / (steps.length - 1)) * 100)}%` }}></div>
            {steps.map((step, idx) => (
              <div key={step.id} className="flex flex-col items-center gap-2 bg-white px-1" data-testid={`customer.order.step.${step.id}`}>
                <div className={cn("w-10 h-10 rounded-full flex items-center justify-center transition-all", idx <= currentStepIndex ? "bg-orange-600 text-white shadow-lg shadow-orange-200" : "bg-slate-100 text-slate-400")}>
                  <step.icon size={18} />
                </div>
                <span className={cn("text-[10px] font-black uppercase tracking-tighter", idx === currentStepIndex ? "text-orange-600" : "text-slate-400")}>{step.label}</span>
              </div>
            ))}
          </div>

          {/* VISUALIZAÇÃO DO MAPA REAL-TIME */}
          {localStatus === 'delivering' ? (
            <div className="space-y-6 animate-in fade-in zoom-in duration-700" data-testid="customer.order.delivery-view">
              <div className="bg-orange-600 text-white p-5 rounded-3xl flex items-center gap-4 shadow-xl shadow-orange-900/20">
                <div className="bg-white/20 p-2 rounded-full animate-pulse"><Bike size={24} /></div>
                <div>
                  <p className="font-black text-sm uppercase tracking-widest leading-none">O Entregador saiu!</p>
                  <p className="text-[10px] text-orange-100 font-bold mt-1">Sua encomenda está a caminho.</p>
                </div>
              </div>
              
              <div className="h-80 w-full" data-testid="customer.order.map">
                <TrackingMap 
                  driverPos={driverPos || [-19.22448, -44.93548]} 
                  clientPos={[-19.22815, -44.94195]} 
                  routeGeojson={routeData?.geometry}
                  duration={routeData?.duration}
                />
              </div>
            </div>
          ) : (
            <div className="py-16 text-center space-y-4 bg-slate-50/50 rounded-3xl border border-dashed border-slate-200" data-testid="customer.order.waiting-view">
               <ChefHat size={48} className="text-slate-200 mx-auto" />
               <p className="text-slate-400 font-black text-[10px] uppercase tracking-[0.2em]">
                  {localStatus === 'ready' ? "Pedido pronto! Aguardando coleta." : "Preparando seu pedido com carinho..."}
               </p>
            </div>
          )}
        </div>

        <button onClick={onNewOrder} className="w-full py-5 rounded-2xl font-black uppercase text-xs tracking-widest text-white shadow-xl shadow-orange-900/20 flex items-center justify-center gap-2 active:scale-95 transition-all" style={{ backgroundColor: primaryColor }}>
          <Plus size={20} /> Novo Pedido
        </button>
      </div>
    </div>
  );
}
