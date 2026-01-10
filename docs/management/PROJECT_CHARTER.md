# 📜 Project Charter: MesaFlow

> **Data de Aprovação:** Janeiro de 2026
> **Patrocinador:** CTO / Board
> **Gerente de Projeto:** MesaFlow Architect

## 1. Propósito e Justificativa
O setor de Food Service enfrenta um gargalo crítico: a fricção entre o desejo do cliente e a capacidade de atendimento da cozinha. Sistemas legados são fragmentados (um para PDV, um para KDS, um para Delivery).
**O MesaFlow nasce para ser o Sistema Operacional Unificado**, eliminando filas, reduzindo custos operacionais em 30% e aumentando o ticket médio em 20% através de IA e autoatendimento.

## 2. Objetivos do Projeto (SMART)
1.  **Específico:** Desenvolver uma plataforma SaaS Híbrida (Web + Mobile) que suporte operação Online e Offline.
2.  **Mensurável:** Atingir tempo de resposta de API < 100ms e sincronia de KDS < 500ms.
3.  **Atingível:** Utilizar stack moderna (FastAPI/Next.js) e infraestrutura escalável (Docker/K8s).
4.  **Relevante:** Resolver a dor de grandes operações (Estádios, Hotéis) que não podem parar por falta de internet.
5.  **Temporal:** Lançamento da versão Enterprise (v3.0) em Q1/2026.

## 3. Escopo
### ✅ Incluso (In-Scope)
- Cardápio Digital (PWA) e App Nativo (Android/iOS).
- KDS (Kitchen Display System) com SLA.
- Motor Financeiro (Split de Pagamento e Assinaturas).
- Módulo Fiscal (NFC-e/SAT) com contingência.
- Logística de Delivery e Rastreamento.

### ❌ Excluso (Out-of-Scope)
- Hardware proprietário (o sistema roda em hardware de mercado).
- Gestão Contábil/RH profunda (focamos na operação, integramos com ERPs contábeis).

## 4. Premissas e Restrições
- **Premissa:** A internet no Brasil é instável; o sistema deve ser Offline-First.
- **Restrição:** O custo de infraestrutura por tenant deve ser marginal (Multi-tenancy lógico).
- **Restrição:** Compliance rigoroso com LGPD e PCI-DSS.

## 5. Marcos Principais (Milestones)
- **Fase 1-4:** MVP e Core Operacional (Concluído).
- **Fase 5-8:** Resiliência, Fintech e Mobile (Concluído).
- **Fase 9:** Legal e Integrações Enterprise (Em Andamento).
- **Fase 10:** Expansão Global e IA Preditiva (Futuro).
