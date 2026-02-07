/**
 * Design Tokens: Cores
 * Fonte Única da Verdade para a paleta MesaFlow Mobile.
 */
export const COLORS = {
  primary: '#EA580C',
  secondary: '#334155',
  background: '#0F172A',
  surface: '#1E293B',

  text: {
    primary: '#FFFFFF',
    secondary: '#94A3B8',
    muted: '#64748B',
    inverse: '#0F172A',
  },

  status: {
    danger: '#EF4444',
    success: '#22C55E',
    warning: '#F59E0B',
    info: '#3B82F6',
  },

  border: '#334155',
  transparent: 'transparent',
} as const;

/** ⛔️ Compat temporária (REMOVER após sweep) */
export const colors = COLORS;
