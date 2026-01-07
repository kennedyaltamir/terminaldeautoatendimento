import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * SettingsState: Gerencia preferências locais do dispositivo.
 * Evoluído na Missão 30B para persistir a impressora selecionada.
 */

interface BluetoothPrinter {
  id: string;
  name: string;
  address: string;
}

interface SettingsState {
  isSilentMode: boolean;
  vibrationEnabled: boolean;
  selectedPrinter: BluetoothPrinter | null;
  
  // Actions
  setSilentMode: (enabled: boolean) => void;
  toggleSilentMode: () => void;
  setSelectedPrinter: (printer: BluetoothPrinter | null) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      isSilentMode: false,
      vibrationEnabled: true,
      selectedPrinter: null,

      setSilentMode: (enabled) => set({ isSilentMode: enabled }),
      
      toggleSilentMode: () => set((state) => ({ 
        isSilentMode: !state.isSilentMode 
      })),

      setSelectedPrinter: (printer) => set({ selectedPrinter: printer }),
    }),
    {
      name: 'mesaflow-operator-settings',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
