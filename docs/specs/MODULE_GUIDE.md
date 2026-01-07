# 📘 Guia de Módulos e Funcionalidades (MesaFlow v2.3)

Este documento detalha o propósito e as ações disponíveis em cada aba do sistema para garantir a consistência operacional.

---

## 1. Painel Administrativo (Gestão)

### 📊 Dashboard
*   **O que faz:** Visão financeira e operacional do dia.
*   **Ações:** Filtro de data, exportação de CSV de vendas, visualização de ticket médio e produtos mais vendidos.

### 🍔 Cardápio (Menu)
*   **O que faz:** Engenharia de produtos.
*   **Ações:** Criar categorias, produtos, grupos de adicionais (opcionais) e vincular fichas técnicas (estoque).

### 🗄️ Estoque (Inventory)
*   **O que faz:** Controle de insumos.
*   **Ações:** Cadastro de ingredientes, ajuste de saldo manual, alerta de estoque mínimo e geração de lista de compras.

### 🪑 Mesas (Tables) - *O Coração do Projeto*
*   **O que faz:** Gestão física do salão e geração de acessos.
*   **Ações:** 
    *   **Criar em Lote:** Gera mesas sequenciais (ex: 1 a 50).
    *   **Imprimir Todos:** Gera uma folha A4 com todos os QR Codes formatados para recorte.
    *   **Detalhes da Mesa:** Mostra quem está ocupando e o **Token de Acesso (10 dígitos)** para recuperação de sessão.

### 👥 Equipe (Team)
*   **O que faz:** Controle de acesso (RBAC).
*   **Ações:** Criar usuários para Garçons, Cozinheiros e Entregadores com permissões restritas.

---

## 2. App do Garçom (Operação Mobile)

### 📱 Salão (Mesas)
*   **O que faz:** Mapa de mesas em tempo real no celular.
*   **Ações:** Abrir mesa, ver PIN de acesso, lançar pedidos, transferir mesa e fechar conta.

### 🛍️ VENDA BALCÃO (Takeout)
*   **O que faz:** Venda rápida para clientes que não ocupam mesa.
*   **Ações:** Lançamento de itens e pagamento imediato.

### 🛵 NOVO DELIVERY
*   **O que faz:** Anotação de pedidos para entrega externa.
*   **Ações:** Cadastro de endereço, telefone e atribuição de motoboy.

### 💰 Fechamento com Pix
*   **O que faz:** Recebimento digital assistido.
*   **Ações:** Gera um QR Code dinâmico com o valor total da comanda para o cliente escanear no celular do garçom.

---

## 3. Monitor de Cozinha (KDS)

### 👨‍🍳 Produção
*   **O que faz:** Fila de preparo digital.
*   **Ações:** Iniciar preparo, finalizar prato, recall (desfazer finalização) e bloqueio rápido de itens esgotados (Regra 86).
