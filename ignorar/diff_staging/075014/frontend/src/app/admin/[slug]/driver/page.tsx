// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 13:50:00
"use client";
import { useEffect, useState, useCallback, useRef } from "react";
import { Bike, MapPin, Navigation, Loader2, Compass, CheckCircle2 } from "lucide-react";
import { Order } from "@/types";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import { fetchRoute } from "@/lib/routing";
import dynamic from "next/dynamic";

const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { ssr: false });

export default function DriverPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [driverPos, setDriverPos] = useState<[number, number]>([-19.22448, -44.93548]);
  const [routeData, setRouteData] = useState<any>(null);
  const watchId = useRef<number | null>(null);

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

  const activeDelivery = orders.find(o => o.status === 'delivering');

  // GPS REAL: Monitora posição do dispositivo e envia para o backend
  useEffect(() => {
    if (activeDelivery && typeof navigator !== "undefined" && "geolocation" in navigator) {
      console.log("🛰️ Ativando GPS Real...");
      watchId.current = navigator.geolocation.watchPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          setDriverPos([latitude, longitude]);
          
          // Envia posição real para o backend para propagar ao cliente
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders/${activeDelivery.id}/location`, {
            method: "POST",
            headers: { 
              "Authorization": `Bearer ${getToken()}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ lat: latitude, lng: longitude })
          }).catch(console.error);
        },
        (err) => toast.error("Erro ao acessar GPS"),
        { enableHighAccuracy: true, distanceFilter: 10 }
      );
    } else {
      if (watchId.current) navigator.geolocation.clearWatch(watchId.current);
    }
    return () => { if (watchId.current) navigator.geolocation.clearWatch(watchId.current); };
  }, [activeDelivery]);

  useEffect(() => {
    if (activeDelivery) {
      // Destino Padrão para Pompéu (Em produção: lat/lng do pedido)
      fetchRoute(driverPos, [-19.22815, -44.94195]).then(setRouteData);
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
      <header className="flex justify-between items-center mb-6 bg-slate-900 p-5 rounded-[2rem] border border-slate-800">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg"><Bike size={28} /></div>
          <div>
            <h1 className="font-black text-xl tracking-tight">Painel Logístico</h1>
            <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest">GPS {watchId.current ? "ATIVO" : "OFFLINE"}</p>
          </div>
        </div>
      </header>

      <main className="space-y-6">
        {activeDelivery ? (
          <div className="space-y-4">
             <div className="bg-white text-slate-900 p-6 rounded-[2.5rem] shadow-2xl flex justify-between items-center">
                <div>
                   <h3 className="font-black text-xl">{activeDelivery.customer_name}</h3>
                   <div className="flex items-center gap-2 text-slate-500 text-sm mt-1">
                      <MapPin size={16} /> {activeDelivery.delivery_address}
                   </div>
                </div>
                <div className="text-right">
                   <p className="text-[10px] font-black text-slate-400 uppercase">Tempo Estimado</p>
                   <p className="text-2xl font-black text-orange-600">{routeData ? Math.ceil(routeData.duration / 60) : "--"} min</p>
                </div>
             </div>
             
             <div className="h-[500px] w-full">
                <TrackingMap 
                  driverPos={driverPos} 
                  clientPos={[-19.22815, -44.94195]} 
                  routeGeojson={routeData?.geometry}
                  duration={routeData?.duration}
                />
             </div>
          </div>
        ) : (
          <section className="space-y-4">
            <h2 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-4">Pedidos para Coleta</h2>
            {orders.filter(o => o.status === 'ready').map(order => (
              <div key={order.id} className="bg-slate-900 rounded-[2rem] p-6 border border-slate-800 flex justify-between items-center">
                <div className="flex-1 mr-4">
                  <h3 className="font-bold text-lg">{order.customer_name}</h3>
                  <p className="text-xs text-slate-500 mt-1 line-clamp-1">{order.delivery_address}</p>
                </div>
                <button 
                  onClick={() => handlePickup(order.id)}
                  className="bg-orange-600 hover:bg-orange-500 text-white px-8 py-4 rounded-2xl font-black uppercase text-xs tracking-widest shadow-xl active:scale-95 transition-all"
                >
                  Pegar
                </button>
              </div>
            ))}
            {orders.filter(o => o.status === 'ready').length === 0 && (
               <div className="py-20 text-center text-slate-600 italic">Nenhum pedido pronto para coleta.</div>
            )}
          </section>
        )}
      </main>

      {loading && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50">
          <Loader2 className="animate-spin text-orange-500" size={48} />
        </div>
      )}
    </div>
  );
}
