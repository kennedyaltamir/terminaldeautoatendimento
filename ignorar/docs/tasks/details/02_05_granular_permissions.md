# 🔐 Detalhamento Técnico: Permissões Granulares ACL (UX-05)

## 1. Problema Atual
As roles são fixas (Owner, Manager, Cashier). Não é possível criar um "Garçom que também pode editar preços" ou um "Cozinheiro que não vê o faturamento".

## 2. Solução Proposta (Aba Equipe)
Implementar uma matriz de permissões baseada em *Capabilities*.

### 2.1 Funcionalidades
- **Custom Roles:** Permitir editar o nome e as permissões de cada cargo.
- **Matriz de Checkboxes:**
    - [ ] Ver Relatórios Financeiros
    - [ ] Editar Preços de Produtos
    - [ ] Cancelar Pedidos Finalizados
    - [ ] Gerenciar Mesas
- **Audit Trail:** Vincular cada ação de log ao ID do funcionário que a realizou.

## 3. Arquivos a Alterar/Criar
- `app/models.py`: Adicionar campo `permissions` (JSONB) na tabela `Employee`.
- `app/routers/auth.py`: Injetar as permissões no JWT.
- `frontend/src/hooks/usePermissions.ts`: Hook para esconder botões da UI baseados no perfil.

## 4. Segurança
- Validação no Backend (Middleware) para cada endpoint sensível, checando o JSON de permissões do token.
