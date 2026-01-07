import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import RootNavigator from './src/navigation/RootNavigator';

/**
 * App Bootstrap: Inicializa o container de navegação e o roteador mestre.
 * Este arquivo é validado pelo script verify_mobile_navigation.py.
 */
export default function App() {
  return (
    <NavigationContainer>
      <RootNavigator />
      <StatusBar style="light" />
    </NavigationContainer>
  );
}
