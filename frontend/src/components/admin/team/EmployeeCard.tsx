"use client";

import React, { memo, useMemo } from "react";
import { Employee, RoleConfig } from "@/types";
import { Edit2, Trash2, History, AlertTriangle, Lock } from "lucide-react";
import { cn } from "@/lib/utils";

interface EmployeeCardProps {
  employee: Employee;
  roleConfig: RoleConfig; // 🛡️ FIX: Tipagem estrita
  searchTerm: string;
  onEdit: (emp: Employee) => void;
  onHistory: (emp: Employee) => void;
  onRevoke: (id: number, email: string) => void;
}

// Helper memoizado para destacar texto
const HighlightText = memo(({ text, highlight }: { text: string, highlight: string }) => {
  const parts = useMemo(() => {
    if (!highlight.trim()) return [text];
    return text.split(new RegExp(`(${highlight})`, 'gi'));
  }, [text, highlight]);

  return (
    <>
      {parts.map((part, i) => 
        part.toLowerCase() === highlight.toLowerCase() ? (
          <span key={i} className="bg-orange-500/30 text-white rounded px-0.5 font-bold">{part}</span>
        ) : (
          part
        )
      )}
    </>
  );
});

HighlightText.displayName = "HighlightText";

const EmployeeCard = memo(({ employee, roleConfig, searchTerm, onEdit, onHistory, onRevoke }: EmployeeCardProps) => {
  const RoleIcon = roleConfig.icon;
  const initials = employee.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

  return (
    <div 
      className={cn(
        "bg-slate-900 border rounded-2xl p-5 shadow-lg transition-all group relative overflow-hidden flex flex-col",
        "hover:shadow-2xl hover:scale-[1.02] duration-300",
        employee.is_active 
          ? "border-slate-800 hover:border-orange-500/30" 
          : "border-red-900/20 bg-slate-950/50 opacity-70 grayscale-[0.8]"
      )}
      tabIndex={0}
      role="article"
      aria-label={`Cartão de ${employee.name}, cargo ${roleConfig.label}`}
      aria-live="polite" // Anuncia mudanças de estado
    >
      {/* Status Indicator */}
      <div className={cn(
        "absolute top-0 left-0 w-1 h-full transition-colors",
        employee.is_active ? "bg-emerald-500" : "bg-red-500"
      )} />

      <div className="flex justify-between items-start mb-4 pl-2">
        <div 
          className={cn(
            "w-12 h-12 rounded-full flex items-center justify-center font-black text-sm border-2 relative transition-transform group-hover:scale-110",
            employee.is_active 
              ? "bg-slate-800 border-slate-700 text-slate-300" 
              : "bg-red-900/20 border-red-900/30 text-red-500"
          )}
          title={!employee.is_active ? "Usuário Inativo" : employee.email}
        >
          {initials}
          {employee.is_active && (
            <span className="absolute bottom-0 right-0 w-3 h-3 bg-emerald-500 border-2 border-slate-900 rounded-full animate-pulse" />
          )}
        </div>
        
        <div className={cn(
          "px-2.5 py-1 rounded-lg border flex items-center gap-1.5",
          roleConfig.bg
        )}>
          <RoleIcon size={12} className={roleConfig.color} />
          <span className={cn("text-[10px] font-black uppercase tracking-wider", roleConfig.color)}>
            {roleConfig.label}
          </span>
        </div>
      </div>

      <div className="pl-2 flex-1">
        <h3 className="text-lg font-bold text-white truncate">
          <HighlightText text={employee.name} highlight={searchTerm} />
        </h3>
        <p className="text-xs text-slate-500 truncate mb-4" title={employee.email}>
          <HighlightText text={employee.email} highlight={searchTerm} />
        </p>
      </div>

      <div className="pt-4 border-t border-slate-800 flex items-center justify-between mt-auto pl-2">
        <div className="flex items-center gap-2">
          {!employee.is_active && (
            <div className="group/tooltip relative">
              <span className="text-[10px] font-bold text-red-500 flex items-center gap-1 bg-red-950/30 px-2 py-0.5 rounded cursor-help">
                <AlertTriangle size={10} /> INATIVO
              </span>
              <span className="absolute bottom-full left-0 mb-2 hidden group-hover/tooltip:block w-max bg-black text-white text-[10px] p-2 rounded border border-slate-800 z-10 shadow-xl">
                Acesso revogado.
              </span>
            </div>
          )}
        </div>

        <div className="flex gap-1">
          <button 
            onClick={() => onHistory(employee)}
            className="p-2 hover:bg-slate-800 rounded-lg text-slate-500 hover:text-blue-400 transition-colors focus:ring-2 focus:ring-blue-500 outline-none"
            title="Ver Histórico"
            aria-label={`Ver histórico de ${employee.name}`}
          >
            <History size={16} />
          </button>
          <button 
            onClick={() => onEdit(employee)} 
            className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors focus:ring-2 focus:ring-orange-500 outline-none"
            title="Editar"
            aria-label={`Editar ${employee.name}`}
          >
            <Edit2 size={16} />
          </button>
          {employee.role !== 'owner' && (
            <button 
              onClick={() => onRevoke(employee.id, employee.email)} 
              className="p-2 hover:bg-red-900/20 rounded-lg text-slate-600 hover:text-red-500 transition-colors focus:ring-2 focus:ring-red-500 outline-none"
              title={employee.is_active ? "Revogar Acesso" : "Excluir"}
              aria-label={employee.is_active ? `Revogar acesso de ${employee.name}` : `Excluir ${employee.name}`}
            >
              {employee.is_active ? <Lock size={16} /> : <Trash2 size={16} />}
            </button>
          )}
        </div>
      </div>
    </div>
  );
});

EmployeeCard.displayName = "EmployeeCard";
export default EmployeeCard;
