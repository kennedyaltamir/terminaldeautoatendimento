# 👥 Módulo: Equipe & Perfil
**Rotas:** `/admin/[slug]/team` | `/admin/[slug]/profile`

## 1. Gestão de Equipe
- **Intenção:** Controle de acesso granular para funcionários.
- **Elementos:**
    - **Employee List:** Nome, E-mail, Role, Status.
    - **Role Selector:** Owner, Manager, Cashier, Kitchen, Driver.
- **Comportamento:** Apenas `owner` pode criar novos administradores.
- **API:** `GET /api/admin/employees`.

## 2. Perfil do Usuário
- **Intenção:** Gestão de credenciais pessoais.
- **Elementos:**
    - **Password Update:** Campos de senha atual e nova senha.
    - **Avatar Upload:** Integração com S3/Local.
- **Comportamento:** Exige validação da senha atual para qualquer alteração sensível.

