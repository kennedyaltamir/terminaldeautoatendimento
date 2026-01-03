"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getTablesDashboard } from "@/lib/api";
import { Table } from "@/types";
import { Search, User, Clock, DollarSign, ChevronRight, Filter, ShoppingBag, Bike } from "lucide-react";
import WaiterBottomNav from "@/components/waiter/WaiterBottomNav";
import { useTerminology } from "@/hooks/useTerminology";
import { Toaster } from "sonner";

interface TableDashboard extends Table {
  status: 'free' | 'occupied' | 'alert';
  active_session?: {
    id: number;
    customer_name: string;
    total_spent: number;
    start_time: string;
  };
}

export default function WaiterTablesPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  const router = useRouter();
  const terms = useTerminology();
  const [tables, setTables] = useState<TableDashboard[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<'all' | 'free' | 'occupied'>('all');

  useEffect(() => {
    getTablesDashboard(slug)
      .then(setTables)
      .finally(() => setLoading(false));
  }, [slug]);

  const filteredTables = tables.filter(t => {
    const matchesSearch = t.table_number.toString().includes(search) || 
                          t.active_session?.customer_name.toLowerCase().includes(search.toLowerCase());
    
    if (filter === 'all') return matchesSearch;
    if (filter === 'free') return matchesSearch && t.status === 'free';
    if (filter === 'occupied') return matchesSearch && (t.status === 'occupied' || t.status === 'alert');
    return matchesSearch;
  });

  const handleTableClick = (table: TableDashboard) => {
    router.push(`/admin/${slug}/waiter/pos/${table.id}`);
  };

  // --- ATUALIZAÇÃO: Redirecionamento Real ---
  const handleQuickOrder = (type: 'delivery' | 'takeout') => {
    router.push(`/admin/${slug}/waiter/pos/quick?mode=${type}`);
  };

  return (
    <>
      <Toaster position="top-center" richColors />
      
      <div className="p-4 bg-gray-900 text-white sticky top-0 z-40 shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-xl font-bold">Salão ({terms.table}s)</h1>
          <div className="flex bg-gray-800 rounded-lg p-1">
            <button onClick={() => setFilter('all')} className={`px-3 py-1 rounded text-xs font-bold ${filter === 'all' ? 'bg-gray-600 text-white' : 'text-gray-400'}`}>Todos</button>
            <button onClick={() => setFilter('free')} className={`px-3 py-1 rounded text-xs font-bold ${filter === 'free' ? 'bg-green-600 text-white' : 'text-gray-400'}`}>Livres</button>
            <button onClick={() => setFilter('occupied')} className={`px-3 py-1 rounded text-xs font-bold ${filter === 'occupied' ? 'bg-red-600 text-white' : 'text-gray-400'}`}>Ocupados</button>
          </div>
        </div>
        
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input 
            type="text" 
            placeholder={`Buscar ${terms.table} ou cliente...`}
            className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-10 pr-4 py-3 text-white focus:ring-2 focus:ring-orange-500 outline-none"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* AÇÕES RÁPIDAS (Links Reais) */}
      <div className="grid grid-cols-2 gap-3 p-4 pb-0">
        <button onClick={() => handleQuickOrder('takeout')} className="bg-orange-50 border border-orange-200 p-3 rounded-xl flex items-center gap-3 active:scale-95 transition-transform">
          <div className="bg-orange-100 p-2 rounded-full text-orange-600"><ShoppingBag size={20}/></div>
          <div className="text-left">
            <p className="text-xs font-bold text-orange-800 uppercase">Venda Balcão</p>
            <p className="text-[10px] text-orange-600">Sem mesa</p>
          </div>
        </button>
        <button onClick={() => handleQuickOrder('delivery')} className="bg-blue-50 border border-blue-200 p-3 rounded-xl flex items-center gap-3 active:scale-95 transition-transform">
          <div className="bg-blue-100 p-2 rounded-full text-blue-600"><Bike size={20}/></div>
          <div className="text-left">
            <p className="text-xs font-bold text-blue-800 uppercase">Novo Delivery</p>
            <p className="text-[10px] text-blue-600">Entrega</p>
          </div>
        </button>
      </div>

      <div className="p-4 grid grid-cols-2 gap-3 pb-24">
        {loading ? (
          <p className="col-span-2 text-center py-10 text-gray-500">Carregando...</p>
        ) : (
          filteredTables.map(table => (
            <button 
              key={table.id}
              onClick={() => handleTableClick(table)}
              className={`p-4 rounded-xl border-2 text-left transition-all active:scale-95 relative overflow-hidden ${
                table.status === 'occupied' || table.status === 'alert'
                  ? 'bg-white border-orange-500 shadow-md' 
                  : 'bg-gray-50 border-gray-200 opacity-80'
              }`}
            >
              <div className="flex justify-between items-start mb-2">
                <span className="text-2xl font-black text-gray-800">{table.table_number}</span>
                {table.status === 'occupied' && <div className="w-3 h-3 bg-orange-500 rounded-full animate-pulse"></div>}
                {table.status === 'alert' && <div className="w-3 h-3 bg-red-500 rounded-full animate-bounce"></div>}
              </div>
              
              {table.active_session ? (
                <div className="space-y-1">
                  <p className="text-sm font-bold text-gray-900 truncate">{table.active_session.customer_name}</p>
                  <p className="text-xs text-gray-500 flex items-center gap-1">
                    <Clock size={12}/> {new Date(table.active_session.start_time).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
                  </p>
                  <p className="text-sm font-bold text-green-600 mt-2">R$ {Number(table.active_session.total_spent).toFixed(2)}</p>
                </div>
              ) : (
                <div className="h-12 flex items-center text-gray-400 text-xs font-medium">
                  Livre
                </div>
              )}
              
              <div className="absolute bottom-2 right-2 text-gray-300">
                <ChevronRight size={20} />
              </div>
            </button>
          ))
        )}
      </div>

      <WaiterBottomNav slug={slug} />
    </>
  );
}