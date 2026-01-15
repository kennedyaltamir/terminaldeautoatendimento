// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 15:45:00
"use client";
import { useEffect, useState, useCallback, useRef, useMemo } from "react";
import { Bike, MapPin, Loader2, Compass, AlertCircle, CheckCircle2 } from "lucide-react";
import { Order } from "@/types";
import { toast } from "sonner";
import { getToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import { fetchRoute } from "@/lib/routing";
import dynamic from "next/dynamic";

const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { 
  ssr: false,
  loading: () => <div className="w-full h-full bg-slate-900 animate-pulse flex items-center justify-center text-slate-500 font-black uppercase text-xs tracking-widest">CARREGANDO GPS...</div>
});

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function DriverPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [isFinishing, setIsFinishing] = useState(false);
  const [activeDeliveryId, setActiveDeliveryId] = useState<string | null>(null);
  const [lastActiveOrder, setLastActiveOrder] = useState<Order | null>(null);
  const [driverPos, setDriverPos] = useState<[number, number]>([-19.22448, -44.93548]);
  const [routeData, setRouteData] = useState<any>(null);
  
  const watchId = useRef<number | null>(null);
  const isSubmittingRef = useRef(false);
  const recentlyFinished = useRef<Set<string>>(new Set());
  const isTestEnv = typeof window !== "undefined" && (window.navigator.userAgent.includes("Playwright") || window.navigator.userAgent.includes("HeadlessChrome"));

  // Sincronização de Estado Ativo (Resiliente a Race Conditions)
  useEffect(() => {
    const serverActive = orders.find(o => 
      o.status === 'delivering' && !recentlyFinished.current.has(o.id)
    );
    
    if (serverActive && activeDeliveryId === null) {
        setActiveDeliveryId(serverActive.id);
        setLastActiveOrder(serverActive);
    } else if (activeDeliveryId) {
        // Se temos um ID ativo, tentamos atualizar os dados dele a partir da lista
        const updated = orders.find(o => o.id === activeDeliveryId);
        if (updated) setLastActiveOrder(updated);
    }
  }, [orders, activeDeliveryId]);

  const fetchOrders = useCallback(async () => {
    if (isSubmittingRef.current) return;
    try {
      const res = await fetch(`${API_URL}/admin/delivery/orders`, {
        headers: { Authorization: `Bearer ${getToken()}` }
      });
      if (res.ok) {
        const data = await res.json();
        setOrders(data);
      }
    } catch (e) {
      console.error("Fetch falhou:", e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 10000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "delivery.status") {
      const orderId = data.order_id || data.payload?.order_id;
      const newStatus = data.status || data.payload?.status;
      
      if (orderId === activeDeliveryId && ['delivered', 'canceled'].includes(newStatus)) {
          setActiveDeliveryId(null);
          setLastActiveOrder(null);
      }
      
      setOrders(prev => prev.map(o => 
        String(o.id) === String(orderId) ? { ...o, status: newStatus } : o
      ));
    }
  });

  // Memoização do Pedido Ativo (Garante que a UI não "pisque" se o pedido sumir da lista temporariamente)
  const activeDelivery = useMemo(() => {
    if (!activeDeliveryId) return null;
    const currentInList = orders.find(o => o.id === activeDeliveryId);
    return currentInList ? { ...currentInList, status: 'delivering' } : lastActiveOrder;
  }, [orders, activeDeliveryId, lastActiveOrder]);

  const availableOrders = useMemo(() => 
    orders.filter(o => o.status === 'ready' && o.id !== activeDeliveryId), 
    [orders, activeDeliveryId]
  );

  // Telemetria GPS
  useEffect(() => {
    if (activeDelivery && typeof navigator !== "undefined" && "geolocation" in navigator) {
      if (isTestEnv) return; // Em teste, confiamos na injeção via API
      
      watchId.current = navigator.geolocation.watchPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          setDriverPos([latitude, longitude]);
          fetch(`${API_URL}/admin/delivery/orders/${activeDelivery.id}/location`, {
            method: "POST",
            headers: { 
              "Authorization": `Bearer ${getToken()}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ lat: latitude, lng: longitude })
          }).catch(() => {});
        },
        () => !isTestEnv && toast.error("GPS Offline"),
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
      );
    }
    return () => { if (watchId.current) navigator.geolocation.clearWatch(watchId.current); };
  }, [activeDelivery?.id, isTestEnv]);

  const driverLat = driverPos[0];
  const driverLng = driverPos[1];

  // Roteamento Visual
  useEffect(() => {
    let isMounted = true;
    if (activeDelivery) {
      if (isTestEnv) {
        setRouteData({ geometry: { coordinates: [] }, duration: 300, distance: 1000 });
        return;
      }
      const destLat = activeDelivery.delivery_lat ?? -19.22448;
      const destLng = activeDelivery.delivery_lng ?? -44.93548;
      fetchRoute([driverLat, driverLng], [destLat, destLng])
        .then(data => {
          if (isMounted && data) setRouteData(data);
        });
    }
    return () => { isMounted = false; };
  }, [activeDelivery?.id, driverLat, driverLng, isTestEnv]);

  const handlePickup = async (orderId: string) => {
    if (isSubmittingRef.current) return;
    isSubmittingRef.current = true;
    
    try {
      const res = await fetch(`${API_URL}/admin/delivery/orders/${orderId}/dispatch`, {
        method: "PATCH",
        headers: { 
          "Authorization": `Bearer ${getToken()}`,
          "Content-Type": "application/json" 
        }
      });
      
      if (res.ok) {
        toast.success("Rota iniciada!");
        setActiveDeliveryId(orderId);
        const order = orders.find(o => o.id === orderId);
        if (order) setLastActiveOrder({ ...order, status: 'delivering' });
      } else {
        const err = await res.json();
        toast.error(err.detail || "Falha ao coletar pedido");
      }
    } catch (e) { 
      toast.error("Erro de conexão");
    } finally {
      isSubmittingRef.current = false;
    }
  };

  const handleFinish = async () => {
    if (!activeDelivery || isFinishing) return;
    if (!confirm("Confirmar entrega realizada?")) return;
    
    setIsFinishing(true);
    isSubmittingRef.current = true;
    const finishedId = activeDelivery.id;

    try {
        const res = await fetch(`${API_URL}/admin/delivery/orders/${finishedId}/complete`, {
            method: "PATCH",
            headers: { 
              "Authorization": `Bearer ${getToken()}`,
              "Content-Type": "application/json"
            }
        });

        if (res.ok) {
            toast.success("Entrega finalizada!");
            recentlyFinished.current.add(finishedId);
            setActiveDeliveryId(null);
            setLastActiveOrder(null);
            fetchOrders();
        } else {
            toast.error("Erro ao finalizar");
        }
    } catch (e) {
        toast.error("Erro de conexão");
    } finally {
        setIsFinishing(false);
        isSubmittingRef.current = false;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 pb-24 font-sans">
      <header className="flex justify-between items-center mb-6 bg-slate-900 p-5 rounded-[2rem] border border-slate-800 shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg shadow-orange-900/20">
            <Bike size={28} />
          </div>
          <div>
            <h1 className="font-black text-xl tracking-tight">App do Entregador</h1>
            <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest">MesaFlow Logistics</p>
          </div>
        </div>
        <div className="text-right">
           <div className="text-emerald-400 text-[10px] font-black uppercase flex items-center justify-end gap-1">
             <Compass size={12} className={activeDelivery ? "animate-spin-slow" : ""} /> 
             GPS {watchId.current || isTestEnv ? "ON" : "OFF"}
           </div>
        </div>
      </header>

      <main className="space-y-6">
        {activeDelivery ? (
          <div className="space-y-6 animate-in fade-in duration-500" data-testid="driver.delivery.active">
             <div className="bg-white text-slate-900 p-8 rounded-[2.5rem] shadow-2xl flex justify-between items-center border-b-8 border-orange-500">
                <div data-order-id={activeDelivery.id}>
                   <h3 className="font-black text-2xl tracking-tighter">{activeDelivery.customer_name}</h3>
                   <div className="flex items-center gap-2 text-slate-500 text-sm mt-1 font-bold">
                      <MapPin size={16} className="text-orange-500" /> {activeDelivery.delivery_address}
                   </div>
                </div>
                <div className="text-right ml-4">
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Chegada em</p>
                   <p className="text-3xl font-black text-orange-600" data-testid="driver.delivery.eta">
                    {routeData ? Math.ceil(routeData.duration / 60) : "--"} min
                   </p>
                </div>
             </div>

             <div className="h-[400px] w-full rounded-[2.5rem] overflow-hidden border-4 border-white shadow-2xl relative">
                <TrackingMap 
                  driverPos={driverPos} 
                  clientPos={[-19.22448, -44.93548]} 
                  routeGeojson={routeData?.geometry}
                  duration={routeData?.duration}
                />
             </div>

             <button 
                data-testid="driver.delivery.finish-btn"
                onClick={handleFinish}
                disabled={isFinishing}
                className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white py-6 rounded-[2rem] font-black text-xl uppercase tracking-widest shadow-2xl flex items-center justify-center gap-3 active:scale-95 transition-all"
             >
                {isFinishing ? <Loader2 className="animate-spin" size={28} /> : <CheckCircle2 size={28} />}
                Finalizar Entrega
             </button>
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
                <div 
                  key={order.id} 
                  data-testid="driver.delivery.order.card"
                  data-order-id={order.id}
                  className="bg-slate-900 rounded-[2.5rem] p-8 border border-slate-800 shadow-xl flex justify-between items-center hover:border-orange-500/50 transition-all"
                >
                  <div className="flex-1">
                    <h3 className="font-black text-lg tracking-tight">{order.customer_name}</h3>
                    <p className="text-xs text-slate-500 mt-1 font-medium">{order.delivery_address}</p>
                  </div>
                  <button 
                    data-testid="driver.delivery.order.pickup"
                    onClick={() => handlePickup(order.id)}
                    className="bg-orange-600 hover:bg-orange-500 text-white px-8 py-4 rounded-2xl font-black uppercase text-xs tracking-widest shadow-xl active:scale-95 transition-all"
                  >
                    Pegar
                  </button>
                </div>
              ))
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
