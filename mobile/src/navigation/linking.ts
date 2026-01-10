import { LinkingOptions } from '@react-navigation/native';
import * as Linking from 'expo-linking';

/**
 * Configuração de Deep Linking para o React Navigation.
 * Permite abrir o app via esquema 'mesaflow://' e mapear URLs para rotas.
 */
export const linking: LinkingOptions<any> = {
  prefixes: [Linking.createURL('/'), 'mesaflow://'],
  config: {
    screens: {
      // Mapeamento de rotas para Deep Link
      // Ex: mesaflow://table/1?code=123456
      AppStack: {
        screens: {
          OrderEntry: 'table/:tableId',
        },
      },
      // Fallback para Auth se não estiver logado é tratado pelo AuthGate
    },
  },
};
