/**
 * 🔐 Gerenciador de Sessão Sincronizado (L6)
 * O Cookie 'auth_token' é a fonte da verdade para o Middleware e Server Components.
 * O LocalStorage é o cache para o estado do React Client.
 */

const ACCESS_TOKEN_KEY = "mesaflow_access_token";
const REFRESH_TOKEN_KEY = "mesaflow_refresh_token";
const USER_ROLE_KEY = "mesaflow_user_role";

export function setTokens(accessToken: string, refreshToken: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
    
    // 🛡️ Sincronização Crítica com Cookie (7 dias)
    const maxAge = 60 * 60 * 24 * 7;
    document.cookie = `auth_token=${accessToken}; path=/; max-age=${maxAge}; samesite=lax; priority=high`;
  }
}

export function setToken(accessToken: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    const maxAge = 60 * 60 * 24 * 7;
    document.cookie = `auth_token=${accessToken}; path=/; max-age=${maxAge}; samesite=lax; priority=high`;
  }
}

export function setUserRole(role: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem(USER_ROLE_KEY, role);
  }
}

export function getUserRole(): string | null {
  return typeof window !== "undefined" ? localStorage.getItem(USER_ROLE_KEY) : null;
}

export function getToken(): string | null {
  if (typeof window !== "undefined") {
    const match = document.cookie.match(new RegExp('(^| )auth_token=([^;]+)'));
    if (match) return match[2];
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  }
  return null;
}

// FIX: Exportação necessária para o lib/api.ts (Refresh Flow)
export function getRefreshToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  }
  return null;
}

export function removeTokens() {
  if (typeof window !== "undefined") {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_ROLE_KEY);
    localStorage.removeItem("mesaflow_company_slug");
    document.cookie = "auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; samesite=lax";
  }
}

export const removeToken = removeTokens;

export function isAuthenticated(): boolean {
  return !!getToken();
}