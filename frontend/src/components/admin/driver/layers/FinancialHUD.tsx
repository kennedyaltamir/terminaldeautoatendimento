import React, { useMemo, useState } from 'react';
import { Eye, EyeOff, Trophy, Target } from 'lucide-react';
import { formatCurrency, cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

interface FinancialHUDProps {
  earnings: number;
  dailyGoal: number;
  rank: number;
}

export default function FinancialHUD({ earnings, dailyGoal, rank }: FinancialHUDProps) {
  const [isStealth, setIsStealth] = useState(false);
  const progress = useMemo(() => Math.min((earnings / dailyGoal) * 100, 100), [earnings, dailyGoal]);

  return (
    <div className="absolute top-20 left-4 right-4 z-20 pointer-events-none">
      <div 
        className="bg-slate-950/80 backdrop-blur-xl border border-white/10 rounded-[2rem] p-5 shadow-2xl pointer-events-auto ring-1 ring-white/5"
        data-testid="financial-hud"
      >
        <div className="flex justify-between items-start mb-3">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Rendimento</p>
              <button 
                onClick={() => setIsStealth(!isStealth)} 
                className="text-slate-500 hover:text-white transition-colors active:scale-90"
                data-testid="stealth-toggle"
              >
                {isStealth ? <EyeOff size={14} /> : <Eye size={14} />}
              </button>
            </div>
            <AnimatePresence mode="wait">
              {isStealth ? (
                <motion.div 
                  key="stealth" 
                  initial={{ opacity: 0 }} 
                  animate={{ opacity: 1 }} 
                  className="h-9 w-32 bg-white/10 rounded-lg animate-pulse mt-1" 
                />
              ) : (
                <motion.h2 
                  key="value" 
                  initial={{ opacity: 0, y: 5 }} 
                  animate={{ opacity: 1, y: 0 }} 
                  className="text-4xl font-black text-white tracking-tighter leading-none"
                  data-testid="financial-hud-value"
                >
                  {formatCurrency(earnings)}
                </motion.h2>
              )}
            </AnimatePresence>
          </div>
          
          <div className="flex flex-col items-end">
            <div className={cn(
              "flex items-center gap-1.5 px-3 py-1.5 rounded-xl border backdrop-blur-md shadow-lg",
              rank === 1 ? "bg-yellow-500/20 border-yellow-500/30 text-yellow-400" : "bg-slate-800/50 border-slate-700 text-slate-300"
            )}>
              <Trophy size={14} />
              <span className="text-xs font-black italic">#{rank}</span>
            </div>
            <span className="text-[8px] font-bold text-slate-500 uppercase tracking-widest mt-1">Ranking Frota</span>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-[10px] font-bold text-slate-400">
            <span className="flex items-center gap-1.5">
              <Target size={12} className="text-orange-500" /> 
              Meta: {formatCurrency(dailyGoal)}
            </span>
            <span className={progress >= 100 ? "text-emerald-400" : "text-orange-400"}>
              {progress.toFixed(0)}%
            </span>
          </div>
          <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-white/5">
            <motion.div 
              className={cn("h-full rounded-full shadow-[0_0_10px_currentColor]", progress >= 100 ? "bg-emerald-500 text-emerald-500" : "bg-orange-500 text-orange-500")} 
              initial={{ width: 0 }} 
              animate={{ width: `${progress}%` }} 
              transition={{ duration: 1.5, ease: "easeOut" }} 
            />
          </div>
        </div>
      </div>
    </div>
  );
}