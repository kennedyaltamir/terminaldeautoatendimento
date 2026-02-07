/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.6.0 (Sovereign Logout Edition)
 * DNA_ID: MF-HEADER-VITALS-V2-6
 * OBJETIVO: Header com rito de saída completo (Modal -> Cleanup -> Login).
 */
"use client";
import React, { useState } from 'react';
import { 
  Battery, Signal, User, X, LogOut, 
  Play, Square, Loader2, AlertTriangle 
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { removeTokens } from '@/lib/auth';
import Modal from '@/components/ui/Modal';

interface HeaderVitalsProps {
  fsmState: string;
  batteryLevel: number;
  gpsSignal: string;
  isPendingSync: boolean;
  onStartShift: (vId: string) => Promise<void>;
  onEndShift: () => void;
}

export default function HeaderVitals({ 
  fsmState, 
  batteryLevel, 
  gpsSignal, 
  onStartShift,
  onEndShift 
}: HeaderVitalsProps) {
  const router = useRouter();
  const [showProfile, setShowProfile] = useState(false);
  const [showExitModal, setShowExitModal] = useState(false);
  const [isStarting, setIsStarting] = useState(false);

  const isOffline = fsmState === 'OFFLINE';
  
  const stateColor = {
    'OFFLINE': 'bg-slate-600',
    'IDLE': 'bg-emerald-500 shadow-[0_0_10px_#10b981]',
    'EN_ROUTE_DELIVERY': 'bg-orange-500 animate-pulse',
    'AT_DESTINATION': 'bg-purple-500',
    'INCIDENT_LOCKED': 'bg-red-500'
  }[fsmState] || 'bg-slate-500';

  const handleStart = async () => {
    setIsStarting(true);
    await onStartShift("MOTO-01");
    setIsStarting(false);
  };

  /** 🛡️ RITO SOBERANO DE LOGOUT */
  const handleFullLogout = () => {
    setShowExitModal(false);
    onEndShift(); // Finaliza Shift na FSM
    removeTokens(); // Limpa Cookies e LocalStorage
    router.push('/admin/login'); // Redireciona
  };

  return (
    <>
      <header className="fixed top-0 left-0 w-full h-20 bg-black/40 backdrop-blur-xl border-b border-white/5 flex justify-between items-center px-4 z-[100]">
        <div className="flex items-center gap-3">
          {/* Perfil & Status */}
          <button 
            onClick={() => setShowProfile(true)}
            className="relative active:scale-95 transition-transform"
          >
            <div className="bg-slate-800 p-2.5 rounded-2xl text-slate-400 border border-white/5">
              <User size={22} />
            </div>
            <div className={cn(
                "absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-black",
                stateColor
            )} />
          </button>

          {/* ⚡ BOTÃO DE TURNO MIGRADO */}
          <div className="h-10 w-[1px] bg-white/10 mx-1" />
          
          <AnimatePresence mode="wait">
            {isOffline ? (
              <motion.button
                key="start-btn"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                onClick={handleStart}
                disabled={isStarting}
                className="bg-orange-600 hover:bg-orange-500 text-white px-5 py-2.5 rounded-2xl font-black text-[10px] uppercase tracking-widest flex items-center gap-2 shadow-lg shadow-orange-900/20 active:scale-95 transition-all"
              >
                {isStarting ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} fill="currentColor" />}
                Iniciar Turno
              </motion.button>
            ) : (
              <motion.button
                key="stop-btn"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                onClick={onEndShift}
                className="bg-slate-800 hover:bg-red-900/40 text-slate-300 hover:text-red-400 px-5 py-2.5 rounded-2xl font-black text-[10px] uppercase tracking-widest flex items-center gap-2 border border-white/5 transition-all active:scale-95"
              >
                <Square size={12} fill="currentColor" />
                Parar
              </motion.button>
            )}
          </AnimatePresence>
        </div>

        {/* Vitals Info */}
        <div className="flex items-center gap-5 text-slate-500">
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-1.5">
              <Signal size={14} className={gpsSignal === 'LOST' ? 'text-red-500' : 'text-emerald-500'} />
              <span className="text-[10px] font-black uppercase text-slate-300">{gpsSignal}</span>
            </div>
            <div className="flex items-center gap-1.5 mt-0.5">
              <Battery size={14} className={batteryLevel < 0.2 ? 'text-red-500' : 'text-slate-500'} />
              <span className="text-[10px] font-bold">{Math.round(batteryLevel * 100)}%</span>
            </div>
          </div>
        </div>
      </header>

      {/* 🛑 MODAL DE CONFIRMAÇÃO DE SAÍDA */}
      <Modal isOpen={showExitModal} onClose={() => setShowExitModal(false)} title="ENCERRAR TURNO?">
        <div className="space-y-6">
          <div className="bg-red-500/10 border border-red-500/20 p-5 rounded-2xl flex gap-4">
            <AlertTriangle className="text-red-500 shrink-0" size={24} />
            <p className="text-sm text-slate-300 font-medium leading-relaxed">
              Ao sair, você deixará de receber novas missões e o rastreamento GPS será finalizado. Confirma encerramento?
            </p>
          </div>
          <div className="flex gap-3">
            <button 
              onClick={() => setShowExitModal(false)}
              className="flex-1 py-4 bg-slate-900 text-slate-400 font-black uppercase text-xs rounded-xl hover:text-white transition-colors"
            >
              Cancelar
            </button>
            <button 
              onClick={handleFullLogout}
              className="flex-[2] py-4 bg-red-600 text-white font-black uppercase text-xs rounded-xl shadow-lg shadow-red-900/20 hover:bg-red-500 transition-all active:scale-95"
            >
              Confirmar Saída
            </button>
          </div>
        </div>
      </Modal>

      {/* Perfil Sidebar */}
      <AnimatePresence>
        {showProfile && (
          <>
            <motion.div 
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setShowProfile(false)}
              className="fixed inset-0 bg-black/80 z-[200] backdrop-blur-sm"
            />
            <motion.div 
              initial={{ x: '-100%' }} animate={{ x: 0 }} exit={{ x: '-100%' }}
              className="fixed inset-y-0 left-0 w-80 bg-slate-950 z-[201] p-8 border-r border-white/10 shadow-2xl flex flex-col"
            >
              <div className="flex justify-between items-center mb-12">
                <h2 className="text-2xl font-black text-white tracking-tighter uppercase">Painel Driver</h2>
                <button onClick={() => setShowProfile(false)} className="text-slate-500 hover:text-white transition-colors">
                  <X />
                </button>
              </div>
              
              <div className="flex-1 space-y-8">
                <div className="flex items-center gap-4 p-5 bg-slate-900 rounded-[2rem] border border-white/5 shadow-inner">
                  <div className="w-16 h-16 bg-gradient-to-br from-orange-600 to-red-600 rounded-full flex items-center justify-center text-white text-2xl font-black shadow-lg">
                    M
                  </div>
                  <div>
                    <p className="text-white font-bold text-lg leading-tight">Admin Master</p>
                    <p className="text-[10px] text-slate-500 uppercase font-black tracking-widest mt-1">ID: #8829</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                   <p className="text-[10px] font-black text-slate-600 uppercase tracking-[0.2em] px-2">Dispositivo & Hardware</p>
                   <div className="bg-slate-900/50 p-6 rounded-3xl border border-white/5 space-y-4">
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-slate-500 font-medium">Veículo Ativo</span>
                        <span className="text-white font-black tracking-wider">MOTO-01</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-slate-500 font-medium">Soberania Kernel</span>
                        <span className="text-emerald-500 font-mono text-[10px]">v24.0.1-GM</span>
                      </div>
                  </div>
                </div>
              </div>

              <button 
                onClick={() => { onEndShift(); setShowProfile(false); }}
                className="w-full py-5 bg-red-600/10 hover:bg-red-600 text-red-500 hover:text-white rounded-2xl font-black uppercase text-xs tracking-[0.2em] transition-all flex items-center justify-center gap-3 border border-red-600/20 active:scale-95"
              >
                <LogOut size={18} /> Encerrar Turno
              </button>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}