"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getKitchenOrders, updateOrderStatus, updateOrderPayment, getServiceRequests, resolveServiceRequest, getRecentCompletedOrders } from "@/lib/api";
import { Order, ServiceRequest, OrderItemResponse } from "@/types";
import { ChefHat, RefreshCw, LogOut, ArrowRightCircle, CheckCircle2, Volume2, VolumeX, DollarSign, Printer, Bike, BellRing, XCircle, Utensils, Wine, Layers, History, Undo2, Box, AlertTriangle, IceCream, Smartphone } from "lucide-react";
import { removeToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import OrderTimer from "@/components/admin/OrderTimer";
import Modal from "@/components/ui/Modal";
import StockModal from "@/components/admin/StockModal";
import { printOrder } from "@/lib/printer/driver";

type StationFilter = 'all' | 'kitchen' | 'bar' | 'dessert';

export default function KitchenPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [serviceRequests, setServiceRequests] = useState<ServiceRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [isMuted, setIsMuted] = useState(false);
  const [printingOrder, setPrintingOrder] = useState<Order | null>(null);
  
  const [activeTab, setActiveTab] = useState<StationFilter>('all');
  const [isRecallOpen, setIsRecallOpen] = useState(false);
  const [isStockOpen, setIsStockOpen] = useState(false);
  const [recentOrders, setRecentOrders] = useState<Order[]>([]);
  
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    const savedStation = localStorage.getItem("mesaflow_kds_station") as StationFilter;
    if (savedStation) {
      setActiveTab(savedStation);
    }
  }, []);

  const handleTabChange = (station: StationFilter) => {
    setActiveTab(station);
    localStorage.setItem("mesaflow_kds_station", station);
  };

  const fetchOrders = useCallback(async () => {
    try {
      const [ordersData, requestsData] = await Promise.all([
        getKitchenOrders(slug),
        getServiceRequests(slug)
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

  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  const handleWebSocketMessage = useCallback((data: any) => {
    if (data.type === "new_order" || data.type === "waiter_call") {
      if (!isMuted && audioRef.current) { audioRef.current.play().catch(() => {}); }
      fetchOrders();
    } else if (data.type === "order_update") {
      fetchOrders();
    }
  }, [fetchOrders, isMuted]);

  useWebSocket(slug, handleWebSocketMessage);

  const handleAdvanceStatus = async (orderId: string, currentStatus: string) => {
    const nextStatus = currentStatus === "pending" ? "preparing" : "ready";
    let newStatusApi = "preparing";
    if (currentStatus === "preparing" || currentStatus === "ready") {
        newStatusApi = "delivered";
    }

    setOrders(prev => prev.map(o => o.id === orderId ? { ...o, status: newStatusApi as any } : o).filter(o => o.status !== 'delivered'));
    try { await updateOrderStatus(slug, orderId, newStatusApi); } catch (e) { fetchOrders(); }
  };

  const handleConfirmPayment = async (orderId: string) => {
    setOrders(prev => prev.map(o => o.id === orderId ? { ...o, payment_status: 'paid' as any } : o));
    try { await updateOrderPayment(orderId, 'paid'); } catch (e) { fetchOrders(); }
  };

  const handleResolveRequest = async (id: number) => {
    setServiceRequests(prev => prev.filter(r => r.id !== id));
    try { await resolveServiceRequest(id); } catch (e) { fetchOrders(); }
  };

  const handlePrint = (order: Order) => {
    setPrintingOrder(order);
    setTimeout(() => {
      window.print();
      setPrintingOrder(null);
    }, 100);
  };

  const handleRawBT = (order: Order) => {
    printOrder(order, slug);
  };

  const openRecallModal = async () => {
    setIsRecallOpen(true);
    try {
        const data = await getRecentCompletedOrders(slug);
        setRecentOrders(data);
    } catch (e) {
        console.error(e);
    }
  };

  const handleRestoreOrder = async (orderId: string) => {
    if(!confirm("Restaurar este pedido para a cozinha?")) return;
    try {
        await updateOrderStatus(slug, orderId, "preparing");
        setIsRecallOpen(false);
        fetchOrders();
    } catch (e) {
        alert("Erro ao restaurar pedido");
    }
  };

  const getServiceLabel = (type: string) => {
    switch(type) {
      case 'bill': return 'Conta';
      case 'cleaning': return 'Limpeza';
      default: return 'Ajuda';
    }
  };

  const filteredOrders = orders.filter(order => {
    if (activeTab === 'all') return true;
    return order.items.some(item => item.product.station === activeTab);
  });

  const renderItems = (items: OrderItemResponse[]) => {
    return items
      .filter(item => activeTab === 'all' || item.product.station === activeTab)
      .map((item) => (
        <li key={item.id} className="flex items-start gap-3 border-b border-gray-100/10 pb-2 last:border-0">
          <div className="bg-black/20 px-2 py-1 rounded font-bold text-lg min-w-[2.5rem] text-center text-white">
            {item.quantity}
          </div>
          <div className="flex-1">
            <p className="font-semibold leading-tight text-gray-200">{item.product.name}</p>
            {item.selected_options?.map((o, i) => (
              <p key={i} className="text-xs text-gray-400">+ {o.name}</p>
            ))}
            {item.notes && (
              <p className="text-red-300 text-xs mt-1 font-bold bg-red-900/30 px-2 py-1 rounded inline-block border border-red-800">
                ⚠️ {item.notes}
              </p>
            )}
          </div>
        </li>
      ));
  };

  const hasMixedItems = (order: Order) => {
    if (activeTab === 'all') return false;
    return order.items.some(item => item.product.station !== activeTab);
  };

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-900 text-gray-500 font-sans animate-pulse">Carregando KDS...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-4 md:p-6 font-sans">
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

            <div className="flex bg-gray-800 p-1.5 rounded-xl overflow-x-auto max-w-full no-scrollbar border border-gray-700">
              <button onClick={() => handleTabChange('all')} className={`px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-all whitespace-nowrap ${activeTab === 'all' ? 'bg-gray-700 text-white shadow-md ring-1 ring-gray-600' : 'text-gray-400 hover:text-white hover:bg-gray-700/50'}`}><Layers size={16} /> Todos</button>
              <button onClick={() => handleTabChange('kitchen')} className={`px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-all whitespace-nowrap ${activeTab === 'kitchen' ? 'bg-orange-600 text-white shadow-md ring-1 ring-orange-500' : 'text-gray-400 hover:text-white hover:bg-gray-700/50'}`}><Utensils size={16} /> Cozinha</button>
              <button onClick={() => handleTabChange('bar')} className={`px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-all whitespace-nowrap ${activeTab === 'bar' ? 'bg-purple-600 text-white shadow-md ring-1 ring-purple-500' : 'text-gray-400 hover:text-white hover:bg-gray-700/50'}`}><Wine size={16} /> Bar</button>
              <button onClick={() => handleTabChange('dessert')} className={`px-4 py-2 rounded-lg text-sm font-bold flex items-center gap-2 transition-all whitespace-nowrap ${activeTab === 'dessert' ? 'bg-pink-600 text-white shadow-md ring-1 ring-pink-500' : 'text-gray-400 hover:text-white hover:bg-gray-700/50'}`}><IceCream size={16} /> Sobremesa</button>
            </div>

            <div className="flex gap-2">
                <button onClick={() => setIsStockOpen(true)} className="p-3 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all text-orange-400 border border-gray-700" title="Gestão de Estoque (86)"><Box size={20} /></button>
                <button onClick={openRecallModal} className="p-3 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all text-blue-400 border border-gray-700" title="Histórico Recente"><History size={20} /></button>
                <button onClick={() => setIsMuted(!isMuted)} className={`p-3 rounded-xl transition-all border ${isMuted ? 'bg-red-900/20 text-red-400 border-red-900/50' : 'bg-gray-800 text-gray-400 border-gray-700'}`}>{isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}</button>
                <button onClick={fetchOrders} className="p-3 bg-gray-800 rounded-xl hover:bg-gray-700 transition-all border border-gray-700 text-gray-300"><RefreshCw size={20} /></button>
                <button onClick={() => { removeToken(); router.push("/admin/login"); }} className="p-3 bg-red-900/20 text-red-400 rounded-xl hover:bg-red-900/40 transition-all border border-red-900/50"><LogOut size={20} /></button>
            </div>
        </header>

        {serviceRequests.length > 0 && (
          <div className="mb-8 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 animate-in slide-in-from-top-4">
            {serviceRequests.map(req => (
              <div key={req.id} className="bg-red-600 text-white p-4 rounded-xl shadow-lg flex justify-between items-start animate-pulse border border-red-500">
                <div className="flex items-start gap-3">
                  <div className="bg-white/20 p-2 rounded-full mt-1"><BellRing size={20} /></div>
                  <div>
                    <h3 className="font-bold text-lg">Mesa {req.table_number}</h3>
                    <p className="text-xs font-medium uppercase opacity-90 tracking-wide">{getServiceLabel(req.service_type)}</p>
                    {req.notes && <p className="text-xs mt-2 bg-red-800/50 p-1.5 rounded italic border border-red-700/50">"{req.notes}"</p>}
                  </div>
                </div>
                <button onClick={() => handleResolveRequest(req.id)} className="text-white/80 hover:text-white hover:bg-white/20 p-2 rounded-full transition-colors"><XCircle size={24} /></button>
              </div>
            ))}
          </div>
        )}

        {filteredOrders.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-32 text-gray-600 border-2 border-dashed border-gray-800 rounded-3xl bg-gray-800/20">
              <ChefHat size={64} className="mb-4 opacity-20" />
              <p className="text-xl font-medium">Tudo tranquilo na {activeTab === 'all' ? 'operação' : activeTab === 'kitchen' ? 'cozinha' : 'estação'}.</p>
              <p className="text-sm mt-2 opacity-60">Aguardando novos pedidos...</p>
            </div>
        ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredOrders.map((order) => (
                <div key={order.id} className={`rounded-2xl border-t-8 shadow-xl overflow-hidden flex flex-col transition-all duration-300 hover:shadow-2xl ${order.status === 'pending' ? 'bg-gray-800 border-green-500' : 'bg-gray-800 border-amber-500'}`}>
                
                <div className="p-4 border-b border-gray-700 bg-gray-800/50">
                    <div className="flex justify-between items-start mb-3">
                        <div>
                        {order.order_type === 'delivery' ? (
                            <div className="flex items-center gap-2 text-blue-400">
                                <Bike size={24}/>
                                <div>
                                  <h2 className="text-xl font-black leading-none">Delivery</h2>
                                  <p className="text-xs font-bold text-gray-400 mt-0.5">#{order.id.slice(0,4)}</p>
                                </div>
                            </div>
                        ) : (
                            <div>
                                <h2 className="text-2xl font-black leading-none text-white">Mesa {order.table?.table_number || "?"}</h2>
                                <p className="text-xs font-bold text-gray-500 mt-1">#{order.id.slice(0,4)} • {order.customer_name || "Cliente"}</p>
                            </div>
                        )}
                        </div>
                        <OrderTimer createdAt={order.created_at} />
                    </div>
                    
                    <div className="flex justify-between items-center">
                       <span className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${order.status === 'pending' ? 'bg-green-900/30 text-green-400 border border-green-900/50' : 'bg-amber-900/30 text-amber-400 border border-amber-900/50'}`}>
                          {order.status === 'pending' ? 'Novo Pedido' : 'Em Preparo'}
                       </span>
                       <div className="flex gap-1">
                         <button onClick={() => handlePrint(order)} className="p-1.5 bg-gray-700 hover:bg-gray-600 rounded text-gray-400 hover:text-white transition-colors" title="Imprimir (Browser)"><Printer size={14}/></button>
                         <button onClick={() => handleRawBT(order)} className="p-1.5 bg-orange-900/30 hover:bg-orange-900/50 rounded text-orange-400 hover:text-orange-300 transition-colors border border-orange-900/50" title="Imprimir (RawBT)"><Smartphone size={14}/></button>
                       </div>
                    </div>
                </div>

                <div className="p-4 flex-1 overflow-y-auto max-h-[350px] bg-gray-800/30">
                    <ul className="space-y-3">
                      {renderItems(order.items)}
                    </ul>
                </div>

                <div className="p-4 bg-gray-900 border-t border-gray-800 mt-auto space-y-3">
                    {hasMixedItems(order) && (
                      <div className="flex items-center gap-2 text-[10px] text-yellow-500 bg-yellow-900/20 p-2 rounded border border-yellow-900/30">
                        <AlertTriangle size={12} />
                        <span>Atenção: Pedido contém itens de outra praça.</span>
                      </div>
                    )}

                    <div className="flex items-center justify-between">
                        <div className="flex flex-col">
                            <span className="text-lg font-black text-white">R$ {Number(order.total_amount).toFixed(2)}</span>
                            <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">{order.payment_method}</span>
                        </div>
                        {order.payment_status === 'paid' ? (
                            <span className="text-green-500 flex items-center gap-1 text-xs font-bold bg-green-900/20 px-2 py-1 rounded border border-green-900/30"><CheckCircle2 size={14}/> PAGO</span>
                        ) : (
                            <button onClick={() => handleConfirmPayment(order.id)} className="bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1 hover:bg-green-600 hover:text-white transition-all border border-gray-600 hover:border-green-500"><DollarSign size={12}/> Confirmar</button>
                        )}
                    </div>
                    
                    <button 
                      onClick={() => handleAdvanceStatus(order.id, order.status)} 
                      className={`w-full py-3.5 rounded-xl font-bold text-white shadow-lg flex items-center justify-center gap-2 transition-all active:scale-95 ${order.status === 'pending' ? 'bg-blue-600 hover:bg-blue-500 shadow-blue-900/20' : 'bg-green-600 hover:bg-green-500 shadow-green-900/20'}`}
                    >
                      {order.status === 'pending' ? <>Iniciar Preparo <ArrowRightCircle size={20} /></> : <>Finalizar Pedido <CheckCircle2 size={20} /></>}
                    </button>
                </div>
                </div>
            ))}
            </div>
        )}
      </div>

      <Modal isOpen={isRecallOpen} onClose={() => setIsRecallOpen(false)} title="Histórico Recente (Recall)">
        <div className="space-y-3 max-h-[60vh] overflow-y-auto pr-1">
            {recentOrders.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Nenhum pedido finalizado recentemente.</p>
            ) : (
                recentOrders.map(order => (
                    <div key={order.id} className="bg-gray-800 p-4 rounded-xl border border-gray-700 flex justify-between items-center hover:border-gray-600 transition-colors">
                        <div>
                            <p className="font-bold text-white text-lg">
                                {order.order_type === 'delivery' ? 'Delivery' : `Mesa ${order.table?.table_number}`} 
                                <span className="text-gray-500 font-normal text-sm ml-2 font-mono">#{order.id.slice(0,6)}</span>
                            </p>
                            <p className="text-xs text-gray-400 mt-1">{new Date(order.created_at).toLocaleTimeString()} • {order.items.length} itens • {order.customer_name}</p>
                        </div>
                        <button 
                            onClick={() => handleRestoreOrder(order.id)}
                            className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-colors shadow-lg shadow-blue-900/20"
                        >
                            <Undo2 size={16} /> Restaurar
                        </button>
                    </div>
                ))
            )}
        </div>
      </Modal>

      <StockModal isOpen={isStockOpen} onClose={() => setIsStockOpen(false)} slug={slug} />

      {printingOrder && (
        <div className="hidden print:block bg-white text-black p-4 w-[80mm] font-mono text-sm">
          <div className="text-center border-b border-dashed border-black pb-2 mb-2">
            <h2 className="text-lg font-bold uppercase">MesaFlow KDS</h2>
            <p>Pedido: #{printingOrder.id.toString().slice(0, 8)}</p>
            <p>{new Date(printingOrder.created_at).toLocaleString()}</p>
          </div>
          
          <div className="mb-2">
            {printingOrder.order_type === 'delivery' ? (
                <>
                    <p className="text-xl font-bold">DELIVERY</p>
                    <p>CLIENTE: {printingOrder.customer_name}</p>
                    <p>TEL: {printingOrder.customer_phone}</p>
                    <p className="mt-1 font-bold">ENDEREÇO:</p>
                    <p>{printingOrder.delivery_address}</p>
                </>
            ) : (
                <>
                    <p className="text-xl font-bold">MESA: {printingOrder.table?.table_number}</p>
                    <p>CLIENTE: {printingOrder.customer_name || "Não informado"}</p>
                </>
            )}
          </div>

          <div className="border-b border-dashed border-black pb-2 mb-2">
            <p className="font-bold mb-1">ITENS:</p>
            {printingOrder.items.map((item, i) => (
              <div key={i} className="mb-2">
                <div className="flex justify-between">
                  <span>{item.quantity}x {item.product.name}</span>
                </div>
                {item.selected_options?.map((o, j) => (
                  <p key={j} className="ml-4 text-xs">+ {o.name}</p>
                ))}
                {item.notes && <p className="ml-4 text-xs italic">Obs: {item.notes}</p>}
              </div>
            ))}
          </div>

          <div className="flex justify-between font-bold text-lg">
            <span>TOTAL:</span>
            <span>R$ {Number(printingOrder.total_amount).toFixed(2)}</span>
          </div>
          
          <div className="mt-4 text-center text-xs border-t border-dashed border-black pt-2">
            <p>Pagamento: {printingOrder.payment_method.toUpperCase()}</p>
            <p>Status: {printingOrder.payment_status.toUpperCase()}</p>
          </div>
        </div>
      )}

      <style jsx global>{`
        @media print {
          body { background: white !important; color: black !important; }
          .print\\:hidden { display: none !important; }
          .print\\:block { display: block !important; }
          @page { margin: 0; size: 80mm auto; }
        }
      `}</style>
    </div>
  );
} 