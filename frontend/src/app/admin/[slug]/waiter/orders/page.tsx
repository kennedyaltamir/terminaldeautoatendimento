"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getKitchenOrders } from "@/lib/api";
import { Order } from "@/types";
import { Clock, CheckCircle2, ChefHat, Search, Printer } from "lucide-react";
import WaiterBottomNav from "@/components/waiter/WaiterBottomNav";
import Receipt from "@/components/waiter/Receipt";
import { toast, Toaster } from "sonner";

export default function WaiterOrdersPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [printingOrder, setPrintingOrder] = useState<Order | null>(null);

  useEffect(() => {
    getKitchenOrders(slug)
      .then(setOrders)
      .catch(() => toast.error("Erro ao carregar pedidos"))
      .finally(() => setLoading(false));
  }, [slug]);

  const filteredOrders = orders.filter(o => 
    o.table?.table_number.toString().includes(search) ||
    o.customer_name?.toLowerCase().includes(search.toLowerCase()) ||
    o.id.includes(search)
  );

  const getStatusColor = (status: string) => {
    switch(status) {
        case 'pending': return 'bg-yellow-100 text-yellow-700';
        case 'preparing': return 'bg-orange-100 text-orange-700';
        case 'ready': return 'bg-green-100 text-green-700 animate-pulse';
        default: return 'bg-gray-100 text-gray-600';
    }
  };

  const getStatusLabel = (status: string) => {
    switch(status) {
        case 'pending': return 'Aguardando';
        case 'preparing': return 'Preparando';
        case 'ready': return 'Pronto p/ Servir';
        default: return status;
    }
  };

  return (
    <div className="pb-24">
      <Toaster position="top-center" richColors />
      
      <div className="p-4 bg-gray-900 text-white sticky top-0 z-40 shadow-md">
        <h1 className="text-xl font-bold mb-4">Pedidos Ativos</h1>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input 
            type="text" 
            placeholder="Buscar por mesa ou cliente..."
            className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-white focus:ring-2 focus:ring-orange-500 outline-none"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="p-4 space-y-3">
        {loading ? (
            <p className="text-center py-10 text-gray-500">Carregando...</p>
        ) : filteredOrders.length === 0 ? (
            <div className="text-center py-10 text-gray-400">
                <ChefHat size={48} className="mx-auto mb-2 opacity-20" />
                <p>Nenhum pedido ativo no momento.</p>
            </div>
        ) : (
            filteredOrders.map(order => (
                <div key={order.id} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                    <div className="flex justify-between items-start mb-3">
                        <div>
                            <h3 className="font-bold text-lg">
                                {order.order_type === 'delivery' ? 'Delivery' : `Mesa ${order.table?.table_number}`}
                            </h3>
                            <p className="text-xs text-gray-500">{order.customer_name || "Cliente"}</p>
                        </div>
                        <span className={`px-2 py-1 rounded text-xs font-bold uppercase ${getStatusColor(order.status)}`}>
                            {getStatusLabel(order.status)}
                        </span>
                    </div>

                    <div className="space-y-1 mb-3">
                        {order.items.map((item, i) => (
                            <div key={i} className="flex justify-between text-sm">
                                <span className="text-gray-700">{item.quantity}x {item.product.name}</span>
                            </div>
                        ))}
                    </div>

                    <div className="flex justify-between items-center pt-3 border-t border-gray-100">
                        <span className="text-xs text-gray-400 flex items-center gap-1">
                            <Clock size={12} /> {new Date(order.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
                        </span>
                        <button 
                            onClick={() => setPrintingOrder(order)}
                            className="flex items-center gap-1 text-xs font-bold bg-gray-100 px-3 py-1.5 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                            <Printer size={14} /> Reimprimir
                        </button>
                    </div>
                </div>
            ))
        )}
      </div>

      <WaiterBottomNav slug={slug} />
      
      {printingOrder && (
        <Receipt 
            order={printingOrder} 
            companyName="MesaFlow" 
            onClose={() => setPrintingOrder(null)} 
        />
      )}
    </div>
  );
}