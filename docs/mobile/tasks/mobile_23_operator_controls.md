# 📱 Task 23: Controles Operacionais do Operador

## 1. Contexto
Implementação da agência do operador sobre o sistema de alertas. O objetivo é permitir que o KDS Mobile seja silenciado em momentos de alta demanda ou por preferência da praça de produção, mantendo a integridade visual do SLA.

## 2. Decisões Técnicas
- **Settings Store:** Criada utilizando Zustand com o middleware `persist`. Isso garante que a escolha do "Silent Mode" sobreviva ao fechamento do aplicativo.
- **AsyncStorage Adapter:** Utilizado como motor de persistência para o estado de configurações.
- **Alert Suppression:** A `OrdersStore` agora atua como um filtro, consultando a `SettingsStore` antes de disparar o `AlertsOutputService`.
- **UI Feedback:** Adicionado um toggle visual no header da `OrdersScreen` com ícones semânticos (`Bell` / `BellOff`).

## 3. Arquivos Afetados
- `mobile/src/store/settings.store.ts` (Novo)
- `mobile/src/store/orders.store.ts` (Lógica de supressão)
- `mobile/src/screens/orders/OrdersScreen.tsx` (Interface de controle)

## 4. Política de Testes
[TEST_EXEMPT: Funcionalidade de UI e persistência local. A validação deve ser feita via Expo Go, alternando o Silent Mode e verificando se a vibração cessa em pedidos CRITICAL/BREACHED.]

---
*Fase 10 — Janeiro de 2026*
