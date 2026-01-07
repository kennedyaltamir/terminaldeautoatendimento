# 📱 Task 25: Estados de Erro & Falhas Operacionais

## 1. Contexto
Implementação da transparência operacional no KDS Mobile. O sistema deve comunicar falhas de rede e de backend de forma proativa, garantindo que o operador não tome decisões baseadas em dados obsoletos sem saber que a sincronia está interrompida.

## 2. Decisões Técnicas
- **Socket Health Tracking:** A `OrdersStore` agora possui a flag `isSocketConnected`, atualizada em tempo real pelo `OrdersRealtimeService`.
- **Offline Banner:** Implementado um banner de alta visibilidade no topo da tela que aparece automaticamente quando o WebSocket é desconectado.
- **Granular Error Handling:**
    - **Hard Error:** Quando a lista inicial falha, exibe tela de erro com botão de retry.
    - **Soft Error:** Quando uma ação (ex: mudar status) falha, exibe um erro temporário na Store sem bloquear a visualização da lista.
- **Stale Data Policy:** O app mantém os pedidos em tela mesmo em erro, mas sinaliza a falta de sincronia.

## 3. Arquivos Afetados
- `mobile/src/store/orders.store.ts` (Novos estados de erro e socket)
- `mobile/src/services/orders.realtime.service.ts` (Notificação de status de conexão)
- `mobile/src/screens/orders/OrdersScreen.tsx` (Banner de rede e Error UI)

## 4. Política de Testes
[TEST_EXEMPT: Lógica de UI e estados de erro. Validação via Expo Go: 1. Abrir o app. 2. Colocar em modo avião. 3. Verificar se o banner vermelho aparece. 4. Tentar avançar um pedido e verificar se o erro temporário é tratado.]

---
*Fase 10 — Janeiro de 2026*
