# 👨‍🍳 Especificação Funcional: Monitor de Cozinha (KDS)

## 1. Visão Geral
Interface de alta visibilidade para tablets, focada em organizar a fila de produção e garantir o cumprimento do SLA.

## 2. Telas e Comportamentos

### 2.1. Fila de Produção (Main View)
- **Cards de Pedido:** Ordenados por tempo de chegada (mais antigos primeiro).
- **SLA Timer:**
    - 0-10 min: Borda Verde.
    - 10-20 min: Borda Amarela.
    - >20 min: Borda Vermelha + Alerta Sonoro.
- **Ações de Status:**
    - **Botão "Iniciar":** Muda status para `preparing`. Notifica o cliente via PWA.
    - **Botão "Pronto":** Muda status para `ready`. Faz o celular do garçom vibrar.
- **Agrupador de Itens:** Painel lateral que soma itens idênticos (ex: "Total: 12 Hambúrgueres na chapa").

### 2.2. Gestão de Estoque (Regra 86)
- **Acesso:** Ícone de "Caixa" no header.
- **Comportamento:** Lista de produtos com toggle de disponibilidade.
- **Impacto:** Ao desativar um item aqui, ele some instantaneamente do cardápio digital do cliente (WebSocket broadcast).

### 2.3. Histórico e Recall
- **Acesso:** Aba "Finalizados".
- **Comportamento:** Permite ver os últimos 20 pedidos concluídos.
- **Recall:** Botão para desfazer a finalização caso o prato precise voltar para a cozinha.

## 3. Regras de Sincronização
- **Setorização:** O KDS pode ser filtrado por "Estação" (ex: Tela do Bar só vê bebidas).
- **Persistence:** O estado do timer é calculado no servidor para evitar reset em caso de refresh da página.
