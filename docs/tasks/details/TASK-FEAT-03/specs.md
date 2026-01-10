# 🔐 Especificação Técnica: TASK-FEAT-03
> **Título:** Gestão de Equipe e Permissões Granulares (RBAC)
> **Status:** SPECIFIED

## 1. Modelo de Permissões (Roles)
- **OWNER:** Acesso total (Financeiro, Configurações, Equipe).
- **MANAGER:** Gestão de cardápio, mesas e relatórios operacionais.
- **CASHIER:** Operação de POS, abertura/fechamento de mesa e pagamentos.
- **KITCHEN:** Acesso exclusivo ao KDS e gestão de estoque (Regra 86).
- **DRIVER:** Acesso exclusivo ao App de Entregas.

## 2. Implementação Técnica
- **Backend:** Middleware de verificação de escopo no FastAPI baseado nas claims do JWT.
- **Frontend:** Componente `Guard` que renderiza ou bloqueia partes da UI baseado na role do usuário.
- **Database:** Tabela `employees` vinculada a `companies` com campo `role`.

## 3. Segurança
- Bloqueio de rotas administrativas no nível de servidor (403 Forbidden).
- Invalidação de sessão imediata ao alterar a role de um funcionário.
