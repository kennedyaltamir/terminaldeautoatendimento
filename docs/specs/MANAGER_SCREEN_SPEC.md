# 👔 Especificação Funcional: Painel do Gerente (Admin)

## 1. Visão Geral
Interface Desktop (Next.js) para gestão estratégica, financeira e configuração do tenant.

## 2. Módulos e Comportamentos

### 2.1. Dashboard de BI
- **KPIs:** Faturamento bruto, Ticket Médio, Taxa de Cancelamento.
- **Gráficos:** Evolução de vendas diária e Heatmap de horários de pico.
- **Exportação:** Botão para gerar CSV/PDF de fechamento de caixa.

### 2.2. Engenharia de Cardápio
- **CRUD Completo:** Categorias, Produtos e Adicionais.
- **Ficha Técnica:** Vinculação de ingredientes para baixa automática de estoque.
- **Preços Dinâmicos:** Configuração de Happy Hour (preços que mudam por horário).

### 2.3. Gestão de Equipe (RBAC)
- **Usuários:** Criação de logins para funcionários.
- **Permissões:** Definição de quem pode ver o financeiro ou apenas operar o KDS.
- **Auditoria:** Log de quem alterou preços ou deletou pedidos.

### 2.4. Configurações Enterprise
- **Fiscal:** Configuração de certificado A1 e CSC para NFC-e.
- **Pagamentos:** Conexão OAuth com Mercado Pago e Stripe.
- **Branding:** Customização de cores, logo e domínio (White Label).

## 3. Regras de Sincronização
- **SSOT:** Todas as alterações de preço refletem em < 1s em todos os dispositivos (Web e Mobile) via invalidação de cache Redis.
