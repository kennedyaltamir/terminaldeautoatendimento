// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 16:30:00
"use client";
import { useEffect, useState, useCallback, useRef, useMemo } from "react";
import { Bike, MapPin, Loader2, Compass, ExternalLink, RefreshCw } from "lucide-react";
import { Order } from "@/types";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import { fetchRoute } from "@/lib/routing";
import dynamic from "next/dynamic";

const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { ssr: false });

const FALLBACK_LAT = -19.22448;
const FALLBACK_LNG = -44.93548;
const DEST_LAT = -19.22815;
const DEST_LNG = -44.94195;

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

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 30000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update") {
      setOrders(prev => prev.map(o => {
        if (String(o.id) === String(data.order_id)) return { ...o, status: data.status };
        if (data.status === 'delivering' && o.status === 'delivering') return { ...o, status: 'ready' };
        return o;
      }));
    }
  });

  const activeDelivery = useMemo(() => orders.find(o => o.status === 'delivering'), [orders]);

  // GPS REAL com THROTTLE
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
        () => toast.error("GPS inacessível"),
        { enableHighAccuracy: true, timeout: 5000 }
      );
    }
    return () => { if (watchId.current) navigator.geolocation.clearWatch(watchId.current); };
  }, [activeDelivery?.id]);

  useEffect(() => {
    if (activeDelivery) {
      const targetPos: [number, number] = [activeDelivery.delivery_lat ?? DEST_LAT, activeDelivery.delivery_lng ?? DEST_LNG];
      fetchRoute(driverPos, targetPos).then(setRouteData);
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
        toast.error(err.detail || "Erro ao coletar");
      }
    } catch (e) { toast.error("Falha na rede"); }
  };

  const openExternalMap = (mode: 'google' | 'waze') => {
    if (!activeDelivery) return;
    const lat = activeDelivery.delivery_lat ?? DEST_LAT;
    const lng = activeDelivery.delivery_lng ?? DEST_LNG;
    const url = mode === 'google' 
      ? `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&travelmode=driving`
      : `https://waze.com/ul?ll=${lat},${lng}&navigate=yes`;
    window.open(url, '_blank');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 pb-24 font-sans">
      <Toaster position="top-center" richColors />
      <header className="flex justify-between items-center mb-6 bg-slate-900 p-5 rounded-[2rem] border border-slate-800 shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg"><Bike size={28} /></div>
          <div>
            <h1 className="font-black text-xl tracking-tight">Painel Logístico</h1>
            <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Pompéu / MG</p>
          </div>
        </div>
        <div className="flex gap-2">
            <button onClick={fetchOrders} className="p-3 bg-slate-800 rounded-xl hover:bg-slate-700 transition-all">
                <RefreshCw size={18} className={loading ? "animate-spin" : ""} />
            </button>
        </div>
      </header>

      <main className="space-y-6">
        {activeDelivery ? (
          <div className="space-y-6 animate-in fade-in zoom-in duration-500" data-testid="driver.delivery.active">
             <div className="bg-white text-slate-900 p-8 rounded-[2.5rem] shadow-2xl flex justify-between items-center border-b-8 border-orange-500">
                <div className="flex-1">
                   <h3 className="font-black text-2xl tracking-tighter line-clamp-1">{activeDelivery.customer_name}</h3>
                   <div className="flex items-start gap-2 text-slate-500 text-sm mt-1 font-bold">
                      <MapPin size={16} className="text-orange-500 mt-0.5 shrink-0" /> 
                      <span className="line-clamp-2">{activeDelivery.delivery_address}</span>
                   </div>
                </div>
                <div className="text-right ml-4">
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Tempo</p>
                   <p className="text-3xl font-black text-orange-600" data-testid="driver.delivery.eta">
                    {routeData ? Math.ceil(routeData.duration / 60) : "--"} min
                   </p>
                </div>
             </div>
             
             <div className="h-[400px] w-full" data-testid="driver.delivery.map">
                <TrackingMap 
                  driverPos={driverPos} 
                  clientPos={[activeDelivery.delivery_lat ?? DEST_LAT, activeDelivery.delivery_lng ?? DEST_LNG]} 
                  routeGeojson={routeData?.geometry}
                  duration={routeData?.duration}
                />
             </div>

             <div className="grid grid-cols-2 gap-3">
                <button onClick={() => openExternalMap('google')} className="bg-slate-800 hover:bg-slate-700 text-white py-4 rounded-2xl font-black uppercase text-xs flex items-center justify-center gap-2 transition-all active:scale-95 shadow-lg">
                    <ExternalLink size={18} /> Google Maps
                </button>
                <button onClick={() => openExternalMap('waze')} className="bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-2xl font-black uppercase text-xs flex items-center justify-center gap-2 transition-all active:scale-95 shadow-lg">
                    <Bike size={18} /> Waze
                </button>
             </div>
          </div>
        ) : (
          <section className="space-y-4 px-2">
            <h2 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-4">Pedidos para Coleta</h2>
            {orders.filter(o => o.status === 'ready').map(order => (
              <div 
                key={order.id} 
                data-testid="driver.delivery.order.card"
                data-order-id={order.id}
                className="bg-slate-900 rounded-[2.5rem] p-8 border border-slate-800 shadow-xl flex justify-between items-center hover:border-orange-500/50 transition-all"
              >
                <div className="flex-1 mr-4">
                  <h3 className="font-black text-lg tracking-tight">{order.customer_name}</h3>
                  <p className="text-xs text-slate-500 mt-1 font-medium line-clamp-1">{order.delivery_address}</p>
                </div>
                <button 
                  data-testid="driver.delivery.order.pickup"
                  onClick={() => handlePickup(order.id)}
                  className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-4 rounded-2xl font-black uppercase text-xs tracking-widest shadow-xl active:scale-95 transition-all"
                >
                  Pegar
                </button>
              </div>
            ))}
            {orders.filter(o => o.status === 'ready').length === 0 && (
               <div className="py-20 text-center text-slate-600 italic">Nenhuma coleta disponível.</div>
            )}
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
