"use client";

import { Search, ArrowUp, ArrowDown } from "lucide-react";
import { cn } from "@/lib/utils";

export type SortOption = 'name' | 'role' | 'status';
export type SortDirection = 'asc' | 'desc';
export type FilterStatus = 'all' | 'active' | 'inactive';

interface TeamFiltersProps {
  searchTerm: string;
  onSearchChange: (term: string) => void;
  filterStatus: FilterStatus;
  onFilterChange: (status: FilterStatus) => void;
  sortBy: SortOption;
  sortDirection: SortDirection;
  onSortChange: (option: SortOption) => void;
  onNewMember: () => void;
}

export default function TeamFilters({
  searchTerm,
  onSearchChange,
  filterStatus,
  onFilterChange,
  sortBy,
  sortDirection,
  onSortChange,
  onNewMember
}: TeamFiltersProps) {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-center gap-3 w-full">
        <div className="relative flex-1 w-full group">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-orange-500 transition-colors" size={18} />
          <input 
            type="text" 
            placeholder="Buscar por nome, email ou função..." 
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:ring-2 focus:ring-orange-500 outline-none transition-all placeholder:text-slate-600"
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            aria-label="Buscar membros da equipe"
          />
        </div>
        <button 
          onClick={onNewMember}
          className="w-full sm:w-auto bg-orange-600 hover:bg-orange-700 text-white px-6 py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-lg shadow-orange-900/20 active:scale-95 whitespace-nowrap focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-black"
          aria-label="Adicionar novo membro"
        >
          + Novo Membro
        </button>
      </div>

      <div className="flex flex-col md:flex-row gap-6 justify-between items-end">
        <div 
          className="flex flex-wrap gap-2 bg-slate-900 p-1 rounded-xl border border-slate-800"
          role="group" 
          aria-label="Filtros de status"
        >
          {(['all', 'active', 'inactive'] as const).map((status) => (
            <button
              key={status}
              onClick={() => onFilterChange(status)}
              aria-pressed={filterStatus === status}
              className={cn(
                "px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all focus:outline-none focus:ring-2 focus:ring-slate-500",
                filterStatus === status 
                  ? "bg-slate-800 text-white shadow-sm ring-1 ring-slate-700" 
                  : "text-slate-500 hover:text-slate-300"
              )}
            >
              {status === 'all' ? 'Todos' : status === 'active' ? 'Ativos' : 'Inativos'}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-bold text-slate-500 uppercase" id="sort-label">Ordenar:</span>
          <div 
            className="flex bg-slate-900 rounded-xl border border-slate-800 p-1"
            role="group"
            aria-labelledby="sort-label"
          >
            {(['name', 'role', 'status'] as const).map((opt) => (
              <button
                key={opt}
                onClick={() => onSortChange(opt)}
                aria-label={`Ordenar por ${opt} ${sortBy === opt ? (sortDirection === 'asc' ? 'decrescente' : 'crescente') : ''}`}
                className={cn(
                  "px-3 py-1.5 rounded-lg text-[10px] font-black uppercase transition-all flex items-center gap-1 focus:outline-none focus:ring-2 focus:ring-slate-500",
                  sortBy === opt ? "bg-slate-800 text-orange-500" : "text-slate-500 hover:text-slate-300"
                )}
              >
                {opt === 'name' ? 'Nome' : opt === 'role' ? 'Cargo' : 'Status'}
                {sortBy === opt && (
                  sortDirection === 'asc' ? <ArrowUp size={10} /> : <ArrowDown size={10} />
                )}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
