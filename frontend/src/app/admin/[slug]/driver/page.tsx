
//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 5.0.0 (Sovereign Gold Master - Unified Edition)
 * DNA_ID: MF-DRIVER-COCKPIT-V5-GOLD
 * OBJETIVO: Cockpit Logístico de Alto Desempenho.
 * Comportamento esperado: 
 *  1. Implementa ISOLAMENTO OPERACIONAL (Theater Mode): Durante missões ativas, oculta HUD financeiro e navegação para foco total na rota.
 *  2. GESTÃO DE ESTADO CRÍTICO: Bloqueia encerramento de turno se houver entrega pendente, forçando reporte de incidente.
 *  3. RESILIÊNCIA GEOGRÁFICA: Sistema de ancoragem para Pompéu-MG com telemetria via useDriverTelemetry.
 *  4. SINCRONIA FSM: Orquestração determinística entre Máquina de Estados, WebSockets e Persistência Offline.
 */
//
"use client";

import React, { use, useState, useEffect, useMemo, useCallback } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Loader2, Radar, ShieldCheck, MapPin } from "lucide-react";

import { useDriverMachine } from "@/hooks/driver/useDriverMachine";
import { useDriverTelemetry } from "@/hooks/driver/useDriverTelemetry";
import { useOfflineSync } from "@/hooks/useOfflineSync";
import { useLanguage } from "@/context/LanguageContext";
import { WebSocketProvider } from "@/context/WebSocketContext";

import HeaderVitals from "@/components/admin/driver/layers/HeaderVitals";
import FinancialHUD from "@/components/admin/driver/layers/FinancialHUD";
import ControlDeck from "@/components/admin/driver/layers/ControlDeck";
import IncidentModal from "@/components/admin/driver/modals/IncidentModal";

import DriverBottomNav, { DriverTab } from "@/components/admin/driver/DriverBottomNav";
import IdleView from "@/components/admin/driver/views/IdleView";
import EnRouteView from "@/components/admin/driver/views/EnRouteView";
import HistoryView from "@/components/admin/driver/views/HistoryView";
import ProfileView from "@/components/admin/driver/views/ProfileView";
import EarningsView from "@/components/admin/driver/views/EarningsView";
import MissionComplete from "@/components/admin/driver/views/MissionComplete";
import PodView from "@/components/admin/driver/views/PodView";

const ANCHOR_COORDS: [number, number] = [-19.2244, -44.9354];

