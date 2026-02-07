"use client";
import React from "react";
import { ShieldAlert, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

export default function AlertPanel({ alerts = [] }: { alerts: any[] }) {
  if (alerts.length === 0) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative group cursor-pointer"
    >
      <div className="absolute -inset-1 bg-gradient-to-r from-red-600 to-orange-600 rounded-[2rem] blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200 animate-pulse"></div>
      <div className="relative bg-slate-900 border border-red-500/50 p-6 rounded-[2rem] flex items-center justify-between shadow-2xl">
        <div className="flex items-center gap-5">
          <div className="bg-red-500 p-3 rounded-2xl text-white shadow-[0_0_20px_rgba(239,68,68,0.4)]">
            <ShieldAlert size={24} />
          </div>
          <div>
            <h4 className="text-red-400 text-[10px] font-black uppercase tracking-[0.2em] mb-1">Alerta Crítico</h4>
            <p className="text-white font-bold text-sm">{alerts[0].msg}</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-slate-400 group-hover:text-white transition-colors font-bold text-xs uppercase tracking-widest">
          Detalhar <ArrowRight size={16} />
        </div>
      </div>
    </motion.div>
  );
}
