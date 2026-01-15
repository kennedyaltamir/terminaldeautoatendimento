"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Order } from "@/types";
import { Bike, MapPin, CheckCircle2, Navigation, Phone, Clock, User, ChefHat, Wallet, Loader2 } from "lucide-react";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";
import DispatchModal from "@/components/admin/DispatchModal";
import DriverCashModal from "@/components/admin/DriverCashModal";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function DeliveryPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState<string | null>(null);
  const [isCashModalOpen, setIsCashModalOpen] = useState(false);
  const router = useRouter();

  const fetchOrders = useCallback(async () => {
    try {
      const token = getToken();
      const res = await fetch(`${API_URL}/admin/delivery/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setOrders(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 15000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  const handleComplete = async (id: string) => {
    if (!confirm("Confirmar entrega realizada?")) return;
    try {
      const token = getToken();
      await fetch(`${API_URL}/admin/delivery/orders/${id}/complete`, {
        method: "PATCH",
        headers: { 
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: null }) 
      });
      toast.success("Entrega finalizada!");
      fetchOrders();
    } catch (e) {
      toast.error("Erro ao finalizar entrega.");
    }
  };

  const openMap = (address: string) => {
    window.open(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`, '_blank');
  };

  const openWhatsApp = (phone: string) => {
    window.open(`https://wa.me/${phone}`, '_blank');
  };

  const getStatusBadge = (status: string) => {
    switch(status) {
        case 'pending': return <span className="bg-yellow-100 text-yellow-700 px-2 py-1 rounded text-xs font-bold uppercase">Pendente</span>;
        case 'preparing': return <span className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs font-bold uppercase">Preparando</span>;
        case 'ready': return <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold uppercase">Pronto</span>;
        case 'delivering': return <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-bold uppercase">Em Rota</span>;
        default: return <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs font-bold uppercase">{status}</span>;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 pb-20 animate-in fade-in duration-500">
      <Toaster position="top-center" richColors />
      
      <header className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 p-6 sticky top-0 z-20 flex justify-between items-center shadow-sm">
        <div>
          <h1 className="text-2xl font-black text-slate-900 dark:text-white flex items-center gap-3 tracking-tight">
            <Bike className="text-orange-500" size={28} /> Logística & Entregas
          </h1>
          <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mt-1">Gestão de Frota Própria</p>
        </div>
        <button 
          type="button"
          onClick={() => setIsCashModalOpen(true)}
          className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-xl font-black uppercase text-xs flex items-center gap-2 transition-all shadow-lg shadow-emerald-900/20 active:scale-95"
        >
          <Wallet size={18} /> Prestação de Contas
        </button>
      </header>

      <div className="p-6 max-w-4xl mx-auto space-y-6">
        {loading ? (
          <div className="py-20 text-center space-y-4">
            <Loader2 className="animate-spin text-slate-400 mx-auto" size={40} />
            <p className="text-slate-500 font-bold">Sincronizando rotas...</p>
          </div>
        ) : orders.length === 0 ? (
          <div className="text-center py-32 bg-white dark:bg-slate-900 rounded-[2.5rem] border-2 border-dashed border-slate-200 dark:border-slate-800">
            <Bike size={64} className="mx-auto mb-4 text-slate-200 dark:text-slate-800" />
            <p className="text-slate-500 font-bold">Nenhuma entrega pendente no momento.</p>
          </div>
        ) : (
          orders.map(order => (
            <div key={order.id} className={cn(
              "bg-white dark:bg-slate-900 rounded-[2rem] shadow-xl border-l-[12px] overflow-hidden transition-all hover:translate-x-1",
              order.status === 'delivering' ? 'border-blue-500' : 'border-orange-500'
            )}>
              <div className="p-8">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="font-black text-2xl text-slate-900 dark:text-white tracking-tight">{order.customer_name}</h3>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">#{order.id.slice(0,6)}</span>
                      <div className="w-1 h-1 bg-slate-300 rounded-full"></div>
                      <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{new Date(order.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</span>
                    </div>
                  </div>
                  <span className={cn(
                    "px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest",
                    order.status === 'delivering' ? 'bg-blue-100 text-blue-700' : 'bg-orange-100 text-orange-700'
                  )}>
                    {order.status === 'delivering' ? 'Em Rota' : 'Pronto'}
                  </span>
                </div>

                <div className="bg-slate-50 dark:bg-slate-800/50 p-5 rounded-2xl mb-8 border border-slate-100 dark:border-slate-800 space-y-3">
                  <div className="flex items-start gap-3">
                    <MapPin size={18} className="text-orange-500 mt-1 shrink-0" />
                    <p className="text-sm text-slate-700 dark:text-slate-300 font-bold leading-relaxed">{order.delivery_address}</p>
                  </div>
                  {order.customer_phone && (
                    <div className="flex items-center gap-3">
                      <Phone size={18} className="text-emerald-500 shrink-0" />
                      <p className="text-sm text-slate-700 dark:text-slate-300 font-mono">{order.customer_phone}</p>
                    </div>
                  )}
                </div>

                {order.status === 'delivering' && order.driver_id && (
                   <div className="flex items-center gap-2 mb-4 text-xs text-blue-600 bg-blue-50 p-2 rounded border border-blue-100">
                      <User size={14} />
                      <span>Entregador atribuído (ID: {order.driver_id})</span>
                   </div>
                )}

                <div className="flex gap-2">
                  {order.status === 'ready' ? (
                    <button 
                      type="button"
                      onClick={() => setSelectedOrder(order.id)}
                      className="flex-1 bg-blue-600 text-white py-4 rounded-2xl font-black uppercase text-xs tracking-widest hover:bg-blue-700 transition-all shadow-lg shadow-blue-900/20 active:scale-95 flex items-center justify-center gap-2"
                    >
                      <Bike size={18} /> Iniciar Entrega
                    </button>
                  ) : (
                    <button 
                      type="button"
                      onClick={() => handleComplete(order.id)}
                      className="flex-1 bg-green-600 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-green-700 transition-colors"
                    >
                      <CheckCircle2 size={18} /> Finalizar
                    </button>
                  ) : (
                    <button disabled className="flex-1 bg-gray-200 text-gray-500 py-3 rounded-lg font-bold flex items-center justify-center gap-2 cursor-not-allowed">
                        <ChefHat size={18} /> Aguardando Cozinha
                    </button>
                  )}
                  
                  <button 
                    type="button"
                    onClick={() => openMap(order.delivery_address || "")}
                    className="bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 p-4 rounded-2xl hover:bg-slate-200 dark:hover:bg-slate-700 transition-all"
                    title="Abrir Mapa"
                  >
                    <Navigation size={22} />
                  </button>
                  
                  {order.customer_phone && (
                    <button 
                      type="button"
                      onClick={() => openWhatsApp(order.customer_phone!)}
                      className="bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 p-4 rounded-2xl hover:bg-emerald-200 transition-all"
                      title="WhatsApp"
                    >
                      <Phone size={22} />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <DispatchModal 
        isOpen={!!selectedOrder} 
        onClose={() => setSelectedOrder(null)} 
        orderId={selectedOrder || ""}
        onSuccess={fetchOrders}
      />

      <DriverCashModal 
        isOpen={isCashModalOpen} 
        onClose={() => setIsCashModalOpen(false)} 
      />
    </div>
  );
}
