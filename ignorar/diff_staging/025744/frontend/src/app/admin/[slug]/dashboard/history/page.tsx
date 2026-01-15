"use client";
import { useEffect, useState } from "react";
import { getOrderHistory } from "@/lib/api";
import { Order } from "@/types";
import { ChevronLeft, ChevronRight, Eye } from "lucide-react";
import Modal from "@/components/ui/Modal";

export default function HistoryPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const limit = 10;

  const fetchHistory = async () => {
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
  };

  useEffect(() => {
    fetchHistory();
  }, [slug, page]);

  const totalPages = Math.ceil(total / limit);

  const statusColors: Record<string, string> = {
    pending: "bg-yellow-500/20 text-yellow-500",
    accepted: "bg-blue-500/20 text-blue-500",
    preparing: "bg-orange-500/20 text-orange-500",
    ready: "bg-purple-500/20 text-purple-500",
    delivered: "bg-green-500/20 text-green-500",
    canceled: "bg-red-500/20 text-red-500",
  };

  const paymentColors: Record<string, string> = {
    paid: "text-green-500",
    pending: "text-yellow-500",
    failed: "text-red-500",
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-white">Histórico de Pedidos</h1>
        <div className="text-sm text-gray-400">Total: {total} pedidos</div>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-400">
            <thead className="bg-gray-900 text-gray-200 uppercase font-bold">
              <tr>
                <th className="px-6 py-4">ID</th>
                <th className="px-6 py-4">Data</th>
                <th className="px-6 py-4">Mesa</th>
                <th className="px-6 py-4">Cliente</th>
                <th className="px-6 py-4">Total</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Pagamento</th>
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
                    <td className="px-6 py-4 font-bold text-white">{order.table?.table_number}</td>
                    <td className="px-6 py-4">{order.customer_name || "-"}</td>
                    <td className="px-6 py-4 font-bold text-white">R$ {Number(order.total_amount).toFixed(2)}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded text-xs font-bold uppercase ${statusColors[order.status] || "bg-gray-700 text-gray-300"}`}>
                        {order.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`font-bold uppercase text-xs ${paymentColors[order.payment_status]}`}>
                        {order.payment_status}
                      </span>
                      <span className="text-[10px] ml-1 text-gray-500">({order.payment_method})</span>
                    </td>
                    <td className="px-6 py-4">
                      <button 
                        type="button"
                        onClick={() => setSelectedOrder(order)} 
                        className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white transition-colors"
                      >
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
            type="button"
            disabled={page === 1} 
            onClick={() => setPage(p => p - 1)}
            className="flex items-center gap-1 text-sm font-medium text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ChevronLeft size={16} /> Anterior
          </button>
          <span className="text-sm text-gray-500">Página {page} de {totalPages || 1}</span>
          <button 
            type="button"
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
                <p className="font-bold text-white">{selectedOrder.table?.table_number}</p>
              </div>
              <div>
                <p className="text-gray-500">Data</p>
                <p className="font-bold text-white">{new Date(selectedOrder.created_at).toLocaleString()}</p>
              </div>
              <div>
                <p className="text-gray-500">Pagamento</p>
                <p className="font-bold text-white uppercase">{selectedOrder.payment_method} ({selectedOrder.payment_status})</p>
              </div>
            </div>
            <div className="border-t border-gray-700 pt-4">
              <h4 className="font-bold text-white mb-2">Itens</h4>
              <ul className="space-y-2">
                {selectedOrder.items.map((item, i) => (
                  <li key={i} className="bg-gray-900 p-3 rounded-lg border border-gray-700">
                    <div className="flex justify-between">
                      <span className="font-bold text-white">{item.quantity}x {item.product.name}</span>
                    </div>
                    {item.selected_options.length > 0 && (
                      <p className="text-xs text-gray-500 mt-1">+ {item.selected_options.map(o => o.name).join(", ")}</p>
                    )}
                    {item.notes && <p className="text-xs text-orange-500 mt-1 italic">Obs: {item.notes}</p>}
                  </li>
                ))}
              </ul>
            </div>
            <div className="border-t border-gray-700 pt-4 flex justify-between items-center">
              <span className="text-lg font-bold text-white">Total</span>
              <span className="text-xl font-black text-orange-500">R$ {Number(selectedOrder.total_amount).toFixed(2)}</span>
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
