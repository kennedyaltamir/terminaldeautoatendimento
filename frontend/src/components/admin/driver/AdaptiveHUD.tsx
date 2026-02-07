/**
 * DOMAIN: FRONTEND / UI
 * COMPONENT: AdaptiveHUD
 * OBJECTIVE: Layout responsivo com Pruning (colapso) e Acessibilidade.
 */
import React, { useState, useEffect } from 'react';
import { useMediaQuery } from '@/hooks/useMediaQuery'; // Hook utilitário
import { motion, AnimatePresence } from 'framer-motion';
import { Wallet, AlertTriangle } from 'lucide-react';

interface AdaptiveHUDProps {
  earnings: number;
  isStealth: boolean;
  notifications: any[];
}

export default function AdaptiveHUD({ earnings, isStealth, notifications }: AdaptiveHUDProps) {
  // 📱 Adaptive Pruning: Detecta viewports ultra-compactas (<360px)
  const isCompact = useMediaQuery('(max-width: 360px)');
  const [highContrast, setHighContrast] = useState(false);

  // ♿ Fallback de Acessibilidade: Detecção de preferência de movimento
  const prefersReducedMotion = useMediaQuery('(prefers-reduced-motion: reduce)');

  return (
    <div 
      className={`relative z-10 transition-all ${highContrast ? 'grayscale contrast-125' : ''}`}
      role="region" 
      aria-label="Painel Financeiro e Status"
    >
      <AnimatePresence mode="wait">
        {isCompact ? (
          // 🔽 Layout Colapsado (Pruning)
          <motion.div 
            key="compact"
            layout
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center justify-between bg-slate-900/90 p-2 rounded-xl border border-slate-700"
          >
            <Wallet size={20} className="text-emerald-500" />
            <span className="font-mono font-bold text-white">
              {isStealth ? '****' : `R$ ${earnings.toFixed(0)}`}
            </span>
          </motion.div>
        ) : (
          // 🔼 Layout Completo
          <motion.div 
            key="full"
            layout
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: prefersReducedMotion ? 0 : 0.3 }}
            className="bg-slate-900/50 backdrop-blur-xl p-4 rounded-3xl border border-white/10 shadow-2xl"
          >
            {/* Conteúdo completo do Widget Financeiro */}
            <div className="flex justify-between items-center">
               <div>
                 <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                   Rendimento Atual
                 </p>
                 <h2 className="text-3xl font-black text-white tracking-tighter">
                   {isStealth ? <span className="blur-sm select-none">R$ 850,00</span> : `R$ ${earnings.toFixed(2)}`}
                 </h2>
               </div>
               {/* Badge de Acessibilidade Visual */}
               <button 
                 onClick={() => setHighContrast(!highContrast)}
                 className="p-2 bg-slate-800 rounded-full text-xs text-slate-400"
                 aria-label="Alternar Alto Contraste"
               >
                 👁️
               </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 🚨 Área de Notificações Críticas (ARIA Live Region) */}
      <div aria-live="assertive" className="sr-only">
        {notifications.map(n => n.message).join(', ')}
      </div>
    </div>
  );
}