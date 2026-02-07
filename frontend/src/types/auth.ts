/**
 * MesaFlow OS - Domain: Authentication & Staff
 * LAST_MODIFIED: 2026-01-27
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
  created_at: string;
  updated_at?: string; // 🛡️ FIX: Necessário para Optimistic Locking
}
