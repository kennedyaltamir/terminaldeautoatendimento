// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 11:15:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { Bike, MapPin, Navigation, Phone, CheckCircle2, Loader2, RefreshCw, Compass } from "lucide-react";
import { getKitchenOrders, updateOrderStatus } from "@/lib/api";
import { Order } from "@/types";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";

export default function DriverPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [coords, setCoords] = useState({ lat: -23.5614, lng: -46.6559 }); // Mock inicial (MASP)

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
        headers: { 
          "Authorization": `Bearer ${getToken()}`,
          "Content-Type": "application/json" 
        }
      });
      if (res.ok) {
        toast.success("Rota iniciada!");
        fetchOrders();
      }
    } catch (e) { toast.error("Erro ao iniciar rota"); }
  };

  const deliveringOrders = orders.filter(o => o.status === 'delivering');
  const readyOrders = orders.filter(o => o.status === 'ready');

  return (
    <div className="min-h-screen bg-slate-900 text-white p-4 pb-24 font-sans">
      <Toaster position="top-center" richColors />
      
      <header className="flex justify-between items-center mb-6 bg-slate-800 p-4 rounded-2xl border border-slate-700 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-xl"><Bike size={24} /></div>
          <div>
            <h1 className="font-black text-lg tracking-tight">App Entregador</h1>
            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">MesaFlow Logistics</p>
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center gap-1 text-emerald-400 text-xs font-bold">
            <Compass size={12} className="animate-spin-slow" /> GPS ATIVO
          </div>
          <p className="text-[10px] font-mono text-slate-500">{coords.lat.toFixed(4)}, {coords.lng.toFixed(4)}</p>
        </div>
      </header>

      <div className="space-y-6">
        {/* ABA: EM ROTA (PRIORIDADE) */}
        {deliveringOrders.length > 0 && (
          <section className="space-y-4">
            <h2 className="text-xs font-black text-blue-400 uppercase tracking-[0.2em] px-2">Em Entrega ({deliveringOrders.length})</h2>
            {deliveringOrders.map(order => (
              <div key={order.id} className="bg-blue-600 rounded-3xl p-6 shadow-2xl border border-blue-400 animate-pulse-slow">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-black">{order.customer_name}</h3>
                  <span className="bg-white/20 px-2 py-1 rounded text-[10px] font-black uppercase">Navegando</span>
                </div>
                <div className="bg-black/20 p-4 rounded-2xl mb-4 flex items-start gap-3">
                  <MapPin size={18} className="text-white mt-1" />
                  <p className="text-sm font-bold leading-tight">{order.delivery_address}</p>
                </div>
                <div className="flex gap-2">
                  <button className="flex-1 bg-white text-blue-600 py-4 rounded-2xl font-black uppercase text-xs flex items-center justify-center gap-2 shadow-lg">
                    <Navigation size={18} /> Abrir Waze
                  </button>
                  <button className="bg-emerald-500 text-white p-4 rounded-2xl shadow-lg">
                    <Phone size={20} />
                  </button>
                </div>
              </div>
            ))}
          </section>
        )}

        {/* ABA: A RETIRAR */}
        <section className="space-y-4">
          <h2 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-2">A Retirar ({readyOrders.length})</h2>
          {readyOrders.length === 0 && !loading && (
            <div className="text-center py-12 bg-slate-800/50 rounded-3xl border-2 border-dashed border-slate-700">
              <p className="text-slate-500 font-bold">Nenhum pedido pronto.</p>
            </div>
          )}
          {readyOrders.map(order => (
            <div key={order.id} className="bg-slate-800 rounded-3xl p-6 border border-slate-700 shadow-xl">
              <div className="flex justify-between items-center mb-4">
                <span className="text-xs font-black text-slate-500">#{order.id.slice(0,6)}</span>
                <span className="text-xs font-black text-orange-500 uppercase">Pronto</span>
              </div>
              <h3 className="text-lg font-bold mb-4">{order.customer_name}</h3>
              <button 
                onClick={() => handlePickup(order.id)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-2xl font-black uppercase text-xs tracking-widest transition-all active:scale-95 shadow-lg shadow-blue-900/20"
              >
                Pegar Pedido
              </button>
            </div>
          ))}
        </section>
      </div>

      {loading && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <Loader2 className="animate-spin text-blue-500" size={48} />
        </div>
      )}
    </div>
  );
}
