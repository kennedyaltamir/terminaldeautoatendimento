# 📋 Backlog Mestre: MesaFlow OS (L6 Edition)
**Status:** VIVO
**Priorização:** RICE Score (Impacto x Esforço)

Este documento unifica as demandas de Produto (Features) e Engenharia (Enablers).

---

## 🚨 Alta Prioridade (Q1 2026)
*Foco: Desbloqueio de Vendas Enterprise e Estabilidade.*

| ID | Tipo | Título | RICE | Status | Dependência |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **TASK-FIS-01** | 🔌 Backend | **Integração Fiscal Real (Focus NFe)** | 98 | 🚧 WIP | `SEC-04` |
| **TASK-MOB-05** | 📱 Mobile | **Publicação nas Lojas (Apple/Google)** | 95 | 📅 Plan | `INF-04` |
| **TASK-INT-02** | 🔌 Backend | **Hub iFood (Ingestão de Pedidos)** | 90 | 📅 Plan | `APP-02` |
| **TASK-FIN-04** | 💰 Fintech | **Conciliação Automática (Ledger vs Gateway)** | 88 | 📅 Plan | `APP-03` |
| **TASK-UX-05** | 🎨 Frontend | **Modo Offline Robusto (Service Workers)** | 85 | 📅 Plan | - |

---

## 🍔 Experiência do Cliente (Growth)
*Foco: Aumentar Ticket Médio e Retenção.*

- [ ] **[FEAT] Upsell Inteligente v2:** Sugestão baseada em histórico real (não apenas regras fixas).
- [ ] **[FEAT] Personalização de Item:** Adicionais e Observações estruturadas (N:N no banco).
- [ ] **[FEAT] Racha-Conta (Split Bill):** Pagamento colaborativo na mesa via WebSocket.
- [ ] **[UX] Gamificação:** Níveis de fidelidade e badges para clientes recorrentes.

## 👨‍🍳 Operação & KDS (Efficiency)
*Foco: Reduzir tempo de preparo e erros.*

- [ ] **[KDS] Visão de Praça:** Filtro por estação (Bar, Cozinha, Sobremesa) persistente por dispositivo.
- [ ] **[KDS] Recall de Pedido:** Desfazer "Pronto" em caso de erro (Undo Action).
- [ ] **[KDS] Impressão de Contingência:** Fallback automático para impressora USB se a rede cair.

## 🏢 Gestão & SaaS (Control)
*Foco: Governança para Franquias.*

- [ ] **[ADM] Multi-Loja:** Dashboard consolidado para redes de franquias.
- [ ] **[ADM] Controle de Estoque (Ficha Técnica):** Baixa de ingredientes composta (1 Burger = 1 Pão + 1 Carne).
- [ ] **[ADM] Auditoria de Preço:** Log de quem alterou preços e quando.

## 🛡️ Engenharia & Segurança (Enablers)
*Foco: Manutenibilidade e Compliance.*

- [ ] **[SEC] Pentest Automatizado:** CI/CD rodando ZAP Scanner semanalmente.
- [ ] **[INF] Multi-Region:** Réplica de leitura do banco em outra zona de disponibilidade.
- [ ] **[DEV] Storybook:** Documentação viva dos componentes de UI.

---
*Legenda: WIP (Work In Progress), Plan (Planejado).*
