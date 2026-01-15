# 👥 Tela: Gestão de Equipe
**Rota:** `/admin/[slug]/team`
**Domínio:** ADMIN / MANAGEMENT

## 1. Especificação Visual
- **Tabela de Membros:** Nome, E-mail, Cargo (Role), Status (Ativo/Inativo).
- **Badges de Role:** Cores distintas para `manager`, `kitchen`, `waiter` e `driver`.

## 2. Elementos Interagíveis
- **Botão "Convidar Membro":** Abre modal para inserir e-mail e definir cargo.
- **Switch "Ativo":** Desativa o acesso do funcionário instantaneamente.
- **Botão "Remover":** Exclusão lógica do membro da equipe.

## 3. Comportamento Esperado
- **RBAC (Role Based Access Control):** Apenas o `owner` pode ver e editar esta página.
- **Segurança:** Um funcionário não pode alterar seu próprio cargo ou se auto-excluir.
- **Convite:** O sistema gera uma senha temporária ou link de ativação enviado por e-mail.

## 4. APIs Consumidas
- `GET /api/admin/employees`: Listagem da equipe.
- `POST /api/admin/employees`: Cadastro de novo membro.
- `DELETE /api/admin/employees/{id}`: Remoção de acesso.
