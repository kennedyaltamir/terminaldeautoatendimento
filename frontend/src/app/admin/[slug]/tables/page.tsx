"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { getTablesDashboard, openTable, closeTable, createTable, createTablesBulk, deleteTable, updateTablePositions } from "@/lib/api";
import { Table } from "@/types";
import { Plus, Trash2, Printer, Copy, Check, Grid, QrCode, User, Clock, DollarSign, BellRing, CreditCard, Banknote, Move, Save, Layout } from "lucide-react";
import { QRCodeSVG } from "qrcode.react";
import Modal from "@/components/ui/Modal";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useTerminology } from "@/hooks/useTerminology"; // NOVO

interface TableDashboard extends Table {
  status: 'free' | 'occupied' | 'alert';
  position_x: number;
  position_y: number;
  active_session?: {
    id: number;
    customer_name: string;
    total_spent: number;
    start_time: string;
  };
  service_request?: string;
}

export default function TablesPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const terms = useTerminology(); // Hook de Dicionário
  const [tables, setTables] = useState<TableDashboard[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<"grid" | "map">("grid");
  const [isEditingLayout, setIsEditingLayout] = useState(false);
  
  const [draggedTable, setDraggedTable] = useState<number | null>(null);
  const mapRef = useRef<HTMLDivElement>(null);
  
  const [selectedTable, setSelectedTable] = useState<TableDashboard | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [customerName, setCustomerName] = useState("");
  
  const [newTableNum, setNewTableNum] = useState("");
  const [bulkStart, setBulkStart] = useState("");
  const [bulkEnd, setBulkEnd] = useState("");
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const fetchTables = useCallback(async () => {
    try {
      const data = await getTablesDashboard(slug);
      setTables(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => {
    fetchTables();
  }, [fetchTables]);

  useWebSocket(slug, (data) => {
    if (data.type === "new_order" || data.type === "order_update" || data.type === "waiter_call") {
      fetchTables();
    }
  });

  const handleMouseDown = (e: React.MouseEvent, tableId: number) => {
    if (!isEditingLayout) return;
    setDraggedTable(tableId);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (draggedTable === null || !mapRef.current) return;
    
    const rect = mapRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    
    const clampedX = Math.max(0, Math.min(90, x));
    const clampedY = Math.max(0, Math.min(90, y));

    setTables(prev => prev.map(t => t.id === draggedTable ? { ...t, position_x: clampedX, position_y: clampedY } : t));
  };

  const handleMouseUp = () => {
    setDraggedTable(null);
  };

  const saveLayout = async () => {
    const positions = tables.map(t => ({ id: t.id, x: t.position_x, y: t.position_y }));
    try {
      await updateTablePositions(positions);
      setIsEditingLayout(false);
      alert("Layout salvo com sucesso!");
    } catch (e) {
      alert("Erro ao salvar layout");
    }
  };

  const handleOpenTable = async () => {
    if (!selectedTable || !customerName) return;
    try {
      await openTable(selectedTable.id, customerName);
      setCustomerName("");
      setSelectedTable(null);
      fetchTables();
    } catch (e) { alert("Erro ao abrir " + terms.table.toLowerCase()); }
  };

  const handleCloseTable = async (method: string) => {
    if (!selectedTable) return;
    if (!confirm(`Confirmar pagamento em ${method.toUpperCase()} e liberar ${terms.table.toLowerCase()}?`)) return;
    try {
      await closeTable(selectedTable.id, method);
      setSelectedTable(null);
      fetchTables();
    } catch (e) { alert("Erro ao fechar " + terms.table.toLowerCase()); }
  };

  const handleCreateSingle = async () => {
    if (!newTableNum) return;
    await createTable(parseInt(newTableNum));
    setNewTableNum("");
    setIsCreateModalOpen(false);
    fetchTables();
  };

  const handleCreateBulk = async () => {
    if (!bulkStart || !bulkEnd) return;
    await createTablesBulk(parseInt(bulkStart), parseInt(bulkEnd));
    setBulkStart(""); setBulkEnd(""); setIsCreateModalOpen(false);
    fetchTables();
  };

  const handleDelete = async (id: number) => {
    if(confirm(`Excluir ${terms.table.toLowerCase()}?`)) {
      await deleteTable(id);
      fetchTables();
    }
  };

  const handleCopyUrl = (table: Table) => {
    if (typeof window === 'undefined') return;
    const host = window.location.origin;
    const url = `${host}/${slug}/menu?mesa=${table.table_number}&token=${table.qr_token}`;
    navigator.clipboard.writeText(url);
    setCopiedId(table.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (loading) return <div className="text-center py-20 text-gray-500">Carregando salão...</div>;

  return (
    <div className="space-y-8 pb-20" onMouseUp={handleMouseUp} onMouseMove={handleMouseMove}>
      <div className="print:hidden flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-xl">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Grid className="text-orange-500" /> Mapa de {terms.table}s
          </h1>
          <p className="text-gray-400 text-sm mt-1">Visão geral da operação em tempo real.</p>
        </div>
        <div className="flex gap-3">
          <div className="bg-gray-900 p-1 rounded-lg flex border border-gray-700">
            <button onClick={() => setViewMode("grid")} className={`p-2 rounded-md transition-all ${viewMode === "grid" ? "bg-gray-700 text-white" : "text-gray-400 hover:text-white"}`}><Grid size={20}/></button>
            <button onClick={() => setViewMode("map")} className={`p-2 rounded-md transition-all ${viewMode === "map" ? "bg-gray-700 text-white" : "text-gray-400 hover:text-white"}`}><Layout size={20}/></button>
          </div>
          
          {viewMode === "map" && (
            isEditingLayout ? (
              <button onClick={saveLayout} className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl flex items-center gap-2 font-bold transition-colors text-sm animate-pulse">
                <Save size={16} /> Salvar Layout
              </button>
            ) : (
              <button onClick={() => setIsEditingLayout(true)} className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-xl flex items-center gap-2 font-bold transition-colors text-sm">
                <Move size={16} /> Editar Posições
              </button>
            )
          )}

          <button onClick={() => setIsCreateModalOpen(true)} className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-xl flex items-center gap-2 font-medium transition-colors text-sm">
            <Plus size={16} /> {terms.table}s
          </button>
          <button onClick={() => window.print()} className="bg-white text-gray-900 px-4 py-2 rounded-xl flex items-center gap-2 font-bold transition-colors text-sm hover:bg-gray-100">
            <Printer size={16} /> QR Codes
          </button>
        </div>
      </div>

      {viewMode === "grid" && (
        <div className="print:hidden grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {tables.map((table) => {
            let cardStyle = "bg-white border-gray-200 hover:border-gray-300";
            let statusIcon = <div className="w-3 h-3 rounded-full bg-green-500"></div>;
            let statusText = "Livre";

            if (table.status === 'occupied') {
              cardStyle = "bg-red-50 border-red-200 hover:border-red-300";
              statusIcon = <div className="w-3 h-3 rounded-full bg-red-500"></div>;
              statusText = "Ocupada";
            } else if (table.status === 'alert') {
              cardStyle = "bg-yellow-50 border-yellow-400 ring-2 ring-yellow-400 animate-pulse";
              statusIcon = <BellRing size={16} className="text-yellow-600 animate-bounce" />;
              statusText = table.service_request === 'bill' ? 'Pediu Conta' : 'Chamando';
            }

            return (
              <div 
                key={table.id} 
                onClick={() => setSelectedTable(table)}
                className={`cursor-pointer rounded-xl p-4 border-2 shadow-sm transition-all relative ${cardStyle}`}
              >
                <div className="flex justify-between items-start mb-3">
                  <span className="text-2xl font-black text-gray-800">#{table.table_number}</span>
                  <div className="flex items-center gap-1 text-xs font-bold text-gray-500 uppercase">
                    {statusIcon} {statusText}
                  </div>
                </div>

                {table.active_session ? (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm text-gray-700 font-medium">
                      <User size={14} /> {table.active_session.customer_name}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-500">
                      <Clock size={14} /> {new Date(table.active_session.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                    <div className="mt-2 pt-2 border-t border-gray-200/50 flex items-center gap-1 text-lg font-bold text-gray-900">
                      <DollarSign size={16} className="text-green-600" /> {Number(table.active_session.total_spent).toFixed(2)}
                    </div>
                  </div>
                ) : (
                  <div className="h-20 flex flex-col items-center justify-center text-gray-400 text-xs">
                    <QrCode size={24} className="mb-1 opacity-50" />
                    Toque para abrir
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {viewMode === "map" && (
        <div 
          ref={mapRef}
          className="relative w-full h-[600px] bg-gray-800 rounded-xl border-2 border-gray-700 overflow-hidden shadow-inner bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]"
        >
          {tables.map((table) => {
            let bgColor = "bg-green-500";
            if (table.status === 'occupied') bgColor = "bg-red-500";
            if (table.status === 'alert') bgColor = "bg-yellow-500 animate-pulse";

            return (
              <div
                key={table.id}
                onMouseDown={(e) => handleMouseDown(e, table.id)}
                onClick={() => !isEditingLayout && setSelectedTable(table)}
                className={`absolute w-24 h-24 rounded-full shadow-lg flex flex-col items-center justify-center text-white font-bold transition-transform ${isEditingLayout ? 'cursor-move hover:scale-110 z-50' : 'cursor-pointer hover:scale-105'} ${bgColor}`}
                style={{ 
                  left: `${table.position_x}%`, 
                  top: `${table.position_y}%`,
                  zIndex: draggedTable === table.id ? 100 : 10
                }}
              >
                <span className="text-2xl">{table.table_number}</span>
                {table.active_session && <span className="text-[10px] opacity-80">R$ {Number(table.active_session.total_spent).toFixed(0)}</span>}
              </div>
            );
          })}
          {isEditingLayout && (
            <div className="absolute bottom-4 right-4 bg-black/50 text-white px-4 py-2 rounded-lg text-xs pointer-events-none">
              Modo de Edição: Arraste os itens
            </div>
          )}
        </div>
      )}

      <Modal isOpen={!!selectedTable} onClose={() => setSelectedTable(null)} title={`${terms.table} ${selectedTable?.table_number}`}>
        {selectedTable?.status === 'free' ? (
          <div className="space-y-4">
            <p className="text-gray-500">Este local está livre. Deseja abrir manualmente?</p>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-1">Nome do Cliente</label>
              <input 
                type="text" 
                className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="Ex: João"
                value={customerName}
                onChange={e => setCustomerName(e.target.value)}
                autoFocus
              />
            </div>
            <button onClick={handleOpenTable} className="w-full bg-green-600 text-white py-3 rounded-lg font-bold hover:bg-green-700">
              Abrir {terms.table}
            </button>
            
            <div className="border-t pt-4 mt-4">
              <p className="text-xs text-gray-400 mb-2">Gestão</p>
              <div className="flex gap-2">
                <button 
                  onClick={() => selectedTable && handleCopyUrl(selectedTable)}
                  className={`flex-1 py-2 rounded-lg text-xs font-bold flex items-center justify-center gap-2 transition-all ${copiedId === selectedTable?.id ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                >
                  {copiedId === selectedTable?.id ? <><Check size={14}/> Link Copiado</> : <><Copy size={14}/> Copiar Link</>}
                </button>
                <button onClick={() => selectedTable && handleDelete(selectedTable.id)} className="text-red-500 text-sm flex items-center gap-2 hover:underline p-2">
                  <Trash2 size={14} /> Excluir
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-gray-50 p-4 rounded-xl border border-gray-200">
              <div className="flex justify-between mb-2">
                <span className="text-gray-500">Cliente</span>
                <span className="font-bold">{selectedTable?.active_session?.customer_name}</span>
              </div>
              <div className="flex justify-between mb-2">
                <span className="text-gray-500">Entrada</span>
                <span className="font-bold">{new Date(selectedTable?.active_session?.start_time || "").toLocaleTimeString()}</span>
              </div>
              <div className="flex justify-between text-xl font-black text-gray-900 border-t border-gray-200 pt-2 mt-2">
                <span>Total</span>
                <span>R$ {Number(selectedTable?.active_session?.total_spent).toFixed(2)}</span>
              </div>
            </div>

            {selectedTable?.status === 'alert' && (
              <div className="bg-yellow-50 text-yellow-800 p-3 rounded-lg text-sm font-bold flex items-center gap-2">
                <BellRing size={16} /> O cliente solicitou: {selectedTable.service_request === 'bill' ? 'A Conta' : terms.waiter}
              </div>
            )}

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Receber Pagamento e Liberar</label>
              <div className="grid grid-cols-3 gap-2">
                <button onClick={() => handleCloseTable('cash')} className="flex flex-col items-center justify-center p-3 border rounded-lg hover:bg-green-50 hover:border-green-500 hover:text-green-700 transition-all">
                  <Banknote size={20} />
                  <span className="text-xs font-bold mt-1">Dinheiro</span>
                </button>
                <button onClick={() => handleCloseTable('card')} className="flex flex-col items-center justify-center p-3 border rounded-lg hover:bg-blue-50 hover:border-blue-500 hover:text-blue-700 transition-all">
                  <CreditCard size={20} />
                  <span className="text-xs font-bold mt-1">Cartão</span>
                </button>
                <button onClick={() => handleCloseTable('pix')} className="flex flex-col items-center justify-center p-3 border rounded-lg hover:bg-purple-50 hover:border-purple-500 hover:text-purple-700 transition-all">
                  <QrCode size={20} />
                  <span className="text-xs font-bold mt-1">Pix</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </Modal>

      <Modal isOpen={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} title={`Adicionar ${terms.table}s`}>
        <div className="space-y-6">
          <div>
            <h4 className="font-bold text-sm text-gray-500 mb-2">Individual</h4>
            <div className="flex gap-2">
              <input type="number" className="flex-1 border rounded-lg p-2" placeholder="Nº" value={newTableNum} onChange={e => setNewTableNum(e.target.value)} />
              <button onClick={handleCreateSingle} className="bg-gray-900 text-white px-4 rounded-lg font-bold">Criar</button>
            </div>
          </div>
          <div className="border-t pt-4">
            <h4 className="font-bold text-sm text-gray-500 mb-2">Em Lote</h4>
            <div className="flex gap-2 items-center">
              <input type="number" className="w-20 border rounded-lg p-2" placeholder="De" value={bulkStart} onChange={e => setBulkStart(e.target.value)} />
              <span>até</span>
              <input type="number" className="w-20 border rounded-lg p-2" placeholder="Até" value={bulkEnd} onChange={e => setBulkEnd(e.target.value)} />
              <button onClick={handleCreateBulk} className="flex-1 bg-orange-600 text-white px-4 py-2 rounded-lg font-bold">Gerar</button>
            </div>
          </div>
        </div>
      </Modal>

      <div className="hidden print:block bg-white absolute top-0 left-0 w-full h-full z-[9999]">
        <div className="grid grid-cols-3 gap-4 p-8">
          {tables.map((table) => (
            <div key={table.id} className="border-2 border-black rounded-xl p-6 flex flex-col items-center justify-center text-center break-inside-avoid page-break-inside-avoid aspect-[3/4]">
              <h2 className="text-3xl font-black mb-2 text-black">{terms.table} {table.table_number}</h2>
              <p className="text-sm mb-4 text-gray-600">Escaneie para pedir</p>
              <QRCodeSVG 
                value={`${typeof window !== 'undefined' ? window.location.origin : ''}/${slug}/menu?mesa=${table.table_number}&token=${table.qr_token}`}
                size={180}
              />
            </div>
          ))}
        </div>
      </div>
      
      <style jsx global>{`
        @media print {
          body > *:not(.print\\:block) { display: none !important; }
          body { background: white !important; color: black !important; }
          @page { margin: 0.5cm; size: A4 portrait; }
          .page-break-inside-avoid { break-inside: avoid; }
        }
      `}</style>
    </div>
  );
}