"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getKitchenOrders, updateOrderStatus, updateOrderPayment, getServiceRequests, resolveServiceRequest, getRecentCompletedOrders } from "@/lib/api";
import { Order, ServiceRequest, OrderItemResponse } from "@/types";
import { ChefHat, RefreshCw, LogOut, ArrowRightCircle, CheckCircle2, Volume2, VolumeX, DollarSign, Printer, Bike, BellRing, XCircle, Utensils, Wine, Layers, History, Undo2, Box } from "lucide-react";
import { removeToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";
import OrderTimer from "@/components/admin/OrderTimer";
import Modal from "@/components/ui/Modal";
import StockModal from "@/components/admin/StockModal";

export default function KitchenPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [serviceRequests, setServiceRequests] = useState<ServiceRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [isMuted, setIsMuted] = useState(false);
  const [printingOrder, setPrintingOrder] = useState<Order | null>(null);
  
  const [activeTab, setActiveTab] = useState<'all' | 'kitchen' | 'bar'>('all');
  
  // Modais
  const [isRecallOpen, setIsRecallOpen] = useState(false);
  const [isStockOpen, setIsStockOpen] = useState(false);
  const [recentOrders, setRecentOrders] = useState<Order[]>([]);
  
  const audioRef = useRef<HTMLAudioElement | null>(null);

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

  // CORREÇÃO: useCallback para evitar recriação da função e loop do WebSocket
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
    return items.filter(item => activeTab === 'all' || item.product.station === activeTab).map((item) => (
      <li key={item.id} className="flex items-start gap-3">
        <div className="bg-black/5 px-2 py-1 rounded font-bold text-lg min-w-[2rem] text-center">{item.quantity}</div>
        <div>
          <p className="font-semibold leading-tight">{item.product.name}</p>
          {item.selected_options?.map((o, i) => (<p key={i} className="text-[10px] text-gray-500">+ {o.name}</p>))}
          {item.notes && <p className="text-red-600 text-[10px] mt-1 font-medium bg-red-50 px-1 rounded inline-block">⚠️ {item.notes}</p>}
        </div>
      </li>
    ));
  };

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-900 text-gray-500 font-sans">Carregando KDS...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6 font-sans">
      <audio ref={audioRef} src="/notification.mp3" preload="auto" />
      
      <div className="print:hidden">
        <header className="flex flex-col md:flex-row justify-between items-center mb-8 border-b border-gray-700 pb-4 gap-4">
            <div>
              <h1 className="text-2xl font-bold flex items-center gap-2"><ChefHat className="text-orange-500" /> Monitor de Produção</h1>
              <p className="text-gray-400 text-sm mt-1">{slug.toUpperCase()} • {lastUpdated.toLocaleTimeString()}</p>
            </div>

            <div className="flex bg-gray-800 p-1 rounded-lg">
              <button 
                onClick={() => setActiveTab('all')}
                className={`px-4 py-2 rounded-md text-sm font-bold flex items-center gap-2 transition-all ${activeTab === 'all' ? 'bg-gray-700 text-white shadow' : 'text-gray-400 hover:text-white'}`}
              >
                <Layers size={16} /> Todos
              </button>
              <button 
                onClick={() => setActiveTab('kitchen')}
                className={`px-4 py-2 rounded-md text-sm font-bold flex items-center gap-2 transition-all ${activeTab === 'kitchen' ? 'bg-orange-600 text-white shadow' : 'text-gray-400 hover:text-white'}`}
              >
                <Utensils size={16} /> Cozinha
              </button>
              <button 
                onClick={() => setActiveTab('bar')}
                className={`px-4 py-2 rounded-md text-sm font-bold flex items-center gap-2 transition-all ${activeTab === 'bar' ? 'bg-purple-600 text-white shadow' : 'text-gray-400 hover:text-white'}`}
              >
                <Wine size={16} /> Bar
              </button>
            </div>

            <div className="flex gap-3">
                <button onClick={() => setIsStockOpen(true)} className="p-2 bg-gray-800 rounded-full hover:bg-gray-700 transition-all text-orange-400" title="Gestão de Estoque (86)"><Box size={20} /></button>
                <button onClick={openRecallModal} className="p-2 bg-gray-800 rounded-full hover:bg-gray-700 transition-all text-blue-400" title="Histórico Recente"><History size={20} /></button>
                <button onClick={() => setIsMuted(!isMuted)} className={`p-2 rounded-full transition-all ${isMuted ? 'bg-red-900/30 text-red-400' : 'bg-gray-800 text-gray-400'}`}>{isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}</button>
                <button onClick={fetchOrders} className="p-2 bg-gray-800 rounded-full hover:bg-gray-700 transition-all"><RefreshCw size={20} /></button>
                <button onClick={() => { removeToken(); router.push("/admin/login"); }} className="p-2 bg-red-900/30 text-red-400 rounded-full hover:bg-red-900/50 transition-all"><LogOut size={20} /></button>
            </div>
        </header>

        {serviceRequests.length > 0 && (
          <div className="mb-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 animate-in slide-in-from-top-4">
            {serviceRequests.map(req => (
              <div key={req.id} className="bg-red-600 text-white p-4 rounded-xl shadow-lg flex justify-between items-start animate-pulse">
                <div className="flex items-start gap-3">
                  <div className="bg-white/20 p-2 rounded-full mt-1"><BellRing size={20} /></div>
                  <div>
                    <h3 className="font-bold text-lg">Mesa {req.table_number}</h3>
                    <p className="text-xs font-medium uppercase opacity-90">{getServiceLabel(req.service_type)}</p>
                    {req.notes && (
                      <p className="text-xs mt-1 bg-red-800/50 p-1 rounded italic">"{req.notes}"</p>
                    )}
                  </div>
                </div>
                <button onClick={() => handleResolveRequest(req.id)} className="text-white/80 hover:text-white hover:bg-white/20 p-2 rounded-full transition-colors">
                  <XCircle size={24} />
                </button>
              </div>
            ))}
          </div>
        )}

        {filteredOrders.length === 0 ? (
            <div className="text-center py-20 text-gray-500"><p className="text-xl">Nenhum pedido para esta estação.</p></div>
        ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filteredOrders.map((order) => (
                <div key={order.id} className={`rounded-xl border-l-8 shadow-lg overflow-hidden flex flex-col transition-all ${order.status === 'pending' ? 'bg-white text-gray-900 border-green-500' : 'bg-amber-100 text-gray-900 border-amber-500'}`}>
                <div className="p-4 border-b flex justify-between items-start">
                    <div>
                    {order.order_type === 'delivery' ? (
                        <>
                            <h2 className="text-2xl font-bold flex items-center gap-2 text-orange-600"><Bike size={28}/> Delivery</h2>
                            <p className="text-sm font-bold mt-1">{order.customer_name}</p>
                        </>
                    ) : (
                        <>
                            <h2 className="text-2xl font-bold">Mesa {order.table?.table_number || "?"}</h2>
                            <p className="text-sm font-medium opacity-70">{order.customer_name || "Cliente"}</p>
                        </>
                    )}
                    </div>
                    <div className="flex flex-col items-end gap-2">
                        <OrderTimer createdAt={order.created_at} />
                        
                        <div className="flex gap-1">
                          <button onClick={() => handlePrint(order)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 transition-colors"><Printer size={16}/></button>
                          <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase flex items-center ${order.status === 'pending' ? 'bg-green-100 text-green-800' : 'bg-amber-500 text-white'}`}>{order.status === 'pending' ? 'Novo' : 'Preparando'}</span>
                        </div>
                    </div>
                </div>

                <div className="p-4 flex-1 overflow-y-auto max-h-[300px]">
                    <ul className="space-y-3">
                      {renderItems(order.items)}
                    </ul>
                </div>

                <div className="p-4 bg-black/5 border-t mt-auto space-y-3">
                    <div className="flex items-center justify-between">
                        <div className="flex flex-col">
                            <span className="text-lg font-black">R$ {Number(order.total_amount).toFixed(2)}</span>
                            <span className="text-[10px] font-bold text-gray-400 uppercase">{order.payment_method}</span>
                        </div>
                        {order.payment_status === 'paid' ? (
                            <span className="text-green-600 flex items-center gap-1 text-xs font-bold"><CheckCircle2 size={14}/> PAGO</span>
                        ) : (
                            <button onClick={() => handleConfirmPayment(order.id)} className="bg-green-600 text-white px-3 py-1 rounded-lg text-xs font-bold flex items-center gap-1 hover:bg-green-700 transition-colors"><DollarSign size={12}/> Confirmar</button>
                        )}
                    </div>
                    <button onClick={() => handleAdvanceStatus(order.id, order.status)} className={`w-full py-3 rounded-lg font-bold text-white shadow-md flex items-center justify-center gap-2 ${order.status === 'pending' ? 'bg-blue-600 hover:bg-blue-700' : 'bg-green-600 hover:bg-green-700'}`}>
                    {order.status === 'pending' ? <>Iniciar Preparo <ArrowRightCircle size={20} /></> : <>Finalizar Pedido <CheckCircle2 size={20} /></>}
                    </button>
                </div>
                </div>
            ))}
            </div>
        )}
      </div>

      {/* MODAL DE RECALL */}
      <Modal isOpen={isRecallOpen} onClose={() => setIsRecallOpen(false)} title="Histórico Recente (Recall)">
        <div className="space-y-4 max-h-[60vh] overflow-y-auto">
            {recentOrders.length === 0 ? (
                <p className="text-gray-400 text-center py-4">Nenhum pedido finalizado recentemente.</p>
            ) : (
                recentOrders.map(order => (
                    <div key={order.id} className="bg-gray-700 p-3 rounded-lg flex justify-between items-center">
                        <div>
                            <p className="font-bold text-white">
                                {order.order_type === 'delivery' ? 'Delivery' : `Mesa ${order.table?.table_number}`} 
                                <span className="text-gray-400 font-normal text-sm ml-2">#{order.id.slice(0,6)}</span>
                            </p>
                            <p className="text-xs text-gray-400">{new Date(order.created_at).toLocaleTimeString()} • {order.items.length} itens</p>
                        </div>
                        <button 
                            onClick={() => handleRestoreOrder(order.id)}
                            className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded text-xs font-bold flex items-center gap-1"
                        >
                            <Undo2 size={14} /> Restaurar
                        </button>
                    </div>
                ))
            )}
        </div>
      </Modal>

      {/* MODAL DE ESTOQUE (86) */}
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