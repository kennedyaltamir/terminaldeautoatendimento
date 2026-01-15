// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 15:00:00
"use client";
import { useEffect, useState, useCallback, useRef } from "react";
import { Bike, MapPin, Loader2, Compass } from "lucide-react";
import { Order } from "@/types";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";
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
  }, [fetchOrders]);

  const activeDelivery = orders.find(o => o.status === 'delivering');

  useEffect(() => {
    if (activeDelivery && typeof navigator !== "undefined" && "geolocation" in navigator) {
      watchId.current = navigator.geolocation.watchPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          setDriverPos([latitude, longitude]);
          fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders/${activeDelivery.id}/location`, {
            method: "POST",
            headers: { 
              "Authorization": `Bearer ${getToken()}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ lat: latitude, lng: longitude })
          }).catch(() => {});
        },
        () => toast.error("Permissão de GPS necessária"),
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
      );
    }
    return () => { if (watchId.current) navigator.geolocation.clearWatch(watchId.current); };
  }, [activeDelivery]);

  useEffect(() => {
    if (activeDelivery) {
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
      <header className="flex justify-between items-center mb-6 bg-slate-900 p-5 rounded-[2rem] border border-slate-800 shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg"><Bike size={28} /></div>
          <div>
            <h1 className="font-black text-xl tracking-tight">App do Entregador</h1>
            <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Pompéu / MG</p>
          </div>
        </div>
        <div className="text-right">
           <div className="text-emerald-400 text-[10px] font-black uppercase flex items-center justify-end gap-1">
             <Compass size={12} className="animate-spin-slow" /> GPS {watchId.current ? "ON" : "OFF"}
           </div>
        </div>
      </header>

      <main className="space-y-6">
        {activeDelivery ? (
          <div className="space-y-6" data-testid="delivery.active-section">
             <div className="bg-white text-slate-900 p-8 rounded-[2.5rem] shadow-2xl flex justify-between items-center border-b-8 border-orange-500">
                <div>
                   <h3 className="font-black text-2xl tracking-tighter">{activeDelivery.customer_name}</h3>
                   <div className="flex items-center gap-2 text-slate-500 text-sm mt-1 font-bold">
                      <MapPin size={16} className="text-orange-500" /> {activeDelivery.delivery_address}
                   </div>
                </div>
                <div className="text-right">
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">ETA</p>
                   <p className="text-3xl font-black text-orange-600" data-testid="delivery.eta-display">{routeData ? Math.ceil(routeData.duration / 60) : "--"} min</p>
                </div>
             </div>
             
             <div className="h-[500px] w-full overflow-hidden rounded-[2.5rem] shadow-2xl border-4 border-white" data-testid="delivery.map-container">
                <TrackingMap 
                  driverPos={driverPos} 
                  clientPos={[-19.22815, -44.94195]} 
                  routeGeojson={routeData?.geometry}
                  duration={routeData?.duration}
                />
             </div>
          </div>
        ) : (
          <section className="space-y-4 px-2">
            <h2 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-4">Pedidos Disponíveis</h2>
            {orders.filter(o => o.status === 'ready').map(order => (
              <div 
                key={order.id} 
                data-testid="delivery.order.card"
                data-order-id={order.id}
                className="bg-slate-900 rounded-[2.5rem] p-8 border border-slate-800 shadow-xl flex justify-between items-center hover:border-orange-500/50 transition-all"
              >
                <div className="flex-1">
                  <h3 className="font-black text-lg tracking-tight" data-testid="delivery.order.customer-name">{order.customer_name}</h3>
                  <p className="text-xs text-slate-500 mt-1 font-medium">{order.delivery_address}</p>
                </div>
                <button 
                  data-testid="delivery.order.pickup"
                  onClick={() => handlePickup(order.id)}
                  className="bg-orange-600 hover:bg-orange-500 text-white px-8 py-4 rounded-2xl font-black uppercase text-xs tracking-widest shadow-xl active:scale-95 transition-all"
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
          <Loader2 className="animate-spin text-orange-600" size={48} />
        </div>
      )}
    </div>
  );
}
