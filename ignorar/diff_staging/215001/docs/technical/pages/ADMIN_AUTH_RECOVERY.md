# 🔐 Telas: Recuperação de Acesso
**Rotas:** `/admin/forgot-password` | `/admin/reset-password`
**Domínio:** ADMIN / AUTH

## 1. Esqueci Minha Senha
- **Intenção:** Solicitação de link de reset via e-mail.
- **Comportamento:** Após o envio, exibe mensagem de sucesso e bloqueia novo envio por 60s (Rate Limit).

## 2. Redefinir Senha
- **Intenção:** Definição de nova credencial via token seguro.
- **Elementos:** Input "Nova Senha" e "Confirmação".
- **Comportamento:** Valida o token da URL. Se expirado, redireciona para o login com erro.

## 3. APIs Consumidas
- `POST /api/auth/forgot-password`: Disparo de e-mail.
- `POST /api/auth/reset-password`: Troca efetiva da senha.
