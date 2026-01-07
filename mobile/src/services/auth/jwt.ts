import { jwtDecode } from 'jwt-decode';
import { UserClaims } from '../../types/auth.types';

/**
 * EXPIRY_GRACE_SECONDS: Margem de segurança (buffer) para compensar
 * latência de rede e dessincronia entre o relógio do dispositivo e o servidor.
 */
const EXPIRY_GRACE_SECONDS = 10;

export const JwtService = {
  getClaims(token: string): UserClaims | null {
    try {
      return jwtDecode<UserClaims>(token);
    } catch {
      return null;
    }
  },

  isTokenExpired(token: string): boolean {
    const claims = this.getClaims(token);
    if (!claims) return true;

    const currentTime = Math.floor(Date.now() / 1000);
    return claims.exp < (currentTime + EXPIRY_GRACE_SECONDS);
  }
};
