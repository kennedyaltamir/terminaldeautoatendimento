// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 20:30:00
"use client";
import { useEffect, useState, useCallback } from "react";
import { 
  getTablesDashboard, createTable, deleteTable, 
  openTable, createTablesBulk, closeTable 
} from "@/lib/api";
import { TableDashboard } from "@/types";
import { 
  Plus, Trash2, QrCode, Users, 
  RefreshCw, Layout, Loader2, CheckCircle2
} from "lucide-react";
import { toast, Toaster } from "sonner";
import Modal from "@/components/ui/Modal";
import { useWebSocket } from "@/hooks/useWebSocket";
import { formatCurrency } from "@/lib/utils";

export default function TablesPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const [tables, setTables] = useState<TableDashboard[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [selectedTable, setSelectedTable] = useState<TableDashboard | null>(null);
  const [newTableNumber, setNewTableNumber] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [customerName, setCustomerName] = useState("");

  const fetchTables = useCallback(async () => {
    try {
      const data = await getTablesDashboard(slug);
      setTables(data);
    } catch (e) {
      toast.error("Erro ao carregar mesas");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => { fetchTables(); }, [fetchTables]);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" || data.type === "waiter_call") {
      fetchTables();
    }
  });

  const handleCreateTable = async () => {
    if (!newTableNumber) return;
    setSubmitting(true);
    try {
      await createTable(parseInt(newTableNumber));
      toast.success("Mesa criada!");
      setIsCreateModalOpen(false);
      setNewTableNumber("");
      fetchTables();
    } catch (e: any) {
      toast.error(e.message || "Erro ao criar mesa");
    } finally {
      setSubmitting(false);
    }
  };

  const handleOpenTable = async () => {
    if (!selectedTable || !customerName) return toast.error("Nome obrigatório");
    setSubmitting(true);
    try {
      await openTable(selectedTable.id, customerName);
      setCustomerName("");
      setSelectedTable(null);
      fetchTables();
      toast.success("Mesa aberta!");
    } catch (e) {
      toast.error("Erro ao abrir mesa.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleCloseTable = async (method: string) => {
    if (!selectedTable) return;
    if (!confirm(`Confirmar pagamento em ${method.toUpperCase()}?`)) return;
    setSubmitting(true);
    try {
      await closeTable(selectedTable.id, method);
      setSelectedTable(null);
      fetchTables();
      toast.success("Mesa liberada!");
    } catch (e) {
      toast.error("Erro ao fechar mesa.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Excluir esta mesa permanentemente?")) return;
    try {
      await deleteTable(id);
      toast.success("Mesa removida");
      fetchTables();
    } catch (e) {
      toast.error("Erro ao excluir");
    }
  };

  if (loading) return <div className="p-10 text-center animate-pulse text-gray-500">Mapeando salão...</div>;

  return (
    <div className="space-y-8 pb-20 animate-in fade-in duration-500">
      <Toaster position="top-right" richColors />
      
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-black text-white flex items-center gap-3">
          <Layout className="text-orange-500" /> Gestão de Mesas
        </h1>
        <button 
          onClick={() => setIsCreateModalOpen(true)}
          className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2.5 rounded-xl font-bold flex items-center gap-2 transition-all shadow-lg"
        >
          <Plus size={18} /> Nova Mesa
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {tables.map((table) => (
          <div 
            key={table.id}
            onClick={() => setSelectedTable(table)}
            className={`relative group cursor-pointer bg-gray-900 border-2 rounded-2xl p-4 transition-all hover:scale-105 ${
              table.status === 'occupied' ? 'border-red-500/50 bg-red-950/10' : 'border-gray-800 hover:border-gray-600'
            }`}
          >
            <div className="flex justify-between items-start mb-4">
              <span className="text-2xl font-black text-white">#{table.table_number}</span>
              <div className={`w-3 h-3 rounded-full ${table.status === 'occupied' ? 'bg-orange-500 animate-pulse' : 'bg-green-500'}`}></div>
            </div>
            <div className="flex flex-col items-center gap-3 py-2">
              <div className={`p-3 rounded-xl ${table.status === 'occupied' ? 'bg-red-500/20 text-red-500' : 'bg-gray-800 text-gray-500'}`}>
                <Users size={24} />
              </div>
              <span className="text-[10px] font-black uppercase tracking-widest text-gray-600">
                {table.status === 'occupied' ? table.active_session?.customer_name : 'Livre'}
              </span>
            </div>
          </div>
        ))}
      </div>

      <Modal isOpen={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} title="Adicionar Mesa">
        <div className="space-y-4">
          <input 
            type="number"
            className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-white outline-none focus:border-orange-500"
            value={newTableNumber}
            onChange={e => setNewTableNumber(e.target.value)}
            placeholder="Número da Mesa"
          />
          <button onClick={handleCreateTable} disabled={submitting} className="w-full bg-orange-600 text-white py-3 rounded-xl font-bold">
            {submitting ? <Loader2 className="animate-spin" /> : "Confirmar"}
          </button>
        </div>
      </Modal>

      <Modal isOpen={!!selectedTable} onClose={() => setSelectedTable(null)} title={`Mesa ${selectedTable?.table_number}`}>
        {selectedTable && (
          <div className="space-y-6">
            {selectedTable.status === 'free' ? (
              <div className="flex gap-2">
                <input 
                  type="text" 
                  className="flex-1 bg-gray-800 border border-gray-600 rounded-lg p-2 text-white outline-none"
                  placeholder="Nome do Cliente"
                  value={customerName}
                  onChange={e => setCustomerName(e.target.value)}
                />
                <button onClick={handleOpenTable} disabled={submitting} className="bg-green-600 text-white px-4 rounded-lg font-bold">Abrir</button>
              </div>
            ) : (
              <div className="bg-orange-900/20 p-5 rounded-2xl border border-orange-500/30 space-y-4">
                <p className="text-white font-black text-2xl uppercase">{selectedTable.active_session?.customer_name}</p>
                <p className="text-white font-black text-2xl">R$ {Number(selectedTable.active_session?.total_spent).toFixed(2)}</p>
                <div className="grid grid-cols-2 gap-2">
                  <button onClick={() => handleCloseTable('cash')} disabled={submitting} className="bg-gray-800 text-white p-3 rounded-lg font-bold">Dinheiro</button>
                  <button onClick={() => handleCloseTable('card')} disabled={submitting} className="bg-gray-800 text-white p-3 rounded-lg font-bold">Cartão</button>
                </div>
              </div>
            )}
            <button onClick={() => handleDelete(selectedTable.id)} className="text-red-400 text-xs font-bold flex items-center gap-1">
              <Trash2 size={14} /> Excluir Mesa
            </button>
          </div>
        )}
      </Modal>
    </div>
  );
}

