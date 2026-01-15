# 👤 Tela: Perfil do Usuário
**Rota:** `/admin/[slug]/profile`
**Domínio:** ADMIN / ACCOUNT

## 1. Especificação Visual
- **Layout:** Duas colunas (Informações Pessoais | Segurança).
- **Componentes:** Avatar circular com iniciais, formulários de texto limpos.

## 2. Elementos Interagíveis
- **Input Nome/E-mail:** Campos editáveis para o perfil.
- **Seção de Senha:** Campos "Senha Atual", "Nova Senha" e "Confirmar Senha".
- **Botão "Salvar Alterações":** Dispara `PATCH /api/admin/company/me`.
- **Botão "Logout":** Encerra a sessão e limpa o LocalStorage.

## 3. Comportamento Esperado
- **Validação de Senha:** O botão de salvar só habilita se a "Nova Senha" e "Confirmação" forem idênticas e possuírem força mínima (8 caracteres, letras e números).
- **Feedback:** Toast de sucesso após atualização. Se a senha for alterada, o sistema deve invalidar os tokens antigos e forçar novo login.

## 4. APIs Consumidas
- `GET /api/admin/company/me`: Carregamento dos dados.
- `PATCH /api/admin/company/me/password`: Atualização de credenciais.

