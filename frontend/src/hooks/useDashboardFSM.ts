/**
 * 🧠 MESAFLOW SOVEREIGN FSM v1.5.2
 * DOMAIN: LOGIC / GOVERNANCE
 * FIX: Added SYNC_RECOVERED to DashboardAction type.
 */
import { useReducer, useEffect } from 'react';

export type DashboardState =
  | 'OPERATIONAL_FULL'
  | 'CONFIDENCE_RESTORED'
  | 'SIMULATION_ACTIVE'
  | 'PASSIVE_OBSERVATION'
  | 'DEGRADED_STALE'
  | 'OFFLINE_LOCKED';

type DashboardAction =
  | { type: 'INIT_OK' }
  | { type: 'SYNC_LAG' }
  | { type: 'SYNC_RECOVERED' } // 🛡️ FIX: Adicionado ao contrato
  | { type: 'NET_LOST' }
  | { type: 'NET_RESTORED' }
  | { type: 'USER_SLIDE' }
  | { type: 'ACTIVITY' }
  | { type: 'IDLE_TIMEOUT' }
  | { type: 'RESET_SIMULATION' };

const initialState: DashboardState = 'OPERATIONAL_FULL';

function dashboardReducer(state: DashboardState, action: DashboardAction): DashboardState {
  switch (action.type) {
    case 'NET_LOST': return 'OFFLINE_LOCKED';
    case 'NET_RESTORED': return 'CONFIDENCE_RESTORED';
    case 'INIT_OK': return 'OPERATIONAL_FULL';
    case 'SYNC_LAG': 
      return state === 'OFFLINE_LOCKED' ? state : 'DEGRADED_STALE';
    case 'USER_SLIDE': return 'SIMULATION_ACTIVE';
    case 'ACTIVITY':
      return state === 'PASSIVE_OBSERVATION' ? 'OPERATIONAL_FULL' : state;
    case 'IDLE_TIMEOUT':
      return state === 'OPERATIONAL_FULL' ? 'PASSIVE_OBSERVATION' : state;
    case 'SYNC_RECOVERED':
      return state === 'DEGRADED_STALE' ? 'CONFIDENCE_RESTORED' : state;
    case 'RESET_SIMULATION': return 'OPERATIONAL_FULL';
    default: return state;
  }
}

export function useDashboardFSM() {
  const [state, dispatch] = useReducer(dashboardReducer, initialState);

  useEffect(() => {
    if (state === 'CONFIDENCE_RESTORED') {
      const timer = setTimeout(() => dispatch({ type: 'INIT_OK' }), 3000);
      return () => clearTimeout(timer);
    }
  }, [state]);

  return { state, dispatch };
}
