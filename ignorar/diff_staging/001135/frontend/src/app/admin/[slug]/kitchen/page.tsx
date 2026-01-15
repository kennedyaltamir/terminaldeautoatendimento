"use client";
import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getKitchenOrders, updateOrderStatus, getServiceRequestsAdmin, resolveServiceRequest } from "@/lib/api";
import { Order, ServiceRequest } from "@/types";
import { ChefHat, RefreshCw, LogOut, ArrowRightCircle, CheckCircle2, Layers, Box, Utensils, Wine, ListChecks, Maximize2, Minimize2, Mic, MicOff } from "lucide-react";
import { removeToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import OrderTimer from "@/components/admin/OrderTimer";
import StockModal from "@/components/admin/StockModal";
import ItemAggregator from "@/components/admin/KDS/ItemAggregator";
import { toast, Toaster } from "sonner";
import { useVoiceControl } from "@/hooks/useVoiceControl";

type StationFilter = 'all' | 'kitchen' | 'bar' | 'dessert';

export default function KitchenPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [serviceRequests, setServiceRequests] = useState<ServiceRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [isMuted, setIsMuted] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [activeTab, setActiveTab] = useState<StationFilter>('all');
  const [isStockOpen, setIsStockOpen] = useState(false);
  const [isAggregatorOpen, setIsAggregatorOpen] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const fetchOrders = useCallback(async () => {
    try {
      const [ordersData, requestsData] = await Promise.all([
        getKitchenOrders(slug),
        getServiceRequestsAdmin(slug)
      ]);
      setOrders(ordersData);
      setServiceRequests(requestsData);
      setLastUpdated(new Date());
    } catch (error: any) {
      if (error.message === "Unauthorized") router.push("/admin/login");
    } finally {
      setLoading(false);
    }
  }, [slug, router]);

  const handleAdvanceStatus = async (orderId: string, currentStatus: string) => {
    const nextStatus = currentStatus === "pending" ? "preparing" : "ready";
    let newStatusApi = nextStatus;
    if (currentStatus === "ready") {
        newStatusApi = "delivered";
    }
    try { 
      await updateOrderStatus(slug, orderId, newStatusApi); 
      fetchOrders();
    } catch (e) { 
      toast.error("Erro ao atualizar status");
    }
  };

  // --- VOICE CONTROL ---
  const voiceCommands = [
    {
      command: /(?:pedido|mesa)\s+(\w+)\s+(?:pronto|entregue|finalizar)/i,
      action: (match: RegExpMatchArray) => {
        const identifier = match[1].toLowerCase();
        const target = orders.find(o => 
          o.id.toLowerCase().startsWith(identifier) || 
          o.id.toLowerCase().endsWith(identifier) ||
          (o.table?.table_number.toString() === identifier)
        );
        if (target) {
          handleAdvanceStatus(target.id, target.status);
        } else {
          toast.warning(`Pedido/Mesa ${identifier} não encontrado.`);
        }
      }
    }
  ];
  const { isListening, isSupported, toggleListening } = useVoiceControl(voiceCommands);

  const toggleFullscreen = useCallback(() => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
        setIsFullscreen(false);
      }
    }
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      const key = e.key;
      if (/^[1-9]$/.test(key)) {
        const index = parseInt(key) - 1;
        const filtered = orders.filter(order => {
            if (activeTab === 'all') return true;
            return order.items.some(item => item.product.station === activeTab);
        });
        const targetOrder = filtered[index];
        if (targetOrder) handleAdvanceStatus(targetOrder.id, targetOrder.status);
      }
      if (key.toLowerCase() === 'r') fetchOrders();
      if (key.toLowerCase() === 'f') toggleFullscreen();
      if (key.toLowerCase() === 's') setIsStockOpen(true);
      if (key.toLowerCase() === 'a') setIsAggregatorOpen(true);
      if (key.toLowerCase() === 'v') toggleListening();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [orders, activeTab, fetchOrders, toggleFullscreen, toggleListening]);

  useEffect(() => {
    const savedStation = localStorage.getItem("mesaflow_kds_station") as StationFilter;
    if (savedStation) setActiveTab(savedStation);
    fetchOrders();
  }, [fetchOrders]);

  const handleTabChange = (station: StationFilter) => {
    setActiveTab(station);
    localStorage.setItem("mesaflow_kds_station", station);
  };

  const handleWebSocketMessage = useCallback((data: any) => {
    if (data.type === "new_order" || data.type === "waiter_call") {
      if (!isMuted && audioRef.current) { audioRef.current.play().catch(() => {}); }
      fetchOrders();
    } else if (data.type === "order_update") {
      fetchOrders();
    }
  }, [fetchOrders, isMuted]);

  useWebSocket(slug, handleWebSocketMessage);

  const filteredOrders = orders.filter(order => {
    if (activeTab === 'all') return true;
    if (!order.items || order.items.length === 0) return true;
    return order.items.some(item => item.product.station === activeTab);
  });

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-900 text-gray-500 font-sans animate-pulse">Carregando KDS...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4 md:p-6 font-sans">
      <Toaster position="top-right" richColors />
      <audio ref={audioRef} src="/notification.mp3" preload="auto" />
      
      <div className="print:hidden">
        <header className="flex flex-col xl:flex-row justify-between items-start xl:items-center mb-6 border-b border-gray-800 pb-4 gap-4">
            <div>
              <h1 className="text-2xl font-bold flex items-center gap-2 text-white">
                <ChefHat className="text-orange-500" /> Monitor de Produção
              </h1>
              <p className="text-gray-500 text-xs mt-1 font-mono uppercase tracking-wider">
                {slug} • Atualizado às {lastUpdated.toLocaleTimeString()}
              </p>
            </div>

            <div className="flex bg-gray-800 p-1.5 rounded-full overflow-x-auto max-w-full no-scrollbar border border-gray-700">
              <button onClick={() => handleTabChange('all')} className={`px-6 py-3 rounded-full text-sm font-bold flex items-center gap-2 transition-all whitespace-nowrap ${activeTab === 'all' ? 'bg-gray-700 text-white shadow-md ring-1 ring-gray-600' : 'text-gray-400 hover:text-white hover:bg-gray-700/50'}`}><Layers size={18} /> Todos</button>
              <button onClick={() => handleTabChange('kitchen')} className={`px-6 py-3 rounded-full text-sm font-bold flex items-center gap-2 transition-all whitespace-nowrap ${activeTab === 'kitchen' ? 'bg-orange-600 text-white shadow-md ring-1 ring-orange-500' : 'text-gray-400 hover:text-white hover:bg-gray-700/50'}`}><Utensils size={18} /> Cozinha</button>
              <button onClick={() => handleTabChange('bar')} className={`px-6 py-3 rounded-full text-sm font-bold flex items-center gap-2 transition-all whitespace-nowrap ${activeTab === 'bar' ? 'bg-purple-600 text-white shadow-md ring-1 ring-purple-500' : 'text-gray-400 hover:text-white hover:bg-gray-700/50'}`}><Wine size={18} /> Bar</button>
            </div>

            <div className="flex gap-2">
                {isSupported && (
                  <button 
                    onClick={toggleListening} 
                    className={`p-4 rounded-xl transition-all border ${isListening ? 'bg-red-600 text-white border-red-500 animate-pulse' : 'bg-gray-800 text-gray-300 border-gray-700'}`} 
                    title="Comando de Voz (V)"
                  >
                    {isListening ? <Mic size={24} /> : <MicOff size={24} />}
                  </button>
                )}
                <button onClick={toggleFullscreen} className={`p-4 rounded-xl transition-all border ${isFullscreen ? 'bg-blue-600 text-white border-blue-500' : 'bg-gray-800 text-gray-300 border-gray-700'}`} title="Tela Cheia (F)">
                  {isFullscreen ? <Minimize2 size={24} /> : <Maximize2 size={24} />}
                </button>
                <button onClick={() => setIsAggregatorOpen(true)} className="p-4 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all text-green-400 border border-gray-700" title="Resumo (A)"><ListChecks size={24} /></button>
                <button onClick={() => setIsStockOpen(true)} className="p-4 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all text-orange-400 border border-gray-700" title="Estoque (S)"><Box size={24} /></button>
                <button onClick={fetchOrders} className="p-4 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all border border-gray-700 text-gray-300" title="Recarregar (R)"><RefreshCw size={24} /></button>
                <button onClick={() => { removeToken(); router.push("/admin/login"); }} className="p-4 bg-red-900/20 text-red-400 rounded-xl hover:bg-red-900/40 transition-all border border-red-900/50"><LogOut size={24} /></button>
            </div>
        </header>

        {filteredOrders.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-32 text-gray-600 border-2 border-dashed border-gray-800 rounded-3xl bg-gray-800/20">
              <ChefHat size={64} className="mb-4 opacity-20" />
              <p className="text-xl font-medium">Tudo tranquilo na operação.</p>
            </div>
        ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredOrders.map((order, index) => (
                <div key={order.id} className={`rounded-2xl border-t-8 shadow-xl overflow-hidden flex flex-col transition-all duration-300 hover:shadow-2xl relative ${order.origin === 'ifood' ? 'bg-red-950/20 border-red-600' : order.status === 'pending' ? 'bg-gray-800 border-green-500' : 'bg-gray-800 border-amber-500'}`}>
                {index < 9 && (
                    <div className="absolute top-2 right-2 w-6 h-6 bg-white/10 rounded flex items-center justify-center text-[10px] font-bold text-gray-400 border border-white/10 z-10">
                        {index + 1}
                    </div>
                )}
                <div className="p-4 border-b border-gray-700 bg-gray-800/50">
                    <div className="flex justify-between items-start mb-3">
                        <div>
                            <div>
                                <h2 className="text-2xl font-black leading-none text-white">Mesa {order.table?.table_number || "?"}</h2>
                                <p className="text-xs font-bold text-gray-500 mt-1">#{order.id.slice(0,4)} • {order.customer_name || "Cliente"}</p>
                            </div>
                        </div>
                        <OrderTimer createdAt={order.created_at} />
                    </div>
                </div>
                <div className="p-4 flex-1 overflow-y-auto max-h-[350px] bg-gray-800/30">
                    <ul className="space-y-3">
                      {order.items.filter(item => activeTab === 'all' || item.product.station === activeTab).map((item) => (
                        <li key={item.id} className="flex items-start gap-3 border-b border-gray-100/10 pb-2 last:border-0">
                          <div className="bg-black/20 px-2 py-1 rounded font-bold text-lg min-w-[2.5rem] text-center text-white">{item.quantity}</div>
                          <div className="flex-1">
                            <p className="font-semibold leading-tight text-gray-200">{item.product.name}</p>
                            {item.notes && <p className="text-red-300 text-xs mt-1 font-bold bg-red-900/30 px-2 py-1 rounded inline-block border border-red-800">⚠️ {item.notes}</p>}
                          </div>
                        </li>
                      ))}
                    </ul>
                </div>
                <div className="p-4 bg-gray-900 border-t border-gray-800 mt-auto">
                    <button 
                      onClick={() => handleAdvanceStatus(order.id, order.status)} 
                      className={`w-full py-5 rounded-xl font-bold text-white shadow-lg flex items-center justify-center gap-2 transition-all active:scale-95 text-xl ${order.status === 'pending' ? 'bg-blue-600 hover:bg-blue-500' : 'bg-green-600 hover:bg-green-500'}`}
                    >
                      {order.status === 'pending' ? <>Iniciar Preparo <ArrowRightCircle size={24} /></> : <>Finalizar Pedido <CheckCircle2 size={24} /></>}
                    </button>
                </div>
                </div>
            ))}
            </div>
        )}
      </div>
      
      <StockModal isOpen={isStockOpen} onClose={() => setIsStockOpen(false)} />
      <ItemAggregator isOpen={isAggregatorOpen} onClose={() => setIsAggregatorOpen(false)} orders={orders} />
    </div>
  );
}
