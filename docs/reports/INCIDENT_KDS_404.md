# 🚨 Relatório de Incidente: KDS Vazio e Erro 404

**Data:** 09/01/2026
**Severidade:** ALTA (Bloqueia a operação da cozinha)
**Sintoma:** A tela do KDS carrega mas permanece vazia ("Tudo tranquilo na operação"), mesmo após a criação de pedidos. O console do navegador exibe erro 404 na rota de `service-requests`.

## 1. Arquivos Envolvidos
1.  **`frontend/src/app/admin/[slug]/kitchen/page.tsx`**: O componente React que orquestra o carregamento de dados.
2.  **`app/routers/admin.py`**: O controlador Backend que deveria expor os endpoints administrativos.
3.  **`frontend/src/lib/api.ts`**: O cliente HTTP que faz as chamadas para o backend.

## 2. Análise de Causa Raiz (As 3 Principais Hipóteses)

### 🔴 Causa 1: Quebra de Promessa (Promise.all Failure) - *Mais Provável*
O código do frontend utiliza `Promise.all` para carregar Pedidos e Chamados de Garçom simultaneamente:
```typescript
const [ordersData, requestsData] = await Promise.all([
  getKitchenOrders(slug),
  getServiceRequests(slug) // <--- ESTE FALHA COM 404
]);
setOrders(ordersData); // <--- ESTA LINHA NUNCA É EXECUTADA
```
Como a rota `/api/admin/.../service-requests` retorna **404 Not Found**, a `Promise.all` rejeita a execução inteira, caindo no bloco `catch`. Consequentemente, o estado `orders` nunca é atualizado, mantendo a lista vazia.

### 🟠 Causa 2: Rota Inexistente no Backend
O endpoint `GET /{company_slug}/service-requests` provavelmente não foi definido ou registrado no `app/routers/admin.py`. O sistema tentou consumir um recurso que ainda não foi implementado no Backend.

### 🟡 Causa 3: Falha Silenciosa de WebSocket (Redis)
Os logs mostram `WARNING: Redis indisponível`. Sem Redis, o backend usa memória local. Se o processo que recebe o Webhook de pagamento (ou script de simulação) for diferente do processo que segura o WebSocket (Gunicorn/Uvicorn workers), o evento de "Novo Pedido" não é propagado, e a tela não atualiza sozinha. Porém, isso não explica por que o *refresh* manual (F5) também falha (o que reforça a Causa 1).

## 3. Plano de Ação
1.  Executar o script de diagnóstico abaixo para confirmar a ausência da rota.
2.  Implementar o endpoint faltante no Backend.
3.  Blindar o Frontend para que a falha em um serviço secundário (Chamados) não derrube o serviço principal (Pedidos).
