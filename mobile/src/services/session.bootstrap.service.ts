import { useAuthStore } from '../store/auth.store';
import { useSessionStore } from '../store/session.store';
import { JwtService } from './auth/jwt';

/**
 * SessionBootstrapService: Orquestra a transição entre Autenticação e Operação.
 * Extrai a identidade operacional das claims do JWT.
 */
export const SessionBootstrapService = {
  /**
   * Realiza o mapeamento de claims para a Session Store.
   * Deve ser chamado sempre que o status de auth mudar para 'authenticated'.
   */
  async run() {
    const accessToken = useAuthStore.getState().accessToken;
    
    if (!accessToken) {
      console.error('[Bootstrap] Falha: Access Token ausente.');
      return false;
    }

    try {
      const claims = JwtService.getClaims(accessToken);

      // Validação de Contexto Operacional Mínimo
      // No MesaFlow, o slug é obrigatório para qualquer operação administrativa/KDS.
      if (!claims || !claims.company_id || !claims.role) {
        throw new Error('INVALID_OPERATIONAL_CONTEXT');
      }

      // DÍVIDA TÉCNICA: O slug atualmente é derivado do sub/email em alguns cenários 
      // ou fixo no backend. Aqui injetamos a lógica de normalização.
      // Futuramente o 'slug' será uma claim primária do JWT.
      const derivedSlug = claims.sub.split('@')[0].replace(/[^a-z0-9]/g, '-');

      useSessionStore.getState().initializeSession({
        slug: derivedSlug,
        role: claims.role,
        companyId: claims.company_id,
      });

      console.log(`[Bootstrap] Sessão operacional pronta: ${derivedSlug} (${claims.role})`);
      return true;

    } catch (error) {
      console.error('[Bootstrap] Erro crítico de identidade:', error);
      // Fail-Safe: Se não há identidade clara, desloga para proteger o sistema.
      useAuthStore.getState().logout();
      return false;
    }
  }
};
