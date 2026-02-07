/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 4.4.2 (Interface Alignment)
 * DNA_ID: MF-DRIVER-FSM-V4-4-2
 * FIX: Adiciona métodos de incidente ao contrato de ações para resolver TS2339.
 */
import { useState, useEffect, useCallback } from 'react';
import { driverMachine, DriverState, DriverEvent } from '@/lib/domain/driver/driverMachine';
import * as api from '@/lib/api';
import { toast } from 'sonner';

export function useDriverMachine(slug: string) {
    const [state, setState] = useState<DriverState>(driverMachine.getState());
    const [activeJourney, setActiveJourney] = useState<any>(null);
    const [orders, setOrders] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const dispatch = useCallback((event: DriverEvent) => {
        const result = driverMachine.transition(event);
        if (result.success) {
            setState(result.newState);
            localStorage.setItem(`mf_driver_state_${slug}`, result.newState);
            if (result.newState === 'IDLE' || result.newState === 'OFFLINE') {
                localStorage.removeItem(`mf_driver_journey_${slug}`);
            }
        }
        return result;
    }, [slug]);

    const fetchOrders = useCallback(async () => {
        if (!slug || slug === "undefined") return;
        try {
            const data = await api.getKitchenOrders(slug);
            const available = data.filter((o: any) => o.status === 'ready' && o.order_type === 'delivery' && !o.driver_id);
            setOrders(available);
        } catch (e) {
            console.warn("[FSM] Data sync skipped.");
        } finally {
            setLoading(false);
        }
    }, [slug]);

    const actions = {
        startShift: async (vId: string) => {
            if (vId === "OFF") {
                dispatch({ type: 'SHIFT_END' });
                setActiveJourney(null);
                return;
            }
            try {
                await api.startDriverShift({ vehicle_id: vId, battery_level: 1.0 });
                dispatch({ type: 'SHIFT_START' });
                await fetchOrders();
            } catch (e) {
                toast.error("Erro ao iniciar turno.");
            }
        },
        acceptOrder: async (orderId: string) => {
            try {
                const orderSnapshot = orders.find(o => o.id === orderId);
                const res = await api.acceptJourney(orderId);
                const journey = { ...res, order: orderSnapshot || res.order };
                
                setActiveJourney(journey);
                localStorage.setItem(`mf_driver_journey_${slug}`, JSON.stringify(journey));
                dispatch({ type: 'ACCEPT_ORDER', payload: { mission: journey } });
                toast.success("Rota aceita!");
            } catch (e) {
                toast.error("Erro ao capturar missão.");
                fetchOrders();
            }
        },
        startNavigation: () => dispatch({ type: 'START_NAVIGATION' }),
        reportArrival: () => dispatch({ type: 'ARRIVED_DESTINATION' }),
        reportIncident: async (reason: string) => {
            // 🛡️ Log de Incidente Operacional
            console.warn(`[INCIDENT] ${reason}`);
            dispatch({ type: 'REPORT_INCIDENT', payload: { reason } });
        },
        resolveIncident: () => dispatch({ type: 'RESOLVE_INCIDENT' }),
        completeDelivery: async (code: string) => {
            if (!activeJourney?.journey_id) return { success: false };
            try {
                await api.updateJourneyStatus(activeJourney.journey_id, 'COMPLETED', code);
                dispatch({ type: 'CONFIRM_POD', payload: { code } });
                return { success: true };
            } catch (e) {
                toast.error("Código inválido.");
                return { success: false };
            }
        },
        finishSuccess: () => {
            dispatch({ type: 'RESET_TO_IDLE' });
            setActiveJourney(null);
            fetchOrders();
        },
        refresh: fetchOrders,
        simulateMissions: () => {
            const mock = { 
                id: 'ord-MOCK',
                customer_name: 'Gabriel Ramos (Simulação)', 
                total_amount: 4500, 
                delivery_address: 'Av. Brigadeiro Faria Lima, 1000',
                delivery_lat: -23.5855,
                delivery_lng: -46.6815,
                status: 'ready',
                order_type: 'delivery',
                delivery_code: '1234',
                items: [{ product: { name: 'Double Bacon Burger' }, quantity: 1 }]
            };
            setOrders([mock]);
        }
    };

    useEffect(() => {
        const savedState = localStorage.getItem(`mf_driver_state_${slug}`);
        if (savedState) {
            driverMachine.hydrate(savedState);
            setState(savedState as DriverState);
        }
        const savedJourney = localStorage.getItem(`mf_driver_journey_${slug}`);
        if (savedJourney) setActiveJourney(JSON.parse(savedJourney));
        fetchOrders();
    }, [slug, fetchOrders]);

    return { state, activeJourney, orders, loading, actions };
}
 