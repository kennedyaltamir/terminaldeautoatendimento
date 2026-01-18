# 📱 Software Design Specification: Mobile
**Domínio:** MOBILE | **Versão:** 5.0

## 1. Stacks de Navegação
- **RootNavigator:** Orquestrador inicial. Decide entre `AuthGate` e `LoadingScreen`.
- **AuthStack:** Telas de Login e Recuperação de Senha.
- **AppStack:** Navegação operacional baseada em Roles (Garçom, Cozinha, Driver).

## 2. Serviços Nativos
- **BluetoothService:** Descoberta e pareamento de impressoras térmicas.
- **NotificationService:** Integração com FCM (Firebase) para alertas de "Pedido Pronto".
- **LocationService:** Captura de coordenadas em background para o módulo de entrega.

## 3. Sincronização de Estado
Utiliza a `useAuthStore` (Zustand) com persistência no `Expo SecureStore` para garantir que a sessão sobreviva ao fechamento do app. O `isHydrated` bloqueia a UI até que os tokens sejam validados.

