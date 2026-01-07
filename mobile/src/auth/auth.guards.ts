import { decodeJwtPayload } from '../lib/jwt';
import { JWTPayload } from './auth.types';

/**
 * @file auth.guards.ts
 * @description Funções de validação semântica de tokens e sessões.
 */

export const AuthGuards = {
  /**
   * Verifica se um token está expirado baseado no tempo atual.
   * Adiciona uma margem de segurança de 10 segundos.
   */
  isTokenExpired(token: string | null): boolean {
    if (!token) return true;
    
    try {
      const payload = decodeJwtPayload(token) as JWTPayload;
      if (!payload.exp) return true;

      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp < (currentTime + 10);
    } catch {
      return true;
    }
  },

  /**
   * Valida se o payload contém as claims mínimas necessárias para operação.
   */
  hasRequiredClaims(token: string | null): boolean {
    if (!token) return false;
    const payload = decodeJwtPayload(token) as JWTPayload;
    return !!(payload.sub && payload.role);
  }
};
