
# 🍎 Apple App Store Review Playbook
**Status:** READY FOR SUBMISSION

Este guia contém as respostas exatas para o formulário do App Store Connect.

## 1. Informações de Login (App Review Information)
A Apple exige uma conta de teste funcional para validar o app.
- **User:** `apple-reviewer@mesaflow.com.br`
- **Pass:** `MesaFlow@2026`
- **Nota:** Esta conta deve estar vinculada a uma empresa de teste com pedidos ativos no KDS.

## 2. Classificação de Conteúdo (Age Rating)
- **Vendas/Comercial:** Sim.
- **Acesso à Web:** Sim (via PWA/WebView se houver).
- **Classificação Sugerida:** 4+ (ou 12+ se houver venda de bebidas alcoólicas no cardápio).

## 3. Privacidade do App (Data Nutrition Label)
Responda "Sim, coletamos dados" e marque:
- **Contact Info:** Name, Email, Phone Number (Linked to user).
- **Identifiers:** Device ID (Linked to user).
- **Usage Data:** Product Interaction (Analytics).
- **Diagnostics:** Crash Data (Sentry).

## 4. Requisito Crítico: Sign in with Apple
**Atenção:** Se o app oferece Google Login, a Apple **exige** o "Sign in with Apple". 
- **Status Atual:** Pendente de implementação ou justificativa (B2B restrito).
- **Justificativa de Isenção:** "O aplicativo é uma ferramenta de uso interno para funcionários de empresas previamente cadastradas, não sendo aberto ao público geral para criação de conta."

---

