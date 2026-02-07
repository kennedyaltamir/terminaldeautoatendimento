import React from "react";
import { Clock, MapPin, CheckCircle2, XCircle } from "lucide-react";
import { formatCurrency } from "@/lib/utils";

const MOCK_HISTORY = [
  { id: "ORD-9921", date: "Hoje, 14:30", amount: 12.50, status: "delivered", address: "Av. Paulista, 1000" },
  { id: "ORD-9918", date: "Hoje, 13:15", amount: 8.00, status: "delivered", address: "Rua Augusta, 500" },
  { id: "ORD-9890", date: "Ontem, 20:00", amount: 15.00, status: "canceled", address: "Alameda Santos, 200" },
];

export default function HistoryView() {
  return (
    <div className="p-6 space-y-6 pb-32 pt-20 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h2 className="text-2xl font-black text-white uppercase tracking-tight">Histórico Recente</h2>
      
      <div className="space-y-4">
        {MOCK_HISTORY.map((item) => (
          <div key={item.id} className="bg-slate-900 border border-slate-800 p-5 rounded-3xl flex justify-between items-center group hover:border-orange-500/30 transition-all">
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-black text-slate-500">{item.id}</span>
                <span className="text-[10px] text-slate-600 font-bold uppercase">• {item.date}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-300 text-sm font-bold mb-3">
                <MapPin size={14} className="text-orange-500 shrink-0" />
                <span className="truncate">{item.address}</span>
              </div>
              <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest ${
                item.status === 'delivered' ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'bg-red-500/10 text-red-500 border border-red-500/20'
              }`}>
                {item.status === 'delivered' ? <CheckCircle2 size={10} /> : <XCircle size={10} />}
                {item.status === 'delivered' ? 'Entregue' : 'Cancelado'}
              </div>
            </div>
            <div className="text-right ml-4">
              <p className="text-2xl font-black text-white tracking-tighter">{formatCurrency(item.amount * 100)}</p>
              <p className="text-[9px] text-slate-500 uppercase font-black tracking-widest">Ganho Líquido</p>
            </div>
          </div>
        ))}
      </div>
      
      <div className="py-10 text-center">
        <p className="text-[10px] text-slate-700 font-mono uppercase tracking-[0.3em]">Fim do registro operacional</p>
      </div>
    </div>
  );
}
