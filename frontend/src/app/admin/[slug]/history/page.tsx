"use client";

import { useEffect, useState, useCallback, use } from "react"; // FIX: Import 'use'
import { getOrderHistory, emitFiscalDocument } from "@/lib/api";
import { Order } from "@/types";
import { ChevronLeft, ChevronRight, Eye, RefreshCw } from "lucide-react";
import Modal from "@/components/ui/Modal";
import FiscalStatusBadge from "@/components/admin/FiscalStatusBadge";
import { toast } from "sonner";
import { useFiscalSync } from "@/hooks/useFiscalSync";
import { formatCurrency } from "@/lib/utils";

export default function HistoryPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  // 🛡️ PROTOCOLO NEXT 16: Unwrapping da Promise de params
  const params = use(paramsPromise);
  const slug = params.slug;
  
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [emittingId, setEmittingId] = useState<string | null>(null);
  const limit = 10;

  const fetchHistory = useCallback(async () => {
    if (!slug || slug === "undefined") return;
    setLoading(true);
    try {
      const data = await getOrderHistory(slug, page, limit);
      setOrders(data.data);
      setTotal(data.total);
    } catch (error) {
      console.error("Erro ao carregar histórico:", error);
    } finally {
      setLoading(false);
    }
  }, [slug, page]);

  const { pendingCount, errorCount, isSyncing, syncNow } = useFiscalSync({
    onSyncComplete: () => fetchHistory()
  });

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleEmitFiscal = async (orderId: string) => {
    setEmittingId(orderId);
    try {
      const res = await emitFiscalDocument(orderId);
      if (res.status === 'error') {
        toast.error(res.message || "Erro na emissão");
      } else {
        toast.success(res.message || "Emissão solicitada!");
      }
      fetchHistory();
    } catch (e: any) {
      toast.error(e.message || "Erro ao emitir nota");
    } finally {
      setEmittingId(null);
    }
  };

  const totalPages = Math.ceil(total / limit);
  const isPrevDisabled = page === 1;
  const isNextDisabled = page >= totalPages;

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-white">Histórico de Pedidos</h1>
        <p className="text-sm text-gray-400">Loja: {slug}</p>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-400">
            <thead className="bg-gray-900 text-gray-200 uppercase font-bold">
              <tr>
                <th className="px-6 py-4">Data</th>
                <th className="px-6 py-4">Mesa</th>
                <th className="px-6 py-4">Total</th>
                <th className="px-6 py-4">Fiscal</th>
                <th className="px-6 py-4">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {loading ? (
                <tr><td colSpan={5} className="px-6 py-8 text-center">Carregando...</td></tr>
              ) : orders.map((order) => (
                  <tr key={order.id} className="hover:bg-gray-700/50 transition-colors">
                    <td className="px-6 py-4">{new Date(order.created_at).toLocaleString()}</td>
                    <td className="px-6 py-4 font-bold text-white">{order.table?.table_number || "Delivery"}</td>
                    <td className="px-6 py-4 font-bold text-white">{formatCurrency(order.total_amount)}</td>
                    <td className="px-6 py-4">
                      <FiscalStatusBadge 
                        orderId={order.id}
                        status={order.fiscal_status || 'pending'} 
                        nfeUrl={order.nfe_url_pdf}
                        onEmit={() => handleEmitFiscal(order.id)}
                        loading={emittingId === order.id}
                        slug={slug}
                      />
                    </td>
                    <td className="px-6 py-4">
                    <button onClick={() => setSelectedOrder(order)} className="p-2 bg-gray-700 rounded-lg text-white">
                        <Eye size={16} />
                      </button>
                    </td>
                  </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="bg-gray-900 px-6 py-4 border-t border-gray-700 flex justify-between items-center">
          <button 
            type="button"
            disabled={isPrevDisabled} 
            onClick={() => setPage(p => p - 1)}
            className="flex items-center gap-1 text-sm font-medium text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft size={16} /> Anterior
          </button>
          <span className="text-sm text-gray-500">Página {page} de {totalPages || 1}</span>
          <button 
            type="button"
            disabled={isNextDisabled} 
            onClick={() => setPage(p => p + 1)}
            className="flex items-center gap-1 text-sm font-medium text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Próxima <ChevronRight size={16} />
          </button>
        </div>
      </div>

      <Modal isOpen={!!selectedOrder} onClose={() => setSelectedOrder(null)} title={`Pedido #${selectedOrder?.id.slice(0,8)}`}>
        {selectedOrder && (
          <div className="space-y-4 text-gray-300">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-500">Cliente</p>
                <p className="font-bold text-white">{selectedOrder.customer_name || "Anônimo"}</p>
              </div>
              <div>
                <p className="text-gray-500">Mesa</p>
                <p className="font-bold text-white">{selectedOrder.table?.table_number || "Delivery"}</p>
              </div>
            </div>
            <div className="border-t border-gray-700 pt-4 flex justify-between items-center">
              <span className="text-lg font-bold text-white">Total</span>
              <span className="text-xl font-black text-orange-500">{formatCurrency(selectedOrder.total_amount)}</span>
            </div>
            <div className="flex justify-end pt-4">
              <button 
                type="button" 
                onClick={() => setSelectedOrder(null)} 
                className="bg-gray-700 text-white px-4 py-2 rounded-lg font-bold"
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
   