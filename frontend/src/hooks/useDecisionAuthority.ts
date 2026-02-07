/**
 * Author: MESAFLOW_AI
 * Version: 11.4
 * DNA_ID: MF-AUTHORITY-V11.4
 * Objective: Gating for Business and Governance modes based on roles and flags.
 */
import { DashboardState } from './useDashboardFSM';
import { getUserRole } from '@/lib/auth';

export function useDecisionAuthority(state: DashboardState, confidence: number) {
  const role = getUserRole();
  const isSimulation = state === 'SIMULATION_ACTIVE';
  const isLocked = state === 'OFFLINE_LOCKED';

  const authority = {
    // Identificação de Perfil
    isAdvancedUser: role === 'owner' || role === 'admin',
    
    // Gating Operacional
    canExport: !isSimulation && confidence >= 90 && !isLocked,
    canExecuteFinancial: confidence > 90 && !isSimulation && !isLocked,
    
    // Gating de Auditoria (Oculto por padrão no modo Business)
    canViewSLA: true, 
    canAuditLedger: (role === 'owner' || role === 'admin') && confidence >= 85,
    
    showWatermark: isSimulation,
    statusLabel: confidence < 70 ? 'SISTEMA LENTO' : confidence < 90 ? 'VERIFIQUE CONEXÃO' : 'SISTEMA ESTÁVEL'
  };

  return { authority };
}
