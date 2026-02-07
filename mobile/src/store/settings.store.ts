import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * @file settings.store.ts
 * @description Gerenciamento de preferências locais do operador (Task 023).
 * Persiste configurações como Modo Silencioso entre sessões.
 */

interface SettingsState {
  isSilentMode: boolean;
  
  // Actions
  toggleSilentMode: () => void;
  setSilentMode: (value: boolean) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      isSilentMode: false,

      toggleSilentMode: () => set((state) => ({ isSilentMode: !state.isSilentMode })),
      
      setSilentMode: (value) => set({ isSilentMode: value }),
    }),
    {
      name: 'mesaflow-settings-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
