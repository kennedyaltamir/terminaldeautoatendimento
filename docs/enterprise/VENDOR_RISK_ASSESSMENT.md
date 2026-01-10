# 🛡️ Avaliação de Risco de Fornecedores (Vendor Risk Assessment)

**Classificação:** CONFIDENCIAL (Uso Interno & Auditores)
**Data de Revisão:** Janeiro de 2026
**Responsável:** CISO / Compliance Officer

---

## 1. Visão Geral
Este documento detalha a análise de risco da cadeia de suprimentos de dados do MesaFlow. Todos os fornecedores listados foram avaliados quanto à sua postura de segurança, conformidade regulatória e criticidade para a operação.

## 2. Matriz de Fornecedores Críticos (Tier 1)

| Fornecedor | Serviço | Dados Processados | Localização | Certificações | Risco | Mitigação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Neon.tech** | Banco de Dados (PostgreSQL) | PII (Nome, Email, Tel), Transações, Logs | EUA (AWS us-east-1) | SOC 2 Type II, ISO 27001 | **Alto** | Backups PITR, Criptografia em Repouso, RLS Ativo. |
| **Render.com** | Hospedagem (Compute) | Logs de Aplicação, Tráfego HTTP | EUA (Oregon) | SOC 2 Type II, ISO 27001 | **Alto** | Variáveis de Ambiente Criptografadas, Deploy Automatizado. |
| **Stripe** | Pagamentos (SaaS) | Dados de Cartão (PCI), Dados Fiscais | Global | PCI-DSS Level 1, SOC 1/2 | **Médio** | Tokenização (MesaFlow não toca no cartão), Webhooks assinados. |
| **Mercado Pago** | Pagamentos (Split) | Chaves Pix, Dados Bancários | Brasil / Latam | PCI-DSS, BACEN Compliant | **Médio** | Split na fonte (Sem custódia), Validação de Conta. |

## 3. Matriz de Fornecedores de Suporte (Tier 2)

| Fornecedor | Serviço | Dados Processados | Localização | Certificações | Risco | Mitigação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sentry** | Observabilidade | Stack Traces, Metadados de Erro | EUA | SOC 2 Type II | **Baixo** | Sanitização de PII no cliente/servidor antes do envio. |
| **Evolution API** | Mensageria (WhatsApp) | Telefone, Nome do Cliente | Brasil | N/A (Proxy) | **Médio** | Uso de Tokens efêmeros, rotação de instâncias. |
| **Focus NFe** | Fiscal | CPF, Endereço, Itens de Venda | Brasil | N/A (Regulado) | **Médio** | Comunicação via TLS 1.2, Validação de Schema. |
| **Vercel** | Frontend / CDN | Assets Estáticos, Cache | Global (Edge) | SOC 2 Type II | **Baixo** | Cache-Control estrito, WAF básico. |

---

## 4. Critérios de Avaliação de Risco

A classificação de risco baseia-se em:
1.  **Volume de Dados:** Quantidade e sensibilidade dos dados processados.
2.  **Dependência Operacional:** Impacto na continuidade do negócio em caso de falha.
3.  **Conformidade:** Existência de certificações de mercado (SOC2, ISO, PCI).

## 5. Monitoramento Contínuo

- **Revisão Anual:** A postura de segurança de todos os fornecedores Tier 1 deve ser reavaliada anualmente.
- **Incidentes:** Qualquer incidente de segurança em um sub-processador deve ser notificado ao MesaFlow em até 24h, conforme DPA.
- **Substituição:** O MesaFlow mantém planos de contingência (Vendor Lock-in Mitigation) para serviços críticos (ex: Migração Neon -> AWS RDS).

---
*Este documento é parte integrante do Programa de Governança de Dados do MesaFlow.*
