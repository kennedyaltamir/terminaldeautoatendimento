"use client";
import React from 'react';
import { Zap, RotateCcw, Info } from 'lucide-react';
import { formatCurrency } from '@/lib/utils';

export default function ScenarioSimulator({ simulation, setSimulation, baseRevenue }: any) {
  const projectedValue = baseRevenue * simulation.ticketMultiplier * simulation.volumeMultiplier;

  return (
    <div className="bg-slate-900/80 border border-slate-800 p-8 rounded-[2.5rem] backdrop-blur-xl shadow-2xl">
      <div className="flex justify-between items-center mb-8">
        <h3 className="text-white font-black text-xs uppercase tracking-widest flex items-center gap-2">
          <Zap size={16} className="text-orange-500" /> Simulador What-If
        </h3>
        <button 
          onClick={() => setSimulation({ ticketMultiplier: 1, volumeMultiplier: 1, deliveryShare: 0.65 })}
          className="text-slate-500 hover:text-white transition-colors"
        >
          <RotateCcw size={14} />
        </button>
      </div>

      <div className="space-y-8">
        <div className="space-y-4">
          <div className="flex justify-between items-end">
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Ticket Médio</span>
            <span className="text-orange-500 font-mono font-bold">x{simulation.ticketMultiplier.toFixed(2)}</span>
          </div>
          <input 
            type="range" min="0.5" max="2" step="0.05" 
            value={simulation.ticketMultiplier}
            onChange={(e) => setSimulation({...simulation, ticketMultiplier: parseFloat(e.target.value)})}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-orange-500"
          />
        </div>

        <div className="space-y-4">
          <div className="flex justify-between items-end">
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Volume de Pedidos</span>
            <span className="text-orange-500 font-mono font-bold">x{simulation.volumeMultiplier.toFixed(2)}</span>
          </div>
          <input 
            type="range" min="0.5" max="3" step="0.1" 
            value={simulation.volumeMultiplier}
            onChange={(e) => setSimulation({...simulation, volumeMultiplier: parseFloat(e.target.value)})}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-orange-500"
          />
        </div>

        <div className="pt-6 border-t border-slate-800">
          <p className="text-[10px] font-black text-slate-500 uppercase mb-2">Resultado Projetado</p>
          <p className="text-3xl font-black text-white tracking-tighter">
            {formatCurrency(projectedValue)}
          </p>
        </div>
      </div>
    </div>
  );
}
