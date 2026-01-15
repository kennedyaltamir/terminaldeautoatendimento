// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 11:45:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { Bike, MapPin, Navigation, Phone, CheckCircle2, Loader2, Compass, ExternalLink, Map as MapIcon } from "lucide-react";
import { Order } from "@/types";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";

export default function DriverPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [coords, setCoords] = useState({ lat: -19.22448, lng: -44.93548 }); // Pompéu MG

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
    const interval = setInterval(fetchOrders, 10000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

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

  const openNavigation = (address: string, mode: 'google' | 'waze') => {
    const encodedAddr = encodeURIComponent(address);
    const url = mode === 'google' 
      ? `https://www.google.com/maps/dir/?api=1&destination=${encodedAddr}`
      : `https://waze.com/ul?q=${encodedAddr}&navigate=yes`;
    window.open(url, '_blank');
  };

  const deliveringOrders = orders.filter(o => o.status === 'delivering');
  const readyOrders = orders.filter(o => o.status === 'ready');

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 pb-24 font-sans">
      <Toaster position="top-center" richColors />
      
      <header className="flex justify-between items-center mb-6 bg-slate-900 p-5 rounded-[2rem] border border-slate-800 shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-blue-600 p-3 rounded-2xl shadow-lg shadow-blue-900/20"><Bike size={28} /></div>
          <div>
            <h1 className="font-black text-xl tracking-tight">Painel de Entrega</h1>
            <p className="text-[10px] text-slate-500 font-black uppercase tracking-widest">Pompéu / MG</p>
          </div>
        </div>
        <div className="text-right bg-black/30 p-3 rounded-2xl border border-white/5">
          <div className="flex items-center justify-end gap-1 text-emerald-400 text-[10px] font-black uppercase">
            <Compass size={12} className="animate-spin-slow" /> GPS Ativo
          </div>
          <p className="text-xs font-mono text-slate-400 mt-1">{coords.lat.toFixed(5)}, {coords.lng.toFixed(5)}</p>
        </div>
      </header>

      <div className="space-y-8">
        {deliveringOrders.map(order => (
          <div key={order.id} className="bg-blue-600 rounded-[2.5rem] p-8 shadow-2xl border border-blue-400 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-10"><Navigation size={120} /></div>
            <div className="relative z-10">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-black tracking-tight">{order.customer_name}</h3>
                  <p className="text-blue-100 text-xs font-bold uppercase tracking-widest mt-1">Pedido #{order.id.slice(0,6)}</p>
                </div>
                <span className="bg-white text-blue-600 px-3 py-1 rounded-full text-[10px] font-black uppercase">Em Rota</span>
              </div>
              
              <div className="bg-black/20 backdrop-blur-md p-5 rounded-3xl mb-8 border border-white/10">
                <p className="text-[10px] text-blue-200 font-black uppercase tracking-widest mb-2">Destino</p>
                <div className="flex items-start gap-3">
                  <MapPin size={20} className="text-white shrink-0 mt-1" />
                  <p className="text-lg font-bold leading-tight">{order.delivery_address}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <button 
                  onClick={() => openNavigation(order.delivery_address || "", 'google')}
                  className="bg-white text-blue-700 py-5 rounded-2xl font-black uppercase text-xs flex items-center justify-center gap-2 shadow-xl active:scale-95 transition-all"
                >
                  <MapIcon size={18} /> Google Maps
                </button>
                <button 
                  onClick={() => openNavigation(order.delivery_address || "", 'waze')}
                  className="bg-slate-900 text-white py-5 rounded-2xl font-black uppercase text-xs flex items-center justify-center gap-2 shadow-xl active:scale-95 transition-all"
                >
                  <ExternalLink size={18} /> Waze
                </button>
              </div>
            </div>
          </div>
        ))}

        <section className="space-y-4">
          <h2 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-4">Pedidos Prontos ({readyOrders.length})</h2>
          {readyOrders.map(order => (
            <div key={order.id} className="bg-slate-900 rounded-[2rem] p-6 border border-slate-800 shadow-xl flex justify-between items-center group hover:border-blue-500/50 transition-all">
              <div>
                <h3 className="font-bold text-slate-200">{order.customer_name}</h3>
                <p className="text-[10px] text-slate-500 font-mono mt-1">{order.delivery_address?.substring(0, 30)}...</p>
              </div>
              <button 
                onClick={() => handlePickup(order.id)}
                className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-xl font-black uppercase text-[10px] tracking-widest transition-all shadow-lg shadow-blue-900/20"
              >
                Pegar
              </button>
            </div>
          ))}
        </section>
      </div>

      {loading && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50">
          <Loader2 className="animate-spin text-blue-500" size={48} />
        </div>
      )}
    </div>
  );
}
