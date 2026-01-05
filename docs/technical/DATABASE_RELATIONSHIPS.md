# 🗄️ Relacionamentos do Banco de Dados

O MesaFlow utiliza um modelo relacional estrito para garantir integridade de dados em um ambiente multi-tenant.

## 1. O Pilar Multi-tenant (`Company`)
Tudo começa na tabela `companies`.
- **Regra de Ouro:** Todas as outras tabelas principais (`products`, `orders`, `tables`, `employees`) possuem uma coluna `company_id` (FK).
- **Isolamento:** Toda query deve filtrar por `company_id` para evitar vazamento de dados entre restaurantes.

## 2. Catálogo (Menu)
- `Category` (1) <-> (N) `Product`
- `Product` (1) <-> (N) `OptionGroup`
- `OptionGroup` (1) <-> (N) `Option`
- **Estoque:** `Product` (N) <-> (N) `Ingredient` (via tabela associativa `product_recipes`).

## 3. Pedidos e Fluxo
- `Table` (1) <-> (N) `TableSession` (Histórico de ocupações).
- `TableSession` (1) <-> (N) `Order` (Uma mesa pode ter vários pedidos na mesma sessão).
- `Order` (1) <-> (N) `OrderItem`.
- `OrderItem` (1) <-> (N) `OrderItemOption` (Snapshot das opções escolhidas no momento da compra).

## 4. Financeiro e Logística
- `CustomerWallet` (1) <-> (1) `Company` + `Phone` (Saldo de cashback por loja).
- `DriverLedger` (N) <-> (1) `Employee` (Motorista).
- `ServiceFeeLedger` (N) <-> (1) `Employee` (Garçom - Gorjetas).

## 5. Diagrama Conceitual (Texto)
```
[Company]
  |
  +-- [Employees] (Garçons, Cozinheiros, Motoristas)
  |
  +-- [Tables] --(tem)--> [TableSessions] --(tem)--> [Orders]
  |
  +-- [Categories] --(tem)--> [Products] --(tem)--> [OptionGroups]
                                   |
                                   +--(usa)--> [Ingredients]
```
