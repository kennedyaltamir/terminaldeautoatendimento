# 🛒 AdminWaiterPosPage
> **Plataforma:** WEB | **Domínio:** OPERACIONAL | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Interface de Ponto de Venda (PDV) otimizada para desktops e tablets. Permite que o staff realize o atendimento completo de uma mesa ou balcão, desde a abertura da comanda até o processamento de pagamentos complexos (divisão de conta).

## 2. Estrutura e Layout
- **Menu Lateral:** Navegação rápida por categorias de produtos.
- **Grid de Produtos:** Cards com fotos, preços e badges de disponibilidade.
- **Carrinho Ativo (Sidebar Direita):** Listagem de itens selecionados, campo de observações e totalizador em tempo real.
- **Barra de Ações:** Botões de "Chamar Garçom", "Transferir Mesa" e "Fechar Conta".

## 3. Elementos Interativos
- **Busca Instantânea:** Filtro de produtos por nome ou código (SKU) com debounce de 300ms.
- **Modificador de Itens:** Modal para seleção de opcionais (ex: ponto da carne, adicionais).
- **Split Bill (Divisão de Conta):** Interface para dividir o total por número de pessoas ou por itens específicos.

## 4. Regras de Negócio
- **Trava de Estoque:** Itens com `stock_quantity === 0` são desabilitados automaticamente (Regra 86).
- **Taxa de Serviço:** Aplicação dinâmica da porcentagem configurada no perfil da empresa (padrão 10%).
- **Idempotência:** Bloqueio de cliques duplos no botão "Finalizar" para evitar pedidos duplicados.

## 5. Fluxos de Usuário
1. **Lançamento:** Selecionar Mesa -> Adicionar Itens -> Confirmar Pedido.
2. **Pagamento:** Clicar em Fechar -> Escolher Método (Pix/Cartão/Dinheiro) -> Emitir Recibo.
3. **Integração:** O pedido é enviado via `POST /api/admin/orders` e notificado ao KDS via WebSocket.

## 6. Documentação Técnica (API)
- **Endpoints:** 
  - `GET /api/admin/{slug}/tables/dashboard`
  - `POST /api/admin/tables/{id}/pay`
  - `PATCH /api/admin/orders/{id}`

---
![POS Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-pos.png)
# 🛒 AdminWaiterPosPage
> **Plataforma:** WEB | **Domínio:** OPERACIONAL | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Ponto de Venda (PDV) fixo para balcão ou tablets. Oferece ferramentas de lançamento e fechamento em interface de alta densidade.

## 2. Estrutura e Layout (Componentes)
- **Product Matrix:** Grid de produtos com busca rápida.
- **Cart Sidebar:** Resumo do pedido atual.

## 3. Interações e Ações (Botões)
- **Quick Search:** Filtro por SKU ou nome.
- **Split Trigger:** Modal de divisão de conta.

## 4. Estados e Cenários (Loading/Error)
- **Processing Order:** Bloqueio de UI durante o envio.
- **Table Occupied:** Alerta visual se a mesa já estiver em uso.

## 5. Fluxo de Navegação
1. Seleção de mesa.
2. Lançamento de itens.
3. Fechamento de conta.

## 6. Documentação Técnica (API)
- **Endpoints:** `POST /api/admin/tables/{id}/pay`, `GET /api/admin/{slug}/tables/dashboard`
- **Assets:** ![POS Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/pos-full.png)
