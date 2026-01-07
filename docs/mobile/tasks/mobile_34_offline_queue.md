# 📱 Task 34: Fila de Pedidos Offline (Contingência POS)

## 1. Contexto
Implementação da resiliência de venda para o Mobile POS. Em ambientes de salão, o Wi-Fi pode oscilar. O garçom deve ser capaz de concluir o lançamento do pedido mesmo sem rede, confiando que o sistema realizará a entrega assim que a conexão retornar.

## 2. Decisões Técnicas
- **Persistência de Contingência:** A `WaiterStore` agora utiliza o middleware `persist` para salvar a `pendingQueue` no `AsyncStorage`. Isso garante que pedidos não enviados não sejam perdidos se o app for fechado ou o dispositivo desligar.
- **Silent Recovery:** O `WaiterSyncService` atua como um worker de fundo, disparado a cada pulso do `GlobalClock`. Ele tenta esvaziar a fila de forma sequencial, respeitando a ordem cronológica dos pedidos.
- **UX de Confiança:** Ao detectar falha de rede no envio, o app exibe uma tela de sucesso alternativa ("Pedido em Fila") com ícone de `WifiOff`, informando ao garçom que a tarefa foi delegada ao motor de sincronia.
- **Idempotência:** O backend já trata o `staff-override` como um sinal de confiança, e a fila local utiliza IDs temporários para evitar duplicidade durante o processo de retry.

## 3. Arquivos Afetados
- `mobile/src/store/waiter.store.ts` (Fila e Persistência)
- `mobile/src/services/waiter.sync.service.ts` (Novo: Worker de sincronia)
- `mobile/src/navigation/stacks/AppStack.tsx` (Orquestração do worker)
- `mobile/src/screens/waiter/OrderReviewScreen.tsx` (UI de contingência)

## 4. Política de Testes
[TEST_EXEMPT: Lógica de persistência e sincronia offline. Validação via Expo Go: 1. Colocar celular em modo avião. 2. Lançar um pedido na mesa. 3. Verificar se aparece a tela "Pedido em Fila". 4. Desativar modo avião. 5. Verificar nos logs do LoggerService se o pedido foi sincronizado.]

---
*Fase 11 — Janeiro de 2026*
