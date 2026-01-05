# 🖥️ Especificação Funcional: Dashboard do Usuário

Este documento descreve o comportamento esperado, dados exibidos e ações disponíveis em cada tela do Painel Administrativo (`/admin/[slug]/...`).

---

## 1. Visão Geral (Dashboard)
**Rota:** `/dashboard`
**Objetivo:** Visão macro da saúde do negócio em tempo real.

### 📊 KPIs (Cards Superiores)
1.  **Faturamento (Hoje):** Soma total de pedidos com `payment_status = 'paid'`.
    *   *Comportamento:* Atualiza em tempo real via WebSocket ou Polling (30s).
2.  **Total de Pedidos:** Contagem de pedidos (exclui cancelados).
3.  **Ticket Médio:** Faturamento / Nº Pedidos.

### 📈 Gráficos
1.  **Evolução de Vendas (Área):** Eixo X = Dias (últimos 7 ou 30), Eixo Y = Valor (R$).
2.  **Horários de Pico (Barras):** Heatmap de vendas por hora (00h - 23h). Ajuda na escala de funcionários.
3.  **Top Produtos (Lista/Barras):** Ranking dos 5 itens mais vendidos por receita.

### 🔘 Ações
- **Filtro de Período:** Botões "Hoje", "7 Dias", "Mês". Recarrega os gráficos.
- **Exportar CSV:** Baixa relatório detalhado de vendas do período selecionado.

---

## 2. Gestão de Franquias (Apenas Dono)
**Rota:** `/franchise`
**Objetivo:** Visão consolidada para donos de múltiplas unidades.

### 📋 Tabela de Lojas
- **Colunas:** Nome da Loja, Faturamento (Hoje), Pedidos (Hoje), Ticket Médio.
- **Ação:** Botão "Acessar" que redireciona para o Dashboard individual daquela loja.

---

## 3. Cardápio (Menu Engineering)
**Rota:** `/menu`
**Objetivo:** Gestão do catálogo de produtos.

### 📂 Categorias
- **Visualização:** Lista horizontal ou vertical.
- **Ações:** Criar, Editar (Nome, Ordem), Excluir (Cascade: avisa se tiver produtos).
- **Agendamento:** Configurar dias da semana/horários que a categoria aparece.

### 🍔 Produtos
- **Card do Produto:** Foto, Nome, Preço, Status (Ativo/Pausado).
- **Edição:**
    - **Básico:** Nome, Descrição, Preço.
    - **Estação:** Definir se imprime na Cozinha ou Bar.
    - **Estoque:** Ativar `track_stock` e definir quantidade.
    - **Ficha Técnica:** Vincular ingredientes (abre modal de receita).
- **Adicionais (Grupos):**
    - Criar grupos (ex: "Ponto da Carne").
    - Definir Min/Max de seleção.
    - Adicionar opções com preço extra.

---

## 4. Estoque (Inventory)
**Rota:** `/inventory`
**Objetivo:** Controle de insumos e custos (CMV).

### 📦 Ingredientes
- **Lista:** Nome, Unidade (kg, un, l), Estoque Atual, Custo Unitário.
- **Ações:**
    - **Entrada:** Adicionar quantidade (compra).
    - **Ajuste:** Correção manual de quebra/perda.
- **Alerta:** Destaque visual (Vermelho) se `current_stock` < `min_stock_alert`.

### 🛒 Compras
- **Sugestão Automática:** Botão que gera uma lista de compras baseada no déficit de estoque.
- **Impressão:** Gerar PDF da ordem de compra por fornecedor.

---

## 5. Mesas (QR Codes)
**Rota:** `/tables`
**Objetivo:** Gestão física do salão.

### 🪑 Grid de Mesas
- **Visual:** Cards representando cada mesa.
- **Status:**
    - 🟢 **Livre:** Pode ser aberta.
    - 🔴 **Ocupada:** Mostra nome do cliente, tempo decorrido e total gasto.
    - 🟡 **Chamado:** Piscando se houver solicitação de serviço.
- **Ações:**
    - **Criar:** Individual ou em Lote (ex: 1 a 50).
    - **Imprimir:** Gerar PDF com o QR Code da mesa.
    - **Abrir/Fechar:** Manualmente pelo gerente.

---

## 6. Marketing & IA
**Rota:** `/marketing`
**Objetivo:** Ferramentas de crescimento e retenção.

### 🧠 Motor de IA
- **Status:** Mostra última execução do treino.
- **Ação:** "Treinar IA Agora" -> Dispara job que analisa histórico e atualiza recomendações de Upsell.

### 🤝 Fidelidade
- **Config:** Slider para definir % de Cashback (0% a 20%).
- **Visualização:** Exemplo de quanto o cliente ganha em uma compra de R$ 100.

### 📱 Automação (WhatsApp)
- **Status:** Conectado/Desconectado (Evolution API).
- **Templates:** Edição das mensagens automáticas ("Pedido Pronto", "Saiu para Entrega").

---

## 7. Equipe (Team)
**Rota:** `/team`
**Objetivo:** Controle de acesso (RBAC).

### 👥 Lista de Membros
- **Colunas:** Nome, Email, Cargo (Role).
- **Cargos Suportados:**
    - **Gerente:** Acesso total (menos dados sensíveis do dono).
    - **Garçom:** Acesso ao App Mobile (`/waiter`) e Mesas.
    - **Cozinha:** Acesso apenas ao KDS (`/kitchen`).
    - **Entregador:** Acesso apenas ao App Driver (`/driver`).
- **Ação:** Adicionar/Remover membro, Resetar senha.

---

## 8. Histórico
**Rota:** `/history`
**Objetivo:** Auditoria e consulta de pedidos passados.

### 📜 Lista de Pedidos
- **Filtros:** Data, Status, Tipo (Mesa/Delivery).
- **Detalhes:** Ao clicar, abre modal com itens, logs de status e pagamentos.
- **Fiscal:**
    - Badge de status (Pendente, Emitida, Erro).
    - Botão "Emitir NFC-e" (se pendente).
    - Link para Download PDF/XML (se emitida).

---

## 9. Configurações
**Rota:** `/settings`
**Objetivo:** Personalização da loja.

### 🎨 Geral & Marca
- **Identidade:** Upload de Logo e Banner.
- **Cores:** Picker para Cor Primária (Botões/Destaques).
- **Horários:** Abertura e Fechamento (Bloqueio automático do cardápio).

### 💳 Financeiro
- **Pagamento:** Conectar Mercado Pago (OAuth) ou Chave Pix Manual.
- **Taxas:** Definir Taxa de Entrega Fixa.

### 🧾 Assinatura (Billing)
- **Plano Atual:** Free ou Pro.
- **Ação:** "Assinar Pro" (Checkout Stripe) ou "Gerenciar Assinatura" (Portal Stripe).
