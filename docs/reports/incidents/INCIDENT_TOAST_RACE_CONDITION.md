# 🩺 Diagnóstico Técnico: Falha de Asserção de Toast (Race Condition)

## 1. A Causa Raiz (The Smoking Gun)
A análise dos logs de execução do Playwright revela uma **Condição de Corrida Temporal** entre a duração da notificação (Toast) e o tempo de execução da asserção anterior.

### Evidência do Log
```text
12.9s Expect "not toBeVisible" getByTestId('driver.delivery.active')
5.0s  Expect "toBeVisible" getByText('Entrega finalizada!') -> FAIL
```

### Explicação do Fenômeno
1. O teste clica em "Finalizar".
2. O código dispara `toast.success` (Duração padrão: ~2000ms a 4000ms).
3. O teste entra na linha `await expect(activePanel).not.toBeVisible()`.
4. Por algum motivo (animação de saída, polling do WebSocket ou latência do emulador), o painel leva **12.9 segundos** para desaparecer completamente do DOM.
5. Quando o teste finalmente chega na linha de verificar o Toast, **ele já desapareceu da tela** (pois durou apenas ~4s).

## 2. Diagnóstico Arquitetural
Além do problema de teste, há um risco arquitetural:
- O componente `<Toaster />` está instanciado dentro de `DriverPage`.
- Se, por qualquer motivo, a lógica de `setActiveDeliveryId(null)` causar um *remount* completo do componente `DriverPage` (ao invés de um re-render), o `Toaster` seria desmontado e a mensagem perdida instantaneamente.

## 3. Solução Definitiva
1. **Código:** Elevar o `<Toaster />` para o `AdminLayout` (Singleton de UI), garantindo que ele nunca seja desmontado por mudanças de estado de uma página filha.
2. **Teste:** Inverter a ordem das asserções ou executá-las em paralelo. O Toast é um evento efêmero; sua verificação deve ter prioridade sobre mudanças de estado persistentes.

---
*MesaFlow Kernel L6 — SRE Division*

