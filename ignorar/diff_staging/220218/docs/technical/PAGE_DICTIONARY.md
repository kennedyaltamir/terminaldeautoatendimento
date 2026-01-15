# 📖 Dicionário de Páginas e Telas (Omniscience Edition)
**Versão:** 9.0 — Total Coverage Specification
**Status:** SELADO / CONTRATUAL

Este documento detalha as 34 rotas do ecossistema. Nenhuma alteração de UI deve divergir destas especificações.

---

## 1. Módulo Público (Cliente Final)
- [x] **Landing Page (`/`)**: Venda SaaS e captura de leads.
- [x] **Cardápio PWA (`/[slug]/menu`)**: Interface de venda offline-first.
- [x] **Totem (`/[slug]/kiosk`)**: Tela de atração para terminais físicos.
- [x] **Monitor (`/[slug]/monitor`)**: Senhas de retirada sincronizadas.
- [x] **Trust Center (`/trust`)**: Status de saúde e segurança.
- [x] **Offline (`/offline`)**: Fallback visual de rede.

## 2. Módulo Administrativo (Gestão)
- [x] **Login/Registro**: Acesso e Onboarding.
- [x] **Dashboard BI**: Métricas e gráficos Recharts.
- [x] **Menu Admin**: Gestão de produtos e categorias.
- [x] **Estoque**: Ingredientes e Ficha Técnica.
- [x] **Mesas**: Layout do salão e QR Codes.
- [x] **Equipe**: Gestão de cargos e permissões.
- [x] **Marketing**: Cupons e Fidelidade.
- [x] **Auditoria**: Ledger Financeiro e Logs de Sistema.
- [x] **Faturamento**: Assinaturas Stripe e Planos.
- [x] **Features**: Gestão de Flags Beta (Suporte).

## 3. Módulo Operacional (KDS & POS)
- [x] **KDS Web/Mobile**: Fila de produção com SLA.
- [x] **Expedição**: Conferência e despacho de pedidos.
- [x] **App Garçom**: POS nativo com mapa de mesas.
- [x] **App Entregador**: Logística e Proof of Delivery.
- [x] **Printer Debug**: Homologação de hardware.

---
*Especificações detalhadas em docs/technical/pages/*.md*
