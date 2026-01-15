// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 16:35:00
"use client";
import { useEffect, useState, useCallback, useRef, useMemo } from "react";
import { Bike, MapPin, Loader2, Compass } from "lucide-react";
import { Order } from "@/types";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import { fetchRoute } from "@/lib/routing";
import dynamic from "next/dynamic";

const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { ssr: false });

const FALLBACK_LAT = -19.22448;
const FALLBACK_LNG = -44.93548;

export default function DriverPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [driverPos, setDriverPos] = useState<[number, number]>([FALLBACK_LAT, FALLBACK_LNG]);
  const [routeData, setRouteData] = useState<any>(null);
  const watchId = useRef<number | null>(null);
  const lastSentRef = useRef<number>(0);

  const fetchOrders = useCallback(async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders`, {
        headers: { Authorization: `Bearer ${getToken()}` }
      });
      if (res.ok) setOrders(await res.json());
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { fetchOrders(); }, [fetchOrders]);

  useWebSocket(slug, (data) => {
    if (data.type === "delivery.status") {
      setOrders(prev => prev.map(o => String(o.id) === String(data.payload.order_id) ? { ...o, status: data.payload.status } : o));
    }
  });

  const activeDelivery = useMemo(() => orders.find(o => o.status === 'delivering'), [orders]);

  // GPS REAL: Propaga posição via POST (Throttle 3s)
  useEffect(() => {
    if (activeDelivery && typeof navigator !== "undefined" && "geolocation" in navigator) {
      watchId.current = navigator.geolocation.watchPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          setDriverPos([latitude, longitude]);
          
          const now = Date.now();
          if (now - lastSentRef.current > 3000) {
            lastSentRef.current = now;
            fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders/${activeDelivery.id}/location`, {
              method: "POST",
              headers: { 
                "Authorization": `Bearer ${getToken()}`,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({ lat: latitude, lng: longitude })
            }).catch(() => {});
          }
        },
        () => toast.error("GPS indisponível"),
        { enableHighAccuracy: true, timeout: 5000 }
      );
    }
    return () => { if (watchId.current) navigator.geolocation.clearWatch(watchId.current); };
  }, [activeDelivery?.id]);

  // ROTA: Calculada apenas uma vez no instante zero da entrega
  useEffect(() => {
    if (activeDelivery) {
      const destLat = activeDelivery.delivery_lat ?? -19.22815;
      const destLng = activeDelivery.delivery_lng ?? -44.94195;
      fetchRoute(driverPos, [destLat, destLng]).then(setRouteData);
    }
  }, [activeDelivery?.id]);

  const handlePickup = async (orderId: string) => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/delivery/orders/${orderId}/dispatch`, {
        method: "PATCH",
        headers: { "Authorization": `Bearer ${getToken()}`, "Content-Type": "application/json" }
      });
      if (res.ok) {
        toast.success("Rota iniciada!");
        fetchOrders();
      } else {
        const err = await res.json();
        toast.error(err.detail);
      }
    } catch (e) { toast.error("Erro na rede"); }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 font-sans">
      <Toaster position="top-center" richColors />
      <header className="flex justify-between items-center mb-6 bg-slate-900 p-5 rounded-[2rem] border border-slate-800 shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg"><Bike size={28} /></div>
          <div>
            <h1 className="font-black text-xl tracking-tight">Painel Logístico</h1>
            <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Ativo em {slug}</p>
          </div>
        </div>
      </header>

      <main className="space-y-6">
        {activeDelivery ? (
          <div className="space-y-6">
             <div className="bg-white text-slate-900 p-8 rounded-[2.5rem] shadow-2xl flex justify-between items-center border-b-8 border-orange-500">
                <div>
                   <h3 className="font-black text-2xl tracking-tighter">{activeDelivery.customer_name}</h3>
                   <div className="flex items-center gap-2 text-slate-500 text-sm mt-1 font-bold">
                      <MapPin size={16} className="text-orange-500" /> {activeDelivery.delivery_address}
                   </div>
                </div>
                <div className="text-right">
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">ETA</p>
                   <p className="text-3xl font-black text-orange-600">{routeData ? Math.ceil(routeData.duration / 60) : "--"} min</p>
                </div>
             </div>
             <div className="h-[500px] w-full">
                <TrackingMap 
                  driverPos={driverPos} 
                  clientPos={[activeDelivery.delivery_lat ?? -19.22815, activeDelivery.delivery_lng ?? -44.94195]} 
                  routeGeojson={routeData?.geometry}
                />
             </div>
          </div>
        ) : (
          <section className="space-y-4 px-2">
            <h2 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-4">Coletas Disponíveis</h2>
            {orders.filter(o => o.status === 'ready').map(order => (
              <div key={order.id} className="bg-slate-900 rounded-[2.5rem] p-8 border border-slate-800 flex justify-between items-center">
                <div className="flex-1">
                  <h3 className="font-black text-lg tracking-tight">{order.customer_name}</h3>
                  <p className="text-xs text-slate-500 mt-1">{order.delivery_address}</p>
                </div>
                <button onClick={() => handlePickup(order.id)} className="bg-orange-600 text-white px-8 py-4 rounded-2xl font-black uppercase text-xs shadow-xl active:scale-95 transition-all">Pegar</button>
              </div>
            ))}
          </section>
        )}
      </main>
      {loading && <div className="fixed inset-0 bg-slate-950/80 flex items-center justify-center z-50"><Loader2 className="animate-spin text-orange-600" size={48} /></div>}
    </div>
  );
}
