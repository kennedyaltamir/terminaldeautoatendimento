# 🔐 Tela: Login Administrativo
**Rota:** `/admin/login`
**Domínio:** ADMIN / AUTH

## 1. Especificação Visual
- **Layout:** Centralizado, fundo escuro (Slate-900).
- **Branding:** Logo MesaFlow em destaque (3xl).
- **Formulário:** Card com bordas arredondadas (xl) e sombra suave.

## 2. Elementos Interagíveis
- **Input E-mail:** Validação de formato em tempo real.
- **Input Senha:** Toggle de visibilidade (ícone Olho).
- **Botão "Entrar":** Dispara `POST /api/auth/token`. Exibe spinner durante o request.
- **Botão "Google":** Integração OAuth2.
- **Link "Esqueci Senha":** Leva para `/admin/forgot-password`.

## 3. Comportamento Esperado
- **Sucesso:** Armazena JWT no LocalStorage e redireciona para `/admin/[slug]/dashboard`.
- **Erro:** Exibe Toast (Sonner) com mensagem amigável ("E-mail ou senha incorretos").
- **Persistência:** Se o token for válido, redireciona automaticamente para o dashboard ao acessar esta rota.

## 4. APIs Consumidas
- `POST /api/auth/token`
- `POST /api/auth/google`

