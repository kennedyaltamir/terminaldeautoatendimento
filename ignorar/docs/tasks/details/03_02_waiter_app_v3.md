# 📱 Detalhamento Técnico: App do Garçom v3.0 (STAFF-02)

## 1. Problema Atual
A interface atual exige muitos cliques para tarefas repetitivas (como adicionar uma água ou café). Em horários de pico, o garçom perde tempo navegando em menus em vez de atender o cliente.

## 2. Solução Proposta
Transformar o App do Garçom em um **Mobile POS de Alta Performance**.

### 2.1 Funcionalidades de Elite
- **Quick-Action Bar:** Barra fixa no topo com os 5 itens mais vendidos da casa para lançamento com 1 toque.
- **Smart Search:** Busca que prioriza o `short_code` (código numérico) do produto.
- **Haptic Feedback:** Vibrações curtas ao confirmar itens e vibração longa quando a cozinha marca um pedido daquela mesa como "Pronto".
- **Offline Buffer:** Capacidade de salvar até 50 pedidos localmente (Dexie.js) caso o Wi-Fi do salão oscile, sincronizando em background.

## 3. Arquivos a Alterar/Criar
- `frontend/src/components/waiter/QuickActions.tsx`: Novo componente de atalhos.
- `frontend/src/hooks/useHaptics.ts`: Hook para gerenciar vibrações nativas.
- `frontend/src/app/admin/[slug]/waiter/pos/page.tsx`: Refatoração do layout para priorizar velocidade.

## 4. Aplicação Prática
O garçom chega na mesa, digita "10" (código da Coca), sente a vibração de confirmação e o pedido já está na fila do bar antes mesmo dele sair do lado do cliente.
