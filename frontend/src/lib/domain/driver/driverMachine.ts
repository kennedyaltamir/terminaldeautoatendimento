/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 2.4.0 (Idempotent Transitions)
 * DNA_ID: MF-DRIVER-FSM-V2-4
 * Objective: Permitir ritos de encerramento mesmo em estados inativos para evitar crashes de UI.
 */
export type DriverState = 
    | 'OFFLINE' 
    | 'IDLE' 
    | 'ASSIGNED' 
    | 'EN_ROUTE_DELIVERY' 
    | 'AT_DESTINATION' 
    | 'DELIVERED'
    | 'INCIDENT_LOCKED' 
    | 'CONTINGENCY';

export type DriverEvent = 
    | { type: 'SHIFT_START' } 
    | { type: 'SHIFT_END' } 
    | { type: 'ACCEPT_ORDER'; payload: { mission: any } } 
    | { type: 'START_NAVIGATION' } 
    | { type: 'ARRIVED_DESTINATION' } 
    | { type: 'CONFIRM_POD'; payload: { code: string } } 
    | { type: 'REPORT_INCIDENT'; payload: { reason: string } } 
    | { type: 'CANCEL_ROUTE' } 
    | { type: 'RESOLVE_INCIDENT' }
    | { type: 'RESET_TO_IDLE' };

export class DriverStateMachine {
    private state: DriverState = 'OFFLINE';
    private transitions: Record<DriverState, Partial<Record<DriverEvent['type'], DriverState>>> = {
        OFFLINE: { 
            SHIFT_START: 'IDLE',
            SHIFT_END: 'OFFLINE' // 🛡️ IDEMPOTÊNCIA: Encerrar o que já está encerrado é permitido.
        },
        IDLE: { 
            ACCEPT_ORDER: 'ASSIGNED', 
            SHIFT_END: 'OFFLINE' 
        },
        ASSIGNED: { 
            START_NAVIGATION: 'EN_ROUTE_DELIVERY', 
            REPORT_INCIDENT: 'INCIDENT_LOCKED',
            CANCEL_ROUTE: 'IDLE',
            SHIFT_END: 'OFFLINE'
        },
        EN_ROUTE_DELIVERY: { 
            ARRIVED_DESTINATION: 'AT_DESTINATION', 
            REPORT_INCIDENT: 'INCIDENT_LOCKED',
            CANCEL_ROUTE: 'IDLE' 
        },
        AT_DESTINATION: { 
            CONFIRM_POD: 'DELIVERED', 
            REPORT_INCIDENT: 'INCIDENT_LOCKED',
            CANCEL_ROUTE: 'IDLE' 
        },
        DELIVERED: { 
            RESET_TO_IDLE: 'IDLE',
            SHIFT_END: 'OFFLINE'
        },
        INCIDENT_LOCKED: { 
            RESOLVE_INCIDENT: 'IDLE',
            SHIFT_END: 'OFFLINE' 
        },
        CONTINGENCY: { SHIFT_END: 'OFFLINE' }
    };

    public transition(event: DriverEvent): { success: boolean; newState: DriverState } {
        const nextState = this.transitions[this.state]?.[event.type];
        if (!nextState) {
            return { success: false, newState: this.state };
        }
        this.state = nextState;
        return { success: true, newState: this.state };
    }

    public hydrate(savedState: string) {
        this.state = (this.transitions[savedState as DriverState] ? savedState : 'OFFLINE') as DriverState;
    }

    public getState(): DriverState {
        return this.state;
    }
}

export const driverMachine = new DriverStateMachine();