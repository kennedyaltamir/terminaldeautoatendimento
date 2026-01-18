# Plataforma: WEB | Arquivo: AdminAuditFinancialPage.md
# 💰 AdminAuditFinancialPage
> **Plataforma:** WEB | **Domínio:** FINTECH | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta tela é o núcleo de integridade financeira do MesaFlow OS. Seu objetivo é permitir a conciliação bancária e a auditoria da cadeia de custódia (Ledger L7), garantindo que cada centavo transacionado no gateway (Mercado Pago/Stripe) tenha uma correspondência exata e imutável no banco de dados do sistema.

## 2. Estrutura e Layout (Arquitetura de Dados)
- **Integridade Banner:** Indicador visual do status da Hash Chain (Verde: Íntegro, Vermelho: Violado).
- **Reconciliation Table:** Comparativo entre o extrato do Gateway e o Ledger interno.
- **Orphan Transaction List:** Painel para identificação de transações que existem no provedor mas não foram processadas pelo sistema (ex: falha de webhook).

## 3. Elementos Interativos e Ações
- **Verify Chain:** Dispara o script `FIN-01` para validar matematicamente todos os hashes da tabela `financial_ledger`.
- **Fix Orphan:** Botão de ação manual para criar uma entrada corretiva no Ledger para transações órfãs validadas.
- **Export Ledger:** Gera um arquivo CSV assinado digitalmente para fins fiscais e contábeis.

## 4. Regras de Negócio e Estados
- **Imutabilidade:** Registros no Ledger não podem ser alterados ou deletados (Append-only).
- **Mismatch Alert:** O sistema destaca em laranja transações onde o valor recebido diverge do valor do pedido.
- **Loading State:** Spinner de alta precisão durante a verificação de integridade da cadeia.

## 5. Fluxos de Navegação
1. O auditor acessa o menu "Auditoria Financeira".
2. O sistema carrega o relatório de conciliação via `GET /api/admin/audit/financial/reconciliation`.
3. O usuário valida as divergências e aplica correções se necessário.

## 6. Documentação Técnica (API)
- **Endpoints:**
  - `GET /api/admin/audit/financial/ledger`
  - `POST /api/admin/audit/financial/fix-orphan`
  - `GET /api/admin/audit/financial/verify-integrity`

---
![Financial Audit Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-audit-fin.png)



################################################################################


# Plataforma: WEB | Arquivo: AdminAuditPage.md
# 📱 AdminAuditPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/audit`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminauditpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\audit\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminBillingPage.md
# 📱 AdminBillingPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/settings/billing`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminbillingpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\settings\billing\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminCounterPage.md
# 📱 AdminCounterPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/counter`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/admincounterpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\counter\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminDashboardHistoryPage.md
# 📜 AdminDashboardHistoryPage
> **Plataforma:** WEB | **Domínio:** AUDITORIA | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta tela fornece uma trilha de auditoria completa e retroativa de todas as transações e mudanças de estado do sistema. É a ferramenta principal para resolução de disputas financeiras, conferência de fechamento de caixa e análise de performance histórica de longo prazo.

## 2. Estrutura e Componentes Técnicos
- **Data Table Engine:** Tabela de alta densidade com suporte a paginação server-side para lidar com milhares de registros sem degradação de performance.
- **Filtros Avançados:** Painel lateral ou superior para filtragem por Status (Pago, Cancelado), Período (Date Range Picker) e Origem (MesaFlow, iFood).
- **Order Detail Modal:** Componente de visualização profunda que exibe itens, taxas, descontos e logs de tempo de cada etapa do pedido.

## 3. Elementos Interativos
- **Paginação Dinâmica:** Controles de "Anterior/Próximo" que atualizam a URL via query params para permitir compartilhamento de links de busca.
- **Visualizador de Recibo:** Botão para re-emitir ou visualizar o cupom térmico original do pedido.
- **Exportador de Auditoria:** Função para gerar relatórios consolidados em PDF ou CSV para contabilidade.

## 4. Regras de Negócio e Integridade
- **Imutabilidade:** Pedidos finalizados ou cancelados não podem ser editados, apenas visualizados.
- **Sincronia de Status:** O histórico reflete o estado final persistido no banco de dados, servindo como "Fonte da Verdade" em caso de divergência no KDS.
- **Cálculo de Taxas:** Exibição clara do split de comissão e taxas de entrega aplicadas no momento da venda.

## 5. Estados da Interface
- **Searching:** Estado de carregamento com Skeletons de linha durante a filtragem.
- **No Results:** Feedback visual amigável quando nenhum pedido atende aos critérios de busca.
- **API Error:** Alerta de falha de comunicação com opção de recarregamento manual.

## 6. Documentação de API
- **Endpoint Principal:** `GET /api/admin/{slug}/history?page=1&limit=10&status=paid`
- **Contrato de Resposta:** Objeto `OrderPagination` contendo metadados de totalização e array de `OrderResponse`.

---
*MesaFlow OS — Auditoria e Transparência.*
# 📜 AdminDashboardHistoryPage
> **Plataforma:** WEB | **Domínio:** AUDITORIA | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Trilha de auditoria retroativa. Permite a conferência de todos os pedidos realizados, servindo como base para fechamento de caixa.

## 2. Estrutura e Layout (Componentes)
- **History Table:** Lista paginada de pedidos finalizados.
- **Filter Panel:** Busca por data, status e método de pagamento.

## 3. Interações e Ações (Botões)
- **View Details:** Abre modal com composição completa do pedido.
- **Export Data:** Gera relatório consolidado do período.

## 4. Estados e Cenários (Loading/Error)
- **Loading:** Skeletons de linha durante o fetch.
- **No Results:** Feedback para busca sem ocorrências.

## 5. Fluxo de Navegação
1. Seleção de período.
2. Localização de pedido específico.
3. Conferência de itens e valores.

## 6. Documentação Técnica (API)
- **Endpoints:** `GET /api/admin/{slug}/history`
- **Assets:** ![History Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-history-full.png)


################################################################################


# Plataforma: WEB | Arquivo: AdminDashboardPage.md
# 📱 AdminDashboardPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/dashboard`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Esta tela é o centro de inteligência tática do MesaFlow OS. Seu objetivo é fornecer ao proprietário e gerentes uma visão consolidada da saúde financeira e operacional do estabelecimento em tempo real, permitindo decisões baseadas em dados sobre estoque, equipe e engenharia de cardápio.

