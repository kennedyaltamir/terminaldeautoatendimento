
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { WaiterDashboard } from '../../screens/waiter/WaiterDashboard';
import { KitchenDashboard } from '../../screens/kitchen/KitchenDashboard';
import { DriverDashboard } from '../../screens/driver/DriverDashboard';
import { useAuthStore } from '../../store/auth.store';
import { colors } from '../../ui/tokens/colors';

const Stack = createNativeStackNavigator();

/**
 * AppStack: Pilha de navegação operacional.
 * FIX: Importações nomeadas para todos os Dashboards.
 */
export const AppStack = () => {
  const user = useAuthStore(state => state.user);

  const getInitialRoute = () => {
    if (user?.role === 'kitchen') return 'KitchenHome';
    if (user?.role === 'driver') return 'DriverHome';
    return 'WaiterHome';
  };

  return (
    <Stack.Navigator 
      initialRouteName={getInitialRoute()}
      screenOptions={{ 
        headerShown: false,
        contentStyle: { backgroundColor: colors.background } 
      }}
    >
      <Stack.Screen name="WaiterHome" component={WaiterDashboard} />
      <Stack.Screen name="KitchenHome" component={KitchenDashboard} />
      <Stack.Screen name="DriverHome" component={DriverDashboard} />
    </Stack.Navigator>
  );
};

