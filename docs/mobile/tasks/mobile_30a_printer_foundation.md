# 📱 Task 30A: Fundação de Impressão Bluetooth & ESC/POS

## 1. Contexto
Implementação da camada de inteligência para emissão de tickets físicos. O Mobile POS agora é capaz de converter pedidos em comandos binários ESC/POS, preparando o terreno para a integração direta com hardware Bluetooth.

## 2. Decisões Técnicas
- **Native Encoder:** Criado o `EscPosEncoder` para gerar `Uint8Array` diretamente. Isso evita a dependência de bibliotecas de terceiros pesadas para a lógica de formatação básica.
- **Normalization:** Implementada normalização de strings para ASCII puro, garantindo que acentos não quebrem a impressão em dispositivos de baixo custo.
- **Post-Sale Flow:** A `OrderReviewScreen` foi evoluída para uma "Success View" após o envio, permitindo que o garçom escolha imprimir o ticket antes de retornar ao mapa de mesas.
- **State Preservation:** A `WaiterStore` agora mantém o `lastSubmittedOrder` para garantir que os dados de impressão estejam disponíveis mesmo após o carrinho ser limpo.

## 3. Arquivos Afetados
- `mobile/src/lib/escpos.encoder.ts` (Novo)
- `mobile/src/services/printer.service.ts` (Novo)
- `mobile/src/store/waiter.store.ts` (Persistência de último pedido)
- `mobile/src/screens/waiter/OrderReviewScreen.tsx` (UI de sucesso e impressão)

## 4. Próximos Passos
**Missão 30B:** Integração com `react-native-ble-plx` ou similar para descoberta de dispositivos e envio real do buffer via Bluetooth.

---
*Fase 11 — Janeiro de 2026*
