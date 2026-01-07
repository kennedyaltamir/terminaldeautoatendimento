"use client";

import { useEffect, useState, useCallback } from "react";
import { getTablesDashboard, createTable, deleteTable, openTable, closeTable, createTablesBulk } from "@/lib/api";
import { Table } from "@/types";
import { Plus, Trash2, Printer, QrCode, Grid, User, DollarSign, Clock, Copy, Check, Banknote, CreditCard, Key, Lock, ChefHat } from "lucide-react";
import { QRCodeSVG } from "qrcode.react";
import Modal from "@/components/ui/Modal";
import { useTerminology } from "@/hooks/useTerminology";
import { toast, Toaster } from "sonner";

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

export default function TablesPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const terms = useTerminology();
  const [tables, setTables] = useState<TableDashboard[]>([]);
  const [loading, setLoading] = useState(true);

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [selectedTable, setSelectedTable] = useState<TableDashboard | null>(null);

  const [newTableNum, setNewTableNum] = useState("");
  const [bulkStart, setBulkStart] = useState("");
  const [bulkEnd, setBulkEnd] = useState("");
  const [customerName, setCustomerName] = useState("");

  const [copiedId, setCopiedId] = useState<number | null>(null);
  const [printMode, setPrintMode] = useState<'all' | 'single'>('all');

  const fetchTables = useCallback(async () => {
    try {
      const data = await getTablesDashboard(slug);
      setTables(data);
    } catch (error) {
      console.error(error);
      toast.error("Erro ao carregar mesas");
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => { fetchTables(); }, [fetchTables]);

  const handleCreate = async () => {
    if (!newTableNum) return;
    try {
      await createTable(parseInt(newTableNum));
      setNewTableNum(""); setIsCreateModalOpen(false); fetchTables();
      toast.success(`${terms.table} criada!`);
    } catch (e) { toast.error("Erro ao criar"); }
  };

  const handleBulkCreate = async () => {
    if (!bulkStart || !bulkEnd) return;
    try {
      await createTablesBulk(parseInt(bulkStart), parseInt(bulkEnd));
      setBulkStart(""); setBulkEnd(""); setIsCreateModalOpen(false); fetchTables();
      toast.success("Mesas criadas em lote!");
    } catch (e) { toast.error("Erro ao criar em lote"); }
  };

  const handleOpenTable = async () => {
    if (!selectedTable || !customerName) return toast.error("Nome obrigatório");
    try {
      await openTable(selectedTable.id, customerName);
      setCustomerName(""); setSelectedTable(null); fetchTables();
      toast.success("Mesa aberta!");
    } catch (e) { toast.error("Erro ao abrir mesa"); }
  };

  const handleCloseTable = async (method: string) => {
    if (!selectedTable) return;
    if (!confirm(`Confirmar pagamento em ${method.toUpperCase()}?`)) return;
    try {
      await closeTable(selectedTable.id, method);
      setSelectedTable(null); fetchTables();
      toast.success("Mesa liberada!");
    } catch (e) { toast.error("Erro ao fechar mesa"); }
  };

  const handleDelete = async (id: number) => {
    if(confirm("Tem certeza? Isso apagará o histórico desta mesa.")) { 
      await deleteTable(id); 
      setSelectedTable(null);
      fetchTables(); 
      toast.success("Mesa removida");
    }
  };

  const getQrUrl = (table: Table) => {
    if (typeof window === 'undefined') return '';
    return `${window.location.origin}/${slug}/menu?mesa=${table.table_number}&token=${table.qr_token}`;
  };

  const handleCopyUrl = (table: Table) => {
    navigator.clipboard.writeText(getQrUrl(table));
    setCopiedId(table.id);
    setTimeout(() => setCopiedId(null), 2000);
    toast.success("Link copiado!");
  };

  const handlePrint = (mode: 'all' | 'single') => {
    setPrintMode(mode);
    setTimeout(() => window.print(), 500);
  };

  if (loading) return <div className="text-center py-20 text-gray-500">Carregando...</div>;

  return (
    <div className="pb-20">
      <Toaster position="top-right" richColors />

      <div className="space-y-8 print:hidden">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-xl">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <Grid className="text-orange-500" /> Gestão de {terms.tables}
            </h1>
            <p className="text-gray-400 text-sm mt-1">Crie e imprima os códigos para seus clientes.</p>
          </div>
          <div className="flex gap-3">
            <button onClick={() => setIsCreateModalOpen(true)} className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl flex items-center gap-2 font-bold transition-colors shadow-lg shadow-orange-900/20">
              <Plus size={16} /> Nova {terms.table}
            </button>
            <button onClick={() => handlePrint('all')} className="bg-white text-gray-900 px-4 py-2 rounded-xl flex items-center gap-2 font-bold transition-colors hover:bg-gray-100">
              <Printer size={16} /> Imprimir Todos
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {tables.map((table) => {
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
                    <QrCode size={32} className="opacity-20 group-hover:opacity-50 transition-opacity" />
                    <span className="font-medium">Livre</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <Modal isOpen={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} title={`Adicionar ${terms.tables}`}>
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

        <Modal isOpen={!!selectedTable} onClose={() => setSelectedTable(null)} title={`${terms.table} ${selectedTable?.table_number}`}>
          {selectedTable && (
            <div className="space-y-6">
              {selectedTable.status === 'free' ? (
                <div className="bg-gray-900 p-4 rounded-xl border border-gray-700">
                  <p className="text-gray-400 text-sm mb-3">Mesa livre. Deseja abrir manualmente?</p>
                  <div className="flex gap-2">
                    <input 
                      type="text" 
                      className="flex-1 bg-gray-800 border border-gray-600 rounded-lg p-2 text-white outline-none focus:ring-2 focus:ring-orange-500"
                      placeholder={`Nome do ${terms.customer}`}
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

                  <div className="bg-black/40 p-4 rounded-xl border border-white/10">
                    <p className="text-blue-400 text-[10px] font-black uppercase tracking-widest mb-1">TOKEN DE ACESSO:</p>
                    <p className="text-white font-mono text-2xl font-black tracking-[0.3em] text-center">
                        {selectedTable.active_session?.access_pin || "----------"}
                    </p>
                    <p className="text-[9px] text-gray-500 mt-2 text-center italic">Forneça este código se o cliente perder o acesso ao QR Code.</p>
                  </div>

                  <div className="grid grid-cols-3 gap-2 pt-2">
                    <button onClick={() => handleCloseTable('cash')} className="bg-gray-800 hover:bg-green-600 text-gray-300 hover:text-white p-2 rounded-lg flex flex-col items-center gap-1 transition-colors border border-gray-700">
                      <Banknote size={18} /> <span className="text-[10px] font-bold">Dinheiro</span>
                    </button>
                    <button onClick={() => handleCloseTable('card')} className="bg-gray-800 hover:bg-blue-600 text-gray-300 hover:text-white p-2 rounded-lg flex flex-col items-center gap-1 transition-colors border border-gray-700">
                      <CreditCard size={18} /> <span className="text-[10px] font-bold">Cartão</span>
                    </button>
                    <button onClick={() => handleCloseTable('pix')} className="bg-gray-800 hover:bg-purple-600 text-gray-300 hover:text-white p-2 rounded-lg flex flex-col items-center gap-1 transition-colors border border-gray-700">
                      <QrCode size={18} /> <span className="text-[10px] font-bold">Pix</span>
                    </button>
                  </div>
                </div>
              )}

              <div className="border-t border-gray-700 pt-4">
                <div className="flex items-center gap-4 mb-4">
                  <div className="bg-white p-2 rounded-lg">
                    <QRCodeSVG value={getQrUrl(selectedTable)} size={80} />
                  </div>
                  <div className="flex-1 space-y-2">
                    <button 
                      onClick={() => handleCopyUrl(selectedTable)}
                      className={`w-full py-2 rounded-lg text-xs font-bold flex items-center justify-center gap-2 transition-all ${copiedId === selectedTable.id ? 'bg-green-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
                    >
                      {copiedId === selectedTable.id ? <Check size={14}/> : <Copy size={14}/>}
                      {copiedId === selectedTable.id ? "Copiado!" : "Copiar Link"}
                    </button>
                    <button 
                      onClick={() => handlePrint('single')}
                      className="w-full bg-gray-700 text-gray-300 py-2 rounded-lg text-xs font-bold flex items-center justify-center gap-2 hover:bg-gray-600"
                    >
                      <Printer size={14} /> Imprimir QR Code
                    </button>
                  </div>
                </div>
              </div>

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

      {/* HEART OF THE PROJECT: PRINT LAYER */}
      <div id="print-layer" className="hidden print:block fixed inset-0 z-[9999] bg-white w-full h-full overflow-visible">
        <div className="grid grid-cols-2 gap-8 p-8 w-full h-full content-start">
          {(printMode === 'single' && selectedTable ? [selectedTable] : tables).map((table) => (
            <div key={table.id} className="border-4 border-black rounded-[2rem] p-8 flex flex-col items-center justify-center text-center break-inside-avoid page-break-inside-avoid h-[450px] relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-4 bg-black"></div>
              <h2 className="text-5xl font-black mb-2 text-black uppercase tracking-tighter">{terms.table} {table.table_number}</h2>
              <p className="text-lg mb-8 text-gray-600 font-black uppercase tracking-[0.2em]">Escaneie para pedir</p>
              <div className="bg-white p-4 border-4 border-black rounded-2xl">
                <QRCodeSVG value={getQrUrl(table)} size={200} fgColor="#000000" bgColor="#ffffff" />
              </div>
              <div className="mt-8 flex items-center gap-3 text-black font-black">
                <ChefHat size={24} />
                <span className="text-xl tracking-tighter">MesaFlow</span>
              </div>
              <div className="absolute bottom-0 left-0 w-full h-4 bg-black"></div>
            </div>
          ))}
        </div>
      </div>

      <style jsx global>{`
        @media print {
          @page { margin: 0; size: A4 portrait; }
          body > *:not(#print-layer) { display: none !important; }
          #print-layer { display: block !important; position: absolute; top: 0; left: 0; width: 100%; }
          .page-break-inside-avoid { break-inside: avoid; }
        }
      `}</style>
    </div>
  );
}
