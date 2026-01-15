# 📱 Tela: Cardápio Público (PWA Cliente)
**Rota:** `/[slug]/menu`
**Domínio:** FRONTEND / PUBLIC

## 1. Especificação Visual
- **Header:** Logo da empresa, Nome, Botão de Chamada de Garçom (se habilitado) e Ícone de Comanda.
- **Navegação:** Barra horizontal de categorias (Sticky).
- **Lista:** Cards de produtos com Imagem, Nome, Descrição curta e Preço.
- **Footer:** Barra de "Ver Carrinho" com total acumulado.

## 2. Elementos Interagíveis
- **Card de Produto:** Abre o `ProductModal`.
- **Botão "+":** Adição rápida ao carrinho (incremento).
- **Barra de Busca:** Filtro client-side por nome ou tags.
- **Botão "Chamar Garçom":** Dispara evento WebSocket `waiter_call`.

## 3. Comportamento Esperado
- **Offline:** Se a rede cair, a tela exibe o banner `NetworkStatus` e permite continuar navegando nos itens cacheados (Dexie).
- **Sincronia:** Se um produto for marcado como "Indisponível" no Admin, ele deve sumir ou ficar desabilitado nesta tela em < 2s via WebSocket.
- **Deep Link:** Se a URL contiver `?table=12`, o sistema deve realizar o check-in automático na mesa 12.

## 4. APIs Consumidas
- `GET /api/{slug}/menu`: Carga inicial de dados.
- `POST /api/{slug}/orders`: Envio do pedido final.
- `GET /api/{slug}/wallet/{phone}`: Consulta de cashback.
