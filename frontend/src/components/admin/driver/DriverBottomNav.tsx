/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 3.1.1 (Contract Fixed)
 * DNA_ID: MF-DRIVER-NAV-V3-1-1
 * FIX: Restaura prop 'onAction' para suportar abertura do modal de incidentes.
 */
"use client";
import React from "react";
import { Package, Wallet, History, User, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

export type DriverTab = 'ORDERS' | 'EARNINGS' | 'HISTORY' | 'PROFILE';

interface DriverBottomNavProps {
  activeTab: DriverTab;
  onTabChange: (tab: DriverTab) => void;
  onAction: () => void; // 🛡️ FIX: Prop restaurada para o contrato
  hasActiveMission: boolean;
  isMotionLocked: boolean;
  unreadCount: number;
}

export default function DriverBottomNav({ 
  activeTab, 
  onTabChange, 
  onAction,
  hasActiveMission, 
  isMotionLocked, 
  unreadCount 
}: DriverBottomNavProps) {
  
  if (hasActiveMission) return null;

  return (
    <nav className="fixed bottom-0 left-0 w-full bg-slate-950/95 backdrop-blur-xl border-t border-white/5 pb-safe pt-2 px-2 z-50 shadow-2xl">
      <div className="flex justify-between items-center max-w-md mx-auto">
        <button
          onClick={() => onTabChange('ORDERS')}
          disabled={isMotionLocked}
          className={cn("flex flex-col items-center gap-1 p-2 flex-1", activeTab === 'ORDERS' ? "text-orange-500" : "text-slate-500")}
        >
          <div className="relative">
            <Package size={22} />
            {unreadCount > 0 && <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-600 rounded-full border-2 border-slate-950" />}
          </div>
          <span className="text-[9px] font-black uppercase">Início</span>
        </button>

        <button
          onClick={() => onTabChange('EARNINGS')}
          disabled={isMotionLocked}
          className={cn("flex flex-col items-center gap-1 p-2 flex-1", activeTab === 'EARNINGS' ? "text-orange-500" : "text-slate-500")}
        >
          <Wallet size={22} />
          <span className="text-[9px] font-black uppercase">Ganhos</span>
        </button>

        {/* 🚨 BOTÃO DE ALERTA: Utiliza onAction passado via props */}
        <button
          onClick={onAction}
          className="flex flex-col items-center gap-1 p-2 flex-1 text-red-500"
        >
          <AlertTriangle size={22} />
          <span className="text-[9px] font-black uppercase">Alertas</span>
        </button>

        <button
          onClick={() => onTabChange('HISTORY')}
          disabled={isMotionLocked}
          className={cn("flex flex-col items-center gap-1 p-2 flex-1", activeTab === 'HISTORY' ? "text-orange-500" : "text-slate-500")}
        >
          <History size={22} />
          <span className="text-[9px] font-black uppercase">Histórico</span>
        </button>

        <button
          onClick={() => onTabChange('PROFILE')}
          disabled={isMotionLocked}
          className={cn("flex flex-col items-center gap-1 p-2 flex-1", activeTab === 'PROFILE' ? "text-orange-500" : "text-slate-500")}
        >
          <User size={22} />
          <span className="text-[9px] font-black uppercase">Perfil</span>
        </button>
      </div>
    </nav>
  );
}
