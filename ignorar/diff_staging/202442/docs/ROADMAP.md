# 🗺️ MesaFlow Master Roadmap: A Jornada da Estabilidade (L6)

> **Visão:** De MVP Promissor para Sistema Operacional à Prova de Balas.
> **Fase Atual:** Blindagem contra Regressão & Consolidação.

Este roadmap não é apenas uma linha do tempo de features; é um compromisso com a qualidade. **Nenhuma nova era se inicia sem que a anterior esteja selada pelo Omni-Test Runner.**

---

## 🏛️ Era 1: Fundação (Concluída & Auditada)
*O nascimento do Monólito Modular e a validação do modelo híbrido.*

### ✅ Q3 2025: O Core Operacional
- **Arquitetura:** FastAPI + Next.js definidos como stack padrão.
- **Segurança:** Implementação do RLS (Row-Level Security) no PostgreSQL.
- **MVP:** Lançamento do Cardápio Digital e KDS Web básico.

### ✅ Q4 2025: A Virada Fintech
- **Pagamentos:** Integração com Mercado Pago (Split de Pagamento).
- **SaaS:** Motor de assinaturas via Stripe.
- **Resiliência:** Migração de WebSockets para Redis Pub/Sub.

---

## 🛡️ Era 2: A Grande Estabilização (Fase Atual - Q1 2026)
*O momento de parar, respirar e garantir que nada mais quebre. O foco é eliminar o retrabalho.*

### 🚧 Jan 2026: O Escudo de Regressão
- **Meta:** Implementar o `run_full_regression.py` que testa todo o sistema em um comando.
- **Ação:** Congelamento de novas features até que a cobertura de testes E2E cubra os fluxos críticos (Pedido -> Cozinha -> Pagamento).
- **Mobile:** Finalização do App Nativo (Expo SDK 54) com suporte Offline-First real.

### 📅 Fev 2026: O Salto Enterprise (Fiscal & Integração)
*Só inicia após o Escudo de Regressão estar ativo.*
- **Fiscal:** Ativação da emissão de NFC-e em produção (Focus NFe).
- **Delivery:** Lançamento do Hub iFood para centralizar pedidos.
- **Lojas:** Publicação oficial dos apps iOS e Android.

---

## 🚀 Era 3: Escala & Inteligência (Q2 2026+)
*Transformando dados em receita e eficiência, sobre uma base inquebrável.*

### 🔮 Q2 2026: MesaFlow Intelligence
- **Previsão de Demanda:** IA analisando histórico para sugerir compras de estoque.
- **Precificação Dinâmica:** Ajuste automático de preços baseado em movimento.

### 🔮 Q3 2026: O Ecossistema Aberto
- **Marketplace de Apps:** API pública para terceiros criarem plugins.
- **MesaFlow Passport:** Identidade única do consumidor em toda a rede de restaurantes.

---
*Este roadmap é regido pelo Protocolo INDA. Nenhuma etapa avança se a anterior apresentar regressão.*
