# 🔐 AuthLoginScreen
> **Plataforma:** MOBILE | **Domínio:** AUTH | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Porta de entrada única para o staff operacional (Garçons, Cozinha e Motoristas). Garante que apenas usuários autorizados acessem o kernel de operações do restaurante, vinculando o dispositivo ao Tenant correto.

## 2. Estrutura e Design (Mobile-First)
- **Estética:** Dark-mode nativo para redução de fadiga ocular em turnos noturnos.
- **Componentes:** Utiliza `AuthInput` com ícones da Lucide e `Button` com feedback tátil (Haptic).
- **Keyboard Handling:** Implementação de `KeyboardAvoidingView` para garantir que o teclado não cubra os campos de input em telas pequenas.

## 3. Elementos Interativos
- **Campos de Input:** E-mail e Senha com validação em tempo real.
- **Toggle de Visibilidade:** Ícone de olho para mostrar/ocultar a senha.
- **Botão de Acesso:** Dispara o fluxo de autenticação e exibe estado de `loading` (Spinner).

## 4. Segurança e Persistência
- **JWT Flow:** O app recebe `access_token` e `refresh_token`.
- **SecureStore:** Armazenamento criptografado dos tokens no hardware do dispositivo.
- **Auto-Hydration:** Ao abrir o app, o `useAuthStore` verifica a validade do token e pula o login se a sessão estiver ativa.

## 5. Estados de Erro
- **Credenciais Inválidas:** Feedback visual vermelho com a mensagem "E-mail ou senha incorretos".
- **Rede Offline:** Bloqueio do botão de login com aviso de "Sem conexão com o servidor".

## 6. Fluxo Técnico
1. Usuário digita credenciais.
2. App chama `POST /api/auth/token`.
3. Sucesso: Decodifica claims (Role/CompanyID), salva no storage e navega para a `AppStack`.

---
*MesaFlow Mobile Kernel v5.0*

