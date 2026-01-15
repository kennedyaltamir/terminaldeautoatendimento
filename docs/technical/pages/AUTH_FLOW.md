# 🔐 Telas: Fluxo de Autenticação
**Rotas:** `/admin/login` | `/admin/register` | `/admin/forgot-password`
**Domínio:** ADMIN / AUTH

## 1. Especificação Visual
- **Login:** Campos de E-mail, Senha (com toggle de visibilidade) e Botão Google.
- **Registro:** Step-by-step (Dados Pessoais -> Dados do Negócio -> Escolha de Link/Slug).
- **Recuperação:** Campo de e-mail único com feedback de "E-mail enviado".

## 2. Elementos Interagíveis
- **Botão "Entrar com Google":** Integração OAuth2.
- **Validador de Slug:** Verifica em tempo real se o nome da loja está disponível.
- **Força de Senha:** Indicador visual de segurança (Fraca/Média/Forte).

## 3. Comportamento Esperado
- **Zero-Touch Onboarding:** Ao finalizar o registro, o sistema deve criar automaticamente a primeira mesa e a primeira categoria para o cliente não ver uma tela vazia.
- **Token Management:** Armazenar `access_token` e `refresh_token` em cookies `HttpOnly` (Produção) ou LocalStorage (Dev).
- **Redirect Logic:** Se o usuário já estiver logado, redirecionar automaticamente para o Dashboard.

## 4. APIs Consumidas
- `POST /api/auth/token`: Login tradicional.
- `POST /api/auth/register`: Criação de tenant.
- `POST /api/auth/google`: Autenticação social.
- `POST /api/auth/forgot-password`: Disparo de e-mail SMTP.
