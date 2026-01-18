# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:15:00
# 🖥️ LoginPage
> **Plataforma:** Web (Next.js 14)
> **Rota:** `/admin/login`
> **Acesso:** Public (Guest)
> **Status:** VALIDATED

## 1. Visão Geral
**Propósito:** Porta de entrada segura para o painel administrativo. Autentica usuários e define o contexto da sessão (Token JWT).
**Persona Principal:** Dono, Gerente, Staff.

## 2. Estrutura de Interface
- **Layout Pai:** Layout limpo (sem sidebar).
- **Componentes Chave:**
  - `LoginForm`: Formulário controlado com validação Zod.
  - `SocialLogin`: Botão para Google Auth (Feature Flag).

## 3. Elementos Interativos & Ações
| Elemento | Tipo | Ação | Feedback Visual | Side Effect |
| :--- | :--- | :--- | :--- | :--- |
| `E-mail` | Input | Digitação | Validação onBlur | State Local |
| `Senha` | Input | Digitação | Toggle Visibility | State Local |
| `Entrar` | Button | `handleSubmit` | Spinner no botão | `POST /api/auth/token` |
| `Esqueci a senha` | Link | Navegação | Hover underline | Redireciona rota |

## 4. Estados da Tela
- **Idle:** Formulário limpo.
- **Submitting:** Inputs desabilitados, botão com spinner.
- **Error:** Toast vermelho ("Credenciais inválidas") + Shake animation.

## 5. Fluxos de Navegação
1. **Entrada:** Acesso direto ou Redirecionamento por 401 (Middleware).
2. **Saída (Sucesso):** `/admin/[slug]/dashboard` (ou rota tentada anteriormente).
3. **Saída (Recuperação):** `/admin/forgot-password`.

## 6. Regras de Negócio Críticas
- [x] Deve impedir submissão com campos vazios.
- [x] Deve limpar o LocalStorage/Cookies antigos ao carregar.
- [x] Deve redirecionar automaticamente se já houver token válido (Check Session).

## 7. Dados & Integração
- **API Endpoints:**
  - `POST /api/auth/token` (Login padrão)

