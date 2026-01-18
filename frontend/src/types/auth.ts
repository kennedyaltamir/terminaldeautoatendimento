/**
 * MesaFlow OS - Domain: Authentication & Staff
 */
export type UserRole = 'ADMIN' | 'WAITER' | 'KITCHEN' | 'DRIVER' | 'CASHIER';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  company_id: string;
  avatar_url?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface Employee {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
}

