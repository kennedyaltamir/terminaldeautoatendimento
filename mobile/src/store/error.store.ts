
import { create } from 'zustand';

export type ErrorType = '403' | '500' | 'OFFLINE' | 'TIMEOUT' | 'UNKNOWN';

interface ErrorState {
  currentError: ErrorType | null;
  errorMessage: string | null;
  setError: (type: ErrorType, message?: string) => void;
  clearError: () => void;
}

/**
 * ErrorStore: Gerencia o estado global de falhas críticas.
 * Utilizado pelo AuthGate para interceptar a renderização e exibir telas de erro.
 */
export const useErrorStore = create<ErrorState>((set) => ({
  currentError: null,
  errorMessage: null,
  setError: (type, message) => set({ currentError: type, errorMessage: message || null }),
  clearError: () => set({ currentError: null, errorMessage: null }),
}));

