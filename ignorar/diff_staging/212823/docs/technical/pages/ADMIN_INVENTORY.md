# 📦 Tela: Gestão de Estoque
**Rota:** `/admin/[slug]/inventory`
**Domínio:** ADMIN / MANAGEMENT

## 1. Especificação Visual
- **Tabela de Ingredientes:** Nome, Unidade (kg, un, l), Estoque Atual, Nível Crítico.
- **Indicadores de Alerta:** Linhas em vermelho para itens abaixo do nível crítico.
- **Botão "Lista de Compras":** Gera resumo de reposição.

## 2. Elementos Interagíveis
- **Botão "Novo Ingrediente":** Abre modal de cadastro.
- **Botão "Editar":** Altera quantidade ou custo unitário.
- **Botão "Ficha Técnica":** Vincula ingredientes a um produto do cardápio.

## 3. Comportamento Esperado
- **Baixa Automática:** Ao finalizar um pedido no KDS, o sistema deve decrementar os ingredientes vinculados na ficha técnica.
- **Regra 86:** Se um ingrediente essencial zerar, o sistema deve pausar automaticamente os produtos dependentes.

## 4. APIs Consumidas
- `GET /api/admin/inventory/ingredients`
- `POST /api/admin/inventory/recipes`
- `GET /api/admin/inventory/shopping-list`
