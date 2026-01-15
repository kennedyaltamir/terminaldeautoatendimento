
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { AuthGate } from './src/navigation/AuthGate';
import { useAuthStore } from './src/store/auth.store';
import { GlobalErrorBoundary } from './src/components/ui/GlobalErrorBoundary';
import { initSentry } from './src/config/sentry';
import * as Sentry from '@sentry/react-native';

// Inicializa telemetria antes do componente montar
initSentry();

function App() {
  const hydrate = useAuthStore((state) => state.hydrate);

  React.useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <GlobalErrorBoundary>
      <NavigationContainer>
        <StatusBar style="light" />
        <AuthGate />
      </NavigationContainer>
    </GlobalErrorBoundary>
  );
}

// Wrap com Sentry para capturar erros de navegação e renderização
export default Sentry.wrap(App);

