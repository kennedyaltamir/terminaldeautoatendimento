"use client";

import React, { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { Delete, Send, ShieldCheck, Loader2 } from "lucide-react";
import { sensory } from "@/lib/SensoryEngine";
import { toast } from "sonner";

interface PodViewProps {
    onSubmit: (code: string) => Promise<{ success: boolean; message?: string }>;
    onIncident: () => void;
    debugCode?: string;
}

export default function PodView({ onSubmit, onIncident, debugCode }: PodViewProps) {
    const [code, setCode] = useState("");
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState(false);

    const handleKey = useCallback((num: string) => {
        if (code.length < 4 && !isProcessing) {
            setCode(prev => prev + num);
            setError(false);
            sensory.vibrate('CLICK');
        }
    }, [code, isProcessing]);

    const handleClear = () => {
        if (isProcessing) return;
        setCode("");
        setError(false);
        sensory.vibrate('CLICK');
    };

    const handleSubmit = async () => {
        if (code.length !== 4 || isProcessing) return;
        setIsProcessing(true);
        setError(false);
        
        const result = await onSubmit(code);
        if (result && result.success) {
            sensory.play('success');
            // O componente pai lidará com a transição de estado
        } else {
            setError(true);
            setIsProcessing(false);
            sensory.vibrate('ERROR');
            toast.error(result?.message || "Erro de validação.");
            if (navigator.vibrate) navigator.vibrate([100, 50, 100]);
        }
    };

    return (
        <div className="h-full flex flex-col justify-between p-6 bg-slate-950">
            <div className="text-center pt-10">
                <div className="flex justify-center mb-4">
                    <div className="bg-orange-500/10 p-3 rounded-2xl border border-orange-500/20">
                        <ShieldCheck className="text-orange-500" size={32} />
                    </div>
                </div>
                <h2 className="text-3xl font-black uppercase text-white tracking-tighter">Fim da Rota</h2>
                <p className="text-slate-500 text-sm mt-2">Peça o código de confirmação ao cliente</p>
                
                {/* 🛡️ REVEALER: Código em destaque para ambiente de teste */}
                {debugCode && (
                    <motion.div 
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="mt-6 bg-emerald-500/10 border border-emerald-500/40 p-4 rounded-3xl"
                    >
                        <p className="text-[10px] font-black text-emerald-500 uppercase tracking-widest mb-1">Validação Master</p>
                        <p className="text-4xl font-mono font-black text-white tracking-[0.4em]">{debugCode}</p>
                    </motion.div>
                )}

                <div className="flex justify-center gap-4 mt-12">
                    {[...Array(4)].map((_, i) => (
                        <motion.div 
                            key={i} 
                            animate={error ? { x: [-5, 5, -5, 5, 0] } : {}}
                            className={`w-14 h-20 rounded-2xl border-2 flex items-center justify-center text-4xl font-black transition-all ${
                                error ? 'border-red-500 text-red-500 bg-red-500/10' : 
                                code[i] ? 'border-orange-500 text-white bg-orange-500/10 shadow-[0_0_20px_rgba(234,88,12,0.3)]' : 
                                'border-slate-800 text-slate-800'
                            }`}
                        >
                            {code[i] || "•"}
                        </motion.div>
                    ))}
                </div>
            </div>

            <div className="space-y-6 mb-8">
                <div className="grid grid-cols-3 gap-4">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => (
                        <button key={n} disabled={isProcessing} onClick={() => handleKey(n.toString())} className="h-20 bg-slate-900 rounded-3xl text-2xl font-black text-white active:bg-orange-600 border border-slate-800 disabled:opacity-50">
                            {n}
                        </button>
                    ))}
                    <button onClick={handleClear} disabled={isProcessing} className="h-20 text-red-500 font-black uppercase text-[10px] flex flex-col items-center justify-center gap-1 active:scale-95 transition-transform disabled:opacity-50">
                        Limpar
                    </button>
                    <button onClick={() => handleKey("0")} disabled={isProcessing} className="h-20 bg-slate-900 rounded-3xl text-2xl font-black text-white active:bg-orange-600 border border-slate-800 disabled:opacity-50">0</button>
                    <button onClick={onIncident} disabled={isProcessing} className="h-20 flex items-center justify-center text-yellow-500 bg-yellow-500/5 rounded-3xl border border-yellow-500/20 font-black disabled:opacity-50">!</button>
                </div>

                <button 
                    disabled={code.length < 4 || isProcessing}
                    onClick={handleSubmit}
                    className="w-full py-6 bg-emerald-600 disabled:bg-slate-800 disabled:text-slate-600 text-white rounded-[2rem] font-black text-lg uppercase tracking-[0.2em] shadow-2xl transition-all active:scale-95 flex items-center justify-center gap-3"
                >
                    {isProcessing ? <Loader2 className="animate-spin" /> : <Send size={24} />}
                    CONCLUIR ENTREGA
                </button>
            </div>
        </div>
    );
}
