import { create } from 'zustand';

/**
 * SessionState: Identidade operacional do usuário no dispositivo.
 * Contém o contexto necessário para roteamento multi-tenant.
 */
interface SessionState {
  slug: string | null;
  role: string | null;
  companyId: string | null;
  isReady: boolean;
  
  // Actions
  initializeSession: (data: { slug: string; role: string; companyId: string }) => void;
  clearSession: () => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  slug: null,
  role: null,
  companyId: null,
  isReady: false,

  initializeSession: (data) => set({
    slug: data.slug,
    role: data.role,
    companyId: data.companyId,
    isReady: true,
  }),

  clearSession: () => set({
    slug: null,
    role: null,
    companyId: null,
    isReady: false,
  }),
}));
