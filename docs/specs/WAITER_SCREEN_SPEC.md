# 📱 Especificação Funcional: App do Garçom (Mobile POS)

## 1. Visão Geral
Interface nativa (React Native) focada em agilidade de salão. O garçom deve conseguir realizar operações críticas com o mínimo de toques possível.

## 2. Telas e Comportamentos

### 2.1. Mapa de Mesas (Home)
- **Visual:** Grid de cards representando as mesas físicas.
- **Estados Visuais:**
    - 🟢 **Verde (Livre):** Toque abre modal de "Abrir Mesa" (pede nome do cliente).
    - 🟠 **Laranja (Ocupada):** Mostra nome do cliente, tempo de permanência e subtotal atual.
    - 🔴 **Vermelho (Alerta):** Piscando se houver chamado de garçom pendente.
- **Sincronização:** Atualiza via WebSocket sempre que um cliente pede pelo QR Code ou outra mesa é alterada.

### 2.2. Lançamento de Pedido
- **Busca Rápida:** Input de texto que filtra por nome ou `short_code` (ex: "10" para Coca-Cola).
- **Categorias:** Abas horizontais para navegação rápida.
- **Carrinho Local:** Permite adicionar múltiplos itens antes de enviar para a cozinha.
- **Observações:** Campo de texto por item (ex: "Sem cebola").
- **Ação Final:** Botão "Enviar para Cozinha" dispara evento para o KDS e persiste no DB.

### 2.3. Fechamento e Pagamento
- **Resumo da Comanda:** Lista detalhada de todos os pedidos da sessão.
- **Divisão de Conta (Split):**
    - Por valor igual (ex: dividir por 4).
    - Por itens selecionados.
- **Métodos de Pagamento:**
    - **Pix Dinâmico:** Gera QR Code na tela do celular do garçom.
    - **Cartão/Dinheiro:** Registra a baixa no sistema e libera a mesa.
- **Calculadora de Troco:** Interface numérica para pagamentos em espécie.

## 3. Regras de Sincronização
- **Auth:** Utiliza o mesmo JWT do login administrativo, validando a role `cashier` ou `manager`.
- **Database:** Todas as operações gravam o `employee_id` para auditoria de gorjetas e performance.
