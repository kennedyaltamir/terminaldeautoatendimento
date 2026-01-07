import React from 'react';
import { useAuthStore } from '../store/auth.store';
import { AuthStack } from './stacks/AuthStack';
import { AppStack } from './stacks/AppStack';

/**
 * AuthGate: Orquestrador soberano da árvore de renderização.
 * Decide qual Stack montar baseado exclusivamente no status semântico.
 */
export const AuthGate = () => {
  const status = useAuthStore((state) => state.status);

  switch (status) {
    case 'authenticated':
      return <AppStack />;

    case 'unauthenticated':
    case 'error':
      return <AuthStack />;

    case 'idle':
    case 'hydrating':
    case 'checking_expiry':
    default:
      return null;
  }
};
