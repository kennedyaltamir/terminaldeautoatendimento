import { decodeJwtPayload } from '../../lib/jwt';
import { UserClaims } from '../../types/auth.types';

/**
 * @file jwt.ts
 * @description Serviço de validação semântica e temporal de tokens JWT.
 * Implementa as regras de negócio da TASK-014A.
 */

// Buffer de segurança para compensar latência de rede e clock skew
const EXPIRY_GRACE_SECONDS = 10;

export const JwtService = {
  /**
   * Decodifica o token e retorna as claims tipadas.
   * Retorna null se o token for malformado.
   */
  getClaims(token: string): UserClaims | null {
    try {
      const payload = decodeJwtPayload(token);
      if (!payload || !payload.sub) return null;
      return payload as UserClaims;
    } catch (error) {
      console.error('[JwtService] Erro ao decodificar token:', error);
      return null;
    }
  },

  /**
   * Verifica se o token está expirado ou prestes a expirar (dentro do buffer).
   * Retorna true se expirado ou inválido.
   */
  isTokenExpired(token: string): boolean {
    const claims = this.getClaims(token);
    if (!claims || !claims.exp) return true;

    const currentTime = Math.floor(Date.now() / 1000);
    // exp deve ser maior que (agora + buffer) para ser considerado válido
    return claims.exp < (currentTime + EXPIRY_GRACE_SECONDS);
  },

  /**
   * Valida se o token contém todas as claims obrigatórias para a operação do sistema.
   * Regra de Negócio: O sistema é multi-tenant, então company_id é obrigatório.
   */
  validateClaims(token: string): boolean {
    const claims = this.getClaims(token);
    if (!claims) return false;

    // 1. Identidade
    if (!claims.sub) return false;

    // 2. Controle de Acesso (RBAC)
    if (!claims.role) return false;

    // 3. Contexto Operacional (Multi-tenancy)
    // Todo usuário operacional (staff) deve estar vinculado a uma empresa
    if (!claims.company_id) return false;

    return true;
  }
};
