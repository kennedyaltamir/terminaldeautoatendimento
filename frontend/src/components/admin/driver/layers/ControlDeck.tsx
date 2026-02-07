import React from 'react';
import { Navigation, AlertTriangle, Map } from 'lucide-react';
import HoldButton from '@/components/ui/HoldButton';

interface ControlDeckProps {
    activeMission: any;
    batchCount: number;
    fsmState: string;
    onAction: (action: string) => void;
    isMotionLocked: boolean;
}

export default function ControlDeck({ activeMission, fsmState, onAction }: ControlDeckProps) {
    const customerName = activeMission?.customer_name || "Aguardando...";
    const address = activeMission?.delivery_address || "Sem destino ativo";

    return (
        <div 
            className="bg-slate-950 border-t border-white/10 p-4 pb-8 shadow-2xl"
            data-testid="control-deck"
        >
            <div className="flex justify-between items-center mb-4 px-2">
                <div className="flex-1 min-w-0">
                    <h3 className="text-white font-black text-lg truncate">{customerName}</h3>
                    <p className="text-slate-400 text-xs truncate">{address}</p>
                </div>
            </div>
            <div className="grid grid-cols-4 gap-3">
                <button 
                    onClick={() => onAction('INCIDENT')} 
                    data-testid="btn-incident"
                    className="col-span-1 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-center text-slate-400 min-h-[64px] active:scale-95 transition-transform"
                >
                    <AlertTriangle size={24} />
                </button>
                <div className="col-span-3">
                    {fsmState === 'EN_ROUTE_DELIVERY' ? (
                        <button 
                            onClick={() => onAction('ARRIVED')} 
                            data-testid="btn-arrived"
                            className="w-full bg-blue-600 text-white rounded-2xl font-black uppercase text-sm flex items-center justify-center gap-3 min-h-[64px] shadow-lg active:scale-95 transition-all"
                        >
                            <Map size={20} /> Cheguei no Local
                        </button>
                    ) : fsmState === 'ASSIGNED' ? (
                        <HoldButton 
                            label="INICIAR ROTA" 
                            data-testid="btn-start-navigation"
                            onComplete={() => onAction('START_ROUTE')} 
                            className="w-full min-h-[64px] bg-orange-600" 
                            icon={<Navigation size={20} />} 
                        />
                    ) : null}
                </div>
            </div>
        </div>
    );
}
