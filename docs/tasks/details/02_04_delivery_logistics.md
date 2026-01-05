# 🛵 Detalhamento Técnico: Logística & Zonas de Entrega (UX-04)

## 1. Problema Atual
A taxa de entrega é única (fixa). Isso gera prejuízo em entregas longas ou impede vendas em raios curtos onde a taxa poderia ser menor.

## 2. Solução Proposta (Aba Financeiro)
Implementar um motor de regras para Delivery.

### 2.1 Funcionalidades
- **Zonas por Raio:** Definir taxas diferentes por distância (ex: 0-2km: R$5, 2-5km: R$10).
- **Pedido Mínimo:** Bloquear o checkout se o subtotal for inferior ao configurado.
- **Frete Grátis:** Configurar valor de compra para isenção de taxa.
- **Tempo Estimado:** Campo para o usuário informar o tempo médio (ex: 40-60 min).

## 3. Arquivos a Alterar/Criar
- `app/models.py`: Tabela `DeliveryZone` (N:1 com Company).
- `app/routers/public.py`: Lógica de validação de pedido mínimo no `create_order`.
- `frontend/src/components/menu/Cart.tsx`: Exibir aviso "Faltam R$ X para frete grátis".

## 4. Testes
- Teste unitário para cálculo de taxa baseado na distância (Mock de coordenadas).
- Teste de integração para bloqueio de pedido abaixo do valor mínimo.
