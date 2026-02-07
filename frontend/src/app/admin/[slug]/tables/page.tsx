"use client";
import { useEffect, useState, use, useCallback, useMemo, useRef } from "react";
import { 
  Plus, 
  RefreshCw, 
  Grid, 
  Map as MapIcon, 
  Loader2, 
  Search, 
  Layers,
  Save,
  Siren,
  Printer // Novo ícone
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { getTablesDashboard, createTable, updateTablePositions } from "@/lib/api";
import { TableDashboard } from "@/types";
import { useWebSocket } from "@/hooks/useWebSocket";
import { formatCurrency, cn } from "@/lib/utils";
import TableCard from "@/components/admin/tables/TableCard";
import TableModal from "@/components/admin/tables/TableModal";
import TableBulkModal from "@/components/admin/tables/TableBulkModal";

export default function TablesPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const params = use(paramsPromise);
  const slug = params.slug;
  const constraintsRef = useRef(null);

  const [tables, setTables] = useState<TableDashboard[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'map'>('grid');
  const [filterStatus, setFilterStatus] = useState<'all' | 'free' | 'occupied' | 'alert'>('all');
  const [selectedTable, setSelectedTable] = useState<TableDashboard | null>(null);
  const [isBulkModalOpen, setIsBulkModalOpen] = useState(false);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [isIncidentMode, setIsIncidentMode] = useState(false);

  const fetchTables = useCallback(async (silent: boolean = false) => {
    if (!silent) setRefreshing(true);
    try {
      const data = await getTablesDashboard();
      setTables(data);
    } catch (e) {
      toast.error("Falha na sincronização das mesas.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchTables();
  }, [fetchTables]);

  useWebSocket(slug, (data) => {
    if (["order_update", "table_update", "waiter_call", "session_closed"].includes(data.type)) {
      fetchTables(true);
    }
  });

  const filteredTables = useMemo(() => {
    return tables.filter(t => {
      if (filterStatus === 'all') return true;
      return t.status === filterStatus;
    });
  }, [tables, filterStatus]);

  const stats = useMemo(() => {
    const occupied = tables.filter(t => t.status === 'occupied').length;
    const totalRevenue = tables.reduce((acc, t) => acc + (t.active_session?.total_spent || 0), 0);
    return { occupied, totalRevenue };
  }, [tables]);

  const handleCreateTable = async () => {
    const nextNumber = tables.length > 0 ? Math.max(...tables.map(t => t.table_number)) + 1 : 1;
    try {
      await createTable({ table_number: nextNumber });
      toast.success(`Mesa ${nextNumber} criada.`);
      fetchTables(true);
    } catch (e) {
      toast.error("Erro ao criar mesa.");
    }
  };

  // Lógica de Drag & Drop
  const handleDragEnd = (id: number, info: any) => {
    setTables(prev => prev.map(t => {
      if (t.id === id) {
        return {
          ...t,
          position_x: (t.position_x || 0) + info.offset.x,
          position_y: (t.position_y || 0) + info.offset.y
        };
      }
      return t;
    }));
    setHasUnsavedChanges(true);
  };

  const savePositions = async () => {
    try {
      const positions = tables.map(t => ({
        id: t.id,
        x: t.position_x || 0,
        y: t.position_y || 0
      }));
      await updateTablePositions(positions);
      toast.success("Layout do salão salvo!");
      setHasUnsavedChanges(false);
    } catch (e) {
      toast.error("Erro ao salvar posições.");
    }
  };

  const handlePrintAll = () => {
    // Abre a página de impressão em uma nova aba
    window.open(`/admin/${slug}/tables/print`, '_blank');
  };

  return (
    <div className={cn(
        "space-y-8 p-4 md:p-8 animate-in fade-in duration-500 min-h-screen transition-colors",
        isIncidentMode ? "bg-red-950/30" : ""
    )}>
      <header className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
        <div>
          <h1 className="text-4xl font-black text-white tracking-tighter flex items-center gap-3">
            <Layers className={isIncidentMode ? "text-red-500 animate-pulse" : "text-orange-500"} size={36} />
            GESTÃO DE <span className={isIncidentMode ? "text-red-500" : "text-orange-500"}>MESAS</span>
          </h1>
          {isIncidentMode && (
              <p className="text-red-400 font-bold text-xs uppercase tracking-widest mt-1 animate-pulse">
                  ⚠️ MODO INCIDENTE ATIVO
              </p>
          )}
        </div>
        <div className="bg-slate-900/50 border border-slate-800 px-6 py-3 rounded-2xl flex items-center gap-4">
          <div className="text-center">
            <p className="text-[10px] font-black text-slate-500 uppercase">Ocupação</p>
            <p className="text-xl font-black text-white">{stats.occupied}/{tables.length}</p>
          </div>
          <div className="w-px h-8 bg-slate-800" />
          <div className="text-center">
            <p className="text-[10px] font-black text-slate-500 uppercase">Em Aberto</p>
            <p className="text-xl font-black text-emerald-500">{formatCurrency(stats.totalRevenue)}</p>
          </div>
        </div>
      </header>

      <div className="flex flex-col md:flex-row justify-between items-center gap-4 bg-slate-900/30 p-4 rounded-[2rem] border border-slate-800/50 backdrop-blur-sm">
        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800">
          {['all', 'free', 'occupied', 'alert'].map((f) => (
            <button
              key={f}
              onClick={() => setFilterStatus(f as any)}
              className={cn(
                "px-4 py-2 rounded-lg text-xs font-black uppercase tracking-widest transition-all",
                filterStatus === f ? "bg-orange-600 text-white shadow-lg" : "text-slate-500 hover:text-slate-300"
              )}
            >
              {f}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          {/* Botão de Impressão em Massa */}
          <button
            onClick={handlePrintAll}
            className="p-3 bg-slate-900 hover:bg-slate-800 rounded-xl text-slate-400 hover:text-white border border-slate-800 transition-all"
            title="Imprimir Todos os QR Codes"
          >
            <Printer size={20} />
          </button>

          {/* Toggle Modo Incidente */}
          <button
            onClick={() => setIsIncidentMode(!isIncidentMode)}
            className={cn(
                "p-3 rounded-xl transition-all border",
                isIncidentMode 
                    ? "bg-red-600 border-red-500 text-white shadow-lg shadow-red-900/50 animate-pulse" 
                    : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
            )}
            title="Modo Incidente (Crise)"
          >
            <Siren size={20} />
          </button>

          {viewMode === 'map' && hasUnsavedChanges && (
            <button 
              onClick={savePositions}
              className="bg-green-600 hover:bg-green-500 text-white px-4 py-2 rounded-xl font-bold text-xs flex items-center gap-2 animate-pulse"
            >
              <Save size={16} /> Salvar Layout
            </button>
          )}
          
          <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800">
            <button 
              onClick={() => setViewMode('grid')} 
              className={cn("p-2 rounded-lg transition-all", viewMode === 'grid' ? "bg-slate-800 text-orange-500" : "text-slate-600")}
              title="Visualização em Grade"
            >
              <Grid size={20} />
            </button>
            <button 
              onClick={() => setViewMode('map')} 
              className={cn("p-2 rounded-lg transition-all", viewMode === 'map' ? "bg-slate-800 text-orange-500" : "text-slate-600")}
              title="Visualização em Mapa (Arrastar)"
            >
              <MapIcon size={20} />
            </button>
          </div>

          <button 
            onClick={() => fetchTables()} 
            className="p-3 bg-slate-900 hover:bg-slate-800 rounded-xl text-slate-400 hover:text-white border border-slate-800 transition-all"
          >
            <RefreshCw size={20} className={cn(refreshing && "animate-spin")} />
          </button>
          
          <button 
            onClick={() => setIsBulkModalOpen(true)} 
            className="bg-slate-100 hover:bg-white text-slate-950 px-6 py-3 rounded-xl font-black uppercase text-xs tracking-widest transition-all active:scale-95"
          >
            Gerar Lote
          </button>
          
          <button 
            onClick={handleCreateTable} 
            className="bg-orange-600 hover:bg-orange-500 text-white px-6 py-3 rounded-xl font-black uppercase text-xs tracking-widest transition-all shadow-lg shadow-orange-900/20 active:scale-95 flex items-center gap-2"
          >
            <Plus size={18} /> Nova Mesa
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-32 gap-4">
          <Loader2 className="animate-spin text-orange-500" size={48} />
          <p className="text-slate-500 font-black uppercase tracking-[0.3em] text-xs">Sincronizando Salão...</p>
        </div>
      ) : (
        <motion.div 
          ref={constraintsRef}
          layout 
          className={cn(
            "relative min-h-[600px] transition-all duration-500", 
            viewMode === 'grid' 
              ? "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6" 
              : "bg-slate-950/50 rounded-[3rem] border-2 border-dashed border-slate-800 p-8 overflow-hidden"
          )}
        >
          {viewMode === 'map' && (
            <div className="absolute inset-0 pointer-events-none opacity-10 bg-[url('/grid-pattern.svg')] bg-center" />
          )}

          <AnimatePresence mode="popLayout">
            {filteredTables.map(table => (
              <motion.div
                key={table.id}
                layout={viewMode === 'grid'}
                drag={viewMode === 'map'}
                dragConstraints={constraintsRef}
                dragMomentum={false}
                onDragEnd={(e, info) => handleDragEnd(table.id, info)}
                initial={viewMode === 'map' ? { x: table.position_x || 0, y: table.position_y || 0 } : { opacity: 0, scale: 0.9 }}
                animate={viewMode === 'map' ? { x: table.position_x || 0, y: table.position_y || 0 } : { opacity: 1, scale: 1 }}
                style={{ 
                  position: viewMode === 'map' ? 'absolute' : 'relative',
                  zIndex: viewMode === 'map' ? 10 : 'auto',
                  width: viewMode === 'map' ? '200px' : 'auto'
                }}
                whileDrag={{ scale: 1.1, zIndex: 50, cursor: 'grabbing' }}
                className={cn(viewMode === 'map' && "cursor-grab")}
              >
                <TableCard 
                  table={table} 
                  slug={slug} 
                  onClick={() => {
                    if (viewMode === 'grid') setSelectedTable(table);
                  }} 
                  onResolveAlert={() => setSelectedTable(table)}
                  isIncidentMode={isIncidentMode}
                />
                {viewMode === 'map' && (
                   <div className="absolute -top-2 -right-2 bg-slate-800 text-white text-[10px] px-2 py-1 rounded-full border border-slate-600 shadow-sm pointer-events-none">
                      x:{Math.round(table.position_x || 0)} y:{Math.round(table.position_y || 0)}
                   </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {filteredTables.length === 0 && (
            <div className="col-span-full flex flex-col items-center justify-center py-32 text-slate-600">
              <Search size={64} className="mb-4 opacity-20" />
              <p className="text-xl font-bold">Nenhuma mesa encontrada.</p>
            </div>
          )}
        </motion.div>
      )}

      {selectedTable && (
        <TableModal 
          isOpen={!!selectedTable}
          table={selectedTable}
          slug={slug}
          onClose={() => setSelectedTable(null)}
          onRefresh={() => fetchTables(true)}
        />
      )}

      <TableBulkModal 
        isOpen={isBulkModalOpen}
        onClose={() => setIsBulkModalOpen(false)}
        onSuccess={() => fetchTables()}
      />

      <style jsx global>{`
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
      `}</style>
    </div>
  );
}