## 2. Screenshot de Referência
![Screenshot](../placeholders/admindashboardpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\dashboard\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminDeliveryPage.md
# 📱 AdminDeliveryPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/delivery`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/admindeliverypage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\delivery\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminDriverPage.md
# 📱 AdminDriverPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/driver`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/admindriverpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\driver\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminExpeditorPage.md
# 📱 AdminExpeditorPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/expeditor`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminexpeditorpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\expeditor\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminFeaturesPage.md
# 📱 AdminFeaturesPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/settings/features`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminfeaturespage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\settings\features\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminFinancialPage.md
# 📱 AdminFinancialPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/audit/financial`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminfinancialpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\audit\financial\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminForgotPasswordPage.md
# 📱 AdminForgotPasswordPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/forgot-password`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Interface de recuperação de conta para usuários administrativos. Permite que proprietários e funcionários solicitem um link de redefinição de senha via e-mail, garantindo a continuidade do acesso mesmo em caso de perda de credenciais.

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminforgotpasswordpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\forgot-password\page.tsx`
**Hooks:** `useForm, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Link**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminFranchisePage.md
# 📱 AdminFranchisePage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/franchise`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminfranchisepage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\franchise\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Link**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminHistoryPage.md
# 📱 AdminHistoryPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/dashboard/history`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminhistorypage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\dashboard\history\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Modal**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminInventoryPage.md
# 📱 AdminInventoryPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/inventory`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/admininventorypage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\inventory\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Modal**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminKitchenPage.md
# 📱 AdminKitchenPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/kitchen`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
O Monitor de Produção (Kitchen Display System - KDS) é a interface crítica para a equipe de preparo. Sua função é substituir as comandas de papel por uma fila digital inteligente, organizada por tempo de permanência e prioridade de SLA.

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminkitchenpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\kitchen\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminLoginPage.md
# 📱 AdminLoginPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/login`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Ponto de acesso centralizado para a administração do ecossistema MesaFlow. Realiza a autenticação de proprietários (Owners) e funcionários (Staff), estabelecendo o contexto de segurança necessário para o isolamento multi-tenant (RLS).

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminloginpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\login\page.tsx`
**Hooks:** `useForm, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Link**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminMarketingPage.md
# 📱 AdminMarketingPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/marketing`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminmarketingpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\marketing\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Modal**: (Descrever ação)
- [ ] **a**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminMenuPage.md
# 📱 AdminMenuPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/menu`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminmenupage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\menu\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Modal**: (Descrever ação)
- [ ] **a**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminOrdersPage.md
# 📱 AdminOrdersPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/waiter/orders`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminorderspage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\waiter\orders\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminPaymentCallbackPage.md
# 🔗 AdminPaymentCallbackPage
> **Plataforma:** WEB | **Domínio:** FINTECH | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta página atua como o "Handshake Final" entre o MesaFlow e os provedores de pagamento (Mercado Pago/Stripe). Sua função é capturar o código de autorização OAuth, trocá-lo por tokens de acesso e vincular a conta financeira do lojista ao seu Tenant no sistema.

## 2. Estrutura Técnica
- **OAuth Handler:** Lógica de captura de parâmetros de URL (`code`, `state`).
- **Security Validator:** Verifica se o parâmetro `state` corresponde ao ID da empresa logada para prevenir ataques de interceptação.
- **Status Stepper:** Visualização do progresso da conexão (Validando -> Vinculando -> Concluído).

## 3. Elementos Interativos
- **Botão de Retorno:** Link para voltar às configurações de pagamento em caso de erro.
- **Auto-Redirect:** Redirecionamento automático para o painel administrativo após o sucesso da operação.

## 4. Regras de Negócio (Integração)
- **Token Exchange:** O sistema realiza uma chamada server-side para converter o código temporário em um `access_token` permanente.
- **Credential Storage:** As credenciais são salvas de forma criptografada no banco de dados, habilitando o Pix Automático e Split de Pagamento.
- **Provider Mapping:** Atualiza o campo `payment_provider` da empresa para o provedor recém-conectado.

## 5. Estados e Cenários
- **Processing:** Spinner de alta prioridade enquanto a troca de tokens ocorre no backend.
- **Success:** Mensagem de celebração: "Conta conectada com sucesso!".
- **Failure:** Diagnóstico de erro (ex: "Código expirado" ou "Permissão negada pelo usuário").

## 6. Fluxo de Dados (API)
- **Inbound:** Recebe `GET /admin/payment/callback?code=...`
- **Outbound:** Dispara `POST /api/admin/payment/callback/{provider}` para finalização no backend.

---
*MesaFlow Fintech Infrastructure.*



################################################################################


# Plataforma: WEB | Arquivo: AdminProfilePage.md
# 📱 AdminProfilePage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/profile`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminprofilepage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\profile\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminRegisterPage.md
# 📱 AdminRegisterPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/register`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Portal de auto-cadastro para novos estabelecimentos. O objetivo é permitir que um novo lojista crie sua conta, defina seu subdomínio (slug) e configure os parâmetros básicos do seu negócio em menos de 2 minutos (Zero-Touch Onboarding).

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminregisterpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\register\page.tsx`
**Hooks:** `useEffect, useForm, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Link**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminResetPasswordPage.md
# 📱 AdminResetPasswordPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/reset-password`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Página de destino do link de recuperação de senha. Permite que o usuário defina uma nova credencial de acesso após validar a posse do e-mail através de um token seguro, restaurando o acesso à plataforma administrativa.

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminresetpasswordpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\reset-password\page.tsx`
**Hooks:** `useForm, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminSettingsBillingPage.md
# 💳 AdminSettingsBillingPage
> **Plataforma:** WEB | **Domínio:** SAAS | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Central de faturamento e gestão de planos. Permite ao lojista realizar o upgrade para o plano Pro, gerenciar métodos de pagamento, visualizar faturas passadas e controlar o consumo de recursos do SaaS.

## 2. Estrutura e Componentes
- **Plan Comparison:** Cards detalhando os benefícios do plano atual vs planos superiores.
- **Usage Monitor:** Gráficos de consumo (ex: "45 de 50 pedidos gratuitos utilizados").
- **Billing History:** Lista de faturas pagas com link para download de recibos.

## 3. Elementos Interativos
- **Upgrade Trigger:** Inicia o fluxo de checkout seguro via Stripe.
- **Customer Portal Link:** Redireciona para o portal de autoatendimento do Stripe para troca de cartão de crédito.
- **Cancel Subscription:** Fluxo de cancelamento com pesquisa de satisfação integrada.

## 4. Regras de Negócio (SaaS)
- **Prorata Logic:** O sistema calcula automaticamente a diferença de valores em upgrades no meio do ciclo.
- **Grace Period:** Mantém o acesso Pro por 3 dias após falha no pagamento antes do bloqueio total.
- **Metered Billing:** Registro de uso para cobrança de taxas variáveis (se aplicável ao plano).

## 5. Estados de UI
- **Active:** Status normal de assinatura.
- **Past Due:** Alerta de pagamento pendente com botão de regularização imediata.
- **Canceled:** Aviso de encerramento de ciclo e perda de recursos Pro.

## 6. Integração Técnica
- **Endpoints:**
  - `POST /api/admin/billing/upgrade`
  - `POST /api/admin/billing/portal`
- **Webhooks:** Processa eventos `customer.subscription.updated` do Stripe.

---
![Billing Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-billing.png)
# 💳 AdminSettingsBillingPage
> **Plataforma:** WEB | **Domínio:** SAAS | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Gestão financeira da assinatura. Centraliza cobrança e controle de limites do plano.

## 2. Estrutura e Layout (Componentes)
- **Subscription Card:** Status e valor.
- **Usage Progress:** Barras de limite de pedidos.

## 3. Interações e Ações (Botões)
- **Upgrade Button:** Gatilho para Stripe.
- **Billing Portal:** Link externo de gestão.

## 4. Estados e Cenários (Loading/Error)
- **Active:** Assinatura em dia.
- **Past Due:** Alerta de atraso.

## 5. Fluxo de Navegação
1. Acesso via Configurações.
2. Seleção de plano.
3. Pagamento.

## 6. Documentação Técnica (API)
- **Endpoints:** `POST /api/admin/billing/upgrade`, `POST /api/admin/billing/portal`
- **Assets:** ![Billing Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/billing-full.png)


################################################################################


# Plataforma: WEB | Arquivo: AdminSettingsFeaturesPage.md
# 🧪 AdminSettingsFeaturesPage
> **Plataforma:** WEB | **Domínio:** GOVERNANÇA | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Painel de controle de funcionalidades experimentais (Feature Flags). Destinado à equipe de suporte e desenvolvedores (Modo Impersonation), permite ativar ou desativar módulos Beta para clientes específicos sem a necessidade de novo deploy de código.

## 2. Estrutura e Layout
- **Feature List:** Grid de cards contendo o nome técnico da flag, descrição funcional e status atual.
- **Support Banner:** Aviso persistente de que o "Modo Suporte" está ativo e as alterações são auditadas.

## 3. Elementos Interativos
- **Feature Toggle:** Switch para ligar/desligar funcionalidades em tempo real.
- **Audit Link:** Atalho para visualizar quem alterou a flag e quando.

## 4. Regras de Segurança (L6)
- **Impersonation Only:** Esta página é invisível e inacessível para lojistas comuns. Exige a claim `impersonator: true` no JWT.
- **Optimistic Rollback:** Se a API falhar ao salvar a flag, a UI reverte o toggle automaticamente para o estado anterior.
- **Cache Invalidation:** A alteração limpa o cache de flags do Tenant no Redis instantaneamente.

## 5. Estados da Tela
- **Loading:** Busca das flags ativas para o Tenant selecionado.
- **Unauthorized:** Bloqueio total com log de tentativa de acesso indevido.
- **Success Toast:** Confirmação de que a funcionalidade foi propagada para o ambiente do cliente.

## 6. Fluxo de Dados (API)
- **Fetch:** `GET /api/admin/features`
- **Update:** `POST /api/admin/features` (Payload: `{ key: string, is_enabled: bool }`)

---
![Features Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-features.png)



################################################################################


# Plataforma: WEB | Arquivo: AdminSettingsPage.md
# 📱 AdminSettingsPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/settings`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Central de configuração da identidade e regras de operação do estabelecimento. Permite personalizar a aparência do cardápio, horários de funcionamento, taxas de serviço e integrações de comunicação (WhatsApp).

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminsettingspage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\settings\page.tsx`
**Hooks:** `useEffect, useForm, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminSupportPage.md
# 📱 AdminSupportPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/support`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminsupportpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\support\page.tsx`
**Hooks:** `useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminTablesPage.md
# 📱 AdminTablesPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/tables`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/admintablespage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\tables\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Modal**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminTeamPage.md
# 📱 AdminTeamPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/team`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminteampage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\team\page.tsx`
**Hooks:** `useEffect, useForm, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Modal**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminWaiterOrdersPage.md
# 📋 AdminWaiterOrdersPage
> **Plataforma:** WEB | **Domínio:** OPERACIONAL | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta tela é o "Live Feed" de operações do salão. Seu objetivo é permitir que supervisores de garçons e gerentes de turno monitorem o fluxo de pedidos em tempo real, identifiquem gargalos de atendimento e realizem intervenções rápidas em comandas específicas sem a necessidade de estar fisicamente na mesa.

## 2. Estrutura e Layout (Monitor de Fluxo)
- **Active Orders Stream:** Lista cronológica de pedidos ativos com identificação visual por mesa e cliente.
- **Service Alert Sidebar:** Painel lateral dedicado a chamados de urgência (ajuda, limpeza, conta).
- **Quick Action Toolbar:** Botões de acesso rápido para cancelamento, estorno e transferência de itens.

## 3. Elementos Interativos
- **Filtro de Status:** Alternância entre pedidos "Pendentes", "Em Preparo" e "Prontos".
- **Busca por Comanda:** Localização instantânea de pedidos via ID ou nome do cliente.
- **Expandable Details:** Clique na linha para abrir a composição completa do pedido e histórico de tempo (SLA).

## 4. Regras de Negócio e Gestão
- **Ownership Tracking:** Identificação de qual funcionário realizou o lançamento original.
- **Audit Trail:** Registro de todas as alterações manuais feitas em pedidos ativos para prevenção de perdas.
- **Priority Highlighting:** Pedidos que excedem o tempo médio de preparo são destacados com bordas pulsantes.

## 5. Estados da Interface
- **Syncing:** Indicador de conexão ativa com o WebSocket.
- **Empty State:** Mensagem "Salão Tranquilo" quando não há pedidos em curso.
- **Action Loading:** Estado de bloqueio de linha enquanto uma alteração de status é processada.

## 6. Documentação Técnica (API)
- **Endpoints:** 
  - `GET /api/admin/{slug}/waiter/orders`
  - `PATCH /api/admin/orders/{id}`
- **WebSocket:** Assina o tópico `order_updates` para refletir mudanças feitas via App Mobile.

---
*MesaFlow OS — Operação de Salão de Alta Performance.*



################################################################################


# Plataforma: WEB | Arquivo: AdminWaiterPage.md
# 📱 AdminWaiterPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/waiter`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Dashboard administrativo para gestão de capital humano e performance de campo. Permite ao proprietário monitorar a eficiência da equipe de garçons, gerenciar escalas de acesso e auditar a distribuição de gorjetas e comissões.

## 2. Screenshot de Referência
![Screenshot](../placeholders/adminwaiterpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\waiter\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: AdminWaiterPosPage.md
# 🛒 AdminWaiterPosPage
> **Plataforma:** WEB | **Domínio:** OPERACIONAL | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Interface de Ponto de Venda (PDV) otimizada para desktops e tablets. Permite que o staff realize o atendimento completo de uma mesa ou balcão, desde a abertura da comanda até o processamento de pagamentos complexos (divisão de conta).

## 2. Estrutura e Layout
- **Menu Lateral:** Navegação rápida por categorias de produtos.
- **Grid de Produtos:** Cards com fotos, preços e badges de disponibilidade.
- **Carrinho Ativo (Sidebar Direita):** Listagem de itens selecionados, campo de observações e totalizador em tempo real.
- **Barra de Ações:** Botões de "Chamar Garçom", "Transferir Mesa" e "Fechar Conta".

## 3. Elementos Interativos
- **Busca Instantânea:** Filtro de produtos por nome ou código (SKU) com debounce de 300ms.
- **Modificador de Itens:** Modal para seleção de opcionais (ex: ponto da carne, adicionais).
- **Split Bill (Divisão de Conta):** Interface para dividir o total por número de pessoas ou por itens específicos.

## 4. Regras de Negócio
- **Trava de Estoque:** Itens com `stock_quantity === 0` são desabilitados automaticamente (Regra 86).
- **Taxa de Serviço:** Aplicação dinâmica da porcentagem configurada no perfil da empresa (padrão 10%).
- **Idempotência:** Bloqueio de cliques duplos no botão "Finalizar" para evitar pedidos duplicados.

## 5. Fluxos de Usuário
1. **Lançamento:** Selecionar Mesa -> Adicionar Itens -> Confirmar Pedido.
2. **Pagamento:** Clicar em Fechar -> Escolher Método (Pix/Cartão/Dinheiro) -> Emitir Recibo.
3. **Integração:** O pedido é enviado via `POST /api/admin/orders` e notificado ao KDS via WebSocket.

## 6. Documentação Técnica (API)
- **Endpoints:** 
  - `GET /api/admin/{slug}/tables/dashboard`
  - `POST /api/admin/tables/{id}/pay`
  - `PATCH /api/admin/orders/{id}`

---
![POS Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-pos.png)
# 🛒 AdminWaiterPosPage
> **Plataforma:** WEB | **Domínio:** OPERACIONAL | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Ponto de Venda (PDV) fixo para balcão ou tablets. Oferece ferramentas de lançamento e fechamento em interface de alta densidade.

## 2. Estrutura e Layout (Componentes)
- **Product Matrix:** Grid de produtos com busca rápida.
- **Cart Sidebar:** Resumo do pedido atual.

## 3. Interações e Ações (Botões)
- **Quick Search:** Filtro por SKU ou nome.
- **Split Trigger:** Modal de divisão de conta.

## 4. Estados e Cenários (Loading/Error)
- **Processing Order:** Bloqueio de UI durante o envio.
- **Table Occupied:** Alerta visual se a mesa já estiver em uso.

## 5. Fluxo de Navegação
1. Seleção de mesa.
2. Lançamento de itens.
3. Fechamento de conta.

## 6. Documentação Técnica (API)
- **Endpoints:** `POST /api/admin/tables/{id}/pay`, `GET /api/admin/{slug}/tables/dashboard`
- **Assets:** ![POS Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/pos-full.png)


################################################################################


# Plataforma: WEB | Arquivo: AuditPage.md
# 📱 AuditPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/audit`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **INPUT**: Buscar logs... — *Ação: onChange* (type:text)

## 4. Estados e Comportamentos
**Estados Detectados:** loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> searchTerm

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.002632*


################################################################################


# Plataforma: WEB | Arquivo: CheckoutPage.md
# 📱 CheckoutPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/[slug]/checkout`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/checkoutpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\[slug]\checkout\page.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: ClientMenuPage.md
# 📱 ClientMenuPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/[slug]/menu`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
*(Descreva aqui o objetivo principal desta tela.)*

## 2. Screenshot de Referência
![Screenshot](../placeholders/clientmenupage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\[slug]\menu\page.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: CounterPage.md
# 📱 CounterPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/counter`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Ponto de venda (PDV) para operação de caixa rápida.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **INPUT**: Buscar produto... — *Ação: onChange* (type:text)
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> searchTerm
1. Executar -> product.id

## 6. Observações Críticas
Foco em acessibilidade por teclado (F2, Enter, Esc).

---
*Gerado automaticamente em 2026-01-18T08:13:19.002942*


################################################################################


# Plataforma: WEB | Arquivo: DashboardPage.md
# 📱 DashboardPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/dashboard`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Visão tática da operação. Decisões baseadas em dados em tempo real.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: Tentar novamente — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error

## 5. Fluxos de Navegação
1. Executar -> fetchMetrics
1. Executar -> p
1. Executar -> handleExport

## 6. Observações Críticas
Dados pesados devem ser carregados via Promise.all. Cache de SWR/React Query recomendado.

---
*Gerado automaticamente em 2026-01-18T08:13:19.003217*


################################################################################


# Plataforma: WEB | Arquivo: DeliveryPage.md
# 📱 DeliveryPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/delivery`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div, header

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick* (type:button)
- **BUTTON**: N/A — *Ação: onClick* (type:button)
- **BUTTON**: N/A — *Ação: onClick* (type:button)
- **BUTTON**: N/A — *Ação: onClick* (type:button)
- **BUTTON**: N/A — *Ação: onClick* (type:button)
- **BUTTON**: N/A — *Ação: onClick* (type:button)

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
- Navegação padrão.

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.003559*


################################################################################


# Plataforma: WEB | Arquivo: DriverPage.md
# 📱 DriverPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/driver`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div, header, main, section

## 3. Elementos Interativos
- **BUTTON**: driver.delivery.finish-btn — *Ação: onClick*
- **BUTTON**: driver.delivery.order.pickup — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> handleFinish

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.003863*


################################################################################


# Plataforma: WEB | Arquivo: ExpeditorPage.md
# 📱 ExpeditorPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/expeditor`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div, header

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
- Navegação padrão.

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.004129*


################################################################################


# Plataforma: WEB | Arquivo: FeaturesBetaPage.md
# 📱 FeaturesBetaPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/settings/features`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Configurações do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- *Nenhum elemento interativo detectado.*

## 4. Estados e Comportamentos
**Estados Detectados:** loading, empty

## 5. Fluxos de Navegação
- Navegação padrão.

## 6. Observações Críticas
Alterações sensíveis devem exigir confirmação.

---
*Gerado automaticamente em 2026-01-18T08:13:19.008789*


################################################################################


# Plataforma: WEB | Arquivo: FinancialAuditPage.md
# 📱 FinancialAuditPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/audit/financial`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error

## 5. Fluxos de Navegação
1. Executar -> fetchAuditData

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.009334*


################################################################################


# Plataforma: WEB | Arquivo: ForgotPasswordPage.md
# 📱 ForgotPasswordPage
> **Plataforma:** WEB
> **Rota:** `/admin/forgot-password`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div, form

## 3. Elementos Interativos
- **LINK**: Voltar para Login — *Ação: navigation*
- **BUTTON**: N/A — *Ação: interaction* (type:submit)
- **LINK**: N/A — *Ação: navigation*

## 4. Estados e Comportamentos
**Estados Detectados:** error

## 5. Fluxos de Navegação
1. Navegar -> /admin/login

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.001105*


################################################################################


# Plataforma: WEB | Arquivo: FranchisePage.md
# 📱 FranchisePage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/franchise`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **LINK**: N/A — *Ação: interaction*

## 4. Estados e Comportamentos
**Estados Detectados:** loading, error

## 5. Fluxos de Navegação
1. Navegar -> /admin/${store.slug}/dashboard (Dinâmico)

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.004391*


################################################################################


# Plataforma: WEB | Arquivo: InventoryPage.md
# 📱 InventoryPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/inventory`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: Buscar ingrediente... — *Ação: onChange* (type:text)
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: N/A — *Ação: onChange* (type:text)
- **SELECT**: N/A — *Ação: onChange*
- **INPUT**: N/A — *Ação: onChange* (type:number)
- **INPUT**: N/A — *Ação: onChange* (type:number)
- **INPUT**: N/A — *Ação: onChange* (type:number)
- **BUTTON**: Salvar — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> searchTerm
1. Executar -> form.name
1. Executar -> form.unit
1. Executar -> form.cost_per_unit
1. Executar -> form.current_stock
1. Executar -> form.min_stock_alert
1. Executar -> handleSubmit

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.004908*


################################################################################


# Plataforma: WEB | Arquivo: KioskAttractScreen.md
# 📱 KioskAttractScreen
> **Plataforma:** Web
> **Rota/Arquivo:** `/[slug]/kiosk`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/kioskattractscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\[slug]\kiosk\page.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: KitchenPage.md
# 📱 KitchenPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/kitchen`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Orquestração de produção (KDS). Substitui impressoras de cozinha.

## 2. Estrutura e Layout
**Containers:** div, header

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: RefreshCw size={24} /> — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> toggleListening
1. Executar -> toggleFullscreen
1. Executar -> fetchOrders

## 6. Observações Críticas
Deve manter estado local se a rede cair. Contraste alto para leitura à distância.

---
*Gerado automaticamente em 2026-01-18T08:13:19.005192*


################################################################################


# Plataforma: WEB | Arquivo: LandingPage.md
# 📱 LandingPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Porta de entrada comercial. Converte visitantes em leads ou contas de teste (PLG).

## 2. Screenshot de Referência
![Screenshot](../placeholders/landingpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\page.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: LoginPage.md
# 📱 LoginPage
> **Plataforma:** WEB
> **Rota:** `/admin/login`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Autenticação de usuário.

## 2. Estrutura e Layout
**Containers:** div, form

## 3. Elementos Interativos
- **LINK**: N/A — *Ação: navigation*
- **LINK**: Esqueceu a senha? — *Ação: navigation*
- **BUTTON**: login-submit — *Ação: interaction* (type:submit)
- **LINK**: Criar conta grátis — *Ação: navigation*

## 4. Estados e Comportamentos
**Estados Detectados:** error

## 5. Fluxos de Navegação
1. Navegar -> /
1. Navegar -> /admin/forgot-password
1. Navegar -> /admin/register

## 6. Observações Críticas
Verificar persistência de sessão.

---
*Gerado automaticamente em 2026-01-18T08:13:19.001411*


################################################################################


# Plataforma: WEB | Arquivo: MarketingPage.md
# 📱 MarketingPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/marketing`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: N/A — *Ação: onChange* (type:number)
- **BUTTON**: Salvar Configuração — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **A**: Configurar — *Ação: navigation*
- **INPUT**: Ex: Desconto de Verão — *Ação: onChange*
- **INPUT**: VERAO10 — *Ação: onChange*
- **SELECT**: N/A — *Ação: onChange*
- **INPUT**: 10 — *Ação: onChange* (type:number)
- **INPUT**: N/A — *Ação: onChange* (type:number)
- **INPUT**: Ilimitado — *Ação: onChange* (type:number)
- **BUTTON**: Criar Promoção — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> handleTrainAI
1. Executar -> loyalty
1. Executar -> handleSaveLoyalty
1. Navegar -> settings
1. Executar -> promoForm.name
1. Executar -> promoForm.code
1. Executar -> promoForm.discount_type
1. Executar -> promoForm.discount_value
1. Executar -> promoForm.min_order_value
1. Executar -> promoForm.usage_limit
1. Executar -> handleCreatePromo

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.005592*


################################################################################


# Plataforma: WEB | Arquivo: OfflinePage.md
# 📱 OfflinePage
> **Plataforma:** Web
> **Rota/Arquivo:** `/offline`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/offlinepage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\offline\page.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: PaymentCallbackPage.md
# 📱 PaymentCallbackPage
> **Plataforma:** WEB
> **Rota:** `/admin/payment/callback`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error

## 5. Fluxos de Navegação
- Navegação padrão.

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.009604*


################################################################################


# Plataforma: WEB | Arquivo: ProfilePage.md
# 📱 ProfilePage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/profile`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div, form

## 3. Elementos Interativos
- **INPUT**: N/A — *Ação: onChange* (required, type:password)
- **INPUT**: N/A — *Ação: onChange* (required, type:password)
- **INPUT**: N/A — *Ação: onChange* (required, type:password)
- **BUTTON**: N/A — *Ação: interaction* (type:submit)

## 4. Estados e Comportamentos
**Estados Detectados:** loading, error

## 5. Fluxos de Navegação
1. Executar -> passForm.current_password
1. Executar -> passForm.new_password
1. Executar -> passForm.confirm_password

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.006178*


################################################################################


# Plataforma: WEB | Arquivo: PublicMonitorPage.md
# 📱 PublicMonitorPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/[slug]/monitor`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/publicmonitorpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\[slug]\monitor\page.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: QuickPosPage.md
# 📱 QuickPosPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/waiter/pos/quick`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/quickpospage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\waiter\pos\quick\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: RegisterPage.md
# 📱 RegisterPage
> **Plataforma:** WEB
> **Rota:** `/admin/register`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Cadastro de novos usuários/tenants.

## 2. Estrutura e Layout
**Containers:** div, form

## 3. Elementos Interativos
- **LINK**: N/A — *Ação: navigation*
- **INPUT**: N/A — *Ação: interaction* (type:radio)
- **INPUT**: link-da-loja — *Ação: interaction*
- **BUTTON**: N/A — *Ação: interaction* (type:submit)
- **LINK**: Fazer Login — *Ação: navigation*

## 4. Estados e Comportamentos
**Estados Detectados:** error

## 5. Fluxos de Navegação
1. Navegar -> /
1. Navegar -> /admin/login

## 6. Observações Críticas
Validar inputs em tempo real.

---
*Gerado automaticamente em 2026-01-18T08:13:19.001746*


################################################################################


# Plataforma: WEB | Arquivo: ResetPasswordPage.md
# 📱 ResetPasswordPage
> **Plataforma:** WEB
> **Rota:** `/admin/reset-password`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div, form

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: interaction* (type:submit)

## 4. Estados e Comportamentos
**Estados Detectados:** error

## 5. Fluxos de Navegação
- Navegação padrão.

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.002102*


################################################################################


# Plataforma: WEB | Arquivo: SettingsPage.md
# 📱 SettingsPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/settings`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Configurações do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **IMAGEUPLOAD**: N/A — *Ação: onChange*
- **IMAGEUPLOAD**: N/A — *Ação: onChange*
- **BUTTON**: N/A — *Ação: onClick* (type:button)
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error

## 5. Fluxos de Navegação
1. Executar -> handleSubmit(onSubmit)
1. Executar -> tab.id
1. Executar -> watchedLogo
1. Executar -> watchedBanner

## 6. Observações Críticas
Alterações sensíveis devem exigir confirmação.

---
*Gerado automaticamente em 2026-01-18T08:13:19.006459*


################################################################################


# Plataforma: WEB | Arquivo: SupportPage.md
# 📱 SupportPage
> **Plataforma:** WEB
> **Rota:** `/admin/support`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div, form

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: interaction* (type:submit)

## 4. Estados e Comportamentos
**Estados Detectados:** loading, error

## 5. Fluxos de Navegação
- Navegação padrão.

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.002390*


################################################################################


# Plataforma: WEB | Arquivo: TablesPage.md
# 📱 TablesPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/tables`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: N/A — *Ação: onChange* (type:number)
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: Nome do Cliente — *Ação: onChange* (type:text)
- **BUTTON**: Abrir — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error

## 5. Fluxos de Navegação
1. Executar -> newTableNumber
1. Executar -> handleCreateTable
1. Executar -> customerName
1. Executar -> handleOpenTable

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.006720*


################################################################################


# Plataforma: WEB | Arquivo: TeamPage.md
# 📱 TeamPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/team`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div, form

## 3. Elementos Interativos
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: Buscar por nome ou email... — *Ação: onChange* (type:text)
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: N/A — *Ação: interaction* (type:radio)
- **INPUT**: N/A — *Ação: interaction* (type:radio)
- **INPUT**: N/A — *Ação: interaction* (type:radio)
- **INPUT**: N/A — *Ação: interaction* (type:radio)
- **BUTTON**: Cadastrar Membro — *Ação: interaction* (type:submit)

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> searchTerm
1. Executar -> tab.id

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.007015*


################################################################################


# Plataforma: WEB | Arquivo: TrustCenterPage.md
# 📱 TrustCenterPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/trust`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/trustcenterpage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\trust\page.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Link**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: TrustSecurityPage.md
# 🔐 TrustSecurityPage
> **Plataforma:** WEB | **Domínio:** SEGURANÇA | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Detalhamento técnico das camadas de defesa do sistema. Destinado a CTOs e auditores de segurança, este documento prova como o MesaFlow protege os dados sensíveis e garante o isolamento entre empresas.

## 2. Estrutura Técnica (Deep Dive)
- **Data Isolation (RLS):** Explicação visual de como o Row-Level Security do PostgreSQL impede o vazamento de dados entre Tenants.
- **Encryption Standards:** Detalhes sobre o uso de TLS 1.2+ para trânsito e AES-256 para dados em repouso.
- **Authentication Architecture:** Descrição do fluxo JWT com rotação de tokens e blacklist via Redis.

## 3. Elementos de Prova
- **Audit Log Samples:** Exemplos (sanitizados) de como o sistema registra ações administrativas.
- **Threat Model:** Menção ao uso do framework STRIDE para mitigação de ameaças.
- **Security Headers:** Lista de headers ativos (CSP, HSTS, X-Frame-Options).

## 4. Regras de Segurança (Manifesto)
- **Zero Trust:** O sistema nunca confia no cliente; toda validação ocorre no Kernel do Backend.
- **Least Privilege:** Roles de banco de dados e API com permissões mínimas necessárias.
- **Immutable Ledger:** Garantia de que registros financeiros não podem ser alterados ou deletados.

## 5. Estados e Cenários
- **Informational:** Texto denso e técnico, organizado em seções expansíveis (Accordions).
- **Contact:** Formulário ou link para contato direto com o DPO (Data Protection Officer).

## 6. Referências de Infraestrutura
- **Database:** PostgreSQL 15 (Neon.tech) com isolamento físico via engine.
- **Auth:** Implementação customizada de OAuth2 com Bcrypt para hashes de senha.

---
*MesaFlow Security — Blindado por Design.*



################################################################################


# Plataforma: WEB | Arquivo: TrustStatusPage.md
# 🟢 TrustStatusPage
> **Plataforma:** WEB | **Domínio:** OBSERVABILIDADE | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Monitor de saúde do sistema em tempo real. Fornece aos lojistas e desenvolvedores a confirmação visual de que todos os subsistemas (API, Banco, Real-time) estão operacionais, reduzindo chamados de suporte durante instabilidades globais.

## 2. Estrutura e Componentes (Real-time)
- **Global Status Indicator:** Banner principal (Verde/Amarelo/Vermelho) com o estado geral do ecossistema.
- **Service Health Grid:** Lista individual de componentes:
  - **API Gateway:** Latência e disponibilidade.
  - **Database Engine:** Conectividade do banco relacional.
  - **Real-time Broker:** Status do Redis e WebSockets.
- **Uptime History:** Gráfico de barras dos últimos 90 dias de operação.

## 3. Elementos Interativos
- **Manual Refresh:** Botão para forçar uma nova verificação de saúde.
- **Incident History:** Lista cronológica de manutenções programadas e incidentes passados com resoluções.
- **Subscribe to Alerts:** Opção para receber notificações de status via e-mail ou webhook.

## 4. Regras de Monitoramento
- **Healthcheck Endpoint:** Consome a rota `/api/health` do backend.
- **Polling Frequency:** Atualização automática a cada 30 segundos.
- **Fail-Open Logic:** Se o monitor falhar ao conectar, ele reporta "Status Desconhecido" em vez de "Operacional".

## 5. Estados da Interface
- **Healthy:** Todos os serviços em verde.
- **Degraded:** Um ou mais serviços com latência alta ou falhas parciais.
- **Outage:** Falha crítica em componentes core (API ou DB).

## 6. Integração Técnica
- **Backend:** `GET /api/health` retorna JSON com status de cada serviço.
- **Frontend:** Utiliza SWR com revalidação em foco para garantir dados frescos.

---
*MesaFlow Status — Transparência em tempo real.*
# 🟢 TrustStatusPage
> **Plataforma:** WEB | **Domínio:** OBSERVABILIDADE | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Monitor de disponibilidade pública. Prova a estabilidade do sistema através de métricas reais de uptime.

## 2. Estrutura e Layout (Componentes)
- **Live Vitals:** Status individual de API, DB e Redis.
- **Uptime Calendar:** Histórico visual dos últimos 90 dias.

## 3. Interações e Ações (Botões)
- **Refresh Health:** Força nova checagem de sinais vitais.
- **Subscribe:** Cadastro para alertas.

## 4. Estados e Cenários (Loading/Error)
- **Operational:** Tudo verde.
- **Major Outage:** Alerta vermelho para serviços offline.

## 5. Fluxo de Navegação
1. Acesso via Trust Center.
2. Consulta de status.
3. Verificação de histórico.

## 6. Documentação Técnica (API)
- **Endpoints:** `GET /api/health`
- **Assets:** ![Status Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/status-full.png)


################################################################################


# Plataforma: WEB | Arquivo: WaiterOrdersPage.md
# 📱 WaiterOrdersPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/waiter/orders`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **INPUT**: Buscar por mesa ou cliente... — *Ação: onChange* (type:text)
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error, empty

## 5. Fluxos de Navegação
1. Executar -> search

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.007517*


################################################################################


# Plataforma: WEB | Arquivo: WaiterPosPage.md
# 📱 WaiterPosPage
> **Plataforma:** Web
> **Rota/Arquivo:** `/admin/[slug]/waiter/pos/[tableId]`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/waiterpospage_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `frontend\src\app\admin\[slug]\waiter\pos\[tableId]\page.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: WEB | Arquivo: WaiterTablesPage.md
# 📱 WaiterTablesPage
> **Plataforma:** WEB
> **Rota:** `/admin/hamburgueria-ze/waiter`
> **Status:** AUTOMATED_DOC

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Estrutura e Layout
**Containers:** div

## 3. Elementos Interativos
- **BUTTON**: RefreshCw size={18}/> — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **INPUT**: N/A — *Ação: onChange* (type:text)
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*
- **BUTTON**: N/A — *Ação: onClick*

## 4. Estados e Comportamentos
**Estados Detectados:** interactive, loading, error

## 5. Fluxos de Navegação
1. Executar -> fetchTables
1. Executar -> `Buscar ${terms.table
1. Executar -> table.id

## 6. Observações Críticas
Nenhuma observação crítica registrada automaticamente.

---
*Gerado automaticamente em 2026-01-18T08:13:19.007254*


################################################################################


# Plataforma: MOBILE | Arquivo: AuthLoginscreen.md
# 🔐 AuthLoginScreen
> **Plataforma:** MOBILE | **Domínio:** AUTH | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Porta de entrada única para o staff operacional (Garçons, Cozinha e Motoristas). Garante que apenas usuários autorizados acessem o kernel de operações do restaurante, vinculando o dispositivo ao Tenant correto.

## 2. Estrutura e Design (Mobile-First)
- **Estética:** Dark-mode nativo para redução de fadiga ocular em turnos noturnos.
- **Componentes:** Utiliza `AuthInput` com ícones da Lucide e `Button` com feedback tátil (Haptic).
- **Keyboard Handling:** Implementação de `KeyboardAvoidingView` para garantir que o teclado não cubra os campos de input em telas pequenas.

## 3. Elementos Interativos
- **Campos de Input:** E-mail e Senha com validação em tempo real.
- **Toggle de Visibilidade:** Ícone de olho para mostrar/ocultar a senha.
- **Botão de Acesso:** Dispara o fluxo de autenticação e exibe estado de `loading` (Spinner).

## 4. Segurança e Persistência
- **JWT Flow:** O app recebe `access_token` e `refresh_token`.
- **SecureStore:** Armazenamento criptografado dos tokens no hardware do dispositivo.
- **Auto-Hydration:** Ao abrir o app, o `useAuthStore` verifica a validade do token e pula o login se a sessão estiver ativa.

## 5. Estados de Erro
- **Credenciais Inválidas:** Feedback visual vermelho com a mensagem "E-mail ou senha incorretos".
- **Rede Offline:** Bloqueio do botão de login com aviso de "Sem conexão com o servidor".

## 6. Fluxo Técnico
1. Usuário digita credenciais.
2. App chama `POST /api/auth/token`.
3. Sucesso: Decodifica claims (Role/CompanyID), salva no storage e navega para a `AppStack`.

---
*MesaFlow Mobile Kernel v5.0*



################################################################################


# Plataforma: MOBILE | Arquivo: DriverDashboard.md
# 📱 DriverDashboard
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/driver/DriverDashboard.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Gestão de entregas para motoboys próprios.

## 2. Screenshot de Referência
![Screenshot](../placeholders/driverdashboard_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\driver\DriverDashboard.tsx`
**Hooks:** `useAuth, useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: DriverdashboardScreen.md
# 🛵 DriverDashboardScreen
> **Plataforma:** MOBILE | **Domínio:** LOGÍSTICA | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Interface principal para o entregador da frota própria. Permite a visualização de pedidos prontos para entrega, gestão de rotas ativas e confirmação de recebimento no destino final, integrando telemetria GPS em tempo real.

## 2. Estrutura e Layout (Mobile-First)
- **Delivery Tabs:** Alternância entre "A Retirar" (Pedidos na expedição) e "Em Rota" (Entregas em curso).
- **Map View:** Integração com Leaflet/Google Maps para visualização do trajeto e localização do cliente.
- **Order Cards:** Informações críticas em destaque: Nome do Cliente, Endereço e Valor a Receber (se for dinheiro).

## 3. Elementos Interativos
- **Pickup Trigger:** Botão "Pegar Pedido" que inicia o rastreamento e notifica o cliente via WebSocket.
- **Navigation Shortcuts:** Botões de atalho para abrir o endereço diretamente no **Waze** ou **Google Maps**.
- **POD (Proof of Delivery):** Campo para inserção do código de segurança fornecido pelo cliente para finalizar a entrega.

## 4. Regras de Negócio e Logística
- **GPS Telemetry:** O app envia coordenadas a cada 3 segundos enquanto houver uma entrega ativa.
- **Cash Management:** Registra automaticamente dívidas no `DriverLedger` para pedidos pagos em dinheiro no ato da entrega.
- **Idempotência de Coleta:** Impede que dois motoristas coletem o mesmo pedido simultaneamente através de locks no backend.

## 5. Estados da Tela
- **Idle:** Lista de pedidos disponíveis para coleta.
- **Active Delivery:** Modo focado no mapa e informações de trânsito.
- **Offline:** Aviso de perda de sinal GPS ou internet, mantendo os dados da rota atual em cache.

## 6. Fluxo Técnico (Real-time)
1. Motorista clica em "Pegar".
2. App chama `PATCH /api/admin/delivery/orders/{id}/dispatch`.
3. Backend emite evento `delivery.status` para o cliente.
4. App inicia o loop de `POST /api/admin/delivery/orders/{id}/location`.

---
*MesaFlow Logistics Kernel v5.0*



################################################################################


# Plataforma: MOBILE | Arquivo: HomeScreen.md
# 📱 HomeScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/app/HomeScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/homescreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\app\HomeScreen.tsx`
**Hooks:** `useAuth`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Button**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: KitchenDashboard.md
# 📱 KitchenDashboard
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/kitchen/KitchenDashboard.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/kitchendashboard_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\kitchen\KitchenDashboard.tsx`
**Hooks:** `useAuth, useEffect`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: KitchendashboardScreen.md
# 📱 KitchenDashboardScreen
> **Plataforma:** MOBILE | **Domínio:** KDS | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Versão nativa do Monitor de Produção, otimizada para tablets instalados em áreas de calor (cozinha) ou balcões de entrega. Sua função é fornecer uma interface de toque robusta para que os cozinheiros gerenciem a fila de produção com zero atrito.

## 2. Estrutura e Design (Industrial)
- **High-Contrast Cards:** Pedidos exibidos em blocos grandes com fontes de alta legibilidade para leitura à distância.
- **Touch-First Controls:** Botões de ação dimensionados para operação rápida, mesmo com luvas ou mãos úmidas.
- **Grid Adaptativo:** Ajuste automático do número de colunas baseado na orientação do tablet (Landscape/Portrait).

## 3. Elementos Interativos
- **Status Advance:** Toque longo ou clique duplo para mover o pedido para "Pronto", evitando toques acidentais.
- **Item Check-off:** Permite marcar itens individuais como "preparados" dentro de um pedido complexo.
- **Sound Toggle:** Controle de alertas sonoros para novos pedidos diretamente na interface.

## 4. Regras de Produção (KDS)
- **SLA Visual:** O card muda de cor (Verde -> Amarelo -> Vermelho) conforme o tempo de preparo configurado.
- **Station Isolation:** O dispositivo pode ser configurado para exibir apenas itens de uma praça específica (ex: apenas "Grelhados").
- **Persistent State:** Em caso de reinicialização do app, a lista de pedidos é recuperada do cache local (`AsyncStorage`) antes da sincronia com o servidor.

## 5. Estados da Tela
- **New Order Flash:** Animação de borda pulsante para destacar a chegada de novos pedidos.
- **Offline Warning:** Banner persistente caso a conexão com o WebSocket seja interrompida.
- **Empty Queue:** Tela de descanso com estatísticas rápidas do turno.

## 6. Fluxo Técnico
- **WebSocket:** Recebe eventos `new_order` e `order_update` via Redis Pub/Sub.
- **Haptic Feedback:** Vibração do dispositivo ao atingir estados críticos de atraso.
- **API:** `PATCH /api/admin/orders/{id}` para atualização de status.

---
*MesaFlow Mobile Kernel v5.0*



################################################################################


# Plataforma: MOBILE | Arquivo: LoadingScreen.md
# 📱 LoadingScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/common/LoadingScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/loadingscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\common\LoadingScreen.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] *Nenhum elemento interativo detectado.*

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: LoginScreen.md
# 📱 LoginScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/auth/LoginScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Autenticação segura e persistente no dispositivo.

## 2. Screenshot de Referência
![Screenshot](../placeholders/loginscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\auth\LoginScreen.tsx`
**Hooks:** `useAuth, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: OrderEntryScreen.md
# 📱 OrderEntryScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/waiter/OrderEntryScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/orderentryscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\waiter\OrderEntryScreen.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: OrderReviewScreen.md
# 📱 OrderReviewScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/waiter/OrderReviewScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/orderreviewscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\waiter\OrderReviewScreen.tsx`
**Hooks:** `useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Button**: (Descrever ação)
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: OrdersScreen.md
# 📱 OrdersScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/orders/OrdersScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/ordersscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\orders\OrdersScreen.tsx`
**Hooks:** `useEffect`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Button**: (Descrever ação)
- [ ] **Pressable**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: PaymentScreen.md
# 📱 PaymentScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/waiter/PaymentScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/paymentscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\waiter\PaymentScreen.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Button**: (Descrever ação)
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: PrinterDebugScreen.md
# 📱 PrinterDebugScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/waiter/PrinterDebugScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/printerdebugscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\waiter\PrinterDebugScreen.tsx`
**Hooks:** `useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Button**: (Descrever ação)
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: WaitercallsScreen.md
# 📱 WaiterCallsScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/waiter/WaiterCallsScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/waitercallsscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\waiter\WaiterCallsScreen.tsx`
**Hooks:** ``

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **Button**: (Descrever ação)
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: WaiterDashboard.md
# 📱 WaiterDashboard
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/waiter/WaiterDashboard.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Gestão de salão em movimento para garçons.

## 2. Screenshot de Referência
![Screenshot](../placeholders/waiterdashboard_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\waiter\WaiterDashboard.tsx`
**Hooks:** `useAuth`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################


# Plataforma: MOBILE | Arquivo: WaiterdashboardScreen.md
# 🏠 WaiterDashboardScreen
> **Plataforma:** MOBILE | **Domínio:** OPERACIONAL | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
O Dashboard do Garçom é o hub inicial de produtividade. Ele fornece uma visão panorâmica das responsabilidades do funcionário no turno, incluindo suas mesas ativas, total de vendas acumuladas e acesso rápido às ferramentas de lançamento e fechamento.

## 2. Estrutura e Design
- **Performance Widgets:** Cards com métricas pessoais (Total Vendido, Gorjetas Estimadas).
- **Active Sessions Carousel:** Atalhos para as últimas mesas onde o garçom realizou lançamentos.
- **Quick Action Grid:** Botões grandes para "Abrir Nova Mesa", "Lançamento Rápido" e "Ver Chamados".

## 3. Elementos Interativos
- **Profile Switcher:** Acesso às configurações de perfil e logout seguro.
- **Notification Bell:** Indicador visual de chamados pendentes com contador em tempo real.
- **Shift Toggle:** Funcionalidade para iniciar ou encerrar o turno de trabalho (Audit Trail).

## 4. Regras de Negócio
- **Role Enforcement:** A interface adapta os botões visíveis baseada na permissão do usuário (ex: Garçom vs Gerente).
- **Data Hydration:** Carregamento inicial via `useAuthStore` para garantir que o contexto do Tenant (CompanyID) esteja correto.
- **Cache Policy:** Utiliza `AsyncStorage` para manter as métricas visíveis mesmo em zonas de sombra de Wi-Fi.

## 5. Estados e Cenários
- **Loading:** Skeletons circulares para os widgets de performance.
- **Offline Mode:** Banner de "Modo Offline" com acesso restrito apenas a funções de consulta local.
- **Error Boundary:** Captura de falhas de renderização com opção de reinicialização do app.

## 6. Fluxo de Navegação
1. O usuário loga e cai no Dashboard.
2. O sistema valida o cargo e carrega as métricas via `GET /api/admin/metrics/staff`.
3. O garçom seleciona uma ação e transita para a `AppStack`.

---
*MesaFlow Mobile Kernel v5.0*



################################################################################


# Plataforma: MOBILE | Arquivo: WaiterOrderentryscreen.md
# 📝 WaiterOrderentryScreen
> **Plataforma:** MOBILE | **Domínio:** WAITER | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Interface de alta performance para garçons realizarem o lançamento de pedidos na mesa. Focada em velocidade de toque e redução de erros de comunicação com a cozinha.

## 2. Estrutura Técnica
- **Header Dinâmico:** Exibe o número da mesa selecionada e o nome do cliente.
- **Category Scroller:** Navegação horizontal por ícones para troca rápida de seção (Bebidas, Lanches, Sobremesas).
- **Product List:** Utiliza `FlashList` (Shopify) para garantir scroll a 60fps mesmo com centenas de itens.

## 3. Elementos Interativos
- **Contador de Quantidade:** Botões de +/- integrados ao card do produto.
- **Campo de Notas:** Acesso rápido para digitar observações (ex: "Sem cebola", "Gelo e limão").
- **Floating Cart Button:** Botão flutuante que exibe o total parcial e leva à revisão do pedido.

## 4. Regras de Negócio (Mobile POS)
- **Volatile Cart:** O carrinho é limpo automaticamente após o envio ou se o garçom trocar de mesa.
- **SLA Awareness:** O tempo de preparo estimado é exibido para que o garçom possa informar o cliente.
- **Offline Queue:** Se a rede cair, o pedido é salvo no `AsyncStorage` e enviado automaticamente quando o sinal retornar.

## 5. Estados da Tela
- **Loading:** Shimmer effects durante o carregamento do cardápio.
- **Search Mode:** Overlay de busca que filtra a lista conforme o garçom digita.
- **Success:** Feedback de "Pedido Enviado" com animação de check.

## 6. Fluxo de Dados
- **Store:** Consome `useWaiterStore` para gerenciar o estado do carrinho.
- **Sync:** Dispara evento `new_order` via WebSocket para atualizar o KDS instantaneamente.

---
*MesaFlow Mobile Kernel v5.0*



################################################################################


# Plataforma: MOBILE | Arquivo: WaiterOrderreviewScreen.md
# 📋 WaiterOrderreviewScreen
> **Plataforma:** MOBILE | **Domínio:** WAITER | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta tela serve como o "Check-out de Lançamento". É o ponto de revisão final onde o garçom valida os itens selecionados, ajusta quantidades e confirma o envio para a cozinha, garantindo a precisão do pedido antes da produção.

## 2. Estrutura e Layout (UX)
- **Order Summary List:** Exibição compacta dos itens com destaque para modificadores e observações.
- **Financial Footer:** Totalizador destacado com cálculo automático de subtotal.
- **Action Bar:** Botões fixos para "Adicionar Mais Itens" e "Confirmar e Enviar".

## 3. Elementos Interativos
- **Swipe to Delete:** Gesto lateral para remover itens do carrinho de forma rápida.
- **Quantity Adjuster:** Botões de incremento/decremento para ajustes de última hora.
- **Submit Trigger:** Botão de confirmação com estado de `loading` para prevenir envios duplicados.

## 4. Regras de Negócio e Validação
- **Empty Cart Guard:** O botão de envio é desabilitado se o carrinho estiver vazio.
- **Table Context:** O sistema valida se a mesa ainda está ativa no backend antes de processar o envio.
- **Optimistic Feedback:** A UI exibe uma animação de sucesso imediata após o 200 OK da API.

## 5. Estados da Tela
- **Submitting:** Overlay de processamento que bloqueia interações durante a persistência.
- **Network Error:** Alerta nativo caso a conexão falhe, oferecendo a opção de salvar na **Fila Offline**.
- **Success View:** Transição para a tela de confirmação com opção de impressão de ticket.

## 6. Fluxo Técnico e API
1. **Persistência:** Chamada ao endpoint `POST /api/hamburgueria-ze/orders`.
2. **Payload:** Envio de array de `product_id`, `quantity` e `notes`.
3. **Broadcast:** O backend emite um evento `new_order` via WebSocket para todos os terminais KDS.

---
*MesaFlow Mobile Kernel v5.0*



################################################################################


# Plataforma: MOBILE | Arquivo: WaiterPaymentScreen.md
# 💰 WaiterPaymentScreen
> **Plataforma:** MOBILE | **Domínio:** FINTECH | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Interface de checkout móvel que transforma o smartphone do garçom em um terminal de recebimento. Permite processar pagamentos via Pix (dinâmico), Dinheiro (com calculadora de troco) e Cartão, integrando o fluxo financeiro diretamente ao Ledger do sistema.

## 2. Estrutura e Componentes
- **Order Summary Header:** Exibição do total da mesa, taxa de serviço e descontos aplicados.
- **Payment Method Grid:** Seleção intuitiva entre Pix, Dinheiro e Cartão.
- **Dynamic QR Code Area:** Renderização nativa do código Pix gerado pelo gateway.
- **Change Calculator:** Teclado numérico otimizado para cálculo de troco em tempo real.

## 3. Elementos Interativos
- **Generate Pix Button:** Dispara a criação da transação no Mercado Pago/Stripe.
- **Manual Confirmation:** Botão de "Confirmar Recebimento" para validação visual do staff.
- **Tip Adjuster:** Permite alterar o valor da gorjeta antes de gerar o total final.

## 4. Regras de Negócio (Fintech)
- **Idempotency Lock:** Impede a geração de múltiplos QR Codes para a mesma tentativa de pagamento.
- **Ledger Entry:** Cada confirmação de pagamento cria um registro imutável no `FinancialLedger` com hash de integridade.
- **Split Logic:** Aplica automaticamente a retenção de comissão da plataforma conforme configurado no Tenant.

## 5. Estados da Tela
- **Processing:** Overlay de carregamento durante a comunicação com o gateway de pagamento.
- **Success Animation:** Feedback visual e tátil (vibration) após a confirmação do pagamento.
- **Payment Failed:** Diagnóstico de erro amigável com opção de troca de método de pagamento.

## 6. Integração Técnica
- **Endpoints:**
  - `POST /api/admin/tables/{id}/close`
  - `POST /api/admin/tables/{id}/pay`
- **Security:** Exige token JWT válido com permissão de `cashier` ou superior.

---
*MesaFlow Fintech Kernel v5.0*
# 💰 WaiterPaymentScreen
> **Plataforma:** MOBILE | **Domínio:** FINTECH | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Terminal de recebimento móvel. Permite o fechamento de contas na mesa com Pix dinâmico.

## 2. Estrutura e Layout (Componentes)
- **Totalizer:** Valor final com taxas.
- **Method Grid:** Seleção de Pix, Dinheiro ou Cartão.

## 3. Interações e Ações (Botões)
- **Generate Pix:** Cria transação no gateway.
- **Confirm Cash:** Baixa manual.

## 4. Estados e Cenários (Loading/Error)
- **Waiting Payment:** Exibição do QR Code.
- **Confirmed:** Animação de sucesso.

## 5. Fluxo de Navegação
1. Seleção de método.
2. Processamento.
3. Finalização.

## 6. Documentação Técnica (API)
- **Endpoints:** `POST /api/admin/tables/{id}/close`
- **Assets:** ![Payment Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/mobile-pay-full.png)


################################################################################


# Plataforma: MOBILE | Arquivo: WaiterPrinterdebugScreen.md
# 🖨️ WaiterPrinterdebugScreen
> **Plataforma:** MOBILE | **Domínio:** HARDWARE | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Ferramenta de diagnóstico e homologação de hardware. Permite que a equipe de suporte e o lojista testem a conectividade Bluetooth e a compatibilidade de comandos ESC/POS com impressoras térmicas locais.

## 2. Estrutura Técnica
- **Device Scanner:** Lista de dispositivos Bluetooth pareados e disponíveis no alcance.
- **Command Console:** Logs em tempo real dos bytes enviados para a impressora.
- **Test Suite:** Botões pré-configurados para testes de alinhamento, fontes e corte.

## 3. Elementos Interativos
- **Scan Devices:** Dispara a busca por novos periféricos via `react-native-ble-plx`.
- **Print Test Page:** Envia um buffer padrão contendo texto, negrito e um QR Code de teste.
- **Open Drawer:** Envia o comando de pulso elétrico para abertura de gaveta de dinheiro.

## 4. Regras de Homologação
- **Encoding Check:** Validação de caracteres especiais (acentuação) no padrão Latin-1.
- **Width Detection:** Configuração entre bobinas de 58mm (32 colunas) e 80mm (48 colunas).
- **Connection Persistence:** Opção de "Salvar como Padrão" para reconexão automática no boot.

## 5. Estados da Tela
- **Searching:** Animação de radar durante o escaneamento Bluetooth.
- **Connected:** Indicador verde com o nome e endereço MAC do hardware ativo.
- **Error:** Diagnóstico de falhas comuns (Bluetooth desligado, sem permissão de GPS).

## 6. Fluxo de Hardware
1. App solicita permissão de `BLUETOOTH_CONNECT`.
2. Usuário seleciona a impressora.
3. `PrinterService` estabelece o socket RFCOMM e envia o stream binário.

---
*MesaFlow Mobile Kernel v5.0*



################################################################################


# Plataforma: MOBILE | Arquivo: Waitertablesscreen.md
# 📱 WaiterTablesScreen
> **Plataforma:** Mobile
> **Rota/Arquivo:** `mobile/src/screens/waiter/WaiterTablesScreen.tsx`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** 2026-01-18

## 1. Propósito e Objetivo
Funcionalidade específica do sistema.

## 2. Screenshot de Referência
![Screenshot](../placeholders/waitertablesscreen_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `mobile\src\screens\waiter\WaiterTablesScreen.tsx`
**Hooks:** `useEffect, useState`

### Props
```typescript
Nenhuma interface de props explícita.
```

## 4. Elementos Interativos
- [ ] **TouchableOpacity**: (Descrever ação)

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
*(Liste regras específicas.)*

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*


################################################################################

