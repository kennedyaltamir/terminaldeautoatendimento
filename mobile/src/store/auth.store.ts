
import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';
import { AuthStatus } from '../types/auth.types';

interface User {
  name: string;
  role: 'owner' | 'manager' | 'cashier' | 'kitchen' | 'driver' | 'waiter';
  company_slug: string;
}

interface AuthState {
  status: AuthStatus;
  accessToken: string | null;
  user: User | null;
  isQaMode: boolean;
  isLoading: boolean;
  setQaMode: (enabled: boolean) => void;
  login: (token: string, user: User) => Promise<void>;
  logout: () => Promise<void>;
  hydrate: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  status: 'idle',
  accessToken: null,
  user: null,
  isQaMode: false,
  isLoading: true,

  setQaMode: (enabled) => set({ isQaMode: enabled }),

  login: async (token, user) => {
    const isTest = user.name.includes('QA');
    set({ accessToken: token, user, status: 'authenticated', isLoading: false, isQaMode: isTest });
    
    try {
      await SecureStore.setItemAsync('mesaflow_token', token);
      await SecureStore.setItemAsync('mesaflow_user', JSON.stringify(user));
    } catch (e) {}
  },

  logout: async () => {
    try {
      await SecureStore.deleteItemAsync('mesaflow_token');
      await SecureStore.deleteItemAsync('mesaflow_user');
    } finally {
      set({ accessToken: null, user: null, status: 'unauthenticated', isQaMode: false });
    }
  },

  hydrate: async () => {
    set({ status: 'hydrating' });
    try {
      const token = await SecureStore.getItemAsync('mesaflow_token');
      const userJson = await SecureStore.getItemAsync('mesaflow_user');
      if (token && userJson) {
        set({ accessToken: token, user: JSON.parse(userJson), status: 'authenticated' });
      } else {
        set({ status: 'unauthenticated' });
      }
    } catch (e) {
      set({ status: 'unauthenticated' });
    } finally {
      set({ isLoading: false });
    }
  },
}));

