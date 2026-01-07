"use client";

import { useEffect, useState, useCallback } from "react";
import { getKitchenOrders, updateOrderStatus } from "@/lib/api";
import { Order } from "@/types";
import { ChefHat, CheckCircle2, Clock, Utensils, Wine, IceCream, Box, ArrowRight, Printer } from "lucide-react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { toast, Toaster } from "sonner";
import { printOrder } from "@/lib/printer/driver";

export default function ExpeditorPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = useCallback(async () => {
    try {
      const data = await getKitchenOrders(slug);
      setOrders(data);
    } catch (e) {
      toast.error("Erro ao carregar pedidos");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => { fetchOrders(); }, [fetchOrders]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "new_order") {
      fetchOrders();
    }
  });

  const handleDeliver = async (order: Order) => {
    try {
      await updateOrderStatus(slug, order.id, "delivered");
      toast.success(`Pedido ${order.customer_name} despachado!`);
      fetchOrders();
    } catch (e) {
      toast.error("Erro ao atualizar status");
    }
  };

  const handlePrint = (order: Order) => {
    printOrder(order, slug);
  };

  const getStationIcon = (station: string) => {
    switch(station) {
      case 'bar': return <Wine size={14} className="text-purple-500" />;
      case 'dessert': return <IceCream size={14} className="text-pink-500" />;
      case 'kitchen': return <Utensils size={14} className="text-orange-500" />;
      default: return <Box size={14} className="text-gray-500" />;
    }
  };

  // Filtros
  const preparingOrders = orders.filter(o => o.status === 'preparing' || o.status === 'pending');
  const readyOrders = orders.filter(o => o.status === 'ready');

  if (loading) return <div className="flex h-screen items-center justify-center bg-gray-100 text-gray-500">Carregando Expedição...</div>;

  return (
    <div className="min-h-screen bg-gray-100 p-6 font-sans">
      <Toaster position="top-right" richColors />
      
      <header className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-black text-gray-900 flex items-center gap-3">
            <ChefHat className="text-blue-600" size={32} /> Expedição & Montagem
          </h1>
          <p className="text-gray-500 text-sm mt-1">Organize as bandejas antes de servir.</p>
        </div>
        <div className="flex gap-4">
            <div className="bg-white px-4 py-2 rounded-xl shadow-sm border border-gray-200 flex flex-col items-center">
                <span className="text-xs font-bold text-gray-400 uppercase">Na Cozinha</span>
                <span className="text-2xl font-black text-orange-500">{preparingOrders.length}</span>
            </div>
            <div className="bg-white px-4 py-2 rounded-xl shadow-sm border border-gray-200 flex flex-col items-center">
                <span className="text-xs font-bold text-gray-400 uppercase">Para Montar</span>
                <span className="text-2xl font-black text-green-500">{readyOrders.length}</span>
            </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[calc(100vh-140px)]">
        
        {/* COLUNA 1: EM PRODUÇÃO */}
        <div className="bg-gray-200/50 rounded-3xl p-4 flex flex-col border border-gray-300/50">
          <h2 className="text-gray-500 font-bold uppercase tracking-widest mb-4 flex items-center gap-2 px-2">
            <Clock size={18} /> Em Produção
          </h2>
          <div className="flex-1 overflow-y-auto space-y-3 pr-2">
            {preparingOrders.map(order => (
              <div key={order.id} className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 opacity-80 hover:opacity-100 transition-opacity">
                <div className="flex justify-between items-start mb-2">
                  <span className="font-bold text-gray-900">#{order.id.slice(0,4)} • {order.customer_name}</span>
                  <span className="text-xs font-bold bg-orange-100 text-orange-700 px-2 py-1 rounded uppercase">{order.status}</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {order.items.map((item, i) => (
                    <span key={i} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded flex items-center gap-1 border border-gray-200">
                      {getStationIcon(item.product.station)} {item.quantity}x {item.product.name}
                    </span>
                  ))}
                </div>
              </div>
            ))}
            {preparingOrders.length === 0 && (
                <div className="text-center py-20 text-gray-400">Cozinha livre.</div>
            )}
          </div>
        </div>

        {/* COLUNA 2: PRONTO PARA MONTAGEM */}
        <div className="bg-blue-50/50 rounded-3xl p-4 flex flex-col border border-blue-100">
          <h2 className="text-blue-800 font-bold uppercase tracking-widest mb-4 flex items-center gap-2 px-2">
            <CheckCircle2 size={18} /> Pronto para Montagem
          </h2>
          <div className="flex-1 overflow-y-auto space-y-4 pr-2">
            {readyOrders.map(order => (
              <div key={order.id} className="bg-white p-5 rounded-2xl shadow-md border-l-4 border-green-500 animate-in slide-in-from-left-4">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-black text-gray-900">
                        {order.order_type === 'delivery' ? 'Delivery' : `Mesa ${order.table?.table_number}`}
                    </h3>
                    <p className="text-sm text-gray-500">{order.customer_name}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs font-mono text-gray-400">#{order.id.slice(0,6)}</p>
                    <p className="text-xs font-bold text-green-600 mt-1">Aguardando {Math.floor((new Date().getTime() - new Date(order.created_at).getTime()) / 60000)} min</p>
                  </div>
                </div>

                <div className="bg-gray-50 rounded-xl p-3 mb-4 border border-gray-100">
                    <p className="text-[10px] font-bold text-gray-400 uppercase mb-2">Conferência de Itens</p>
                    <ul className="space-y-2">
                        {order.items.map((item, i) => (
                            <li key={i} className="flex items-center gap-3 text-sm text-gray-700">
                                <div className="w-5 h-5 rounded-full border-2 border-gray-300 flex items-center justify-center"></div>
                                <span className="font-bold">{item.quantity}x</span>
                                <span className="flex-1">{item.product.name}</span>
                                {getStationIcon(item.product.station)}
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="flex gap-3">
                    <button 
                        onClick={() => handlePrint(order)}
                        className="p-3 bg-gray-100 text-gray-600 rounded-xl hover:bg-gray-200 transition-colors"
                        title="Imprimir Ticket"
                    >
                        <Printer size={20} />
                    </button>
                    <button 
                        onClick={() => handleDeliver(order)}
                        className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-green-200 transition-all active:scale-95"
                    >
                        Despachar / Servir <ArrowRight size={20} />
                    </button>
                </div>
              </div>
            ))}
            {readyOrders.length === 0 && (
                <div className="text-center py-20 text-gray-400">Nenhum pedido aguardando montagem.</div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
