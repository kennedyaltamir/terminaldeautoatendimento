/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.2.0 (Forensic Data Recovery)
 * DNA_ID: MF-DRIVER-IDLE-V2-2
 * Objective: Garantir que a lista de pedidos seja resiliente e o botão de simulação seja atômico.
 */
"use client";
import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
    MapPin, 
    Clock, 
    Zap, 
    Navigation,
    Radar,
    RefreshCw
} from "lucide-react";
import { formatCurrency, cn } from "@/lib/utils";
import HoldButton from "@/components/ui/HoldButton";

interface IdleViewProps {
    orders: any[];
    onAccept: (orderId: string) => Promise<void>;
    onSimulate: () => void;
    onRefresh?: () => void; // 🛡️ NOVO: Refresh Manual
}

export default function IdleView({ orders = [], onAccept, onSimulate, onRefresh }: IdleViewProps) {
    const hasOrders = Array.isArray(orders) && orders.length > 0;

    return (
        <div className="space-y-6 pb-20">
            <div className="flex justify-between items-center px-2">
                <div className="flex items-center gap-3">
                    <div className={cn("w-2 h-2 rounded-full", hasOrders ? "bg-emerald-500 animate-pulse" : "bg-slate-700")} />
                    <span className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">
                        {hasOrders ? `${orders.length} Missões Prontas` : "Varrendo Perímetro..."}
                    </span>
                </div>
                {onRefresh && (
                    <button onClick={onRefresh} className="p-2 text-slate-500 hover:text-white transition-colors">
                        <RefreshCw size={16} />
                    </button>
                )}
            </div>

            <AnimatePresence mode="popLayout">
                {!hasOrders ? (
                    <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="flex flex-col items-center justify-center py-20 text-center"
                    >
                        <div className="relative w-40 h-40 flex items-center justify-center mb-10">
                            <motion.div 
                                animate={{ scale: [1, 2], opacity: [0.2, 0] }}
                                transition={{ duration: 3, repeat: Infinity, ease: "easeOut" }}
                                className="absolute inset-0 bg-orange-500 rounded-full"
                            />
                            <div className="bg-slate-900 p-8 rounded-full border border-orange-500/20 relative z-10 shadow-[0_0_40px_rgba(234,88,12,0.1)]">
                                <Radar size={56} className="text-orange-500 animate-pulse" />
                            </div>
                        </div>
                        
                        <div className="space-y-2">
                            <h3 className="text-white font-black text-2xl uppercase tracking-tighter">Buscando Rotas</h3>
                            <p className="text-slate-500 text-sm font-bold uppercase tracking-widest">
                                Aguardando novas entregas na região.
                            </p>
                        </div>

                        <div className="mt-12 flex flex-col gap-3 w-full max-w-xs">
                            <button 
                                onClick={onSimulate}
                                className="flex items-center justify-center gap-3 px-8 py-5 bg-orange-600 hover:bg-orange-500 text-white rounded-2xl text-xs font-black uppercase tracking-[0.2em] shadow-xl shadow-orange-900/20 transition-all active:scale-95"
                            >
                                <Zap size={16} fill="currentColor" /> Ativar Simulação
                            </button>
                            <p className="text-[9px] text-slate-600 font-bold uppercase">Uso exclusivo para homologação de ritos</p>
                        </div>
                    </motion.div>
                ) : (
                    <div className="grid grid-cols-1 gap-5">
                        {orders.map((order, idx) => (
                            <motion.div 
                                key={order.id}
                                layout
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: idx * 0.05 }}
                                className="bg-slate-900 rounded-[2.5rem] border border-white/10 shadow-2xl p-7 relative overflow-hidden group active:scale-[0.98]"
                            >
                                <div className="flex justify-between items-start mb-6">
                                    <div className="space-y-1">
                                        <div className="flex items-center gap-2">
                                            <span className="px-2 py-0.5 bg-orange-600 text-white text-[9px] font-black rounded-md uppercase">
                                                {order.origin || 'Delivery'}
                                            </span>
                                            <span className="text-[10px] font-mono font-bold text-slate-500">ID: #{order.id.slice(-4).toUpperCase()}</span>
                                        </div>
                                        <h3 className="text-2xl font-black text-white truncate max-w-[220px] tracking-tight">{order.customer_name}</h3>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-3xl font-black text-emerald-400 tabular-nums">{formatCurrency(order.total_amount)}</p>
                                        <p className="text-[9px] text-slate-500 uppercase font-black tracking-widest">Ganhos</p>
                                    </div>
                                </div>

                                <div className="bg-black/40 backdrop-blur-sm p-5 rounded-3xl mb-8 space-y-4 border border-white/5">
                                    <div className="flex items-start gap-4">
                                        <div className="p-2 bg-orange-500/10 rounded-xl">
                                            <MapPin size={20} className="text-orange-500" />
                                        </div>
                                        <p className="text-sm text-slate-300 font-bold leading-relaxed">{order.delivery_address}</p>
                                    </div>
                                    <div className="h-px bg-white/5 w-full" />
                                    <div className="flex items-center gap-4">
                                        <div className="p-2 bg-slate-800 rounded-xl">
                                            <Clock size={18} className="text-slate-400" />
                                        </div>
                                        <p className="text-xs text-slate-400 font-bold uppercase tracking-wider">
                                            Emitido às {new Date(order.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
                                        </p>
                                    </div>
                                </div>

                                <HoldButton 
                                    label="ACEITAR MISSÃO" 
                                    onComplete={() => onAccept(order.id)} 
                                    className="w-full bg-slate-800 py-6" 
                                    color="bg-emerald-600"
                                    duration={1200}
                                    icon={<Navigation size={20} className="fill-current" />}
                                    data-testid="btn-accept-route"
                                />
                            </motion.div>
                        ))}
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
}
