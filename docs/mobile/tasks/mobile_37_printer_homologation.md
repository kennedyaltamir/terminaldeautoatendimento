# 📱 Task 37: Homologação de Impressão em Campo

## 1. Contexto
Com o aplicativo rodando em modo nativo (Missão 36), é necessário validar a integração com hardware real. Esta missão implementa uma interface de diagnóstico para testar a comunicação Bluetooth e a fidelidade dos comandos ESC/POS gerados pelo sistema.

## 2. Decisões Técnicas
- **Printer Debug Screen:** Criada uma tela isolada para testes de hardware. Isso permite que o suporte técnico valide a impressora do cliente sem precisar realizar um pedido real.
- **Raw Buffer Test:** O teste de impressão envia um pedido fictício ("TEST-123") para validar:
    - Alinhamento de texto.
    - Formatação de preços.
    - Comando de corte de papel (Cut).
    - Abertura de gaveta (se houver).
- **Navigation Integration:** A rota `PrinterDebug` foi adicionada à `AppStack`, permitindo acesso rápido durante o setup inicial do restaurante.

## 3. Arquivos Afetados
- `mobile/src/screens/waiter/PrinterDebugScreen.tsx` (Novo)
- `mobile/src/navigation/stacks/AppStack.tsx` (Registro de rota)
- `docs/TASKS.md` (Update de status)

## 4. Política de Testes
[TEST_EXEMPT: Teste de hardware físico. A validação deve ser feita com uma impressora Bluetooth real pareada ao dispositivo.]

---
*Fase 12 — Janeiro de 2026*
