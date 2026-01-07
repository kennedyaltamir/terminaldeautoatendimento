# 📱 Task 24: Resiliência & Recuperação Operacional

## 1. Contexto
Implementação da camada de confiabilidade para o KDS Mobile. Em ambientes de restaurante, quedas de Wi-Fi são comuns. O sistema deve garantir que, ao recuperar a conexão, o estado local seja imediatamente reconciliado com o servidor, evitando que o operador trabalhe com dados desatualizados.

## 2. Decisões Técnicas
- **Sync State:** Introduzida a flag `isSyncing` na `OrdersStore` para diferenciar carregamentos iniciais (`isLoading`) de atualizações de fundo.
- **Reconciliation Trigger:** O `OrdersRealtimeService` agora dispara o callback `onReconnect` assim que o socket abre. A `AppStack` orquestra esse evento chamando `OrdersSyncService.performFullSync`.
- **UI Feedback:** Adicionado um indicador de sincronia ("Sincronizando") no header da `OrdersScreen`, visível apenas durante o processo de reconciliação.
- **Determinismo:** O `performFullSync` invalida o estado local e injeta a verdade absoluta do backend, garantindo consistência.

## 3. Arquivos Afetados
- `mobile/src/store/orders.store.ts` (Estado de sincronia)
- `mobile/src/services/orders.sync.service.ts` (Lógica de reconciliação)
- `mobile/src/screens/orders/OrdersScreen.tsx` (Feedback visual)

## 4. Política de Testes
[TEST_EXEMPT: Lógica de rede e sincronia. A validação deve ser feita via Expo Go: 1. Desativar Wi-Fi. 2. Alterar um pedido via Web Admin. 3. Reativar Wi-Fi no celular. 4. Verificar se o app mobile atualiza o pedido automaticamente e mostra o spinner de sincronia.]

---
*Fase 10 — Janeiro de 2026*
