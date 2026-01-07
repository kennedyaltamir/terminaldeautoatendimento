import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '../screens/app/HomeScreen';

const Stack = createNativeStackNavigator();

/**
 * AppStack: Pilha de navegação para usuários autenticados.
 * Preparado para futura expansão com Tabs e sub-rotas operacionais.
 */
export default function AppStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Home" component={HomeScreen} />
    </Stack.Navigator>
  );
}
