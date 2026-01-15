# 📋 Backlog Mestre: Ecossistema MesaFlow OS (Completo)
**Versão:** 6.0 — Total Coverage
**Regra de Ouro:** Funcionalidades marcadas como [CONFERIDO] devem ser re-validadas pelo Omni-Check a cada deploy.

---

## 🛡️ Camada 0: Qualidade & Anti-Regressão (IMEDIATO)
- [ ] **[QA] Omni-Check Script:** Script que roda todos os validadores (`.py` e `.ts`) simultaneamente.
- [ ] **[QA] Questionários de 100 Perguntas:** Implementar os 6 arquivos de checagem técnica por perfil.
- [ ] **[DOC] Dicionário de Telas:** Documento individual para cada uma das 34 rotas mapeadas.
- [ ] **[DOC] Checklist de Produção:** Implementar o Hard-Gate de segurança e infra.

## 🍔 Experiência do Cliente (Frontend/PWA)
- [x] [CONFERIDO] Navegação de Categorias.
- [x] [CONFERIDO] Carrinho Local.
- [ ] **[REGRESSÃO]** Adicionais e Observações (N:N).
- [ ] **[REGRESSÃO]** Lógica de Meio a Meio.
- [ ] **[REGRESSÃO]** Upsell via IA (Sugestões baseadas no carrinho).
- [ ] **[REGRESSÃO]** Split de Conta Multiplayer (WebSocket Sync).

## 👨‍🍳 Operação & KDS (Mobile/Web)
- [x] [CONFERIDO] Recebimento de Pedidos (Real-time).
- [x] [CONFERIDO] Alertas Sonoros/Vibratórios.
- [ ] **[REGRESSÃO]** Recall de Pedido (Undo Action).
- [ ] **[REGRESSÃO]** Filtro de Estação (Bar vs Cozinha).
- [ ] **[REGRESSÃO]** Modo Pausa de Cozinha.
- [ ] **[REGRESSÃO]** Impressão Bluetooth Nativa.

## 💳 Fintech & Fiscal (Backend)
- [x] [CONFERIDO] Split de Pagamento Mercado Pago.
- [x] [CONFERIDO] Gestão de Assinaturas Stripe.
- [ ] **[REGRESSÃO]** Emissão de Nota Fiscal (Focus NFe).
- [ ] **[REGRESSÃO]** Conciliação Financeira (Ledger vs Gateway).
- [ ] **[REGRESSÃO]** Wallet de Cliente (Cashback & Saldo).

## 🏢 Gestão & Admin (Web)
- [x] [CONFERIDO] Dashboard Financeiro.
- [ ] **[REGRESSÃO]** Gestão de Franquias (Multi-unidade).
- [ ] **[REGRESSÃO]** Controle de Estoque (Ficha Técnica/Ingredientes).
- [ ] **[REGRESSÃO]** Auditoria de Preço e Logs de Alteração.

---
*Este backlog é a única fonte de verdade para a próxima sprint.*
