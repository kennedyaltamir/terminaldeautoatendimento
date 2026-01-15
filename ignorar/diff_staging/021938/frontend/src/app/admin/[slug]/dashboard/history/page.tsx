"use client";
import { useEffect, useState, useCallback } from "react";
import { getOrderHistory } from "@/lib/api";
import { Order } from "@/types";
import { ChevronLeft, ChevronRight, Eye, History, Search, Filter } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { formatCurrency } from "@/lib/utils";
import { cn } from "@/lib/utils";

export default function DashboardHistoryPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const limit = 10;

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getOrderHistory(slug, page, limit);
      setOrders(data.data);
      setTotal(data.total);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, [slug, page, limit]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="space-y-8 pb-20 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <History className="text-orange-500" /> Histórico de Vendas
          </h1>
          <p className="text-slate-400 text-sm mt-1">Auditoria completa de transações e pedidos.</p>
        </div>
        <div className="flex gap-2 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
            <input type="text" placeholder="Buscar pedido..." className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-10 pr-4 py-2 text-sm text-white outline-none focus:border-orange-500 transition-all" />
          </div>
          <button type="button" className="p-2 bg-slate-800 text-slate-400 rounded-xl border border-slate-700 hover:text-white transition-colors">
            <Filter size={20} />
          </button>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-[2rem] overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800/50 text-slate-500 font-black uppercase text-[10px] tracking-[0.2em]">
              <tr>
                <th className="px-6 py-5">ID</th>
                <th className="px-6 py-5">Data/Hora</th>
                <th className="px-6 py-5">Cliente</th>
                <th className="px-6 py-5">Total</th>
                <th className="px-6 py-5">Status</th>
                <th className="px-6 py-5 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {loading ? (
                <tr><td colSpan={6} className="px-6 py-20 text-center text-slate-500 font-bold animate-pulse">Carregando registros...</td></tr>
              ) : orders.length === 0 ? (
                <tr><td colSpan={6} className="px-6 py-20 text-center text-slate-500 italic">Nenhum pedido encontrado.</td></tr>
              ) : (
                orders.map((order) => (
                  <tr key={order.id} className="hover:bg-slate-800/30 transition-colors group">
                    <td className="px-6 py-4 font-mono text-xs text-slate-500">#{order.id.slice(0, 8)}</td>
                    <td className="px-6 py-4 text-slate-300">{new Date(order.created_at).toLocaleString()}</td>
                    <td className="px-6 py-4 font-bold text-white">{order.customer_name || "Consumidor"}</td>
                    <td className="px-6 py-4 font-black text-orange-500">{formatCurrency(order.total_amount)}</td>
                    <td className="px-6 py-4">
                      <span className={cn(
                        "px-2 py-1 rounded text-[10px] font-black uppercase tracking-tighter",
                        order.status === 'delivered' ? 'bg-emerald-900/30 text-emerald-500' : 'bg-slate-800 text-slate-400'
                      )}>
                        {order.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button 
                        type="button"
                        onClick={() => setSelectedOrder(order)} 
                        className="p-2 bg-slate-800 text-slate-400 rounded-lg hover:text-white hover:bg-slate-700 transition-all"
                      >
                        <Eye size={18} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        
        {/* Paginação */}
        <div className="bg-slate-800/30 px-6 py-5 border-t border-slate-800 flex justify-between items-center">
          <button 
            type="button"
            disabled={page === 1} 
            onClick={() => setPage(p => p - 1)}
            className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-slate-500 hover:text-white disabled:opacity-30 transition-colors"
          >
            <ChevronLeft size={16} /> Anterior
          </button>
          <span className="text-[10px] font-black text-slate-600 uppercase tracking-widest">Página {page} de {totalPages || 1}</span>
          <button 
            type="button"
            disabled={page >= totalPages} 
            onClick={() => setPage(p => p + 1)}
            className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-slate-500 hover:text-white disabled:opacity-30 transition-colors"
          >
            Próxima <ChevronRight size={16} />
          </button>
        </div>
      </div>

      <Modal isOpen={!!selectedOrder} onClose={() => setSelectedOrder(null)} title={`Detalhes do Pedido`}>
        {selectedOrder && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4 bg-slate-50 dark:bg-slate-900 p-4 rounded-2xl border border-slate-100 dark:border-slate-800">
              <div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Cliente</p>
                <p className="font-bold text-slate-900 dark:text-white">{selectedOrder.customer_name || "Não informado"}</p>
              </div>
              <div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total</p>
                <p className="font-black text-orange-600 text-lg">{formatCurrency(selectedOrder.total_amount)}</p>
              </div>
            </div>
            <div className="flex justify-end">
              <button 
                type="button"
                onClick={() => setSelectedOrder(null)} 
                className="bg-slate-900 dark:bg-white text-white dark:text-slate-900 px-6 py-2 rounded-xl font-black uppercase text-xs active:scale-95 transition-all"
              >
                Fechar
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
