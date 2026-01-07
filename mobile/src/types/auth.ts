/**
 * Definições de tipos e classes de erro para o domínio de Autenticação.
 */

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface UserSession {
  userName: string;
  userRole: string;
  companySlug: string;
  companyName: string;
}

export class AuthError extends Error {
  constructor(public message: string, public status?: number) {
    super(message);
    this.name = 'AuthError';
  }
}

export class TokenExpiredError extends AuthError {
  constructor() {
    super('Sessão expirada. Por favor, faça login novamente.', 401);
    this.name = 'TokenExpiredError';
  }
}

export class RefreshTokenError extends AuthError {
  constructor() {
    super('Falha ao renovar credenciais.', 401);
    this.name = 'RefreshTokenError';
  }
}
