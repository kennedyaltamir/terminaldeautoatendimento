// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 14:50:00
"use client";

import { useEffect, useState, useCallback, useRef, useMemo } from "react";
import { Bike, MapPin, Loader2, Compass, AlertCircle } from "lucide-react";
import { Order } from "@/types";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import { fetchRoute } from "@/lib/routing";
import dynamic from "next/dynamic";

// Carregamento dinâmico do Leaflet para evitar erros de SSR
const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { 
  ssr: false,
  loading: () => <div className="w-full h-full bg-slate-900 animate-pulse flex items-center justify-center text-slate-500 font-bold">CARREGANDO GPS...</div>
});

export default function DriverPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [driverPos, setDriverPos] = useState<[number, number]>([-19.22448, -44.93548]);
  const [routeData, setRouteData] = useState<any>(null);
  const watchId = useRef<number | null>(null);

  const fetchOrders = useCallback(async () => {
    if (isTransitioning) return;
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders`, {
        headers: { Authorization: `Bearer ${getToken()}` }
      });
      if (res.ok) {
        const data = await res.json();
        setOrders(data);
      }
    } catch (e) {
      console.error("Erro ao buscar pedidos:", e);
    } finally {
      setLoading(false);
    }
  }, [isTransitioning]);

  useEffect(() => {
    fetchOrders();
    // Polling de segurança caso o WebSocket/Redis falhe
    const interval = setInterval(fetchOrders, 10000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "delivery.status") {
      const orderId = data.order_id || data.payload?.order_id;
      const newStatus = data.status || data.payload?.status;
      setOrders(prev => prev.map(o => String(o.id) === String(orderId) ? { ...o, status: newStatus } : o));
    }
  });

  // Identifica se há uma entrega ativa (READY ou DELIVERING)
  const activeDelivery = useMemo(() => 
    orders.find(o => o.status === 'delivering'), 
  [orders]);

  const availableOrders = useMemo(() => 
    orders.filter(o => o.status === 'ready'), 
  [orders]);

  const handlePickup = async (orderId: string) => {
    if (isTransitioning) return;
    setIsTransitioning(true);
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders/${orderId}/dispatch`, {
        method: "PATCH",
        headers: { 
          "Authorization": `Bearer ${getToken()}`,
          "Content-Type": "application/json" 
        }
      });
      
      if (res.ok) {
        toast.success("Rota iniciada!");
        // Atualização local imediata para redundância ao WebSocket
        setOrders(prev => prev.map(o => o.id === orderId ? { ...o, status: 'delivering' } : o));
      } else {
        const err = await res.json();
        toast.error(err.detail || "Falha ao coletar");
        setIsTransitioning(false);
      }
    } catch (e) { 
      toast.error("Erro de conexão");
      setIsTransitioning(false);
    }
  };

  useEffect(() => {
    if (activeDelivery) setIsTransitioning(false);
  }, [activeDelivery]);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 pb-24 font-sans">
      <Toaster position="top-center" richColors />
      
      <header className="flex justify-between items-center mb-6 bg-slate-900 p-5 rounded-[2rem] border border-slate-800 shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg shadow-orange-900/20">
            <Bike size={28} />
          </div>
          <h1 className="font-black text-xl tracking-tight">App do Entregador</h1>
        </div>
        <div className="text-emerald-400 text-[10px] font-black uppercase flex items-center gap-1">
          <Compass size={12} className={activeDelivery ? "animate-spin-slow" : ""} /> GPS ON
        </div>
      </header>

      <main className="space-y-6">
        {activeDelivery ? (
          <div className="space-y-6 animate-in fade-in duration-500" data-testid="driver.delivery.active">
             <div className="bg-white text-slate-900 p-8 rounded-[2.5rem] shadow-2xl flex justify-between items-center border-b-8 border-orange-500">
                <div>
                   <h3 className="font-black text-2xl tracking-tighter">{activeDelivery.customer_name}</h3>
                   <div className="flex items-center gap-2 text-slate-500 text-sm mt-1 font-bold">
                      <MapPin size={16} className="text-orange-500" /> {activeDelivery.delivery_address}
                   </div>
                </div>
             </div>
             <div className="h-[500px] w-full rounded-[2.5rem] overflow-hidden border-4 border-white shadow-2xl">
                <TrackingMap driverPos={driverPos} clientPos={[-19.22815, -44.94195]} />
             </div>
          </div>
        ) : (
          <section className="space-y-4 px-2">
            <h2 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-4">Pedidos Disponíveis</h2>
            {availableOrders.length === 0 ? (
              <div className="py-20 text-center bg-slate-900/50 rounded-[2.5rem] border-2 border-dashed border-slate-800">
                <AlertCircle size={48} className="mx-auto mb-4 text-slate-700" />
                <p className="text-slate-500 font-bold">Nenhum pedido pronto para coleta.</p>
              </div>
            ) : (
              availableOrders.map(order => (
                <div key={order.id} data-testid="driver.delivery.order.card" data-order-id={order.id} className="bg-slate-900 rounded-[2.5rem] p-8 border border-slate-800 shadow-xl flex justify-between items-center hover:border-orange-500/50 transition-all">
                  <div className="flex-1">
                    <h3 className="font-black text-lg tracking-tight">{order.customer_name}</h3>
                    <p className="text-xs text-slate-500 mt-1">{order.delivery_address}</p>
                  </div>
                  <button 
                    data-testid="driver.delivery.order.pickup"
                    disabled={isTransitioning}
                    onClick={() => handlePickup(order.id)}
                    className="bg-orange-600 hover:bg-orange-500 text-white px-8 py-4 rounded-2xl font-black uppercase text-xs tracking-widest shadow-xl active:scale-95 disabled:opacity-50"
                  >
                    {isTransitioning ? "..." : "Pegar"}
                  </button>
                </div>
              ))
            )}
          </section>
        )}
      </main>

      {(loading || isTransitioning) && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50">
          <Loader2 className="animate-spin text-orange-600" size={48} />
        </div>
      )}
    </div>
  );
}
