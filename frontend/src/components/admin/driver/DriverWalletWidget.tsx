"use client";

import React, { useState, useMemo } from "react";
import { 
  Wallet, TrendingUp, Map, Eye, EyeOff, 
  ChevronDown, ChevronUp, Trophy, 
  Bike, Target, Zap, Coins 
} from "lucide-react";
import { formatCurrency, cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";

interface DriverWalletWidgetProps {
  earnings: number;
  rides: number;
  km: number;
  dailyGoal?: number;
  rank?: number;
  hourlyData?: number[];
  isOffline?: boolean;
}

export default function DriverWalletWidget({ 
  earnings, 
  rides, 
  km, 
  dailyGoal = 30000,
  rank = 3,
  hourlyData = [12, 25, 18, 40, 32, 18, 22],
  isOffline = false
}: DriverWalletWidgetProps) {
  const [isStealth, setIsStealth] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  
  const { progress, isGoalReached, maxHourlyVal, breakdown } = useMemo(() => {
    const currentProgress = Math.min((earnings / dailyGoal) * 100, 100);
    return {
      progress: currentProgress,
      isGoalReached: currentProgress >= 100,
      maxHourlyVal: Math.max(...hourlyData),
      breakdown: {
        fees: earnings * 0.75,
        tips: earnings * 0.20,
        bonus: earnings * 0.05
      }
    };
  }, [earnings, dailyGoal, hourlyData]);

  return (
    <div className={cn(
      "bg-[#000000] border rounded-[2.5rem] p-6 mb-6 shadow-2xl relative overflow-hidden transition-all duration-500",
      isOffline ? "border-slate-800 opacity-60 grayscale" : "border-slate-700 group"
    )}>
      <div className="absolute bottom-0 left-0 right-0 h-24 flex items-end gap-1.5 px-6 opacity-[0.07] pointer-events-none">
        {hourlyData.map((val, i) => (
          <motion.div 
            key={i} 
            initial={{ height: 0 }}
            animate={{ height: `${(val / maxHourlyVal) * 100}%` }}
            className={cn("flex-1 rounded-t-md", isGoalReached ? "bg-emerald-500" : "bg-orange-500")}
          />
        ))}
      </div>

      <div className="relative z-10">
        <div className="flex justify-between items-start mb-6">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Rendimento do Turno</p>
              <button 
                onClick={() => setIsStealth(!isStealth)} 
                data-testid="stealth-toggle"
                className="p-2 text-slate-300 hover:text-white transition-colors active:scale-90"
              >
                {isStealth ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
            <AnimatePresence mode="wait">
              {isStealth ? (
                <motion.div key="stealth" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-10 w-40 bg-slate-900/50 rounded-2xl animate-pulse flex items-center px-4">
                  <div className="flex gap-1">{[...Array(5)].map((_, i) => <div key={i} className="w-2 h-2 bg-slate-700 rounded-full" />)}</div>
                </motion.div>
              ) : (
                <motion.h2 key="value" initial={{ y: 10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="text-5xl font-black text-white tracking-tighter">
                  {formatCurrency(earnings)}
                </motion.h2>
              )}
            </AnimatePresence>
          </div>
          <div className={cn("flex flex-col items-end gap-1 px-4 py-2 rounded-2xl border backdrop-blur-md", rank === 1 ? "bg-yellow-500/10 border-yellow-500/20" : "bg-slate-900 border-slate-800")}>
            <div className="flex items-center gap-2">
              <Trophy size={14} className={rank === 1 ? "text-yellow-500" : "text-slate-400"} />
              <span className="text-xs font-black italic text-white">#{rank}</span>
            </div>
            <span className="text-[8px] font-bold text-slate-500 uppercase tracking-widest">Frota Local</span>
          </div>
        </div>

        <div className="space-y-2 mb-8">
          <div className="flex justify-between items-end">
            <div className="flex items-center gap-1.5 text-[9px] font-black text-slate-400 uppercase tracking-widest">
              <Target size={12} className="text-orange-500" /> Meta: {formatCurrency(dailyGoal)}
            </div>
            <span className={cn("text-xs font-mono font-black", isGoalReached ? "text-emerald-500" : "text-orange-500")}>
              {progress.toFixed(0)}%
            </span>
          </div>
          <div className="h-2 w-full bg-slate-900/50 rounded-full overflow-hidden border border-white/5">
            <motion.div initial={{ width: 0 }} animate={{ width: `${progress}%` }} className={cn("h-full rounded-full", isGoalReached ? "bg-emerald-500" : "bg-orange-600")} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-slate-900/40 backdrop-blur-sm rounded-3xl p-4 border border-white/5 flex items-center gap-4">
            <div className="bg-blue-500/20 p-2.5 rounded-xl text-blue-400"><Bike size={20} /></div>
            <div>
              <p className="text-2xl font-black text-white leading-none">{rides}</p>
              <p className="text-[9px] text-slate-500 uppercase font-black">Entregas</p>
            </div>
          </div>
          <div className="bg-slate-900/40 backdrop-blur-sm rounded-3xl p-4 border border-white/5 flex items-center gap-4">
            <div className="bg-purple-500/20 p-2.5 rounded-xl text-purple-400"><Map size={20} /></div>
            <div>
              <p className="text-2xl font-black text-white leading-none">{km.toFixed(1)}k</p>
              <p className="text-[9px] text-slate-500 uppercase font-black">Percorrido</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
