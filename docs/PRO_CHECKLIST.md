# 🚀 Checklist de Profissionalização SaaS: MesaFlow

Este documento registra os requisitos críticos para a transição do MVP para a fase Comercial (Produção).

## 🛡️ 1. Segurança e Resiliência (Hardening)
- [ ] **Anti-Spam de Pedidos:** Implementar Middleware de Rate Limiting. Limite de 1 pedido por sessão/IP a cada 30 segundos.
- [ ] **Senhas Fortes:** Implementar validador de complexidade de senha no Registro (Regex: Min 8 chars, letras e números).
- [ ] **Proteção de Admin:** Implementar bloqueio temporário de conta após 5 tentativas de login falhas.
- [ ] **Monitoramento de Erros:** Integração com Sentry.io para capturar falhas em tempo real (Back e Front).
- [ ] **Uptime:** Configuração de UptimeRobot para monitoramento de disponibilidade 24/7.

## 🏗️ 2. Verticalização (Multi-Segmento)
- [ ] **Registro Segmentado:** Adicionar campo `segment` no modelo de `Company` (Enum: GASTRO, EVENT, HOTEL, CORP).
- [ ] **Dicionário de Termos Dinâmico:** 
    - Se segment = HOTEL: "Mesa" vira "Quarto", "Garçom" vira "Serviço de Quarto".
    - Se segment = EVENT: "Mesa" vira "Assento/Camarote".
- [ ] **Formulário de Cadastro Pro:** Capturar telefone (WhatsApp) e cargo do responsável no momento do Sign-up.

## 💰 3. Motor de SaaS & Monetização
- [ ] **Gestão de Planos:** Adicionar campo `plan_tier` e `trial_ends_at` no banco de dados.
- [ ] **Paywalls (Limitações):**
    - Plano Free: Limite de 50 pedidos/mês e 15 itens no cardápio.
    - Bloqueio automático de funções se o Trial expirar.
- [ ] **Captura de Leads:** Criar pop-up de "Assine nossa Newsletter" ou "Baixe Guia de Gestão" para capturar e-mails de visitantes que não criaram conta.

## 📈 4. Marketing & Onboarding
- [ ] **Onboarding de Primeiro Acesso:** Tutorial guiado (Joyride) no Dashboard explicando: 1. Criar Categoria, 2. Adicionar Produto, 3. Gerar QR Code.
- [ ] **Melhoria da Landing Page:** Adicionar seção de "Casos de Uso" para Hotéis e Eventos.
- [ ] **CRM Interno:** Tela para o SuperAdmin (você) ver a lista de proprietários e status de uso.

## 🚀 5. Infraestrutura de Produção
- [ ] **Domínio Próprio:** Configuração de `mesaflow.com.br`.
- [ ] **Upgrade Render:** Migração para Plano Starter ($7) para eliminar o Cold Start.
- [ ] **HTTPS/SSL:** Garantir que o WebSocket (`wss://`) e API funcionem sob certificado seguro.


# 🚀 Checklist de Profissionalização SaaS: MesaFlow

## 🛡️ 1. Segurança e Resiliência (Hardening)
- [x] **Anti-Spam de Pedidos:** Implementar Middleware de Rate Limiting.
- [x] **Senhas Fortes:** Implementar validador de complexidade de senha.
- [x] **Proteção de Admin:** Implementar bloqueio temporário (Rate Limit no Login).
- [ ] **Monitoramento de Erros:** Integração com Sentry.io.
- [ ] **Uptime:** Configuração de UptimeRobot.

## 🏗️ 2. Verticalização (Multi-Segmento)
- [x] **Registro Segmentado:** Adicionar campo `segment` no modelo.
- [ ] **Dicionário de Termos Dinâmico:** (EM ANDAMENTO AGORA)
    - Se segment = HOTEL: "Mesa" vira "Quarto".
- [x] **Formulário de Cadastro Pro:** Capturar telefone e cargo.

## 💰 3. Motor de SaaS & Monetização
- [x] **Gestão de Planos:** Adicionar campo `plan_tier` e `trial_ends_at`.
- [ ] **Paywalls (Limitações):** (EM ANDAMENTO AGORA)
    - Plano Free: Limite de 50 pedidos/mês e 15 itens no cardápio.
