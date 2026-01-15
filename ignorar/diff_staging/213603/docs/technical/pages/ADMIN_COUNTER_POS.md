# 🏪 Tela: Balcão (PDV Rápido)
**Rota:** `/admin/[slug]/counter`
**Domínio:** ADMIN / OPERATION

## 1. Especificação Visual
- **Layout Split:** Esquerda (Cardápio Rápido), Direita (Carrinho e Pagamento).
- **Grid de Produtos:** Botões grandes para toque rápido.
- **Status de Produção:** Mini-lista lateral de pedidos aguardando retirada.

## 2. Elementos Interagíveis
- **Botão de Produto:** Adiciona 1 unidade ao carrinho instantaneamente.
- **Botão "Dinheiro/Cartão/Pix":** Finaliza a venda com um clique.
- **Input de Troco:** Calculadora automática para pagamentos em espécie.

## 3. Comportamento Esperado
- **Agilidade:** O foco é fechar a venda em menos de 10 segundos.
- **Impressão:** Dispara automaticamente o cupom não fiscal após a confirmação.

## 4. APIs Consumidas
- `GET /api/admin/menu/products`: Carga de itens.
- `POST /api/[slug]/orders`: Criação de pedido com status `delivered` e `paid` imediato.
