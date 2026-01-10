import React from 'react';
import { useAuthStore } from '../store/auth.store';
import { AuthStack } from './stacks/AuthStack';
import { AppStack } from './stacks/AppStack';

/**
 * @file AuthGate.tsx
 * @description Componente de fronteira soberana (Task 14B).
 * Responsável único por decidir qual árvore de navegação montar
 * baseado no estado semântico da autenticação.
 */
export const AuthGate = () => {
  const status = useAuthStore((state) => state.status);

  // Mapeamento de Estados para Stacks
  switch (status) {
    case 'authenticated':
      return <AppStack />;

    case 'unauthenticated':
    case 'error':
      return <AuthStack />;

    // Estados de transição (Splash Screen nativa deve persistir)
    case 'idle':
    case 'hydrating':
    case 'checking_expiry':
    default:
      return null;
  }
};
