/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Incident Reporting Protocol with High-Stress UX.
 * DNA_ID: MF-INCIDENT-MODAL-V3
 */
"use client";
import React from "react";
import { AlertTriangle, UserX, MapPinOff, ShieldAlert, Wrench, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";

interface DriverIncidentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onReport: (reason: string) => void;
}

export default function DriverIncidentModal({ isOpen, onClose, onReport }: DriverIncidentModalProps) {
  const reasons = [
    { 
      id: "CLIENT_ABSENT", 
      label: "Cliente Ausente", 
      desc: "Ninguém atende no local",
      icon: UserX,
      color: "text-orange-500",
      bg: "bg-orange-500/10 border-orange-500/20"
    },
    { 
      id: "WRONG_ADDRESS", 
      label: "Endereço Errado", 
      desc: "Localização não bate",
      icon: MapPinOff,
      color: "text-yellow-500",
      bg: "bg-yellow-500/10 border-yellow-500/20"
    },
    { 
      id: "MECHANICAL", 
      label: "Problema Mecânico", 
      desc: "Pneu furado / Moto quebrou",
      icon: Wrench,
      color: "text-slate-400",
      bg: "bg-slate-800 border-slate-700"
    },
    { 
      id: "SECURITY", 
      label: "Risco de Segurança", 
      desc: "Área de risco / Ameaça",
      icon: ShieldAlert,
      color: "text-red-500",
      bg: "bg-red-500/10 border-red-500/20"
    },
  ];

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[9999] flex items-end sm:items-center justify-center bg-red-950/90 backdrop-blur-md p-4">
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-slate-950 w-full max-w-md rounded-[2.5rem] border-2 border-red-900/50 shadow-2xl overflow-hidden relative"
          >
            {/* Header de Alerta */}
            <div className="bg-red-900/20 p-6 border-b border-red-900/30 flex justify-between items-center">
              <div className="flex items-center gap-3">
                <div className="bg-red-600 p-2 rounded-xl animate-pulse shadow-lg shadow-red-900/40">
                  <AlertTriangle className="text-white" size={24} />
                </div>
                <div>
                  <h2 className="text-xl font-black text-white uppercase tracking-tight">Reportar Problema</h2>
                  <p className="text-[10px] font-bold text-red-400 uppercase tracking-widest">SLA Pausado Imediatamente</p>
                </div>
              </div>
              <button onClick={onClose} className="p-2 bg-slate-900 rounded-full text-slate-400 hover:text-white transition-colors">
                <X size={20} />
              </button>
            </div>

            <div className="p-6 space-y-4">
              <p className="text-sm text-slate-400 font-medium leading-relaxed">
                Selecione o motivo para alertar a base. A equipe de suporte entrará em contato.
              </p>
              <div className="grid grid-cols-1 gap-3">
                {reasons.map((r) => (
                  <button
                    key={r.id}
                    onClick={() => onReport(r.label)}
                    className={cn(
                      "flex items-center gap-4 p-4 rounded-2xl border transition-all active:scale-95 text-left group hover:bg-white/5",
                      r.bg
                    )}
                  >
                    <div className={cn("p-3 rounded-xl bg-black/20", r.color)}>
                      <r.icon size={24} />
                    </div>
                    <div>
                      <span className="block text-sm font-black text-white uppercase tracking-wide">{r.label}</span>
                      <span className="text-xs text-slate-400 group-hover:text-slate-300">{r.desc}</span>
                    </div>
                  </button>
                ))}
              </div>
              <button 
                onClick={onClose}
                className="w-full py-4 bg-slate-900 text-slate-500 font-bold text-xs uppercase tracking-widest rounded-xl border border-slate-800 mt-2 hover:bg-slate-800 hover:text-white transition-colors"
              >
                Cancelar e Voltar
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
