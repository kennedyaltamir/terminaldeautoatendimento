# 🛡️ Arquitetura de Segurança & Multi-tenancy

## 1. Isolamento de Dados (Multi-tenancy)
O MesaFlow utiliza **Isolamento Lógico em Nível de Linha**.
- **A Regra de Ouro:** Toda e qualquer query ao banco de dados DEVE conter o filtro `.filter(Model.company_id == current_user.company_id)`.
- **Prevenção de IDOR:** Nunca confie no ID enviado na URL para operações sensíveis. Sempre valide se o recurso pertence à empresa do usuário autenticado.

## 2. Autenticação & Autorização
- **JWT (JSON Web Token):** Utilizado para persistência de sessão. O payload contém `sub` (email), `role` e `account_type`.
- **RBAC (Role Based Access Control):**
    - `owner`: Acesso total, incluindo faturamento e equipe.
    - `manager`: Gestão operacional e cardápio.
    - `cashier`: Operação de mesas e fechamento.
    - `kitchen`: Apenas visualização e avanço de status no KDS.
    - `driver`: Acesso restrito ao módulo de entregas.

## 3. Proteção de Perímetro
- **Rate Limiting:** Implementado via `SlowAPI`. Limites rígidos no login (5/min) e criação de pedidos (10/min por IP).
- **Sanitização:** Todos os inputs de texto passam por `sanitize_html` para prevenir XSS Stored.
- **CORS:** Configurado para aceitar apenas o domínio oficial e localhost em desenvolvimento.
