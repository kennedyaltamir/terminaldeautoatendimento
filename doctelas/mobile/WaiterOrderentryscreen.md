# 📝 WaiterOrderentryScreen
> **Plataforma:** MOBILE | **Domínio:** WAITER | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Interface de alta performance para garçons realizarem o lançamento de pedidos na mesa. Focada em velocidade de toque e redução de erros de comunicação com a cozinha.

## 2. Estrutura Técnica
- **Header Dinâmico:** Exibe o número da mesa selecionada e o nome do cliente.
- **Category Scroller:** Navegação horizontal por ícones para troca rápida de seção (Bebidas, Lanches, Sobremesas).
- **Product List:** Utiliza `FlashList` (Shopify) para garantir scroll a 60fps mesmo com centenas de itens.

## 3. Elementos Interativos
- **Contador de Quantidade:** Botões de +/- integrados ao card do produto.
- **Campo de Notas:** Acesso rápido para digitar observações (ex: "Sem cebola", "Gelo e limão").
- **Floating Cart Button:** Botão flutuante que exibe o total parcial e leva à revisão do pedido.

## 4. Regras de Negócio (Mobile POS)
- **Volatile Cart:** O carrinho é limpo automaticamente após o envio ou se o garçom trocar de mesa.
- **SLA Awareness:** O tempo de preparo estimado é exibido para que o garçom possa informar o cliente.
- **Offline Queue:** Se a rede cair, o pedido é salvo no `AsyncStorage` e enviado automaticamente quando o sinal retornar.

## 5. Estados da Tela
- **Loading:** Shimmer effects durante o carregamento do cardápio.
- **Search Mode:** Overlay de busca que filtra a lista conforme o garçom digita.
- **Success:** Feedback de "Pedido Enviado" com animação de check.

## 6. Fluxo de Dados
- **Store:** Consome `useWaiterStore` para gerenciar o estado do carrinho.
- **Sync:** Dispara evento `new_order` via WebSocket para atualizar o KDS instantaneamente.

---
*MesaFlow Mobile Kernel v5.0*

