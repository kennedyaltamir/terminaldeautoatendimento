/**
 * @file auth.types.ts
 * @description Definições de tipos para o payload JWT e metadados de sessão.
 */

export interface JWTPayload {
  sub: string;          // Email do usuário
  role: string;         // Cargo (owner, manager, etc)
  account_type: string; // company ou employee
  company_id?: string;  // UUID da empresa (se employee)
  impersonator?: boolean; // Flag de modo suporte
  exp: number;          // Timestamp de expiração (segundos)
  iat: number;          // Timestamp de emissão
  type: 'access' | 'refresh';
}

export interface SessionMetadata {
  isValid: boolean;
  isExpired: boolean;
  willExpireSoon: boolean; // Útil para refresh proativo
}
