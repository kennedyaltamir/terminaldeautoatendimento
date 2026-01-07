import { decodeJwtPayload } from '../../lib/jwt';
import { UserClaims } from '../../types/auth.types';

/**
 * EXPIRY_GRACE_SECONDS: Margem de segurança (buffer) para compensar
 * latência de rede e dessincronia entre o relógio do dispositivo e o servidor.
 */
const EXPIRY_GRACE_SECONDS = 10;

export const JwtService = {
  getClaims(token: string): UserClaims | null {
    try {
      // Missão 14A: Usando o decodificador interno resiliente (polyfill atob incluso)
      const payload = decodeJwtPayload(token);
      if (!payload || !payload.sub) return null;
      return payload as UserClaims;
    } catch {
      return null;
    }
  },

  isTokenExpired(token: string): boolean {
    const claims = this.getClaims(token);
    if (!claims) return true;

    const currentTime = Math.floor(Date.now() / 1000);
    return claims.exp < (currentTime + EXPIRY_GRACE_SECONDS);
  },

  /**
   * Missão 14A: Validação Semântica de Claims.
   * Garante que o token possui a estrutura mínima para operação multi-tenant.
   */
  validateClaims(token: string): boolean {
    const claims = this.getClaims(token);
    if (!claims) return false;

    // 1. Verificação de Identidade e Papel
    if (!claims.sub || !claims.role) return false;

    // 2. Verificação de Contexto Operacional (Multi-tenancy)
    if (!claims.company_id) return false;

    return true;
  }
};
