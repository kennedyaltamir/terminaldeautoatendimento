# 📋 Backlog Mestre: MesaFlow OS (Zero Regression Edition)
**Status:** VIVO
**Foco Atual:** Blindagem contra Retrabalho & Expansão Controlada

Este documento contém **todas** as funcionalidades do sistema, desde o núcleo já construído até a visão de futuro.

---

## 🛡️ Prioridade Zero: Escudo de Regressão (IMEDIATO)
*O objetivo aqui é parar de quebrar o que já funciona. Nenhuma feature nova deve ser iniciada antes disso.*

- [ ] **[QA] Omni-Test Runner:** Criar script `scripts/validation/run_full_regression.py` que executa sequencialmente:
    1.  Linting & Static Analysis (Backend/Frontend).
    2.  Testes Unitários (Pytest).
    3.  Testes de Integração (API Routes).
    4.  Testes E2E Críticos (Playwright: Pedido -> Cozinha -> Pagamento).
    5.  Auditoria de Governança (XMLs, Enums).
- [ ] **[QA] Snapshot Testing:** Congelar o HTML/JSON de saídas conhecidas para detectar mudanças indesejadas na UI ou API.
- [ ] **[CI] Bloqueio de Commit:** Configurar *pre-commit hook* que impede commit se o Omni-Test falhar.

---

## 🏗️ Infraestrutura & Core (Fundação)
*Estado: Construído, mas requer validação contínua.*

- [x] **[Back] Arquitetura Modular:** FastAPI + SQLAlchemy com separação de domínios.
- [x] **[Sec] Row-Level Security (RLS):** Isolamento de dados por Tenant no PostgreSQL.
- [x] **[Infra] Redis Pub/Sub:** Mensageria para WebSockets escaláveis.
- [x] **[Auth] JWT Semântico:** Tokens com claims de papel e tenant.
- [ ] **[Infra] Multi-Region Read Replicas:** (Futuro) Para latência baixa em todo o país.
- [ ] **[Sec] Pentest Automatizado:** Scanner de vulnerabilidades (OWASP ZAP) no pipeline.

---

## 🍔 Experiência do Cliente (Frontend)
*Estado: MVP Funcional. Faltam refinamentos de UX.*

- [x] **[Feat] Cardápio Digital:** Navegação por categorias e produtos.
- [x] **[Feat] Carrinho Local:** Persistência via LocalStorage/Zustand.
- [ ] **[Feat] Adicionais e Observações:** "Sem cebola", "Borda recheada" (N:N).
- [ ] **[Feat] Meio a Meio:** Lógica para pizzas (preço pela maior).
- [ ] **[Feat] Combos Dinâmicos:** "Escolha 1 Bebida + 1 Lanche".
- [ ] **[UX] Busca e Filtros:** Pesquisa rápida e filtros (Vegano, Sem Glúten).
- [ ] **[Feat] Racha-Conta (Split Bill):** Pagamento colaborativo na mesa (Multiplayer).
- [ ] **[Feat] Gamificação:** Níveis de fidelidade e badges para clientes.

---

## 👨‍🍳 Operação & KDS (Cozinha)
*Estado: KDS Básico Operacional.*

- [x] **[Feat] Monitor de Pedidos:** Lista de pedidos em tempo real (WebSocket).
- [x] **[Feat] Gestão de Status:** Avanço de Pendente -> Preparando -> Pronto.
- [ ] **[Feat] Visão de Praça:** Filtro por estação (Bar vê apenas bebidas, Cozinha vê comida).
- [ ] **[Feat] Botão Recall:** Desfazer "Pronto" em caso de erro (Undo).
- [ ] **[Feat] Impressão de Contingência:** Fallback para impressora USB/Bluetooth se a tela falhar.
- [ ] **[Feat] Modo Pausa:** Cozinha pode pausar recebimento de pedidos se sobrecarregada.
- [ ] **[Feat] Métricas de Preparo:** Alerta visual se o pedido estourar o SLA (ex: 20 min).

---

## 💳 Fintech & Fiscal (O Dinheiro)
*Estado: Integrações Mockadas/Parciais.*

- [x] **[Pay] Split de Pagamento:** Lógica de divisão de comissão (Marketplace).
- [x] **[Pay] Assinaturas:** Integração Stripe para cobrança do SaaS.
- [ ] **[Fisc] Emissão NFC-e Real:** Integração Focus NFe/eNotas em produção.
- [ ] **[Fisc] Contingência Offline:** Fila de notas para emitir quando a internet voltar.
- [ ] **[Pay] Conciliação Automática:** Script que bate Ledger Interno vs Extrato Bancário.
- [ ] **[Pay] Wallet do Cliente:** Saldo pré-pago e Cashback utilizável.

---

## 📱 Mobile & Logística (App Nativo)
*Estado: Estrutura L5 pronta, aguardando publicação.*

- [x] **[Mob] Infraestrutura Expo:** SDK 54, NativeWind, Offline-first.
- [x] **[Mob] KDS Nativo:** App Android para tablets.
- [x] **[Mob] POS Garçom:** Lançamento de pedidos na mesa.
- [ ] **[Mob] Publicação Lojas:** Apple App Store e Google Play.
- [ ] **[Log] App do Entregador:** Roteirização e prova de entrega.
- [ ] **[Log] Rastreamento em Tempo Real:** Cliente vê o motoboy no mapa.

---

## 🏢 Gestão & Expansão (Admin)
*Estado: Dashboard Básico.*

- [x] **[Adm] Dashboard Financeiro:** Visão de vendas e ticket médio.
- [ ] **[Adm] Multi-Loja:** Visão consolidada para redes de franquias.
- [ ] **[Adm] Controle de Estoque (Ficha Técnica):** Baixa de ingredientes composta (1 Burger = 1 Pão + 1 Carne).
- [ ] **[Adm] Auditoria de Preço:** Log de quem alterou preços e quando.
- [ ] **[Int] Hub iFood:** Centralização de pedidos de delivery externos no KDS.

---
*Legenda: [x] = Implementado (Sujeito a Regressão), [ ] = A Fazer.*