- [ ] **Captura de Leads:** Criar pop-up de Newsletter.

## 📈 4. Marketing & Onboarding
- [ ] **Onboarding de Primeiro Acesso:** Tutorial guiado (Joyride).
- [ ] **Melhoria da Landing Page:** Seção de Casos de Uso.
- [ ] **CRM Interno:** Tela para o SuperAdmin.

## 🚀 5. Infraestrutura de Produção
- [ ] **Domínio Próprio:** Configuração de DNS.
- [ ] **HTTPS/SSL:** Certificados seguros.





# 🚀 Checklist de Profissionalização SaaS: MesaFlow

Este documento registra os requisitos críticos para a transição do MVP para a fase Comercial (Produção).

## 🛡️ 1. Segurança e Resiliência (Hardening)
- [x] **Anti-Spam de Pedidos:** Implementar Middleware de Rate Limiting.
- [x] **Senhas Fortes:** Implementar validador de complexidade de senha.
- [x] **Proteção de Admin:** Implementar bloqueio temporário de conta.
- [ ] **Monitoramento de Erros:** Integração com Sentry.io.
- [ ] **Uptime:** Configuração de UptimeRobot.

## 🏗️ 2. Verticalização (Multi-Segmento)
- [x] **Registro Segmentado:** Adicionar campo `segment` no modelo.
- [x] **Dicionário de Termos Dinâmico:** Adaptação de "Mesa/Quarto" no frontend.
- [x] **Formulário de Cadastro Pro:** Capturar telefone e cargo.

## 💰 3. Motor de SaaS & Monetização
- [x] **Gestão de Planos:** Adicionar campo `plan_tier` e `trial_ends_at`.
- [x] **Paywalls (Limitações):** Bloqueio de produtos/pedidos no plano Free.
- [ ] **Captura de Leads:** (EM ANDAMENTO AGORA)

## 📈 4. Marketing & Onboarding
- [ ] **Onboarding de Primeiro Acesso:** (EM ANDAMENTO AGORA) Tutorial guiado.
- [ ] **Melhoria da Landing Page:** Adicionar seção de "Casos de Uso".
- [ ] **CRM Interno:** Tela para o SuperAdmin.

## 🚀 5. Infraestrutura de Produção
- [ ] **Domínio Próprio:** Configuração de `mesaflow.com.br`.
- [ ] **HTTPS/SSL:** Certificados seguros.



# 🚀 Checklist de Profissionalização SaaS: MesaFlow

Este documento registra os requisitos críticos para a transição do MVP para a fase Comercial (Produção).

## 🛡️ 1. Segurança e Resiliência (Hardening)
- [x] **Anti-Spam de Pedidos:** Implementar Middleware de Rate Limiting.
- [x] **Senhas Fortes:** Implementar validador de complexidade de senha.
- [x] **Proteção de Admin:** Implementar bloqueio temporário de conta.
- [ ] **Monitoramento de Erros:** Integração com Sentry.io (Pendente para Prod).
- [ ] **Uptime:** Configuração de UptimeRobot (Pendente para Prod).

## 🏗️ 2. Verticalização (Multi-Segmento)
- [x] **Registro Segmentado:** Adicionar campo `segment` no modelo.
- [x] **Dicionário de Termos Dinâmico:** Adaptação de "Mesa/Quarto" no frontend.
- [x] **Formulário de Cadastro Pro:** Capturar telefone e cargo.

## 💰 3. Motor de SaaS & Monetização
- [x] **Gestão de Planos:** Adicionar campo `plan_tier` e `trial_ends_at`.
- [x] **Paywalls (Limitações):** Bloqueio de produtos/pedidos no plano Free.
- [x] **Captura de Leads:** Pop-up de Newsletter na Home.

## 📈 4. Marketing & Onboarding
- [x] **Onboarding de Primeiro Acesso:** Tutorial guiado (Joyride).
- [x] **Melhoria da Landing Page:** Seção de Casos de Uso e Simulador.
- [ ] **CRM Interno:** Tela para o SuperAdmin (Fase 4).

## 🚀 5. Infraestrutura de Produção
- [ ] **Domínio Próprio:** Configuração de `mesaflow.com.br`.
- [ ] **HTTPS/SSL:** Certificados seguros.