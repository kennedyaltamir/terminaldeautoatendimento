// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 10:10:00
"use client";
import { Clock, ChefHat, CheckCircle2, Banknote, Copy, Loader2, Utensils, Plus, MapPin, Navigation, Star, Map as MapIcon } from "lucide-react";
import { Order } from "@/types";
import { QRCodeSVG } from "qrcode.react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useState, useCallback, useEffect } from "react";
import FeedbackModal from "@/components/menu/FeedbackModal";
import { formatCurrency, cn } from "@/lib/utils";

export default function OrderStatusView({ order, onNewOrder, primaryColor }: { order: Order, onNewOrder: () => void, primaryColor: string }) {
  const [localStatus, setLocalStatus] = useState(order.status);
  const [driverLocation, setDriverLocation] = useState<{lat: number, lng: number} | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);

  const isPaid = order.payment_status === 'paid';
  const isOnline = order.payment_method === 'online';
  const slug = typeof window !== 'undefined' ? window.location.pathname.split('/')[1] : "";

  useEffect(() => { setLocalStatus(order.status); }, [order.status]);

  const handleWebSocketMessage = useCallback((data: any) => {
    if (data.order_id === order.id) {
      if (data.type === "order_update") {
        setLocalStatus(data.status);
      } else if (data.type === "driver_location") {
        setDriverLocation({ lat: data.lat, lng: data.lng });
      }
    }
  }, [order.id]);

  useWebSocket(slug, handleWebSocketMessage); 

  const steps = [
    { id: 'pending', label: 'Recebido', icon: Clock },
    { id: 'preparing', label: 'Preparando', icon: ChefHat },
    { id: 'ready', label: 'Pronto', icon: CheckCircle2 },
    { id: 'delivering', label: 'Em Rota', icon: MapPin },
  ];

  const currentStepIndex = steps.findIndex(s => s.id === localStatus);

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col pb-10 font-sans">
      <div className="bg-white p-6 shadow-sm border-b border-slate-200">
        <h1 className="text-2xl font-black text-slate-900 tracking-tight">Olá, {order.customer_name?.split(' ')[0] || 'Cliente'}!</h1>
        <p className="text-slate-500 text-xs font-bold uppercase tracking-widest mt-1">Pedido <span className="text-orange-600">#{order.id.slice(0, 6)}</span></p>
      </div>

      <div className="p-6 space-y-6 max-w-md mx-auto w-full">
        {/* TRACKING RADAR */}
        <div className="bg-white p-8 rounded-[2.5rem] shadow-xl border border-slate-100 relative overflow-hidden">
          <div className="flex justify-between relative mb-10">
            <div className="absolute top-1/2 left-0 w-full h-1 bg-slate-100 -z-10 -translate-y-1/2 rounded-full"></div>
            <div className="absolute top-1/2 left-0 h-1 bg-orange-500 -z-10 -translate-y-1/2 rounded-full transition-all duration-1000" style={{ width: `${Math.max(0, (currentStepIndex / (steps.length - 1)) * 100)}%` }}></div>
            {steps.map((step, idx) => (
              <div key={step.id} className="flex flex-col items-center gap-2 bg-white px-1">
                <div className={cn("w-10 h-10 rounded-full flex items-center justify-center transition-all", idx <= currentStepIndex ? "bg-orange-600 text-white shadow-lg shadow-orange-200" : "bg-slate-100 text-slate-400")}>
                  <step.icon size={18} />
                </div>
                <span className={cn("text-[10px] font-black uppercase tracking-tighter", idx === currentStepIndex ? "text-orange-600" : "text-slate-400")}>{step.label}</span>
              </div>
            ))}
          </div>

          {localStatus === 'delivering' && (
            <div className="space-y-6 animate-in fade-in zoom-in duration-500">
              <div className="bg-blue-600 text-white p-4 rounded-2xl flex items-center gap-4 shadow-lg shadow-blue-900/20">
                <div className="bg-white/20 p-2 rounded-full animate-pulse"><Navigation size={20} /></div>
                <div>
                  <p className="font-black text-sm uppercase tracking-widest">Motorista a caminho!</p>
                  <p className="text-xs text-blue-100">Acompanhe o trajeto no mapa abaixo.</p>
                </div>
              </div>

              {/* SIMULATED MAP VIEW */}
              <div className="aspect-video bg-slate-100 rounded-3xl border-2 border-slate-200 relative flex items-center justify-center overflow-hidden group">
                <div className="absolute inset-0 opacity-20 bg-[url('https://www.google.com/maps/vt/pb=!1m4!1m3!1i15!2i15185!3i9455!2m3!1e0!2sm!3i604145415!3m8!2spt-BR!3sUS!5e1105!12m4!1e68!2m2!1sset!2sRoadmap!4e0!5m4!1e0!8m2!1sen!1sUS!6m6!1e12!2i2!11e0!12e3!20e3!29e0')] bg-cover"></div>
                {driverLocation ? (
                  <div className="relative z-10 text-center">
                    <div className="w-12 h-12 bg-orange-600 rounded-full flex items-center justify-center text-white shadow-2xl animate-bounce mx-auto border-4 border-white">
                      <Bike size={24} />
                    </div>
                    <div className="mt-4 bg-white/90 backdrop-blur px-4 py-2 rounded-full border border-slate-200 shadow-sm">
                      <p className="text-[10px] font-black text-slate-900 uppercase tracking-widest">Localização Atual</p>
                      <p className="text-xs font-mono text-slate-500">{driverLocation.lat.toFixed(5)}, {driverLocation.lng.toFixed(5)}</p>
                    </div>
                  </div>
                ) : (
                  <div className="text-slate-400 flex flex-col items-center gap-2">
                    <MapIcon size={40} className="opacity-20" />
                    <p className="text-xs font-bold uppercase">Aguardando sinal GPS...</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* RESUMO DO PEDIDO */}
        <div className="bg-white rounded-[2rem] shadow-sm border border-slate-100 overflow-hidden">
          <div className="p-5 border-b border-slate-50 bg-slate-50/50 flex justify-between items-center">
            <h3 className="font-black text-slate-900 uppercase text-xs tracking-widest flex items-center gap-2"><Utensils size={14}/> Itens do Pedido</h3>
            <span className="bg-white px-2 py-1 rounded-lg border border-slate-200 text-[10px] font-black text-slate-500">{order.items.length} Itens</span>
          </div>
          <div className="p-6 space-y-4">
            {order.items.map((item, i) => (
              <div key={i} className="flex justify-between items-center">
                <div className="flex gap-3 items-center">
                  <div className="bg-slate-100 w-8 h-8 rounded-xl flex items-center justify-center text-xs font-black text-slate-600">{item.quantity}x</div>
                  <p className="text-sm font-bold text-slate-800">{item.product.name}</p>
                </div>
                <span className="text-sm font-mono text-slate-400">{formatCurrency(item.product.price * item.quantity)}</span>
              </div>
            ))}
            <div className="border-t border-dashed border-slate-200 pt-4 mt-4 flex justify-between items-end">
              <span className="text-xs font-black text-slate-400 uppercase tracking-widest">Total Pago</span>
              <span className="text-2xl font-black text-slate-900">{formatCurrency(order.total_amount)}</span>
            </div>
          </div>
        </div>

        {canRate && (
          <button data-testid="btn-avaliar" onClick={() => setShowFeedback(true)} className="w-full py-4 rounded-2xl border-2 border-yellow-400 text-yellow-600 font-black uppercase text-xs tracking-widest flex items-center justify-center gap-2 hover:bg-yellow-50 transition-all active:scale-95 shadow-lg shadow-yellow-900/10">
            <Star size={18} className="fill-current" /> Avaliar Experiência
          </button>
        )}

        <button onClick={onNewOrder} className="w-full py-5 rounded-2xl font-black uppercase text-xs tracking-widest text-white shadow-xl shadow-orange-900/20 flex items-center justify-center gap-2 active:scale-95 transition-all" style={{ backgroundColor: primaryColor }}>
          <Plus size={20} /> Novo Pedido
        </button>
      </div>

      <FeedbackModal isOpen={showFeedback} onClose={() => setShowFeedback(false)} orderId={order.id} slug={slug} />
    </div>
  );
}
