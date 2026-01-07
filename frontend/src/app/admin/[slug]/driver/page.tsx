"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Order } from "@/types";
import { Bike, MapPin, Phone, CheckCircle2, Navigation, RefreshCw, LogOut, Radio } from "lucide-react";
import { toast, Toaster } from "sonner";
import { getToken, removeToken } from "@/lib/auth";
import Modal from "@/components/ui/Modal";
import { useWebSocketContext } from "@/context/WebSocketContext";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function DriverApp({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'assigned' | 'delivering'>('assigned');
  const [confirmingOrderId, setConfirmingOrderId] = useState<string | null>(null);
  const [confirmationCode, setConfirmationCode] = useState("");
  const [isTracking, setIsTracking] = useState(false);

  const router = useRouter();
  const { sendMessage } = useWebSocketContext();
  const watchId = useRef<number | null>(null);

  const fetchMyOrders = async () => {
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

  // Lógica de Rastreamento GPS
  useEffect(() => {
    const myDeliveries = orders.filter(o => o.status === 'delivering');

    if (myDeliveries.length > 0 && !isTracking) {
      startTracking(myDeliveries);
    } else if (myDeliveries.length === 0 && isTracking) {
      stopTracking();
    }

    return () => stopTracking();
  }, [orders]);

  const startTracking = (activeOrders: Order[]) => {
    if (!('geolocation' in navigator)) return;

    setIsTracking(true);
    toast.info("Rastreamento GPS Ativo 🛰️");

    watchId.current = navigator.geolocation.watchPosition(
      (position) => {
        const { latitude, longitude } = position.coords;

        // Envia localização para cada pedido ativo
        activeOrders.forEach(order => {
          sendMessage({
            type: "driver_location",
            order_id: order.id,
            lat: latitude,
            lng: longitude,
            timestamp: new Date().toISOString()
          });
        });
      },
      (error) => console.error("Erro GPS:", error),
      { enableHighAccuracy: true, maximumAge: 10000, timeout: 5000 }
    );
  };

  const stopTracking = () => {
    if (watchId.current !== null) {
      navigator.geolocation.clearWatch(watchId.current);
      watchId.current = null;
    }
    setIsTracking(false);
  };

  const handleStartDelivery = async (id: string) => {
    try {
      const token = getToken();
      await fetch(`${API_URL}/admin/delivery/orders/${id}/dispatch`, {
        method: "PATCH",
        headers: { Authorization: `Bearer ${token}` },
        body: JSON.stringify({}) 
      });

      toast.success("Rota iniciada!");
      fetchMyOrders();
      setActiveTab('delivering');
    } catch (e) {
      toast.error("Erro ao iniciar");
    }
  };

  const handleComplete = async () => {
    if (!confirmingOrderId) return;

    try {
      const token = getToken();
      const res = await fetch(`${API_URL}/admin/delivery/orders/${confirmingOrderId}/complete`, {
        method: "PATCH",
        headers: { 
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}` 
        },
        body: JSON.stringify({ code: confirmationCode })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Erro ao finalizar");
      }

      toast.success("Entrega finalizada! 💰");
      setConfirmingOrderId(null);
      setConfirmationCode("");
      fetchMyOrders();
    } catch (e: any) {
      toast.error(e.message);
    }
  };

  const openMap = (address: string, app: 'waze' | 'google') => {
    const encoded = encodeURIComponent(address);
    if (app === 'waze') {
        window.open(`https://waze.com/ul?q=${encoded}`, '_blank');
    } else {
        window.open(`https://www.google.com/maps/dir/?api=1&destination=${encoded}`, '_blank');
    }
  };

  const openWhatsApp = (phone: string) => {
    window.open(`https://wa.me/${phone}`, '_blank');
  };

  const handleLogout = () => {
    removeToken();
    router.push("/admin/login");
  };

  const readyOrders = orders.filter(o => o.status === 'ready');
  const myDeliveries = orders.filter(o => o.status === 'delivering'); 

  const displayedOrders = activeTab === 'assigned' ? readyOrders : myDeliveries;

  return (
    <div className="min-h-screen bg-gray-100 pb-20 font-sans">
      <Toaster position="top-center" richColors />

      <div className="bg-blue-600 text-white p-4 sticky top-0 z-10 shadow-md flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold flex items-center gap-2">
            <Bike className="text-white" /> App Entregador
          </h1>
          <div className="flex items-center gap-2">
            <p className="text-xs opacity-80">MesaFlow Logistics</p>
            {isTracking && (
              <span className="flex items-center gap-1 bg-blue-800 px-2 py-0.5 rounded-full text-[10px] font-bold animate-pulse">
                <Radio size={10} /> GPS ON
              </span>
            )}
          </div>
        </div>
        <div className="flex gap-2">
            <button onClick={fetchMyOrders} className="p-2 bg-blue-700 rounded-full hover:bg-blue-800" title="Atualizar"><RefreshCw size={20}/></button>
            <button onClick={handleLogout} className="p-2 bg-red-500/20 rounded-full hover:bg-red-500/40" title="Sair"><LogOut size={20}/></button>
        </div>
      </div>

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
                  <span className={`px-2 py-1 rounded text-xs font-bold ${order.payment_method === 'cash' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                    {order.payment_method === 'cash' ? 'Cobrar R$ ' + Number(order.total_amount).toFixed(2) : 'Já Pago'}
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
                            onClick={() => openMap(order.delivery_address || "", 'google')}
                            className="flex-1 bg-gray-100 text-gray-800 py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-gray-200"
                        >
                            <Navigation size={18} /> Maps
                        </button>
                        <button 
                            onClick={() => openMap(order.delivery_address || "", 'waze')}
                            className="flex-1 bg-blue-50 text-blue-600 py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-blue-100"
                        >
                            <Navigation size={18} /> Waze
                        </button>
                    </div>
                    {order.customer_phone && (
                        <button 
                            onClick={() => openWhatsApp(order.customer_phone!)}
                            className="w-full bg-green-100 text-green-700 py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-green-200"
                        >
                            <Phone size={18} /> WhatsApp
                        </button>
                    )}
                    <button 
                        onClick={() => setConfirmingOrderId(order.id)}
                        className="w-full bg-green-600 text-white py-3 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-green-700 transition-colors shadow-lg shadow-green-200 mt-2"
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

      <Modal isOpen={!!confirmingOrderId} onClose={() => setConfirmingOrderId(null)} title="Confirmar Entrega">
        <div className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 text-center">
                <p className="text-sm text-blue-800 font-bold">Segurança de Entrega</p>
                <p className="text-xs text-blue-600">Peça o código de 4 dígitos ao cliente.</p>
            </div>

            <input 
                type="tel" 
                maxLength={4}
                placeholder="0000"
                className="w-full text-center text-3xl font-bold tracking-[0.5em] p-4 border-2 border-gray-300 rounded-xl focus:border-blue-500 outline-none"
                value={confirmationCode}
                onChange={e => setConfirmationCode(e.target.value)}
            />

            <button 
                onClick={handleComplete}
                disabled={confirmationCode.length < 4}
                className="w-full bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold text-lg shadow-lg"
            >
                Validar e Finalizar
            </button>
        </div>
      </Modal>
    </div>
  );
}
