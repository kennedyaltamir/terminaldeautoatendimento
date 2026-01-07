# 📱 Task 30B: Integração Bluetooth & Descoberta

## 1. Contexto
Implementação da comunicação real com hardware de impressão. O aplicativo agora possui a inteligência para escanear o ambiente, identificar impressoras térmicas e persistir a escolha do operador para uso contínuo.

## 2. Decisões Técnicas
- **Bluetooth Bridge:** Criado o `BluetoothService` com suporte a Mock. Isso permite que a equipe de frontend continue desenvolvendo a UI sem depender de uma impressora física conectada ao computador.
- **Printer Persistence:** A `SettingsStore` agora salva o objeto da impressora selecionada. O fluxo de impressão tenta reconectar automaticamente ao dispositivo salvo antes de cada emissão.
- **UI Picker:** Implementada uma interface de seleção de dispositivos (Picker) que é disparada automaticamente caso o garçom tente imprimir sem ter configurado uma impressora previamente.
- **Error Handling:** O sistema detecta falhas de conexão Bluetooth e invalida a impressora salva, forçando uma nova busca para garantir a resiliência operacional.

## 3. Arquivos Afetados
- `mobile/src/services/bluetooth.service.ts` (Novo)
- `mobile/src/store/settings.store.ts` (Persistência de hardware)
- `mobile/src/services/printer.service.ts` (Integração de fluxo)
- `mobile/src/screens/waiter/OrderReviewScreen.tsx` (UI de seleção e disparo)

## 4. Próximos Passos
**Missão 31:** Implementação de Notificações Push nativas via Firebase para alertas de "Pedido Pronto" e "Chamado de Mesa" com o app em background.

---
*Fase 11 — Janeiro de 2026*
