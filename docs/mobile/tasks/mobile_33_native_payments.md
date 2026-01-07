# 📱 Task 33: Pagamentos Nativos e QR Code Dinâmico

## 1. Contexto
Implementação da funcionalidade de recebimento financeiro no Mobile POS. O garçom agora pode fechar a conta de uma mesa e apresentar o QR Code Pix dinâmico diretamente no seu dispositivo, eliminando a necessidade de o cliente escanear o QR Code fixo da mesa novamente para pagar.

## 2. Decisões Técnicas
- **QR Code Rendering:** Utilizada a biblioteca `react-native-qrcode-svg` para gerar o código visual a partir da string Pix (EMV) retornada pelo backend. Esta abordagem é superior ao carregamento de imagens externas por ser instantânea e funcionar offline (caso a string já esteja em cache).
- **Payment State:** A `WaiterStore` gerencia o objeto `paymentData`. Ao iniciar um pagamento, o app bloqueia a UI (`isSubmitting`) e aguarda a resposta do backend com o total calculado e os dados do Pix.
- **Manual Confirmation:** Como o sistema de webhooks pode ter latência, incluímos um botão de confirmação manual para o garçom. Isso garante que a mesa possa ser liberada imediatamente após a conferência visual do comprovante no celular do cliente.
- **Navigation Integration:** A `PaymentScreen` foi adicionada à `AppStack`, permitindo que o garçom transite do resumo do pedido para o recebimento com um único clique.

## 3. Arquivos Afetados
- `mobile/package.json` (Nova dependência)
- `mobile/src/store/waiter.store.ts` (Lógica de fechamento)
- `mobile/src/screens/waiter/PaymentScreen.tsx` (Nova interface)
- `mobile/src/navigation/stacks/AppStack.tsx` (Registro de rota)

## 4. Próximos Passos
**Missão 34:** Offline Order Queue — Implementação de fila de pedidos local para resiliência total em quedas de Wi-Fi.

---
*Fase 11 — Janeiro de 2026*
