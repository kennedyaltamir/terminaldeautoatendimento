import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';

interface User {
  name: string;
  role: 'owner' | 'manager' | 'cashier' | 'kitchen' | 'driver';
  company_slug: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string, user: User) => Promise<void>;
  logout: () => Promise<void>;
  hydrate: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (token, user) => {
    try {
      await SecureStore.setItemAsync('mesaflow_token', token);
      await SecureStore.setItemAsync('mesaflow_user', JSON.stringify(user));
      set({ token, user, isAuthenticated: true });
    } catch (error) {
      console.error("Erro ao salvar sessão", error);
    }
  },

  logout: async () => {
    try {
      await SecureStore.deleteItemAsync('mesaflow_token');
      await SecureStore.deleteItemAsync('mesaflow_user');
      set({ token: null, user: null, isAuthenticated: false });
    } catch (error) {
      console.error("Erro ao encerrar sessão", error);
    }
  },

  hydrate: async () => {
    try {
      const token = await SecureStore.getItemAsync('mesaflow_token');
      const userJson = await SecureStore.getItemAsync('mesaflow_user');
      
      if (token && userJson) {
        const user = JSON.parse(userJson);
        // TODO: Implementar TASK-014A (Validação de expiração do JWT)
        set({ token, user, isAuthenticated: true });
      }
    } catch (e) {
      console.error("Erro ao hidratar auth", e);
    } finally {
      set({ isLoading: false });
    }
  },
}));
