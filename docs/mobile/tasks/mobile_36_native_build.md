# 📱 Task 36: Build & Smoke Test Nativo (Hotfix v1.1)

## 1. Contexto
O primeiro build falhou na fase de bundling devido ao uso de tags Web (`div`) e propriedades incompatíveis (`className`) em componentes nativos.

## 2. Decisões Técnicas
- **Native Hardening:** Substituição de `div` por `View` e `className` por `style` em `OrdersScreen.tsx`.
- **Singleton Fix:** Correção do `BluetoothService.getInstance()` que retornava a instância do Logger por erro de digitação.
- **Metro Config Reset:** Remoção do alias de `lucide-react-native` para evitar que o bundler tentasse usar a versão Web da biblioteca.

## 3. Status
- [x] Purificação de código nativo.
- [x] Correção de lógica de serviços.
- [x] Ajuste de configuração do Metro.

---
*Fase 12 — Janeiro de 2026*
