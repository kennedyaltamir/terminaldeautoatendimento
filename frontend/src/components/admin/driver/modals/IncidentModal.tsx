import React, { useState, useEffect } from 'react';
import { AlertTriangle, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface IncidentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onReport: (reason: string) => Promise<void>;
}

export default function IncidentModal({ isOpen, onClose, onReport }: IncidentModalProps) {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') e.preventDefault();
    };
    if (isOpen) window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  const handleReason = async (reason: string) => {
    setLoading(true);
    await onReport(reason);
    setLoading(false);
    setSuccess(true);
    setTimeout(() => {
      setSuccess(false);
      onClose();
    }, 1500);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9999] bg-red-950/90 backdrop-blur-md flex items-center justify-center p-4">
      <motion.div initial={{ scale: 0.9 }} animate={{ scale: 1 }} className="bg-slate-900 border-2 border-red-500 w-full max-w-md rounded-3xl p-6 shadow-2xl">
        {success ? (
          <div className="text-center py-10">
            <CheckCircle2 size={64} className="text-emerald-500 mx-auto mb-4 animate-bounce" />
            <h2 className="text-2xl font-black text-white uppercase">SLA Pausado</h2>
            <p className="text-slate-400">Suporte notificado.</p>
          </div>
        ) : (
          <>
            <div className="flex items-center gap-3 mb-6 text-red-500">
              <AlertTriangle size={32} />
              <h2 className="text-2xl font-black uppercase tracking-tighter">Reportar Incidente</h2>
            </div>
            <div className="grid grid-cols-1 gap-3">
              {['Pneu Furado', 'Acidente', 'Área de Risco', 'Problema Veículo'].map(reason => (
                <button key={reason} onClick={() => handleReason(reason)} disabled={loading} className="bg-slate-800 hover:bg-red-900/30 text-white p-4 rounded-xl font-bold text-left border border-slate-700 hover:border-red-500 transition-all">
                  {reason}
                </button>
              ))}
            </div>
            <button onClick={onClose} disabled={loading} className="w-full mt-6 py-4 text-slate-500 font-bold uppercase tracking-widest hover:text-white">
              Cancelar
            </button>
          </>
        )}
      </motion.div>
    </div>
  );
}
