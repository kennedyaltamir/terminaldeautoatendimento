"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Order } from "@/types";
import { Bike, MapPin, Phone, CheckCircle2, Navigation, RefreshCw, LogOut } from "lucide-react";
import { toast, Toaster } from "sonner";
import { getToken, removeToken } from "@/lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function DriverApp({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'assigned' | 'delivering'>('assigned');
  const router = useRouter();

  const fetchMyOrders = async () => {
    try {
      const token = getToken();
      // Reutilizamos a rota de delivery, mas o backend poderia ter um filtro "meus pedidos"
      // Por enquanto, filtramos no front ou assumimos que o endpoint retorna tudo e filtramos aqui
      // Idealmente: GET /api/driver/my-orders. 
      // Como estamos usando a rota admin, vamos filtrar os que tem driver_id igual ao usuario logado?
      // O endpoint atual /admin/delivery/orders retorna TODOS os pedidos READY/DELIVERING.
      // Vamos assumir que o motorista vê todos os "READY" (para pegar) e os "DELIVERING" que são dele.
      
      const res = await fetch(`${API_URL}/admin/delivery/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (res.ok) {
        const data = await res.json();
        setOrders(data);
      }
    } catch (error) {
      console.error(error);
      toast.error("Erro ao atualizar");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMyOrders();
    const interval = setInterval(fetchMyOrders, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleStartDelivery = async (id: string) => {
    try {
      const token = getToken();
      // Despachar para si mesmo (se já não estiver atribuído)
      // O endpoint dispatch aceita driver_id. Se não mandar, assume quem chamou?
      // Vamos mandar o ID do pedido. O backend atualiza para DELIVERING.
      // Se o pedido já tiver driver_id, ok. Se não, o backend pode atribuir.
      // Como o endpoint dispatch é de admin, o motorista pode não ter permissão se a role não for checada.
      // Vamos assumir que o motorista tem permissão na rota (ajustamos o backend se precisar).
      
      await fetch(`${API_URL}/admin/delivery/orders/${id}/dispatch`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify({}) // Body vazio, mantém driver se já tiver
      });
      
      toast.success("Rota iniciada!");
      fetchMyOrders();
      setActiveTab('delivering');
    } catch (e) {
      toast.error("Erro ao iniciar");
    }
  };

  const handleComplete = async (id: string) => {
    if (!confirm("Confirmar entrega realizada?")) return;
    try {
      const token = getToken();
      await fetch(`${API_URL}/admin/delivery/orders/${id}/complete`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success("Entrega finalizada! 💰");
      fetchMyOrders();
    } catch (e) {
      toast.error("Erro ao finalizar");
    }
  };

  const openMap = (address: string) => {
    // Tenta abrir Waze, fallback para Google Maps
    const encoded = encodeURIComponent(address);
    // Deep link universal
    window.open(`https://www.google.com/maps/dir/?api=1&destination=${encoded}`, '_blank');
  };

  const openWhatsApp = (phone: string) => {
    window.open(`https://wa.me/${phone}`, '_blank');
  };

  const handleLogout = () => {
    removeToken();
    router.push("/admin/login");
  };

  // Filtros
  const readyOrders = orders.filter(o => o.status === 'ready'); // Disponíveis para pegar
  const myDeliveries = orders.filter(o => o.status === 'delivering'); // Em rota (assumindo que só vejo os meus ou todos)

  const displayedOrders = activeTab === 'assigned' ? readyOrders : myDeliveries;

  return (
    <div className="min-h-screen bg-gray-100 pb-20 font-sans">
      <Toaster position="top-center" richColors />
      
      {/* HEADER */}
      <div className="bg-blue-600 text-white p-4 sticky top-0 z-10 shadow-md flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold flex items-center gap-2">
            <Bike className="text-white" /> App Entregador
          </h1>
          <p className="text-xs opacity-80">MesaFlow Logistics</p>
        </div>
        <div className="flex gap-2">
            <button onClick={fetchMyOrders} className="p-2 bg-blue-700 rounded-full hover:bg-blue-800"><RefreshCw size={20}/></button>
            <button onClick={handleLogout} className="p-2 bg-red-500/20 rounded-full hover:bg-red-500/40"><LogOut size={20}/></button>
        </div>
      </div>

      {/* TABS */}
      <div className="flex bg-white border-b border-gray-200">
        <button 
          onClick={() => setActiveTab('assigned')}
          className={`flex-1 py-3 text-sm font-bold border-b-2 transition-colors ${activeTab === 'assigned' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500'}`}
        >
          A Retirar ({readyOrders.length})
        </button>
        <button 
          onClick={() => setActiveTab('delivering')}
          className={`flex-1 py-3 text-sm font-bold border-b-2 transition-colors ${activeTab === 'delivering' ? 'border-green-600 text-green-600' : 'border-transparent text-gray-500'}`}
        >
          Em Rota ({myDeliveries.length})
        </button>
      </div>

      {/* LISTA */}
      <div className="p-4 space-y-4">
        {loading ? (
          <p className="text-center text-gray-500 py-10">Carregando...</p>
        ) : displayedOrders.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <Bike size={48} className="mx-auto mb-2 opacity-20" />
            <p>{activeTab === 'assigned' ? "Nenhum pedido aguardando." : "Você não tem entregas em andamento."}</p>
          </div>
        ) : (
          displayedOrders.map(order => (
            <div key={order.id} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="p-4">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-bold text-lg text-gray-900">{order.customer_name}</h3>
                    <p className="text-xs text-gray-500">#{order.id.slice(0,6)}</p>
                  </div>
                  <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs font-bold">
                    {order.payment_method === 'cash' ? 'Cobrar na Entrega' : 'Já Pago'}
                  </span>
                </div>

                <div className="bg-gray-50 p-3 rounded-lg mb-4 border border-gray-100 space-y-2">
                  <div className="flex items-start gap-2">
                    <MapPin size={16} className="text-red-500 mt-0.5 shrink-0" />
                    <p className="text-sm text-gray-700 leading-tight font-medium">{order.delivery_address}</p>
                  </div>
                  {order.customer_phone && (
                    <div className="flex items-center gap-2">
                      <Phone size={16} className="text-green-500 shrink-0" />
                      <p className="text-sm text-gray-700">{order.customer_phone}</p>
                    </div>
                  )}
                </div>

                {activeTab === 'assigned' ? (
                  <button 
                    onClick={() => handleStartDelivery(order.id)}
                    className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200"
                  >
                    <Bike size={20} /> Pegar Pedido
                  </button>
                ) : (
                  <div className="flex flex-col gap-2">
                    <div className="flex gap-2">
                        <button 
                            onClick={() => openMap(order.delivery_address || "")}
                            className="flex-1 bg-gray-100 text-gray-800 py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-gray-200"
                        >
                            <Navigation size={18} /> GPS
                        </button>
                        {order.customer_phone && (
                            <button 
                                onClick={() => openWhatsApp(order.customer_phone!)}
                                className="flex-1 bg-green-100 text-green-700 py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-green-200"
                            >
                                <Phone size={18} /> WhatsApp
                            </button>
                        )}
                    </div>
                    <button 
                        onClick={() => handleComplete(order.id)}
                        className="w-full bg-green-600 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-green-700 transition-colors shadow-lg shadow-green-200"
                    >
                        <CheckCircle2 size={20} /> Confirmar Entrega
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}