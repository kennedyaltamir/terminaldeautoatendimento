// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 12:55:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { Bike, MapPin, Navigation, Loader2, Compass } from "lucide-react";
import { Order } from "@/types";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import { fetchRoute } from "@/lib/routing";
import dynamic from "next/dynamic";

// Carregamento dinâmico do mapa para evitar erros de SSR (Leaflet precisa de window)
const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { 
  ssr: false,
  loading: () => <div className="w-full h-full bg-slate-900 flex items-center justify-center text-slate-500 font-bold">Iniciando Map Engine...</div>
});

// Coordenadas padrão da loja (Pompéu MG)
const STORE_LAT = -19.22448;
const STORE_LNG = -44.93548;

export default function DriverPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [driverPos, setDriverPos] = useState<[number, number]>([STORE_LAT, STORE_LNG]);
  const [route, setRoute] = useState<any>(null);

  const fetchOrders = useCallback(async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders`, {
        headers: { Authorization: `Bearer ${getToken()}` }
      });
      if (res.ok) setOrders(await res.json());
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 15000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  // Escuta atualizações de localização (para espelhamento ou simulação)
  useWebSocket(slug, (msg) => {
    if (msg.type === "DELIVERY_LOCATION") {
      setDriverPos([msg.payload.lat, msg.payload.lng]);
    }
  });

  const activeDelivery = orders.find(o => o.status === 'delivering');

  // Ao detectar entrega ativa, calcula a rota
  useEffect(() => {
    if (activeDelivery && activeDelivery.delivery_address) {
      // Mock de destino: Em produção, o backend deveria enviar lat/lng do endereço.
      const destPos: [number, number] = [-19.22815, -44.94195]; 
      fetchRoute(driverPos, destPos).then(setRoute);
    }
  }, [activeDelivery, driverPos]);

  const handlePickup = async (orderId: string) => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders/${orderId}/dispatch`, {
        method: "PATCH",
        headers: { "Authorization": `Bearer ${getToken()}`, "Content-Type": "application/json" }
      });
      if (res.ok) {
        toast.success("Rota iniciada!");
        fetchOrders();
      }
    } catch (e) { toast.error("Erro ao iniciar rota"); }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 pb-24 font-sans">
      <Toaster position="top-center" richColors />
      <header className="flex justify-between items-center mb-6 bg-slate-900 p-5 rounded-[2rem] border border-slate-800 shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-blue-600 p-3 rounded-2xl"><Bike size={28} /></div>
          <div>
            <h1 className="font-black text-xl tracking-tight">App do Entregador</h1>
            <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Ativo em {slug}</p>
          </div>
        </div>
        <div className="text-right">
           <div className="text-emerald-400 text-[10px] font-black uppercase flex items-center justify-end gap-1">
             <Compass size={12} className="animate-spin-slow" /> Georeferenciado
           </div>
        </div>
      </header>

      <main className="space-y-6">
        {activeDelivery ? (
          <div className="space-y-4">
             <div className="bg-white text-slate-900 p-6 rounded-[2.5rem] shadow-2xl">
                <h3 className="font-black text-xl">{activeDelivery.customer_name}</h3>
                <div className="flex items-center gap-2 text-slate-500 text-sm mt-1">
                   <MapPin size={16} /> {activeDelivery.delivery_address}
                </div>
             </div>
             
             <div className="h-[450px] w-full">
                <TrackingMap 
                  driverPos={driverPos} 
                  clientPos={[-19.22815, -44.94195]} 
                  routeGeojson={route}
                />
             </div>
          </div>
        ) : (
          <section className="space-y-4">
            <h2 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-4">Aguardando Coleta</h2>
            {orders.filter(o => o.status === 'ready').map(order => (
              <div key={order.id} className="bg-slate-900 rounded-[2rem] p-6 border border-slate-800 shadow-xl flex justify-between items-center">
                <div>
                  <h3 className="font-bold">{order.customer_name}</h3>
                  <p className="text-[10px] text-slate-500 mt-1">{order.delivery_address?.substring(0, 30)}...</p>
                </div>
                <button 
                  onClick={() => handlePickup(order.id)}
                  className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-xl font-black uppercase text-[10px] tracking-widest transition-all"
                >
                  Pegar
                </button>
              </div>
            ))}
          </section>
        )}
      </main>

      {loading && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50">
          <Loader2 className="animate-spin text-blue-500" size={48} />
        </div>
      )}
    </div>
  );
}
