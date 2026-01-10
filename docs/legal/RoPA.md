# 📋 Registro de Operações de Tratamento de Dados (RoPA)

**Controlador:** Estabelecimento (Cliente do MesaFlow)
**Operador:** MesaFlow Tecnologia Ltda
**Data de Atualização:** Janeiro de 2026
**Conformidade:** LGPD (Art. 37)

Este documento mapeia o ciclo de vida dos dados pessoais dentro da plataforma MesaFlow.

---

## 1. Categorias de Dados Tratados

| ID | Categoria | Dados Específicos | Fonte |
| :--- | :--- | :--- | :--- |
| **D01** | **Identificação** | Nome, Sobrenome, CPF (opcional). | Fornecido pelo Titular (Checkout). |
| **D02** | **Contato** | E-mail, Telefone (WhatsApp). | Fornecido pelo Titular. |
| **D03** | **Financeiro** | Hash do Cartão, Token de Pagamento, Histórico de Transações. | Gateway de Pagamento (API). |
| **D04** | **Localização** | Endereço de Entrega, Geolocalização (GPS). | Fornecido pelo Titular / Dispositivo. |
| **D05** | **Técnico** | Endereço IP, User-Agent, Logs de Acesso, Device ID. | Coleta Automática (Sistema). |

---

## 2. Finalidade e Base Legal

| Processo de Negócio | Dados Envolvidos | Finalidade (Para que serve?) | Base Legal (LGPD) |
| :--- | :--- | :--- | :--- |
| **Processamento de Pedido** | D01, D02, D04 | Executar a venda e entrega do produto. | Execução de Contrato (Art. 7º, V) |
| **Emissão Fiscal (NFC-e)** | D01 (CPF) | Cumprimento de obrigação tributária. | Obrigação Legal (Art. 7º, II) |
| **Notificações (WhatsApp)** | D01, D02 | Informar status do pedido (Transacional). | Execução de Contrato (Art. 7º, V) |
| **Fidelidade (Cashback)** | D02 (Telefone) | Identificar saldo e aplicar descontos. | Legítimo Interesse (Art. 7º, IX) |
| **Segurança e Auditoria** | D05 | Prevenção à fraude e rastreabilidade. | Legítimo Interesse / Proteção do Crédito |
| **Marketing (Newsletter)** | D02 (E-mail) | Envio de promoções. | Consentimento (Art. 7º, I) |

---

## 3. Compartilhamento com Terceiros (Sub-operadores)

| Parceiro | Função | Dados Compartilhados | Localização |
| :--- | :--- | :--- | :--- |
| **Neon.tech** | Banco de Dados | Todos (Criptografados em repouso). | EUA (AWS us-east-1) |
| **Render.com** | Hospedagem | Logs de Aplicação (D05). | EUA (Oregon) |
| **Mercado Pago** | Processamento | D01, D03 (Financeiro). | Brasil / Latam |
| **Stripe** | Assinaturas | D01, D03 (Financeiro). | Global |
| **Focus NFe** | Fiscal | D01 (CPF), D04 (Endereço). | Brasil |
| **Evolution API** | Mensageria | D02 (Telefone), Nome. | Brasil |
| **Sentry** | Observabilidade | Stack Traces (Dados anonimizados). | EUA |

---

## 4. Medidas de Segurança
- **Criptografia:** TLS 1.2+ em trânsito; AES-256 em repouso (Banco de Dados).
- **Controle de Acesso:** RLS (Row-Level Security) garantindo isolamento lógico por Tenant.
- **Minimização:** Logs de aplicação não registram dados sensíveis (PII) em texto plano.