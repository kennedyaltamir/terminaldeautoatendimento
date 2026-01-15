# 🛡️ Análise de Incidente: Loop de Autenticação em Testes de UI
**Data:** 10 de Janeiro de 2026
**Status:** CRÍTICO
**Origem:** Ultimate UI Stress Test (v5)

## 1. O Problema
O relatório e o vídeo indicam que o script de teste está **perdendo a sessão de autenticação** ao navegar entre as páginas.
- O script faz login com sucesso na primeira etapa.
- Ao tentar acessar `/admin/hamburgueria-ze/menu`, o sistema redireciona automaticamente para `/admin/login` (comportamento de segurança correto para usuários não autenticados).
- O script, não esperando esse redirecionamento, tenta interagir com elementos da página de Menu, mas encontra apenas os elementos da página de Login (3 elementos: Email, Senha, Entrar), gerando falsos positivos ou erros de `ERR_ABORTED`.

## 2. Causa Raiz Técnica
O Playwright, por padrão, não persiste `localStorage` ou `Cookies` entre contextos de navegação se não for explicitamente instruído.
O MesaFlow armazena o JWT em `localStorage`. Quando o script usa `page.goto()`, se o estado de armazenamento não for injetado corretamente no contexto do navegador, a aplicação React entende que o usuário é anônimo e o expulsa para o login.

## 3. Solução Definitiva (Script v6)
Para corrigir isso e atender aos requisitos de "clicar em tudo" e "preencher formulários", o novo script implementará:

1.  **Persistência de Estado (Storage State):**
    - O script fará login uma vez.
    - Salvará o estado (Cookies + LocalStorage) em um arquivo `auth.json`.
    - Reutilizará esse arquivo para **todas** as navegações subsequentes, garantindo que o robô seja reconhecido como "Admin".

2.  **Detector de Redirecionamento:**
    - Se a URL mudar para `/login` durante o teste de uma rota interna, o script abortará aquela rota e marcará como FALHA DE AUTH, em vez de tentar clicar em botões inexistentes.

3.  **Interação Inteligente (Smart Monkey):**
    - Antes de clicar em qualquer botão, o script verificará se há inputs visíveis ao redor.
    - Se houver, preencherá com dados do `Faker`.
    - Se um modal abrir, ele mudará o foco para o modal.

---
*Relatório gerado pelo MesaFlow Architect Kernel.*
