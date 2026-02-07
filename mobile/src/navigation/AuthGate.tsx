
import React from 'react';
import { useAuthStore } from '../store/auth.store';
import { useErrorStore } from '../store/error.store';
import { AuthStack } from './stacks/AuthStack';
import { AppStack } from './stacks/AppStack';
import { ErrorStateView } from '../components/ui/ErrorStateView';

/**
 * AuthGate: Decide qual árvore de navegação renderizar.
 * FIX: Importações nomeadas das Stacks.
 */
export const AuthGate = () => {
  const status = useAuthStore((state) => state.status);
  const logout = useAuthStore((state) => state.logout);
  const { currentError, clearError } = useErrorStore();

  if (currentError) {
    return (
      <ErrorStateView 
        type={currentError} 
        onRetry={() => clearError()} 
        onAction={currentError === '403' ? logout : undefined}
        actionLabel={currentError === '403' ? "Voltar para Login" : undefined}
      />
    );
  }

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