function DriverCockpitContent({ slug }: { slug: string }) {
  const { t } = useLanguage();
  const { dbReady, pendingCount } = useOfflineSync();
  const { state, activeJourney, orders = [], loading, actions } = useDriverMachine(slug);
  
  const [activeTab, setActiveTab] = useState<DriverTab>('ORDERS');
  const [isIncidentOpen, setIsIncidentOpen] = useState(false);

  const isMissionActive = useMemo(() => 
    ['ASSIGNED', 'EN_ROUTE_DELIVERY', 'AT_DESTINATION'].includes(state),
  [state]);

  const { currentSpeed, gpsSignal, coords } = useDriverTelemetry(
    isMissionActive || state === 'IDLE', 
    activeJourney?.journey_id || "standby"
  );

  const handleSystemExit = useCallback(() => {
    if (isMissionActive) {
      setIsIncidentOpen(true);
    } else {
      actions.startShift("OFF");
    }
  }, [isMissionActive, actions]);

  const destinationCoords: [number, number] = useMemo(() => {
    if (activeJourney?.order?.delivery_lat && activeJourney?.order?.delivery_lng) {
      return [activeJourney.order.delivery_lat, activeJourney.order.delivery_lng];
    }
    return ANCHOR_COORDS;
  }, [activeJourney]);

  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  if (!mounted || loading || !dbReady) return (
    <div className="fixed inset-0 bg-slate-950 flex flex-col items-center justify-center z-[10000] gap-8">
      <motion.div
        animate={{ scale: [1, 1.1, 1], opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <ShieldCheck className="text-orange-500" size={80} strokeWidth={1.5} />
      </motion.div>
      <div className="text-center space-y-3">
        <p className="text-white font-black uppercase tracking-[0.4em] text-sm">MesaFlow Logistics</p>
        <div className="flex items-center justify-center gap-2">
          <Loader2 className="animate-spin text-orange-500/50" size={16} />
          <p className="text-slate-500 font-bold text-[10px] uppercase tracking-widest">Iniciando Protocolo de Segurança</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="fixed inset-0 bg-black overflow-hidden flex flex-col font-sans select-none text-white h-[100dvh]">
      <div className="fixed top-0 left-0 w-full z-50">
        <HeaderVitals 
          fsmState={state} 
          batteryLevel={1.0} 
          gpsSignal={gpsSignal} 
          isPendingSync={pendingCount > 0} 
          onStartShift={actions.startShift} 
          onEndShift={handleSystemExit} 
        />
        
        <AnimatePresence>
          {!isMissionActive && state !== 'OFFLINE' && state !== 'INCIDENT_LOCKED' && activeTab === 'ORDERS' && (
            <motion.div 
              initial={{ y: -120, opacity: 0 }} 
              animate={{ y: 0, opacity: 1 }} 
              exit={{ y: -120, opacity: 0 }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
            >
              <FinancialHUD earnings={146.46} dailyGoal={30000} rank={3} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <main className="flex-1 relative z-10 flex flex-col h-full">
        <AnimatePresence mode="wait">
          {state === 'OFFLINE' ? (
            <motion.div 
              key="offline" 
              initial={{ opacity: 0, scale: 0.95 }} 
              animate={{ opacity: 1, scale: 1 }} 
              exit={{ opacity: 0, scale: 1.05 }} 
              className="h-full flex items-center justify-center p-8"
            >
               <div className="bg-slate-900/40 backdrop-blur-md p-16 rounded-[4rem] border border-white/5 shadow-2xl text-center">
                  <Radar size={100} className="text-slate-800 mx-auto mb-10 animate-pulse" />
                  <h2 className="text-3xl font-black uppercase tracking-tighter text-white">Terminal Inativo</h2>
                  <p className="text-slate-500 text-xs mt-4 font-bold uppercase tracking-[0.2em] max-w-[200px] mx-auto leading-relaxed">
                    Aguardando início de turno para ativação de telemetria
                  </p>
               </div>
            </motion.div>
          ) : state === 'DELIVERED' ? (
            <MissionComplete 
              key="complete" 
              earnings={15.00} 
              timeMinutes={25} 
              distanceKm={4.2} 
              onDone={actions.finishSuccess} 
            />
          ) : state === 'AT_DESTINATION' ? (
            <PodView 
              key="pod" 
              onSubmit={actions.completeDelivery} 
              onIncident={() => setIsIncidentOpen(true)} 
              debugCode={activeJourney?.order?.delivery_code} 
            />
          ) : isMissionActive ? (
            <EnRouteView 
              key="enroute"
              activeMission={activeJourney} 
              speed={currentSpeed} 
              onIncident={() => setIsIncidentOpen(true)} 
              driverPos={coords || ANCHOR_COORDS} 
              destPos={destinationCoords} 
            />
          ) : (
            <motion.div 
              key="dashboards" 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }} 
              className="flex-1 overflow-y-auto pt-24 pb-32 px-4 custom-scrollbar"
            >
                {activeTab === 'ORDERS' && (
                  <IdleView 
                    orders={orders} 
                    onAccept={actions.acceptOrder} 
                    onSimulate={actions.simulateMissions} 
                    onRefresh={actions.refresh} 
                  />
                )}
                {activeTab === 'EARNINGS' && <EarningsView />}
                {activeTab === 'HISTORY' && <HistoryView />}
                {activeTab === 'PROFILE' && (
                  <ProfileView 
                    driverName="Admin Master" 
                    vehicleId="MOTO-01" 
                    rating={4.9} 
                    totalDeliveries={142} 
                    fsmState={state} 
                    onLogout={handleSystemExit} 
                  />
                )}
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <div className="fixed bottom-0 left-0 w-full z-40">
        <AnimatePresence>
          {isMissionActive && state !== 'AT_DESTINATION' ? (
            <motion.div 
              initial={{ y: 150 }} 
              animate={{ y: 0 }} 
              exit={{ y: 150 }}
              className="shadow-[0_-20px_60px_rgba(0,0,0,1)]"
            >
               <ControlDeck 
                  activeMission={activeJourney} 
                  batchCount={1} 
                  fsmState={state} 
                  onAction={async (act) => {
                    if (act === 'ARRIVED') await actions.reportArrival();
                    else if (act === 'START_ROUTE') await actions.startNavigation();
                    else setIsIncidentOpen(true);
                  }} 
                  isMotionLocked={currentSpeed > 15} 
               />
            </motion.div>
          ) : !isMissionActive && state !== 'OFFLINE' && (
            <motion.div
              initial={{ y: 100 }}
              animate={{ y: 0 }}
              exit={{ y: 100 }}
            >
              <DriverBottomNav 
                activeTab={activeTab} 
                onTabChange={setActiveTab} 
                onAction={() => setIsIncidentOpen(true)} 
                hasActiveMission={false} 
                isMotionLocked={currentSpeed > 15} 
                unreadCount={0} 
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <IncidentModal 
        isOpen={isIncidentOpen} 
        onClose={() => setIsIncidentOpen(false)} 
        onReport={async (reason) => { 
            await actions.reportIncident(reason); 
            setIsIncidentOpen(false); 
        }} 
      />
    </div>
  );
}

export default function DriverCockpitPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(paramsPromise);
  return (
    <WebSocketProvider slug={slug}>
      <DriverCockpitContent slug={slug} />
    </WebSocketProvider>
  );
}