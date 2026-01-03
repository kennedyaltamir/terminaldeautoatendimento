const ACCESS_TOKEN_KEY = "mesaflow_access_token";
const REFRESH_TOKEN_KEY = "mesaflow_refresh_token";
const USER_ROLE_KEY = "mesaflow_user_role"; // Novo

export function setTokens(accessToken: string, refreshToken: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
}

export function setToken(accessToken: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  }
}

// Nova função para salvar o cargo
export function setUserRole(role: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem(USER_ROLE_KEY, role);
  }
}

export function getUserRole(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem(USER_ROLE_KEY);
  }
  return null;
}

export function getToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  }
  return null;
}

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
  }
}

export const removeToken = removeTokens;

export function isAuthenticated(): boolean {
  return !!getToken();
}