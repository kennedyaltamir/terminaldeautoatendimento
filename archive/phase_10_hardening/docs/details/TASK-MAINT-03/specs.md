# 📸 Especificação Técnica: TASK-MAINT-03
> **Título:** Automação de Captura de Telas (Visual Audit)
> **Status:** APROVADO
> **Objetivo:** Gerar evidências visuais de todas as interfaces do sistema para documentação e auditoria de UI.

## 1. Escopo de Captura
O script deve automatizar o navegador para:
1. Realizar login administrativo.
2. Percorrer todas as rotas definidas no `open_all_screens.py`.
3. Capturar versões **Desktop** (1280x720) e **Mobile** (390x844).
4. Salvar os arquivos em `docs/screenshots/` com nomes padronizados.

## 2. Requisitos Técnicos
- **Ferramenta:** Playwright (Python).
- **Autenticação:** O script deve injetar o token JWT no `localStorage` ou realizar o fluxo de login real.
- **Estabilidade:** Aguardar `networkidle` para garantir que gráficos e imagens carregaram.
