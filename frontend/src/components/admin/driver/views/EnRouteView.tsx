/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 26.4.0 (Diamond Hardened - Logic Restored)
 * DNA_ID: MF-ENROUTE-V26-4-GOLD
 * OBJETIVO: Cockpit de navegação profissional com todas as referências e modais integrados.
 * Comportamento esperado: 
 *  1. Mapa dinâmico (35% vs 78% da viewport) via Theater Mode.
 *  2. Todos os modais (Manifesto, Comunicação, Incidente) funcionais.
 *  3. Normalização de dados via missionData para compatibilidade com templates de mensagem.
 *  4. Tipagem estrita de parâmetros para conformidade total com o compilador.
 */
"use client";

import React, { useState, useEffect, useMemo } from 'react';
import dynamic from 'next/dynamic';
import { 
    Maximize2, Minimize2, Navigation, AlertTriangle, 
    Package, MapPin, Gauge, Compass, Info, MessageSquare,
    Locate
} from 'lucide-react';
import { cn, formatCurrency } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';
import { fetchRoute, calculateHaversineDistance } from '@/lib/routing';
import type { MapMode } from '@/components/ui/TrackingMap';

// --- COMPONENTS: OPERATIONAL MODALS ---
import DriverCommunicationModal from '../DriverCommunicationModal';
import DriverIncidentModal from '../DriverIncidentModal';
import OrderManifest from '../OrderManifest';

// Carregamento dinâmico do mapa
const TrackingMap = dynamic(() => import("@/components/ui/TrackingMap"), { 
    ssr: false,
    loading: () => (
        <div className="w-full h-full bg-slate-900 animate-pulse flex flex-col items-center justify-center text-slate-600 font-mono text-xs gap-3">
            <Compass size={32} className="animate-spin text-orange-500" />
            <span className="tracking-[0.3em]">CARREGANDO MAPA...</span>
        </div>
    )
});

interface EnRouteViewProps {
    activeMission: any;
    speed: number;
    onIncident: () => void;
    driverPos: [number, number];
    destPos: [number, number];
}

