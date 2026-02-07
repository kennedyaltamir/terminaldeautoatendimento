
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { LoginScreen } from '../../screens/auth/LoginScreen';

const Stack = createNativeStackNavigator();

/**
 * AuthStack: Pilha de navegação para usuários não autenticados.
 * FIX: Importação nomeada de LoginScreen para evitar 'undefined'.
 */
export const AuthStack = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Login" component={LoginScreen} />
    </Stack.Navigator>
  );
};

