import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuthStore } from '../store/auth.store';
import { LoginScreen } from '../screens/auth/LoginScreen';
import { WaiterDashboard } from '../screens/waiter/WaiterDashboard';
import { KitchenDashboard } from '../screens/kitchen/KitchenDashboard';
import { DriverDashboard } from '../screens/driver/DriverDashboard';
import { View, ActivityIndicator } from 'react-native';

const Stack = createNativeStackNavigator();

export function RootNavigator() {
  const { isAuthenticated, isLoading, user } = useAuthStore();

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#0f172a' }}>
        <ActivityIndicator size="large" color="#ea580c" />
      </View>
    );
  }

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {!isAuthenticated ? (
        <Stack.Screen name="Login" component={LoginScreen} />
      ) : (
        <>
          {/* Roteamento condicional baseado no cargo para definir a tela inicial */}
          {user?.role === 'kitchen' ? (
            <Stack.Screen name="KitchenHome" component={KitchenDashboard} />
          ) : user?.role === 'driver' ? (
            <Stack.Screen name="DriverHome" component={DriverDashboard} />
          ) : (
            <Stack.Screen name="WaiterHome" component={WaiterDashboard} />
          )}
          
          {/* Telas auxiliares acessíveis por navegação */}
          <Stack.Screen name="WaiterDashboard" component={WaiterDashboard} />
          <Stack.Screen name="KitchenDashboard" component={KitchenDashboard} />
          <Stack.Screen name="DriverDashboard" component={DriverDashboard} />
        </>
      )}
    </Stack.Navigator>
  );
}
