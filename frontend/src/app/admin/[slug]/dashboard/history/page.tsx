/**
 * Author: MESAFLOW_AI
 * Version: 11.2 (Next.js 16 Hardened)
 * DNA_ID: history-page-v11-2
 */
"use client";
import { useEffect, useState, useCallback, use } from "react";
import { getOrderHistory } from "@/lib/api";
import { Order } from "@/types";
import { ChevronLeft, ChevronRight, Eye, Loader2 } from "lucide-react";
import Modal from "@/components/ui/Modal";

export default function HistoryPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const params = use(paramsPromise);
  const slug = params.slug;
  
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const limit = 10;

  const fetchHistory = useCallback(async () => {
    if (!slug || slug === "undefined") return;
    setLoading(true);
    try {
      const data = await getOrderHistory(slug, page, limit);
      setOrders(data.data);
      setTotal(data.total);
    } catch (error) {
      console.error("[History] Sync Error:", error);
    } finally {
      setLoading(false);
    }
  }, [slug, page]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="space-y-6 p-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-black text-white tracking-tighter uppercase">Histórico de Pedidos</h1>
        <div className="text-xs font-bold text-slate-500 uppercase tracking-widest">Total: {total}</div>
      </div>
      
      <div className="bg-slate-900 border border-slate-800 rounded-[2rem] overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-400">
            <thead className="bg-slate-950 text-slate-500 uppercase font-black text-[10px] tracking-widest">
              <tr>
                <th className="px-6 py-4">ID</th>
                <th className="px-6 py-4">Data</th>
                <th className="px-6 py-4">Mesa</th>
                <th className="px-6 py-4">Total</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {loading ? (
                <tr><td colSpan={6} className="px-6 py-20 text-center"><Loader2 className="animate-spin mx-auto text-orange-500" /></td></tr>
              ) : orders.length === 0 ? (
                <tr><td colSpan={6} className="px-6 py-20 text-center font-bold uppercase text-xs text-slate-600">Nenhum registro encontrado.</td></tr>
              ) : (
                orders.map((order) => (
                  <tr key={order.id} className="hover:bg-slate-800/50 transition-colors">
                    <td className="px-6 py-4 font-mono text-xs">#{order.id.slice(-6).toUpperCase()}</td>
                    <td className="px-6 py-4 text-xs">{new Date(order.created_at).toLocaleString()}</td>
                    <td className="px-6 py-4 font-bold text-white">{order.table?.table_number || "DELIVERY"}</td>
                    <td className="px-6 py-4 font-black text-emerald-500">R$ {(Number(order.total_amount)/100).toFixed(2)}</td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 rounded-lg bg-slate-800 text-[10px] font-black uppercase tracking-tighter">
                        {order.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <button onClick={() => setSelectedOrder(order)} className="p-2 bg-slate-800 hover:bg-orange-600 text-white rounded-xl transition-all">
                        <Eye size={16} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}