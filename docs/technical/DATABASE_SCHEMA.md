# 🗄️ Dicionário de Dados & Arquitetura ERD

O MesaFlow utiliza PostgreSQL com isolamento lógico por estabelecimento.

## 1. Entidades Principais

### 🏢 Company (Estabelecimento)
- **ID (UUID):** Chave primária.
- **Slug:** Identificador único para URL (ex: `hamburgueria-ze`).
- **PlanTier:** Enum (`free`, `pro`, `enterprise`).
- **Branding:** Cores, Logo, Banner.
- **WhatsApp Config:** URL, Instance e Token para notificações.

### 🪑 Table & Session
- **Table:** Representa o local físico (Mesa, Quarto, Assento).
- **TableSession:** Criada no Check-in. Vincula um cliente a uma mesa.
- **Regra:** Apenas uma sessão `is_active=True` por mesa.

### 🍔 Menu (Category & Product)
- **Category:** Agrupador (Lanches, Bebidas). Possui `availability_days` e horários.
- **Product:** Itens de venda. Possui `station` (Cozinha/Bar) e `track_stock`.
- **OptionGroup:** Grupos de adicionais (ex: Ponto da Carne).

### 📝 Order & OrderItem
- **Order:** Cabeçalho do pedido. Vinculado a `company_id` e opcionalmente a `table_id`.
- **OrderItem:** Itens do pedido com `unit_price` fixado no momento da compra.
- **OrderItemOption:** Opções selecionadas para aquele item específico.

## 2. Fluxo de Integridade
- **Deleção:** O sistema utiliza `cascade="all, delete-orphan"` para garantir que ao deletar uma categoria, os produtos vinculados sejam tratados, mas pedidos históricos são preservados.
- **Financeiro:** Valores são armazenados como `Numeric(10, 2)` para precisão decimal absoluta.
