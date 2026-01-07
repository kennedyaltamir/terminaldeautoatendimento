import React, { useEffect } from 'react';
import { useAuthStore } from '../store/auth.store';
import { AuthGate } from './AuthGate';

/**
 * RootNavigator: Ponto de entrada da lógica de navegação.
 * Inicia o ciclo de vida da sessão e renderiza o Gate.
 */
export default function RootNavigator() {
  const hydrate = useAuthStore((state) => state.hydrate);

  useEffect(() => {
    // Dispara a hidratação (leitura de tokens e validação temporal) no boot.
    hydrate();
  }, [hydrate]);

  return <AuthGate />;
}
