/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 13.2.1 (Final Render-Safe Edition)
 * DNA_ID: MF-EXPEDITOR-V13-FIX-FINAL
 * Objective: Remove redundant Toaster to eliminate React 19 render-phase warnings.
 */
"use client";

import React, { useEffect, useState, useCallback, useMemo, use } from "react";
import { useRouter } from "next/navigation";
import { 
  ChefHat, CheckCircle2, Clock, Utensils, Wine, 
  IceCream, Box, ArrowRight, Printer, AlertCircle,
  PackageCheck, Loader2, Timer,Truck
} from "lucide-react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { toast, Toaster } from "sonner";
import { getKitchenOrders, updateOrderStatus } from "@/lib/api";
import { Order } from "@/types";
import { printOrder } from "@/lib/printer/driver";
import { cn } from "@/lib/utils";

export default function ExpeditorPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  // 🛡️ PROTOCOLO NEXT 16: Unwrapping da Promise de params
  const { slug } = use(paramsPromise);
  const router = useRouter();
  
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const fetchData = useCallback(async () => {
    if (!slug || slug === "undefined") return;
    try {
      const data = await getKitchenOrders(slug);
      setOrders(data);
      setLastUpdated(new Date());
    } catch (e) {
      console.error("[Expeditor] Sync Error");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "new_order") {
      fetchData();
    }
  });

  const handleDeliver = async (order: Order) => {
    setUpdatingId(order.id);
    try {
      await updateOrderStatus(slug, order.id, "delivered");
      toast.success(`Pedido #${order.id.slice(0, 4)} despachado!`);
      setOrders(prev => prev.filter(o => o.id !== order.id));
    } catch (e) {
      toast.error("Falha ao atualizar status");
      fetchData();
    } finally {
      setUpdatingId(null);
    }
  };

  const handlePrint = (order: Order) => {
    try {
      printOrder(order, slug);
      toast.info("Enviando para impressora...");
    } catch (e) {
      toast.error("Erro ao imprimir ticket");
    }
  };

  const getStationIcon = (station: string) => {
    switch (station) {
      case 'bar': return <Wine size={14} className="text-purple-500" />;
      case 'dessert': return <IceCream size={14} className="text-pink-500" />;
      case 'kitchen': return <Utensils size={14} className="text-orange-500" />;
      default: return <Box size={14} className="text-gray-400" />;
    }
  };

  const preparingOrders = useMemo(() => 
    orders.filter(o => o.status === 'preparing' || o.status === 'pending'), 
  [orders]);

  const readyOrders = useMemo(() => 
    orders.filter(o => o.status === 'ready'), 
  [orders]);

  if (loading) {
    return (
      <div className="h-screen w-full flex flex-col items-center justify-center bg-gray-50 gap-4">
        <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
        <p className="text-gray-500 font-medium animate-pulse">Sincronizando com a cozinha...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8 font-sans text-slate-900">
      <Toaster position="top-right" richColors />
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-2xl shadow-lg shadow-blue-200">
              <ChefHat className="text-white" size={28} />
            </div>
            <h1 className="text-3xl font-black tracking-tight">Expedição</h1>
          </div>
          <p className="text-slate-500 text-sm mt-1 font-medium">
            Monitor de montagem e despacho • {slug.toUpperCase()}
          </p>
        </div>
        <div className="flex gap-3 w-full md:w-auto">
          <div className="flex-1 md:flex-none bg-white px-6 py-3 rounded-2xl shadow-sm border border-slate-200 flex flex-col items-center">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Em Preparo</span>
            <span className="text-2xl font-black text-orange-500">{preparingOrders.length}</span>
          </div>
          <div className="flex-1 md:flex-none bg-white px-6 py-3 rounded-2xl shadow-sm border border-slate-200 flex flex-col items-center">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Prontos</span>
            <span className="text-2xl font-black text-green-500">{readyOrders.length}</span>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[calc(100vh-180px)]">
        <div className="bg-slate-200/40 rounded-[2.5rem] p-6 flex flex-col border border-slate-200">
          <h2 className="text-slate-500 font-black uppercase text-xs tracking-[0.2em] mb-6 flex items-center gap-2">
            <Timer size={16} /> Fluxo da Cozinha
          </h2>
          <div className="flex-1 overflow-y-auto space-y-4 custom-scrollbar pr-2">
            {preparingOrders.map(order => (
              <div key={order.id} className="bg-white/80 backdrop-blur-sm p-5 rounded-2xl shadow-sm border border-slate-100 transition-all hover:shadow-md">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <span className="font-black text-slate-900 text-lg">#{order.id.slice(0,4)}</span>
                    <p className="text-xs font-bold text-slate-400 uppercase">{order.customer_name || "Balcão"}</p>
                  </div>
                  <span className={cn(
                    "text-[10px] font-black px-2 py-1 rounded-lg uppercase tracking-tighter",
                    order.status === 'preparing' ? "bg-amber-100 text-amber-700" : "bg-slate-100 text-slate-600"
                  )}>
                    {order.status === 'preparing' ? 'Preparando' : 'Pendente'}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {order.items.map((item, i) => (
                    <div key={i} className="group relative flex items-center gap-1.5 bg-slate-50 border border-slate-100 px-2.5 py-1.5 rounded-xl">
                      {getStationIcon(item.product.station)}
                      <span className="text-xs font-bold text-slate-700">{item.quantity}x</span>
                      <span className="text-xs font-medium text-slate-600">{item.product.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-blue-600 rounded-[2.5rem] p-6 flex flex-col shadow-2xl shadow-blue-200">
          <h2 className="text-blue-100 font-black uppercase text-xs tracking-[0.2em] mb-6 flex items-center gap-2">
            <CheckCircle2 size={16} /> Pronto para Despacho
          </h2>
          <div className="flex-1 overflow-y-auto space-y-4 custom-scrollbar pr-2">
            {readyOrders.map(order => (
              <div key={order.id} className="bg-white p-6 rounded-[2rem] shadow-xl animate-in fade-in slide-in-from-right-4 duration-500">
                <div className="flex justify-between items-start mb-5">
                  <div>
                    <h3 className="text-2xl font-black text-slate-900 leading-none">
                        {order.order_type === 'delivery' ? '🚀 Delivery' : `🪑 Mesa ${order.table?.table_number || '?'}`}
                    </h3>
                    <p className="text-sm font-bold text-blue-600 mt-1 uppercase tracking-tight">
                      {order.customer_name}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center gap-1 text-slate-400 font-mono text-[10px] justify-end">
                      <Clock size={10} /> {new Date(order.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                  </div>
                </div>
                <div className="flex gap-3">
                    <button 
                        onClick={() => handlePrint(order)}
                        className="p-4 bg-slate-100 text-slate-600 rounded-2xl hover:bg-slate-200 transition-all active:scale-90"
                    >
                        <Printer size={22} />
                    </button>
                    <button 
                        disabled={updatingId === order.id}
                        onClick={() => handleDeliver(order)}
                        className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-3 shadow-lg shadow-blue-200 transition-all active:scale-[0.98]"
                    >
                        {updatingId === order.id ? (
                          <Loader2 className="animate-spin" />
                        ) : (
                          <>DESPACHAR AGORA <ArrowRight size={20} /></>
                        )}
                    </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
