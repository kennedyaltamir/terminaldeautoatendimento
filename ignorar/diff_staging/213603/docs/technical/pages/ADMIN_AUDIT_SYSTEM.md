# 🕵️ Tela: Auditoria de Sistema
**Rota:** `/admin/[slug]/audit`
**Domínio:** ADMIN / GOVERNANCE

## 1. Especificação Visual
- **Tabela de Logs:** Lista cronológica de ações (Usuário, Ação, Recurso, Data, IP).
- **Filtros:** Busca por tipo de ação (Create, Update, Delete, Login).
- **Visualizador JSON:** Modal para ver o `details` de cada log.

## 2. Elementos Interagíveis
- **Botão "Ver Detalhes":** Abre modal com o payload técnico da alteração.
- **Seletor de Limite:** Escolha entre 50, 100 ou 500 registros.

## 3. Comportamento Esperado
- **Imutabilidade:** Logs não podem ser editados ou excluídos via interface.
- **Performance:** Paginação obrigatória para evitar lentidão em bancos com milhares de logs.

## 4. APIs Consumidas
- `GET /api/admin/audit`: Lista de logs filtrada por Tenant.