export default function EnRouteView({ 
    activeMission, 
    speed, 
    onIncident, 
    driverPos, 
    destPos 
}: EnRouteViewProps) {
    // --- UI STATES ---
    const [isMapMinimized, setIsMapMinimized] = useState(false);
    const [isManifestOpen, setIsManifestOpen] = useState(false);
    const [isCommOpen, setIsCommOpen] = useState(false);
    const [isIncidentOpen, setIsIncidentOpen] = useState(false);
    
    // --- MAP STATES ---
    const [mapMode, setMapMode] = useState<MapMode>("AUTO_FOLLOW");
    const [routeData, setRouteData] = useState<any>(null);
    const [distanceText, setDistanceText] = useState("Calculando...");

    // 1. RESOLUÇÃO DE ROTA
    useEffect(() => {
        if (!driverPos || !destPos) return;
        const distMeters = calculateHaversineDistance(driverPos, destPos);
        setDistanceText(distMeters < 1000 ? `${Math.round(distMeters)}m` : `${(distMeters / 1000).toFixed(1)}km`);
        fetchRoute(driverPos, destPos).then(data => {
            if (data) setRouteData(data);
        });
    }, [driverPos, destPos]);

    // 2. NORMALIZAÇÃO DE DADOS (Contrato de Domínio)
    const order = useMemo(() => activeMission?.order || {}, [activeMission]);
    const items = useMemo(() => order.items || [], [order]);
    const totalCents = order.total_amount || 0;

    // 🛡️ RESTAURAÇÃO: missionData para compatibilidade com Modais
    const missionData = useMemo(() => {
        return {
            customerName: order.customer_name || "Cliente",
            phone: order.customer_phone || ""
        };
    }, [order]);

    // 3. HANDLERS DE NAVEGAÇÃO EXTERNA
    const openExternalMap = (app: 'google' | 'waze') => {
        const [lat, lng] = destPos;
        if (app === 'google') {
            window.open(`https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&travelmode=driving`, '_blank');
        } else {
            window.open(`https://waze.com/ul?ll=${lat},${lng}&navigate=yes`, '_blank');
        }
    };

    return (
        <div className="flex flex-col h-full bg-black relative overflow-hidden">
            
            {/* 🗺️ GIS STAGE (MAPA) */}
            <motion.div 
                initial={false}
                animate={{ height: isMapMinimized ? "35vh" : "78vh" }}
                className="relative w-full z-10 transition-all duration-700 ease-[0.16, 1, 0.3, 1]"
            >
                <TrackingMap 
                    driverPos={driverPos} 
                    clientPos={destPos} 
                    routeGeojson={routeData?.geometry}
                    mapMode={mapMode}
                    onMapModeChange={setMapMode}
                />
                
                {/* HUD: TELEMETRIA */}
                <div className="absolute top-24 left-4 z-[400] flex flex-col gap-2 pointer-events-none">
                    <div className="bg-black/80 backdrop-blur-md px-3 py-2 rounded-xl border border-white/10 shadow-lg flex items-center gap-3">
                        <Gauge size={14} className="text-orange-500" />
                        <div>
                            <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Velocidade</p>
                            <p className="text-lg font-mono font-black text-white">{Math.round(speed)} <span className="text-[10px] font-normal">km/h</span></p>
                        </div>
                    </div>
                    <div className="bg-black/80 backdrop-blur-md px-3 py-2 rounded-xl border border-white/10 shadow-lg flex items-center gap-3">
                        <Navigation size={14} className="text-blue-500" />
                        <div>
                            <p className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Distância</p>
                            <p className="text-lg font-mono font-black text-white">{distanceText}</p>
                        </div>
                    </div>
                </div>

                {/* HUD: CONTROLES DE MAPA */}
                <div className="absolute bottom-6 right-4 z-[500] flex flex-col gap-3 items-end">
                    <AnimatePresence>
                        {mapMode === "MANUAL" && (
                            <motion.button
                                initial={{ scale: 0, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                exit={{ scale: 0, opacity: 0 }}
                                onClick={() => setMapMode("AUTO_FOLLOW")}
                                className="bg-orange-600 text-white p-3 rounded-full shadow-xl border-2 border-white/20 active:scale-90"
                            >
                                <Locate size={20} className="animate-pulse" />
                            </motion.button>
                        )}
                    </AnimatePresence>

                    {/* Botão de Maximizar/Minimizar */}
                    <button 
                        onClick={() => setIsMapMinimized(!isMapMinimized)}
                        className="bg-white text-slate-950 p-3 rounded-full shadow-xl active:scale-90 transition-transform border-4 border-black/10"
                    >
                        {isMapMinimized ? <Maximize2 size={20} /> : <Minimize2 size={20} />}
                    </button>
                </div>

                {/* BOTÃO DE INCIDENTE RÁPIDO (DIREITA SUPERIOR) */}
                {!isMapMinimized && (
                    <button 
                        onClick={() => setIsIncidentOpen(true)}
                        className="absolute top-24 right-4 z-[400] bg-red-600 text-white p-3 rounded-xl shadow-xl active:scale-95 border-2 border-white/20"
                    >
                        <AlertTriangle size={20} />
                    </button>
                )}
            </motion.div>

            {/* 📋 OPERATIONAL DECK (PAINEL INFERIOR) */}
            <motion.div 
                initial={false}
                animate={{ height: isMapMinimized ? "65vh" : "22vh" }}
                className="bg-slate-950 rounded-t-[3rem] -mt-8 relative z-20 border-t border-white/10 p-6 flex flex-col shadow-[0_-20px_50px_rgba(0,0,0,0.9)]"
            >
                <div className="flex justify-between items-start mb-4">
                    <div className="min-w-0 flex-1 pr-4">
                        <div className="flex items-center gap-2 mb-1">
                            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                            <p className="text-[10px] font-black text-emerald-500 uppercase tracking-[0.2em]">Em Rota</p>
                        </div>
                        <h2 className="text-2xl font-black text-white leading-none truncate tracking-tight">
                            {order.customer_name || "Cliente"}
                        </h2>
                        <div className="flex items-center gap-2 mt-2 text-slate-400">
                            <MapPin size={14} className="text-red-500 shrink-0" />
                            <p className="text-xs font-bold truncate">
                                {order.delivery_address || "Endereço não informado"}
                            </p>
                        </div>
                    </div>
                    
                    <div className="flex flex-col items-end gap-2">
                        <div className="bg-slate-900 px-2 py-1 rounded-lg border border-white/5 font-mono text-[10px] text-slate-500 font-bold uppercase">
                            #{order.id?.slice(0, 6).toUpperCase()}
                        </div>
                        <p className="text-base font-black text-emerald-500">{formatCurrency(totalCents)}</p>
                    </div>
                </div>

                {/* ÁREA EXPANSÍVEL (VISÍVEL APENAS QUANDO MINIMIZADO) */}
                <AnimatePresence>
                    {isMapMinimized && (
                        <motion.div 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 20 }}
                            className="flex-1 flex flex-col min-h-0 space-y-4 mt-2"
                        >
                            {/* Botões de Ação Rápida */}
                            <div className="grid grid-cols-2 gap-3">
                                <button 
                                    onClick={() => setIsManifestOpen(true)}
                                    className="flex items-center justify-center gap-2 py-4 bg-slate-900 rounded-xl font-bold text-xs uppercase tracking-widest text-orange-400 border border-orange-500/20 active:scale-95 transition-all"
                                >
                                    <Package size={16} /> Ver Itens
                                </button>
                                <button 
                                    onClick={() => setIsCommOpen(true)}
                                    className="flex items-center justify-center gap-2 py-4 bg-slate-900 rounded-xl font-bold text-xs uppercase tracking-widest text-blue-400 border border-blue-500/20 active:scale-95 transition-all"
                                >
                                    <MessageSquare size={16} /> Contato
                                </button>
                            </div>

                            {/* Nota de Entrega */}
                            {order.pickup_note && (
                                <div className="p-4 bg-orange-600/10 border border-orange-500/20 rounded-xl flex gap-3">
                                    <Info size={18} className="text-orange-500 shrink-0 mt-0.5" />
                                    <div>
                                        <p className="text-[9px] font-black text-orange-500 uppercase tracking-widest mb-1">Observação</p>
                                        <p className="text-xs text-orange-100 font-medium leading-relaxed italic">"{order.pickup_note}"</p>
                                    </div>
                                </div>
                            )}

                            <div className="mt-auto pt-4 border-t border-white/5">
                                <div className="grid grid-cols-2 gap-3">
                                    <button 
                                        onClick={() => openExternalMap('waze')}
                                        className="flex items-center justify-center gap-2 py-3 bg-blue-500 text-white rounded-xl font-bold text-xs uppercase tracking-wider active:scale-95"
                                    >
                                        <Navigation size={16} /> Waze
                                    </button>
                                    <button 
                                        onClick={() => openExternalMap('google')}
                                        className="flex items-center justify-center gap-2 py-3 bg-slate-800 text-white rounded-xl font-bold text-xs uppercase tracking-wider border border-white/10 active:scale-95"
                                    >
                                        <MapPin size={16} /> Maps
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>

            {/* 🛡️ OVERLAYS & MODALS */}
            <OrderManifest 
                order={order} 
                isOpen={isManifestOpen} 
                onClose={() => setIsManifestOpen(false)} 
            />

            <DriverCommunicationModal 
                isOpen={isCommOpen} 
                onClose={() => setIsCommOpen(false)} 
                customerName={missionData.customerName}
                customerPhone={missionData.phone}
                restaurantName="MesaFlow Delivery"
            />
            
            <DriverIncidentModal 
                isOpen={isIncidentOpen}
                onClose={() => setIsIncidentOpen(false)}
                onReport={(reason: string) => {
                    onIncident();
                    setIsIncidentOpen(false);
                }}
            />
        </div>
    );
}