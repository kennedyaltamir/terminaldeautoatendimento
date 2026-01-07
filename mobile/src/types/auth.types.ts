export type AuthStatus = 
  | 'idle' 
  | 'hydrating' 
  | 'checking_expiry'
  | 'authenticated' 
  | 'unauthenticated' 
  | 'error';

export interface UserClaims {
  sub: string;         // email
  role: string;        // owner, manager, cashier, kitchen, driver
  company_id?: string; 
  exp: number;         
  iat: number;         
}

export interface AuthUser {
  email: string;
  role: string;
  company_id?: string;
}

export enum AuthErrorType {
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  NETWORK_ERROR = 'NETWORK_ERROR',
  SESSION_EXPIRED = 'SESSION_EXPIRED',
  UNKNOWN = 'UNKNOWN'
}

export interface AuthError {
  type: AuthErrorType;
  message?: string;
  code?: number;
}

export interface AuthState {
  status: AuthStatus;
  user: AuthUser | null;
  error: AuthError | null;

  hydrate: () => Promise<void>;
  login: (credentials: any) => Promise<void>;
  logout: () => Promise<void>;
}
