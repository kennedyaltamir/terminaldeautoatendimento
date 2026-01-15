"use client";
import { useEffect, useState, useCallback } from "react";
import { getOrderHistory, emitFiscalDocument } from "@/lib/api";
import { Order } from "@/types";
import { ChevronLeft, ChevronRight, Eye, AlertTriangle, RefreshCw, WifiOff } from "lucide-react";
import Modal from "@/components/ui/Modal";
import FiscalStatusBadge from "@/components/admin/FiscalStatusBadge";
import { toast, Toaster } from "sonner";
import { useFiscalSync } from "@/hooks/useFiscalSync";
import { formatCurrency } from "@/lib/utils";

export default function HistoryPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [emittingId, setEmittingId] = useState<string | null>(null);
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

  // Ativa o motor de sincronização fiscal com callback de refresh
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
      toast.success(res.message || "Emissão solicitada!");
      fetchHistory();
    } catch (e: any) {
      toast.error(e.message || "Erro ao emitir nota");
    } finally {
      setEmittingId(null);
    }
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="space-y-6">
      <Toaster position="top-right" richColors />
      
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Histórico de Pedidos</h1>
          <p className="text-sm text-gray-400">Total: {total} pedidos registrados</p>
        </div>
        
        {/* Indicador de Contingência Fiscal */}
        {(pendingCount > 0 || errorCount > 0) && (
          <div 
            onClick={() => !isSyncing && syncNow()}
            className={`flex items-center gap-3 px-4 py-2 rounded-xl border cursor-pointer transition-all animate-in slide-in-from-right ${
              errorCount > 0 ? 'bg-red-900/20 border-red-500 text-red-200' : 'bg-orange-900/20 border-orange-500 text-orange-200'
            }`}
          >
            {isSyncing ? <RefreshCw size={18} className="animate-spin" /> : <AlertTriangle size={18} />}
            <div className="text-xs">
              <p className="font-bold">{pendingCount} Notas em Contingência</p>
              {errorCount > 0 && <p className="opacity-80">{errorCount} erros detectados</p>}
            </div>
            {!isSyncing && <RefreshCw size={14} className="ml-2 opacity-50" />}
          </div>
        )}
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-400">
            <thead className="bg-gray-900 text-gray-200 uppercase font-bold">
              <tr>
                <th className="px-6 py-4">ID</th>
                <th className="px-6 py-4">Data</th>
                <th className="px-6 py-4">Mesa</th>
                <th className="px-6 py-4">Total</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Pagamento</th>
                <th className="px-6 py-4">Fiscal</th>
                <th className="px-6 py-4">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {loading ? (
                <tr><td colSpan={8} className="px-6 py-8 text-center">Carregando...</td></tr>
              ) : orders.length === 0 ? (
                <tr><td colSpan={8} className="px-6 py-8 text-center">Nenhum pedido encontrado.</td></tr>
              ) : (
                orders.map((order) => (
                  <tr key={order.id} className="hover:bg-gray-700/50 transition-colors">
                    <td className="px-6 py-4 font-mono text-xs">{order.id.slice(0, 8)}</td>
                    <td className="px-6 py-4">{new Date(order.created_at).toLocaleString()}</td>
                    <td className="px-6 py-4 font-bold text-white">{order.table?.table_number || "Delivery"}</td>
                    <td className="px-6 py-4 font-bold text-white">{formatCurrency(order.total_amount)}</td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 rounded text-[10px] font-bold uppercase bg-gray-700 text-gray-300">
                        {order.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`font-bold uppercase text-xs ${order.payment_status === 'paid' ? 'text-green-500' : 'text-yellow-500'}`}>
                        {order.payment_status}
                      </span>
                    </td>
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
                      <button onClick={() => setSelectedOrder(order)} className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white transition-colors">
                        <Eye size={16} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        <div className="bg-gray-900 px-6 py-4 border-t border-gray-700 flex justify-between items-center">
          <button 
            disabled={page === 1} 
            onClick={() => setPage(p => p - 1)}
            className="flex items-center gap-1 text-sm font-medium text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft size={16} /> Anterior
          </button>
          <span className="text-sm text-gray-500">Página {page} de {totalPages || 1}</span>
          <button 
            disabled={page >= totalPages} 
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
          </div>
        )}
      </Modal>
    </div>
  );
}
