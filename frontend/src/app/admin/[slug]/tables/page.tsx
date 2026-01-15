"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { Grid, Plus, Printer, RefreshCw, Trash2, User, Clock, AlertTriangle } from "lucide-react";
import { getTablesDashboard, createTable, deleteTable, openTable, closeTable, createTablesBulk } from "@/lib/api";
import { Table } from "@/types";
import Modal from "@/components/ui/Modal";
import { toast } from "sonner";

// Enterprise Standard: Typing for Table Entities based on API response
interface TableDashboard extends Table {
  status: 'free' | 'occupied' | 'alert';
  active_session?: {
    id: number;
    customer_name: string;
    total_spent: number;
    start_time: string;
    access_pin?: string;
  };
  service_request?: string;
}

interface PageState {
  data: TableDashboard[];
  loading: boolean;
  error: string | null;
}

/**
 * HYPEROPTIMUS FIX: 2026-01-10
 * Reason: Previous implementation caused render loops/SSR aborts.
 * Strategy: Stabilized useEffect, explicit state management, standard UI feedback.
 */
export default function TablesPage() {
  const params = useParams();
  const slug = params?.slug as string;

  // Stable State Management
  const [state, setState] = useState<PageState>({
    data: [],
    loading: true,
    error: null,
  });

  // Modal States
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [selectedTable, setSelectedTable] = useState<TableDashboard | null>(null);
  const [newTableNum, setNewTableNum] = useState("");
  const [bulkStart, setBulkStart] = useState("");
  const [bulkEnd, setBulkEnd] = useState("");
  const [customerName, setCustomerName] = useState("");

  // Data Fetching Mechanism - Memoized to prevent reference instability
  const fetchTables = useCallback(async () => {
    if (!slug) return;

    try {
      const data = await getTablesDashboard(slug);
      
      // Safety Check: Ensure payload is an array
      const safeData = Array.isArray(data) ? data : [];

      setState({
        data: safeData,
        loading: false,
        error: null,
      });
    } catch (err: any) {
      console.error("[TablesPage] Fetch Error:", err);
      setState((prev) => ({
        ...prev,
        loading: false,
        error: err.message || "Unknown error occurred.",
      }));
      toast.error("Erro ao carregar mesas.");
    }
  }, [slug]);

  // Effect: Trigger fetch only on slug change or mount
  useEffect(() => {
    let mounted = true;

    if (mounted && slug) {
      fetchTables();
    }

    return () => {
      mounted = false;
    };
  }, [slug, fetchTables]);

  // Handlers
  const handleCreate = async () => {
    if (!newTableNum) return;
    try {
      await createTable(parseInt(newTableNum));
      setNewTableNum("");
      setIsCreateModalOpen(false);
      fetchTables();
      toast.success("Mesa criada!");
    } catch (e) {
      toast.error("Erro ao criar mesa.");
    }
  };

  const handleBulkCreate = async () => {
    if (!bulkStart || !bulkEnd) return;
    try {
      await createTablesBulk(parseInt(bulkStart), parseInt(bulkEnd));
      setBulkStart("");
      setBulkEnd("");
      setIsCreateModalOpen(false);
      fetchTables();
      toast.success("Mesas criadas em lote!");
    } catch (e) {
      toast.error("Erro ao criar em lote.");
    }
  };

  const handleOpenTable = async () => {
    if (!selectedTable || !customerName) return toast.error("Nome obrigatório");
    try {
      await openTable(selectedTable.id, customerName);
      setCustomerName("");
      setSelectedTable(null);
      fetchTables();
      toast.success("Mesa aberta!");
    } catch (e) {
      toast.error("Erro ao abrir mesa.");
    }
  };

  const handleCloseTable = async (method: string) => {
    if (!selectedTable) return;
    if (!confirm(`Confirmar pagamento em ${method.toUpperCase()}?`)) return;
    try {
      await closeTable(selectedTable.id, method);
      setSelectedTable(null);
      fetchTables();
      toast.success("Mesa liberada!");
    } catch (e) {
      toast.error("Erro ao fechar mesa.");
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm("Tem certeza? Isso apagará o histórico desta mesa.")) {
      try {
        await deleteTable(id);
        setSelectedTable(null);
        fetchTables();
        toast.success("Mesa removida.");
      } catch (e) {
        toast.error("Erro ao remover mesa.");
      }
    }
  };

  // RENDER: Loading State
  if (state.loading) {
    return (
      <div className="p-8 flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
        <span className="ml-4 text-gray-500 font-medium">Carregando Mesas...</span>
      </div>
    );
  }

  // RENDER: Error State
  if (state.error) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-r">
          <div className="flex">
            <div className="flex-shrink-0"><AlertTriangle className="text-red-500" /></div>
            <div className="ml-3">
              <p className="text-sm text-red-700 font-bold">Erro do Sistema</p>
              <p className="text-sm text-red-600">{state.error}</p>
              <button 
                onClick={() => fetchTables()}
                className="mt-2 text-sm font-bold text-red-700 hover:text-red-900 underline"
              >
                Tentar Novamente
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // RENDER: Success State
  return (
    <div className="pb-20 animate-in fade-in duration-500">
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-xl">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <Grid className="text-orange-500" /> Gestão de Mesas
            </h1>
            <p className="text-gray-400 text-sm mt-1">Gerencie o layout e status do salão.</p>
          </div>
          <div className="flex gap-3">
            <button onClick={() => fetchTables()} className="bg-gray-700 hover:bg-gray-600 text-white p-2 rounded-xl transition-colors" title="Atualizar">
              <RefreshCw size={20} />
            </button>
            <button onClick={() => setIsCreateModalOpen(true)} className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl flex items-center gap-2 font-bold transition-colors shadow-lg shadow-orange-900/20">
              <Plus size={16} /> Nova Mesa
            </button>
            <button onClick={() => window.print()} className="bg-white text-gray-900 px-4 py-2 rounded-xl flex items-center gap-2 font-bold transition-colors hover:bg-gray-100">
              <Printer size={16} /> Imprimir
            </button>
          </div>
        </div>

        {/* Grid */}
        {state.data.length === 0 ? (
          <div className="text-center py-20 bg-gray-800/50 rounded-2xl border border-dashed border-gray-700">
            <Grid size={48} className="mx-auto text-gray-600 mb-4" />
            <p className="text-gray-400">Nenhuma mesa cadastrada.</p>
            <button onClick={() => setIsCreateModalOpen(true)} className="mt-4 text-orange-500 font-bold hover:underline">Criar a primeira mesa</button>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {state.data.map((table) => {
              const isOccupied = table.status === 'occupied' || table.status === 'alert';
              return (
                <div 
                  key={table.id} 
                  onClick={() => setSelectedTable(table)}
                  className={`cursor-pointer rounded-xl p-4 border-2 shadow-sm transition-all relative group hover:-translate-y-1 ${
                    isOccupied 
                      ? 'bg-gray-800 border-orange-500/50 hover:border-orange-500' 
                      : 'bg-gray-800 border-gray-700 hover:border-gray-500'
                  }`}
                >
                  <div className="flex justify-between items-start mb-3">
                    <span className="text-2xl font-black text-white">#{table.table_number}</span>
                    <div className={`w-3 h-3 rounded-full ${isOccupied ? 'bg-orange-500 animate-pulse' : 'bg-green-500'}`}></div>
                  </div>
                  {table.active_session ? (
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-sm text-gray-300 font-medium truncate">
                        <User size={14} className="text-orange-500" /> {table.active_session.customer_name}
                      </div>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <Clock size={12} /> {new Date(table.active_session.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </div>
                      <div className="mt-2 pt-2 border-t border-gray-700 flex items-center justify-between">
                        <span className="text-lg font-bold text-green-400">R$ {Number(table.active_session.total_spent).toFixed(2)}</span>
                      </div>
                    </div>
                  ) : (
                    <div className="h-20 flex flex-col items-center justify-center text-gray-500 text-xs gap-2">
                      <span className="font-medium uppercase tracking-widest">Livre</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Modais */}
      <Modal isOpen={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} title="Adicionar Mesas">
        <div className="space-y-6">
          <div>
            <h4 className="font-bold text-sm text-gray-500 mb-2 uppercase">Individual</h4>
            <div className="flex gap-2">
              <input type="number" className="flex-1 bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Número" value={newTableNum} onChange={e => setNewTableNum(e.target.value)} />
              <button onClick={handleCreate} className="bg-orange-600 text-white px-6 rounded-lg font-bold hover:bg-orange-700">Criar</button>
            </div>
          </div>
          <div className="border-t border-gray-700 pt-4">
            <h4 className="font-bold text-sm text-gray-500 mb-2 uppercase">Em Lote (Sequência)</h4>
            <div className="flex gap-2 items-center">
              <input type="number" className="w-24 bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="De" value={bulkStart} onChange={e => setBulkStart(e.target.value)} />
              <span className="text-gray-500">até</span>
              <input type="number" className="w-24 bg-gray-900 border border-gray-700 rounded-lg p-3 text-white outline-none focus:ring-2 focus:ring-orange-500" placeholder="Até" value={bulkEnd} onChange={e => setBulkEnd(e.target.value)} />
              <button onClick={handleBulkCreate} className="flex-1 bg-gray-700 text-white px-4 py-3 rounded-lg font-bold hover:bg-gray-600">Gerar</button>
            </div>
          </div>
        </div>
      </Modal>

      <Modal isOpen={!!selectedTable} onClose={() => setSelectedTable(null)} title={`Mesa ${selectedTable?.table_number}`}>
        {selectedTable && (
          <div className="space-y-6">
            {selectedTable.status === 'free' ? (
              <div className="bg-gray-900 p-4 rounded-xl border border-gray-700">
                <p className="text-gray-400 text-sm mb-3">Mesa livre. Deseja abrir manualmente?</p>
                <div className="flex gap-2">
                  <input 
                    type="text" 
                    className="flex-1 bg-gray-800 border border-gray-600 rounded-lg p-2 text-white outline-none focus:ring-2 focus:ring-orange-500"
                    placeholder="Nome do Cliente"
                    value={customerName}
                    onChange={e => setCustomerName(e.target.value)}
                    autoFocus
                  />
                  <button onClick={handleOpenTable} className="bg-green-600 text-white px-4 rounded-lg font-bold hover:bg-green-700">Abrir</button>
                </div>
              </div>
            ) : (
              <div className="bg-orange-900/20 p-5 rounded-2xl border border-orange-500/30 space-y-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-orange-200 text-[10px] font-black uppercase tracking-widest">OCUPADA POR:</p>
                    <p className="text-white font-black text-2xl uppercase">{selectedTable.active_session?.customer_name}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-orange-200 text-[10px] font-black uppercase tracking-widest">TOTAL:</p>
                    <p className="text-white font-black text-2xl">R$ {Number(selectedTable.active_session?.total_spent).toFixed(2)}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2 pt-2">
                  <button onClick={() => handleCloseTable('cash')} className="bg-gray-800 hover:bg-green-600 text-gray-300 hover:text-white p-3 rounded-lg font-bold transition-colors border border-gray-700">
                    Dinheiro
                  </button>
                  <button onClick={() => handleCloseTable('card')} className="bg-gray-800 hover:bg-blue-600 text-gray-300 hover:text-white p-3 rounded-lg font-bold transition-colors border border-gray-700">
                    Cartão / Pix
                  </button>
                </div>
              </div>
            )}
            <div className="border-t border-gray-700 pt-4 flex justify-between items-center">
              <span className="text-xs text-gray-500">ID: {selectedTable.id}</span>
              <button onClick={() => handleDelete(selectedTable.id)} className="text-red-400 hover:text-red-300 text-xs font-bold flex items-center gap-1 hover:bg-red-900/20 px-3 py-1.5 rounded-lg transition-colors">
                <Trash2 size={14} /> Excluir Mesa
              </button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
