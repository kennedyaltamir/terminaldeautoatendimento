"use client";
import React from "react";
import Modal from "@/components/ui/Modal";
import { formatCurrency } from "@/lib/utils";
import { ArrowRight } from "lucide-react";

interface DrillDownModalProps {
  data: any;
  isOpen: boolean;
  onClose: () => void;
}

export default function DrillDownModal({ data, isOpen, onClose }: DrillDownModalProps) {
  if (!data) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Detalhamento: ${data.date}`}>
      <div className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <p className="text-[10px] font-black text-slate-500 uppercase mb-1">Faturamento</p>
            <p className="text-xl font-black text-white">{formatCurrency(data.simulatedValue || data.value)}</p>
          </div>
          <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800">
            <p className="text-[10px] font-black text-slate-500 uppercase mb-1">Pedidos</p>
            <p className="text-xl font-black text-white">{data.count || 0}</p>
          </div>
        </div>

        <div className="space-y-2">
          {['Delivery', 'Balcao', 'App'].map((canal) => (
            <div key={canal} className="flex justify-between p-3 bg-slate-900 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400">{canal}</span>
              <span className="text-xs font-bold text-white">{formatCurrency(data[canal] || 0)}</span>
            </div>
          ))}
        </div>

        <button 
          onClick={onClose}
          className="w-full py-4 bg-orange-600 text-white rounded-xl font-black uppercase text-xs flex items-center justify-center gap-2"
        >
          Fechar <ArrowRight size={14} />
        </button>
      </div>
    </Modal>
  );
}
