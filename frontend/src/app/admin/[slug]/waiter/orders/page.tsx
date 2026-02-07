"use client";

import { useEffect, useState, useCallback, use } from "react";
import { getKitchenOrders } from "@/lib/api";
import { Order } from "@/types";
import { Loader2, Clock, CheckCircle2, XCircle, Bike } from "lucide-react";
import { formatCurrency, cn } from "@/lib/utils";
import { toast } from "sonner";

export default function WaiterOrdersPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  // 🛡️ FIX: Unwrapping de params com use()
  const { slug } = use(paramsPromise);
  
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = useCallback(async () => {
    if (!slug) return;
    try {
      const data = await getKitchenOrders(slug);
      // Filtra pedidos recentes (últimas 24h)
      setOrders(data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()));
    } catch (e) {
      console.error("Erro ao buscar pedidos:", e);
      toast.error("Falha ao atualizar lista de pedidos.");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => {
    fetchOrders();
    const interval = setInterval(fetchOrders, 15000);
    return () => clearInterval(interval);
  }, [fetchOrders]);

  if (loading) return (
    <div className="flex h-[50vh] items-center justify-center">
      <Loader2 className="animate-spin text-orange-500" size={32} />
    </div>
  );

  return (
    <div className="p-4 space-y-4 pb-24">
      <h1 className="text-2xl font-black text-slate-900 uppercase tracking-tight mb-6">Pedidos Recentes</h1>
      
      {orders.length === 0 ? (
        <div className="text-center py-10 text-gray-400">
          <p>Nenhum pedido encontrado.</p>
        </div>
      ) : (
        orders.map((order) => (
          <div key={order.id} className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex justify-between items-start mb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-black text-lg text-slate-900">
                    {order.order_type === 'delivery' ? 'Delivery' : `Mesa ${order.table?.table_number || '?'}`}
                  </span>
                  <span className="text-xs font-mono text-gray-400">#{order.id.slice(0,4)}</span>
                </div>
                <p className="text-xs text-gray-500 font-bold uppercase">{order.customer_name || "Cliente"}</p>
              </div>
              <span className={cn(
                "px-2 py-1 rounded text-[10px] font-black uppercase tracking-widest",
                order.status === 'ready' ? "bg-green-100 text-green-700" :
                order.status === 'delivered' ? "bg-gray-100 text-gray-600" :
                "bg-orange-100 text-orange-700"
              )}>
                {order.status}
              </span>
            </div>
            
            <div className="space-y-1 mb-3">
              {order.items.map((item, i) => (
                <div key={i} className="flex justify-between text-sm">
                  <span className="text-gray-600">{item.quantity}x {item.product.name}</span>
                </div>
              ))}
            </div>

            <div className="pt-3 border-t border-gray-100 flex justify-between items-center">
              <span className="text-xs text-gray-400 flex items-center gap-1">
                <Clock size={12} /> {new Date(order.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
              </span>
              <span className="font-black text-slate-900">{formatCurrency(order.total_amount)}</span>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
