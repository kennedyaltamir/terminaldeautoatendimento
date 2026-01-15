# 📱 Tela: App do Garçom (Mobile POS)
**Tela:** `WaiterTablesScreen` / `OrderEntryScreen`
**Domínio:** MOBILE / OPERATION

## 1. Especificação Visual
- **Mapa de Mesas:** Grid de botões representando as mesas físicas.
- **Status Visual:**
    - **Cinza:** Livre.
    - **Laranja:** Ocupada (com consumo).
    - **Vermelho Piscante:** Chamado de ajuda pendente.
- **Carrinho de Lançamento:** Lista vertical com busca rápida por código ou nome.

## 2. Elementos Interagíveis
- **Mesa:** Clique abre o detalhe da conta ou inicia novo pedido.
- **Busca de Produto:** Input com foco automático ao abrir a tela de lançamento.
- **Botão "Fechar Conta":** Abre o modal de pagamento (Pix/Dinheiro/Cartão).
- **Botão "Transferir":** Inicia fluxo de troca de mesa.

## 3. Comportamento Esperado
- **Offline-First:** O garçom pode lançar o pedido mesmo sem Wi-Fi. O pedido fica na `pendingQueue` e sincroniza automaticamente ao detectar rede.
- **Impressão:** Botão de "Imprimir Conferência" envia comandos ESC/POS via Bluetooth para a impressora pareada.
- **Segurança:** Exige PIN de acesso caso o garçom tente acessar uma mesa já ocupada por outro staff.

## 4. APIs Consumidas
- `GET /api/admin/tables`: Status do salão.
- `POST /api/admin/tables/{id}/open`: Abertura de sessão.
- `POST /api/admin/orders`: Lançamento de itens.
