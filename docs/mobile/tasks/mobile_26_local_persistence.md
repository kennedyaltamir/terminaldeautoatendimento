# 📱 Task 26: Persistência Local & Boot Determinístico

## 1. Contexto
Implementação do suporte offline real para o KDS Mobile. O objetivo é garantir que o aplicativo seja resiliente a reinicializações em ambientes sem conectividade, exibindo o último estado válido dos pedidos imediatamente após o boot.

## 2. Decisões Técnicas
- **Orders Persistence:** A `OrdersStore` agora utiliza o middleware `persist` do Zustand. A lista de pedidos é salva no `AsyncStorage` a cada atualização.
- **Hydration Guard:** Introduzida a flag `isHydrated`. A UI agora aguarda a leitura do cache local antes de tentar realizar o primeiro fetch ou renderizar a lista vazia, evitando o "flicker" de dados.
- **Stale-While-Revalidate:** Ao abrir o app, os dados locais são exibidos instantaneamente. O sistema tenta um fetch em background; se falhar, o operador continua vendo os dados locais com o aviso de "Conexão Perdida" (Missão 25).
- **Selective Persistence:** Apenas a lista de `orders` é persistida. Estados voláteis como `isLoading`, `isSyncing` e `error` são resetados a cada boot para evitar estados inconsistentes.

## 3. Arquivos Afetados
- `mobile/src/store/orders.store.ts` (Persistência e Hydration)
- `scripts/tests/test_mobile_integration_contracts.py` (Fix de teste de refresh)
- `mobile/src/services/orders.realtime.service.ts` (Hardening de erro)

## 4. Política de Testes
[TEST_EXEMPT: Persistência local. Validação via Expo Go: 1. Carregar pedidos. 2. Fechar o app totalmente. 3. Desativar internet. 4. Abrir o app. 5. Verificar se os pedidos aparecem instantaneamente.]

---
*Fase 10 — Janeiro de 2026*
