"use client";

import { useEffect, useState, useCallback, use } from "react";
import { useRouter } from "next/navigation";
import { 
  Bike, 
  MapPin, 
  CheckCircle2, 
  Navigation, 
  Phone, 
  Clock, 
  User, 
  ChefHat, 
  Wallet, 
  Loader2,
  AlertCircle,
  RefreshCw,
  Undo2,
  ExternalLink
} from "lucide-react";
import { toast, Toaster } from "sonner";
import { Order } from "@/types";
import { getToken } from "@/lib/auth";
import { cn, formatCurrency } from "@/lib/utils";
// Componentes de Suporte
import DispatchModal from "@/components/admin/DispatchModal";
import DriverCashModal from "@/components/admin/DriverCashModal";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function DeliveryPage({ params }: { params: Promise<{ slug: string }> }) {
  // FIX: Desembrulhando params com use()
  const { slug } = use(params);
  const router = useRouter();

  // --- ESTADOS ---
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);
  const [isCashModalOpen, setIsCashModalOpen] = useState(false);

  // --- BUSCA DE DADOS ---
  const fetchOrders = useCallback(async (isManual = false) => {
    if (isManual) setRefreshing(true);
    try {
      const token = getToken();
      const res = await fetch(`${API_URL}/admin/delivery/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        // Filtra apenas pedidos de entrega (Delivery)
        setOrders(data.filter((o: Order) => o.order_type === 'delivery'));
      } else if (res.status === 401) {
        router.push("/admin/login");
      }
    } catch (error) {
      console.error("[Logística] Erro de sincronização:", error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [router]);

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(() => fetchOrders(), 15000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  // --- AÇÕES ---
  const handlePickup = async (orderId: string) => {
    try {
      const token = getToken();
      const res = await fetch(`${API_URL}/admin/delivery/orders/${orderId}/dispatch`, {
        method: "PATCH",
        headers: { 
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });
      if (res.ok) {
        toast.success("Entrega iniciada! O cliente já pode rastrear.");
        fetchOrders();
      }
    } catch (e) {
      toast.error("Falha ao iniciar rota.");
    }
  };

  const handleComplete = async (orderId: string) => {
    if (!confirm("Confirmar que o pedido foi entregue ao cliente?")) return;
    try {
      const token = getToken();
      const res = await fetch(`${API_URL}/admin/delivery/orders/${orderId}/complete`, {
        method: "PATCH",
        headers: { 
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: null })
      });
      if (res.ok) {
        toast.success("Pedido finalizado com sucesso!");
        fetchOrders();
      }
    } catch (e) {
      toast.error("Erro ao concluir entrega.");
    }
  };

  const handleRollback = async (orderId: string) => {
    if (!confirm("Devolver este pedido para a fila da cozinha?")) return;
    try {
      const token = getToken();
      await fetch(`${API_URL}/admin/orders/${orderId}`, {
        method: "PATCH",
        headers: { 
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ status: "preparing" })
      });
      toast.info("Pedido devolvido para a cozinha.");
      fetchOrders();
    } catch (e) {
      toast.error("Erro ao estornar pedido.");
    }
  };

  const openMap = (address: string) => {
    if (!address) return toast.error("Endereço não informado.");
    window.open(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`, '_blank');
  };

  const openWhatsApp = (phone: string) => {
    if (!phone) return toast.error("Telefone não disponível.");
    const cleanPhone = phone.replace(/\D/g, '');
    window.open(`https://wa.me/${cleanPhone}`, '_blank');
  };

  // --- UI HELPERS ---
  const getStatusBadge = (status: string) => {
    const config: any = {
      pending: { label: "Pendente", class: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20" },
      preparing: { label: "Cozinha", class: "bg-orange-500/10 text-orange-500 border-orange-500/20" },
      ready: { label: "Pronto", class: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" },
      delivering: { label: "Em Rota", class: "bg-blue-500/10 text-blue-500 border-blue-500/20" },
    };
    const current = config[status] || { label: status, class: "bg-slate-500/10 text-slate-500" };
    return (
      <span className={cn("px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border", current.class)}>
        {current.label}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white pb-20 animate-in fade-in duration-500">
      <Toaster position="top-center" richColors theme="dark" />
      
      {/* HEADER */}
      <header className="bg-slate-900/50 backdrop-blur-md border-b border-white/5 p-6 sticky top-0 z-30 flex justify-between items-center shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="bg-orange-600 p-3 rounded-2xl shadow-lg shadow-orange-900/20">
            <Bike className="text-white" size={28} />
          </div>
          <div>
            <h1 className="text-2xl font-black tracking-tighter uppercase">Logística</h1>
            <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
              <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
              {orders.length} Entregas Ativas
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => fetchOrders(true)}
            className="p-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-all text-slate-400 hover:text-white"
            title="Atualizar Lista"
          >
            <RefreshCw size={20} className={refreshing ? "animate-spin" : ""} />
          </button>
          <button 
            onClick={() => setIsCashModalOpen(true)}
          className="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-3 rounded-2xl font-black uppercase text-xs flex items-center gap-2 transition-all shadow-lg shadow-emerald-900/20 active:scale-95"
          >
            <Wallet size={18} /> Prestação de Contas
          </button>
        </div>
      </header>

      <div className="p-6 max-w-5xl mx-auto space-y-6">
        {loading ? (
          <div className="py-32 text-center space-y-4">
            <Loader2 className="animate-spin text-orange-500 mx-auto" size={48} />
            <p className="text-slate-500 font-black uppercase tracking-widest text-xs">Sincronizando Rotas...</p>
          </div>
        ) : orders.length === 0 ? (
          <div className="text-center py-40 bg-slate-900/30 rounded-[3rem] border-2 border-dashed border-white/5">
            <Bike size={80} className="mx-auto mb-6 text-slate-800 opacity-50" />
            <h2 className="text-xl font-bold text-slate-400">Nenhuma entrega pendente</h2>
            <p className="text-sm text-slate-600 mt-2">Pedidos prontos para entrega aparecerão aqui.</p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
            {orders.map(order => (
              <div 
                key={order.id} 
                data-testid={`driver-card-${order.id}`}
                className={cn(
                  "bg-slate-900 rounded-[2.5rem] border-l-[12px] overflow-hidden transition-all hover:shadow-2xl hover:translate-y-[-2px] border border-white/5",
                  order.status === 'delivering' ? 'border-l-blue-600' : 'border-l-emerald-600'
                )}
              >
                <div className="p-8">
                  <div className="flex justify-between items-start mb-6">
                    <div>
                      <h3 className="font-black text-2xl tracking-tight truncate max-w-[200px]">
                        {order.customer_name || "Cliente"}
                      </h3>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">#{order.id.slice(0,6)}</span>
                        <div className="w-1 h-1 bg-slate-700 rounded-full"></div>
                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1">
                          <Clock size={10} /> {new Date(order.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
                        </span>
                      </div>
                    </div>
                    {getStatusBadge(order.status)}
                  </div>

                  {/* INFO BOX */}
                  <div className="bg-slate-950/50 p-5 rounded-3xl mb-8 border border-white/5 space-y-4">
                    <div className="flex items-start gap-3">
                      <MapPin size={20} className="text-orange-500 mt-1 shrink-0" />
                      <p className="text-sm text-slate-300 font-bold leading-relaxed">
                        {order.delivery_address || "Retirada no Balcão"}
                      </p>
                    </div>
                    {order.customer_phone && (
                      <div className="flex items-center gap-3">
                        <Phone size={18} className="text-emerald-500 shrink-0" />
                        <p className="text-sm text-slate-400 font-mono">{order.customer_phone}</p>
                      </div>
                    )}
                  </div>

                  {/* DRIVER ASSIGNMENT */}
                  {order.status === 'delivering' && order.driver_id && (
                     <div className="flex items-center gap-2 mb-6 text-[10px] font-black uppercase tracking-widest text-blue-400 bg-blue-500/10 p-3 rounded-xl border border-blue-500/20">
                        <User size={14} />
                        <span>Entregador ID: {order.driver_id}</span>
                     </div>
                  )}

                  {/* BOTÕES DE AÇÃO (IDs ÚNICOS PARA PLAYWRIGHT) */}
                  <div className="flex gap-3">
                    {order.status === 'ready' ? (
                      <>
                        <button 
                          type="button"
                          data-testid={`pickup-button-${order.id}`}
                          onClick={() => handlePickup(order.id)}
                          className="flex-[3] bg-orange-600 hover:bg-orange-500 text-white py-5 rounded-2xl font-black uppercase text-xs tracking-[0.2em] shadow-xl shadow-orange-900/20 active:scale-95 transition-all flex items-center justify-center gap-2"
                        >
                          <Bike size={20} /> Pegar
                        </button>
                        <button 
                          onClick={() => handleRollback(order.id)}
                          className="flex-1 bg-slate-800 hover:bg-red-900/20 text-slate-500 hover:text-red-500 py-5 rounded-2xl transition-all border border-white/5 flex items-center justify-center"
                          title="Devolver para Cozinha"
                        >
                          <Undo2 size={20} />
                        </button>
                      </>
                    ) : order.status === 'delivering' ? (
                      <button 
                        type="button"
                        data-testid={`complete-button-${order.id}`} // 🛡️ ID ÚNICO
                        onClick={() => handleComplete(order.id)}
                        className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white py-5 rounded-2xl font-black uppercase text-xs tracking-[0.2em] shadow-xl shadow-emerald-900/20 active:scale-95 transition-all flex items-center justify-center gap-2"
                      >
                        <CheckCircle2 size={20} /> Finalizar
                      </button>
                    ) : (
                      <div className="flex-1 bg-slate-800 text-slate-600 py-5 rounded-2xl font-black uppercase text-xs tracking-[0.2em] flex items-center justify-center gap-2 border border-white/5">
                        <ChefHat size={20} /> Em Preparo
                      </div>
                    )}
                    
                    <button 
                      type="button"
                      onClick={() => window.open(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(order.delivery_address || "")}`, '_blank')}
                      className="bg-slate-800 text-slate-400 p-5 rounded-2xl hover:bg-slate-700 hover:text-white transition-all border border-white/5"
                      title="Abrir no Mapa"
                    >
                      <Navigation size={24} />
                    </button>

                    {order.customer_phone && (
                      <button 
                        type="button"
                        onClick={() => openWhatsApp(order.customer_phone!)}
                        className="bg-emerald-900/20 text-emerald-500 p-5 rounded-2xl hover:bg-emerald-900/40 transition-all border border-emerald-500/20"
                        title="WhatsApp"
                      >
                        <Phone size={24} />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* MODAIS */}
      <DispatchModal 
        isOpen={!!selectedOrderId} 
        onClose={() => setSelectedOrderId(null)} 
        orderId={selectedOrderId || ""}
        onSuccess={fetchOrders}
      />
      <DriverCashModal 
        isOpen={isCashModalOpen} 
        onClose={() => setIsCashModalOpen(false)} 
      />
    </div>
  );
}
