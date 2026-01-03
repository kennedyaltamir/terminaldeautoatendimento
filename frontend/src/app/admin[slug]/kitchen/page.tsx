"use client";

import { useEffect, useState, use, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getKitchenOrders, updateOrderStatus, updateOrderPayment } from "@/lib/api";
import { Order } from "@/types";
import { ChefHat, RefreshCw, LogOut, ArrowRightCircle, CheckCircle2, Volume2, VolumeX, DollarSign, Printer } from "lucide-react";
import { removeToken } from "@/lib/auth";
import { useWebSocket } from "@/hooks/useWebSocket";

export default function KitchenPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params);
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [isMuted, setIsMuted] = useState(false);
  const [printingOrder, setPrintingOrder] = useState<Order | null>(null);
  
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const fetchOrders = useCallback(async () => {
    try {
      const data: Order[] = await getKitchenOrders(slug);
      setOrders(data);
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

  // WebSocket Integration
  useWebSocket(slug, (data) => {
    if (data.type === "new_order") {
      // Toca som e recarrega
      if (!isMuted && audioRef.current) { audioRef.current.play().catch(() => {}); }
      fetchOrders();
    } else if (data.type === "order_update") {
      // Atualiza status/pagamento sem recarregar tudo se possível, ou recarrega
      fetchOrders();
    }
  });

  const handleAdvanceStatus = async (orderId: string, currentStatus: string) => {
    const nextStatus = currentStatus === "pending" ? "preparing" : "ready";
    // Otimista
    setOrders(prev => prev.map(o => o.id === orderId ? { ...o, status: nextStatus as any } : o).filter(o => o.status !== 'ready'));
    try { await updateOrderStatus(slug, orderId, nextStatus); } catch (e) { fetchOrders(); }
  };

  const handleConfirmPayment = async (orderId: string) => {
    setOrders(prev => prev.map(o => o.id === orderId ? { ...o, payment_status: 'paid' as any } : o));
    try { await updateOrderPayment(orderId, 'paid'); } catch (e) { fetchOrders(); }
  };

  const handlePrint = (order: Order) => {
    setPrintingOrder(order);
    setTimeout(() => {
      window.print();
      setPrintingOrder(null);
    }, 100);
  };

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-900 text-gray-500 font-sans">Carregando KDS...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6 font-sans">
      <audio ref={audioRef} src="/notification.mp3" preload="auto" />
      
      {/* --- ÁREA DE TELA --- */}
      <div className="print:hidden">
        <header className="flex justify-between items-center mb-8 border-b border-gray-700 pb-4">
            <div>
            <h1 className="text-2xl font-bold flex items-center gap-2"><ChefHat className="text-orange-500" /> Monitor de Cozinha (Tempo Real)</h1>
            <p className="text-gray-400 text-sm mt-1">{slug.toUpperCase()} • {lastUpdated.toLocaleTimeString()}</p>
            </div>
            <div className="flex gap-3">
                <button onClick={() => setIsMuted(!isMuted)} className={`p-2 rounded-full transition-all ${isMuted ? 'bg-red-900/30 text-red-400' : 'bg-gray-800 text-gray-400'}`}>{isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}</button>
                <button onClick={fetchOrders} className="p-2 bg-gray-800 rounded-full hover:bg-gray-700 transition-all"><RefreshCw size={20} /></button>
                <button onClick={() => { removeToken(); router.push("/admin/login"); }} className="p-2 bg-red-900/30 text-red-400 rounded-full hover:bg-red-900/50 transition-all"><LogOut size={20} /></button>
            </div>
        </header>

        {orders.length === 0 ? (
            <div className="text-center py-20 text-gray-500"><p className="text-xl">Nenhum pedido pendente.</p></div>
        ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {orders.map((order) => (
                <div key={order.id} className={`rounded-xl border-l-8 shadow-lg overflow-hidden flex flex-col transition-all ${order.status === 'pending' ? 'bg-white text-gray-900 border-green-500' : 'bg-amber-100 text-gray-900 border-amber-500'}`}>
                <div className="p-4 border-b flex justify-between items-start">
                    <div>
                    <h2 className="text-2xl font-bold">Mesa {order.table?.table_number || "?"}</h2>
                    <p className="text-sm font-medium opacity-70">{order.customer_name || "Cliente"}</p>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                        <button onClick={() => handlePrint(order)} className="p-1.5 bg-gray-100 hover:bg-gray-200 rounded text-gray-600 transition-colors"><Printer size={16}/></button>
                        <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${order.status === 'pending' ? 'bg-green-100 text-green-800' : 'bg-amber-500 text-white'}`}>{order.status === 'pending' ? 'Novo' : 'Preparando'}</span>
                    </div>
                </div>

                <div className="p-4 flex-1 overflow-y-auto max-h-[300px]">
                    <ul className="space-y-3">
                    {order.items.map((item) => (
                        <li key={item.id} className="flex items-start gap-3">
                        <div className="bg-black/5 px-2 py-1 rounded font-bold text-lg min-w-[2rem] text-center">{item.quantity}</div>
                        <div>
                            <p className="font-semibold leading-tight">{item.product.name}</p>
                            {item.selected_options?.map((o, i) => (<p key={i} className="text-[10px] text-gray-500">+ {o.name}</p>))}
                            {item.notes && <p className="text-red-600 text-[10px] mt-1 font-medium bg-red-50 px-1 rounded inline-block">⚠️ {item.notes}</p>}
                        </div>
                        </li>
                    ))}
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

      {/* --- ÁREA DE IMPRESSÃO (Cupom Térmico) --- */}
      {printingOrder && (
        <div className="hidden print:block bg-white text-black p-4 w-[80mm] font-mono text-sm">
          <div className="text-center border-b border-dashed border-black pb-2 mb-2">
            <h2 className="text-lg font-bold uppercase">MesaFlow KDS</h2>
            <p>Pedido: #{printingOrder.id.toString().slice(0, 8)}</p>
            <p>{new Date(printingOrder.created_at).toLocaleString()}</p>
          </div>
          
          <div className="mb-2">
            <p className="text-xl font-bold">MESA: {printingOrder.table?.table_number}</p>
            <p>CLIENTE: {printingOrder.customer_name || "Não informado"}</p>
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