"use client";

import React from "react";
import { Clock, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";
import { AuditEvent } from "@/types";

const MOCK_HISTORY: AuditEvent[] = [
  { id: 1, action: "update", field: "role", old: "waiter", new: "manager", user: "Admin Zé", date: "2026-01-27T10:30:00" },
  { id: 2, action: "update", field: "password", old: "***", new: "***", user: "Admin Zé", date: "2026-01-26T18:45:00" },
  { id: 3, action: "create", field: "all", old: null, new: "created", user: "Admin Zé", date: "2026-01-25T09:00:00" },
];

interface AuditTimelineProps {
  employeeId: number;
}

export default function AuditTimeline({ employeeId }: AuditTimelineProps) {
  return (
    <div className="space-y-6 py-2 animate-in fade-in duration-500">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2 text-xs font-black text-slate-500 uppercase tracking-[0.2em]">
          <Clock size={14} className="text-orange-500" /> Histórico Operacional
        </div>
        <span className="text-[9px] bg-slate-900 border border-slate-800 px-2 py-1 rounded text-slate-500 font-mono">
          ID: {employeeId}
        </span>
      </div>

      <div 
        className="relative border-l-2 border-slate-800 ml-3 space-y-8 pb-4"
        role="list"
        aria-label="Registros de auditoria"
        aria-relevant="additions"
      >
        {MOCK_HISTORY.map((event) => (
          <div key={event.id} className="relative pl-8 group" role="listitem">
            {/* Marcador de Alta Visibilidade */}
            <div className={cn(
              "absolute -left-[11px] top-0 w-5 h-5 rounded-full border-4 border-slate-950 shadow-lg transition-transform group-hover:scale-125",
              event.action === 'create' ? "bg-emerald-500" : "bg-blue-600"
            )} />
            
            <div className="flex flex-col gap-1.5 bg-slate-900/30 p-4 rounded-2xl border border-slate-800/50 hover:border-slate-700 transition-colors">
              <time 
                dateTime={event.date}
                className="text-[10px] font-black font-mono text-slate-500 uppercase tracking-widest"
              >
                {new Date(event.date).toLocaleString('pt-BR', {
                    day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
                })}
              </time>
              
              <div className="text-sm text-slate-300 leading-relaxed">
                <span className="font-black text-white">{event.user}</span>
                {event.action === 'create' && (
                  <span className="text-emerald-400 font-bold"> criou este acesso.</span>
                )}
                {event.action === 'update' && (
                  <>
                    {" modificou "}
                    <span className="font-bold text-orange-400">{event.field}</span>
                    <span className="text-slate-500 mx-1">→</span>
                    <span className="font-bold text-white">{event.new}</span>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-orange-500/5 p-4 rounded-2xl border border-orange-500/20 flex gap-4 items-center shadow-inner">
        <ShieldAlert className="text-orange-500 shrink-0" size={20} />
        <p className="text-[11px] text-orange-200/60 font-medium leading-normal">
          Registros forenses são imutáveis. Em conformidade com protocolos de segurança L7 e LGPD.
        </p>
      </div>
    </div>
  );
}
