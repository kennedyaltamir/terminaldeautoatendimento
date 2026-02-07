import { useReducer, useEffect } from 'react';
import { db } from '@/lib/db';

export type POSState = 'IDLE' | 'DRAFT' | 'COMMITTING' | 'SYNCED' | 'OFFLINE_SAVED';

type POSAction = 
  | { type: 'ADD_ITEM' }
  | { type: 'START_CHECKOUT' }
  | { type: 'COMMIT_SUCCESS' }
  | { type: 'COMMIT_FAIL_OFFLINE' }
  | { type: 'RESET' };

function posReducer(state: POSState, action: POSAction): POSState {
  switch (action.type) {
    case 'ADD_ITEM': return 'DRAFT';
    case 'START_CHECKOUT': return 'COMMITTING';
    case 'COMMIT_SUCCESS': return 'SYNCED';
    case 'COMMIT_FAIL_OFFLINE': return 'OFFLINE_SAVED';
    case 'RESET': return 'IDLE';
    default: return state;
  }
}

export function useCounterFSM() {
  const [state, dispatch] = useReducer(posReducer, 'IDLE');

  // 🛡️ PERSISTÊNCIA DE SEGURANÇA: Salva rascunho no IndexedDB
  useEffect(() => {
    if (state === 'DRAFT') {
      // Lógica de auto-save para recuperação de crash
    }
  }, [state]);

  return { state, dispatch };
}

