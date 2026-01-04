"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Order } from "@/types";
import { Bike, MapPin, CheckCircle2, Navigation, Phone, Clock, User, ChefHat } from "lucide-react";
import { toast, Toaster } from "sonner";
import { getToken } from "@/lib/auth";
import DispatchModal from "@/components/admin/DispatchModal";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function DeliveryPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState<string | null>(null);
  const router = useRouter();

  const fetchOrders = async () => {
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
  };

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleComplete = async (id: string) => {
    if (!confirm("Confirmar entrega realizada?")) return;
    try {
      const token = getToken();
      await fetch(`${API_URL}/admin/delivery/orders/${id}/complete`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify({ code: null }) // Admin pode bypassar código se necessário, ou implementar modal
      });
      toast.success("Entrega finalizada!");
      fetchOrders();
    } catch (e) {
      toast.error("Erro ao finalizar");
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
    <div className="min-h-screen bg-gray-100 pb-20">
      <Toaster position="top-center" richColors />
      
      <div className="bg-gray-900 text-white p-4 sticky top-0 z-10 shadow-md">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <Bike className="text-orange-500" /> Entregas
        </h1>
        <p className="text-xs text-gray-400">Gestão de Logística</p>
      </div>

      <div className="p-4 space-y-4">
        {loading ? (
          <p className="text-center text-gray-500 py-10">Carregando...</p>
        ) : orders.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <Bike size={48} className="mx-auto mb-2 opacity-20" />
            <p>Nenhuma entrega pendente.</p>
          </div>
        ) : (
          orders.map(order => (
            <div key={order.id} className={`bg-white rounded-xl shadow-sm border-l-4 overflow-hidden ${order.status === 'delivering' ? 'border-blue-500' : order.status === 'ready' ? 'border-green-500' : 'border-yellow-500'}`}>
              <div className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-bold text-lg">{order.customer_name}</h3>
                    <p className="text-xs text-gray-500">#{order.id.slice(0,6)} • {new Date(order.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</p>
                  </div>
                  {getStatusBadge(order.status)}
                </div>

                <div className="bg-gray-50 p-3 rounded-lg mb-4 border border-gray-100">
                  <div className="flex items-start gap-2 mb-2">
                    <MapPin size={16} className="text-orange-500 mt-0.5 shrink-0" />
                    <p className="text-sm text-gray-700 leading-tight">{order.delivery_address}</p>
                  </div>
                  {order.customer_phone && (
                    <div className="flex items-center gap-2">
                      <Phone size={16} className="text-green-500 shrink-0" />
                      <p className="text-sm text-gray-700">{order.customer_phone}</p>
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
                      onClick={() => setSelectedOrder(order.id)}
                      className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-blue-700 transition-colors"
                    >
                      <Bike size={18} /> Iniciar Entrega
                    </button>
                  ) : order.status === 'delivering' ? (
                    <button 
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
                    onClick={() => openMap(order.delivery_address || "")}
                    className="bg-gray-100 text-gray-700 p-3 rounded-lg hover:bg-gray-200"
                    title="Abrir Mapa"
                  >
                    <Navigation size={20} />
                  </button>
                  
                  {order.customer_phone && (
                    <button 
                      onClick={() => openWhatsApp(order.customer_phone!)}
                      className="bg-green-100 text-green-700 p-3 rounded-lg hover:bg-green-200"
                      title="WhatsApp"
                    >
                      <Phone size={20} />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {selectedOrder && (
        <DispatchModal 
          isOpen={!!selectedOrder} 
          onClose={() => setSelectedOrder(null)} 
          orderId={selectedOrder}
          onSuccess={fetchOrders}
        />
      )}
    </div>
  );
}