# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico por `company_id`.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com Alerta Sonoro e Atualização Otimista.
- [x] **Gestão Admin:** CRUD de Categorias, Produtos e Mesas.
- [x] **Branding:** Personalização de cores e logos por restaurante.
- [x] **Segurança:** Autenticação JWT e proteção de rotas administrativas.
- [x] **Regras de Negócio:** Horário de funcionamento e métodos de pagamento (Pix/Cartão/Dinheiro).

## 🔄 Fase 2: Profissionalização & SaaS (EM ANDAMENTO)
- [x] **Perfil do Usuário:** Interface para edição de dados cadastrais e senha.
- [x] **Gestão de Adicionais:** Interface para criar Grupos de Opções e Opções via Admin.
- [x] **Dashboard Avançado:** Gráficos de faturamento e filtros por período.
- [x] **Pagamentos (Modo Pix Direto):** Geração de QR Code estático para pagamento direto na conta do restaurante (Sem taxas, baixa manual).
- [ ] **Segurança:** Refresh Tokens e Logs de Auditoria.

## 🚀 Fase 3: Escala & Automação Financeira (FUTURO)
- [ ] **Ativar Mercado Pago:** Configurar Tokens de Produção para habilitar baixa automática.
- [ ] **Split de Pagamento:** Implementar divisão automática (Comissão SaaS vs Restaurante).
- [ ] **WebSockets:** Substituir Polling por comunicação bidirecional real.
- [ ] **PWA:** Tornar o frontend instalável como aplicativo.
- [ ] **WhatsApp API:** Notificações automáticas de status para o cliente.




# 🗺️ Roadmap MesaFlow (Atualizado)

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico total por `company_id`.
- [x] **Gestão Admin:** CRUD de Categorias, Produtos e Mesas.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets.

## ✅ Fase 2: Profissionalização & SaaS (CONCLUÍDO)
- [x] **Auto-Cadastro (Sign-up):** Donos criam suas próprias contas via Web.
- [x] **Refresh Tokens:** Sessão administrativa persistente por 7 dias.
- [x] **Controle de Estoque:** Bloqueio automático de produtos esgotados.
- [x] **Landing Page:** Página institucional moderna e persuasiva.
- [x] **PWA:** Aplicativo instalável no Android/iOS via navegador.
- [x] **Pagamentos (Modo Pix Direto):** QR Code dinâmico apontando para chave do dono.

## 🔄 Fase 3: Escala & Fintech (PRÓXIMOS PASSOS)
- [ ] **Integração Real Mercado Pago:** Sincronização de Webhooks em produção.
- [ ] **Split de Pagamento:** Divisão automática de comissão (SaaS vs Restaurante).
- [ ] **Suporte a Variações:** Tamanhos (P/M/G) e Meio-a-Meio.
- [ ] **WhatsApp API:** Notificação de "Pedido Pronto" para o cliente.






# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico por `company_id`.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets e Alerta Sonoro.
- [x] **Gestão Admin:** CRUD de Categorias, Produtos e Mesas.
- [x] **KDS Setorizado:** Filtros para Cozinha e Bar.

## ✅ Fase 2: Experiência & Híbrido (CONCLUÍDO)
- [x] **Modo Delivery:** Suporte a pedidos sem mesa (Endereço + Telefone).
- [x] **Sessão de Mesa (Comanda):** Segurança via Token e persistência de pedidos.
- [x] **Chamada de Garçom:** Notificação digital com tipos de serviço.
- [x] **Upselling (Recomendação):** Sugestão de produtos complementares no carrinho.
- [x] **Landing Page B2B:** Site institucional de alta conversão com i18n e animações.
- [x] **Conformidade:** Banner de Cookies e Página 404.

## 🔄 Fase 3: Profissionalização & Fintech (PRÓXIMO PASSO)
- [ ] **Perfil do Usuário Avançado:** Upload de Logo real, Configuração de Cores, Horários complexos.
- [ ] **Tela de Login/Registro 2.0:** Layout Split, validações visuais e feedback refinado.
- [ ] **Pagamento Real (Split):** Integração profunda com Mercado Pago/Stripe para dividir o dinheiro (SaaS vs Restaurante) automaticamente.
- [ ] **Dashboard Financeiro:** Gráficos de faturamento real, ticket médio e projeções.
- [ ] **Gestão de Estoque Avançada:** Ficha técnica (Ingredientes).

## 🚀 Fase 4: Escala & Ecossistema (FUTURO)
- [ ] **PWA Real:** Instalação nativa no celular e cache offline.
- [ ] **Integração Fiscal:** Emissão de NFC-e/SAT.
- [ ] **WhatsApp Automation:** Notificações de status via Zap.
- [ ] **App do Garçom:** Interface móvel para lançar pedidos na mesa.

# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico por `company_id`.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets e Alerta Sonoro.
- [x] **Gestão Admin:** CRUD de Categorias, Produtos e Mesas.
- [x] **KDS Setorizado:** Filtros para Cozinha e Bar.

## ✅ Fase 2: Experiência & Híbrido (CONCLUÍDO)
- [x] **Modo Delivery:** Suporte a pedidos sem mesa (Endereço + Telefone).
- [x] **Sessão de Mesa (Comanda):** Segurança via Token e persistência de pedidos.
- [x] **Chamada de Garçom:** Notificação digital com tipos de serviço.
- [x] **Upselling (Recomendação):** Sugestão de produtos complementares no carrinho.
- [x] **Landing Page B2B:** Site institucional de alta conversão com i18n e animações.
- [x] **Conformidade:** Banner de Cookies e Página 404.
- [x] **Gestão de Mesas:** Criação em lote, Impressão de QR Codes e Status em Tempo Real.

## 🔄 Fase 3: Profissionalização & Fintech (PRÓXIMO PASSO)
- [ ] **Tela de Login/Registro 2.0:** Layout Split, validações visuais e feedback refinado.
- [ ] **Perfil do Usuário Avançado:** Upload de Logo real, Configuração de Cores, Horários complexos.
- [ ] **Pagamento Real (Split):** Integração profunda com Mercado Pago/Stripe para dividir o dinheiro (SaaS vs Restaurante) automaticamente.
- [ ] **Dashboard Financeiro:** Gráficos de faturamento real, ticket médio e projeções.
- [ ] **Gestão de Estoque Avançada:** Ficha técnica (Ingredientes).

## 🚀 Fase 4: Escala & Ecossistema (FUTURO)
- [ ] **PWA Real:** Instalação nativa no celular e cache offline.
- [ ] **Integração Fiscal:** Emissão de NFC-e/SAT.
- [ ] **WhatsApp Automation:** Notificações de status via Zap.
- [ ] **App do Garçom:** Interface móvel para lançar pedidos na mesa.
# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico por `company_id`.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets e Alerta Sonoro.
- [x] **Gestão Admin:** CRUD de Categorias, Produtos e Mesas.
- [x] **KDS Setorizado:** Filtros para Cozinha e Bar.

## ✅ Fase 2: Experiência & Híbrido (CONCLUÍDO)
- [x] **Modo Delivery:** Suporte a pedidos sem mesa (Endereço + Telefone).
- [x] **Sessão de Mesa (Comanda):** Segurança via Token e persistência de pedidos.
- [x] **Chamada de Garçom:** Notificação digital com tipos de serviço.
- [x] **Upselling (Recomendação):** Sugestão de produtos complementares no carrinho.
- [x] **Landing Page B2B:** Site institucional de alta conversão com i18n e animações.
- [x] **Gestão de Mesas:** Criação em lote, Impressão de QR Codes e Status em Tempo Real.

## 🔄 Fase 3: Profissionalização & Fintech (PRÓXIMO PASSO)
- [ ] **Tela de Login/Registro 2.0:** Layout Split, validações visuais e feedback refinado.
- [ ] **Perfil do Usuário Avançado:** Upload de Logo real, Configuração de Cores, Horários complexos.
- [ ] **Pagamento Real (Split):** Integração profunda com Mercado Pago/Stripe para dividir o dinheiro (SaaS vs Restaurante) automaticamente.
- [ ] **Dashboard Financeiro:** Gráficos de faturamento real, ticket médio e projeções.
- [ ] **Gestão de Estoque Avançada:** Ficha técnica (Ingredientes).
- [ ] **Gestão de Permissões (ACL):** Níveis de acesso (Dono, Gerente, Garçom, Cozinha).

## 🚀 Fase 4: Escala & Ecossistema (FUTURO)
- [ ] **PWA Real:** Instalação nativa no celular e cache offline.
- [ ] **Integração Fiscal:** Emissão de NFC-e/SAT.
- [ ] **WhatsApp Automation:** Notificações de status via Zap.
- [ ] **App do Garçom:** Interface móvel para lançar pedidos na mesa.



# docs/ROADMAP.md
```markdown
# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico por `company_id`.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets.

## ✅ Fase 2: Experiência & Híbrido (CONCLUÍDO)
- [x] **Modo Delivery:** Suporte a pedidos sem mesa.
- [x] **Sessão de Mesa:** Segurança via Token e persistência.
- [x] **Chamada de Garçom:** Notificação digital.
- [x] **Landing Page B2B:** Site institucional de alta conversão.
- [x] **Gestão de Mesas:** Mapa de sala visual (Drag & Drop).

## ✅ Fase 3: Profissionalização & Fintech (CONCLUÍDO)
- [x] **Login/Registro 2.0:** Layout Split, validações Zod e feedback visual.
- [x] **Perfil Avançado:** Upload de Logo (URL), Color Picker e Configurações.
- [x] **Motor Financeiro:** Cálculo seguro de Split de Pagamento e taxas.
- [x] **Gestão de Estoque:** Ficha técnica (Receitas) e baixa automática.
- [x] **Segurança:** Rate Limiting (Anti-Spam) e proteção de rotas.
- [x] **PWA:** Configuração de manifesto e service workers.

## 🚀 Fase 4: Escala & Ecossistema (FUTURO)
- [ ] **Integração Fiscal:** Emissão de NFC-e/SAT (Integração eNotas/Focus).
- [ ] **WhatsApp Automation:** Notificações de status via Zap (Twilio/Evolution).
- [ ] **App do Garçom:** Interface móvel dedicada para lançar pedidos na mesa.
- [ ] **Dashboard Multi-loja:** Visão consolidada para franquias.
- [ ] **Impressão Nativa:** Integração direta com impressoras térmicas via USB/RawBT.


# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico por `company_id`.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets.

## ✅ Fase 2: Experiência & Híbrido (CONCLUÍDO)
- [x] **Modo Delivery:** Suporte a pedidos sem mesa.
- [x] **Sessão de Mesa:** Segurança via Token e persistência.
- [x] **Chamada de Garçom:** Notificação digital.
- [x] **Landing Page B2B:** Site institucional de alta conversão.
- [x] **Gestão de Mesas:** Mapa de sala visual (Drag & Drop).

## ✅ Fase 3: Profissionalização & Fintech (CONCLUÍDO)
- [x] **Login/Registro 2.0:** Layout Split, validações Zod e feedback visual.
- [x] **Perfil Avançado:** Upload de Logo (URL), Color Picker e Configurações.
- [x] **Motor Financeiro:** Cálculo seguro de Split de Pagamento e taxas.
- [x] **Gestão de Estoque:** Ficha técnica (Receitas) e baixa automática.
- [x] **Segurança:** Rate Limiting (Anti-Spam) e proteção de rotas.
- [x] **PWA:** Configuração de manifesto e service workers.
- [x] **Onboarding:** Tour guiado para novos usuários.
- [x] **Verticalização:** Adaptação para Hotéis e Eventos.

## 🚀 Fase 4: Escala & Ecossistema (PRÓXIMOS PASSOS)
- [ ] **Integração Fiscal:** Emissão de NFC-e/SAT (Integração eNotas/Focus).
- [ ] **WhatsApp Automation:** Notificações de status via Zap (Twilio/Evolution).
- [ ] **App do Garçom:** Interface móvel dedicada para lançar pedidos na mesa.
- [ ] **Dashboard Multi-loja:** Visão consolidada para franquias.
- [ ] **Impressão Nativa:** Integração direta com impressoras térmicas via USB/RawBT.



# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico total por estabelecimento.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets e Alerta Sonoro.

## ✅ Fase 2: Profissionalização & Operação (CONCLUÍDO)
- [x] **App do Garçom (Mobile POS):** Lançamento de pedidos, troca de nomes e fechamento de conta.
- [x] **Gestão de Estoque (Regra 86):** Baixa automática por ficha técnica e bloqueio de produtos esgotados.
- [x] **Automação de WhatsApp:** Notificações de "Pedido Pronto" e "Mesa Aberta".
- [x] **Motor Financeiro SaaS:** Integração com Stripe para cobrança de mensalidades (Planos Free/Pro).
- [x] **Impressão Térmica:** Recibos formatados para 80mm/58mm.

## 🔄 Fase 3: Experiência do Usuário & Fintech (EM ANDAMENTO)
- [ ] **Login/Registro 2.0:** Layout profissional (Split Screen), validações visuais e feedback refinado.
- [ ] **Perfil do Usuário Avançado:** Upload de Logo, configuração de cores da marca e horários complexos.
- [ ] **Dashboard Financeiro:** Gráficos de faturamento real, ticket médio e produtos mais vendidos.
- [ ] **Integração Mercado Pago:** Ativação de Pix Dinâmico para o restaurante receber direto.

## 🚀 Fase 4: Escala & Ecossistema (FUTURO)
- [ ] **PWA Real:** Instalação nativa no celular e cache offline.
- [ ] **Integração Fiscal:** Emissão de NFC-e/SAT automática.
- [ ] **Multi-loja:** Gestão centralizada para franquias e redes.


# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico total por estabelecimento.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets e Alerta Sonoro.

## ✅ Fase 2: Profissionalização & Operação (CONCLUÍDO)
- [x] **App do Garçom (Mobile POS):** Lançamento de pedidos, troca de nomes e fechamento de conta.
- [x] **Gestão de Estoque (Regra 86):** Baixa automática por ficha técnica e bloqueio de produtos esgotados.
- [x] **Automação de WhatsApp:** Notificações de "Pedido Pronto" e "Mesa Aberta".
- [x] **Motor Financeiro SaaS:** Integração com Stripe para cobrança de mensalidades (Planos Free/Pro).
- [x] **Impressão Térmica:** Recibos formatados para 80mm/58mm.

## 🔄 Fase 3: Experiência do Usuário & Fintech (PRÓXIMOS PASSOS)
- [ ] **Login/Registro 2.0:** Layout profissional (Split Screen), validações visuais e feedback refinado.
- [ ] **Perfil do Usuário Avançado:** Upload de Logo, configuração de cores da marca e horários complexos.
- [ ] **Dashboard Financeiro:** Gráficos de faturamento real, ticket médio e produtos mais vendidos.
- [ ] **Integração Mercado Pago:** Ativação de Pix Dinâmico para o restaurante receber direto.

## 🚀 Fase 4: Escala & Ecossistema (FUTURO)
- [ ] **PWA Real:** Instalação nativa no celular e cache offline.
- [ ] **Integração Fiscal:** Emissão de NFC-e/SAT automática.
- [ ] **Multi-loja:** Gestão centralizada para franquias e redes.

# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico por `company_id`.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets.

## ✅ Fase 2: Experiência & Híbrido (CONCLUÍDO)
- [x] **Modo Delivery:** Suporte a pedidos sem mesa.
- [x] **Sessão de Mesa:** Segurança via Token e persistência.
- [x] **Chamada de Garçom:** Notificação digital.
- [x] **Landing Page B2B:** Site institucional de alta conversão.
- [x] **Gestão de Mesas:** Mapa de sala visual (Drag & Drop).

## ✅ Fase 3: Profissionalização & Fintech (CONCLUÍDO)
- [x] **Login/Registro 2.0:** Layout Split, validações Zod e feedback visual.
- [x] **Perfil Avançado:** Upload de Logo (URL), Color Picker e Configurações.
- [x] **Motor Financeiro:** Cálculo seguro de Split de Pagamento e taxas.
- [x] **Gestão de Estoque:** Ficha técnica (Receitas) e baixa automática.
- [x] **Segurança:** Rate Limiting (Anti-Spam) e proteção de rotas.
- [x] **PWA:** Configuração de manifesto e service workers.

## ✅ Fase 4: Escala & Ecossistema (CONCLUÍDO)
- [x] **Assinaturas SaaS:** Integração completa com Stripe (Checkout/Portal/Webhooks).
- [x] **Dashboard Financeiro:** Gráficos reais via SQL Aggregation.
- [x] **Fidelidade (Cashback):** Carteira digital automática para clientes.
- [x] **App do Garçom 2.0:** Mobile POS com Venda Balcão, Delivery e Transferência de Mesas.
- [x] **Logística (Driver App):** App do Entregador, Gestão de Frota e Despacho.
- [x] **Notificações Sensoriais:** Vibração e Som para garçons.

## 🚀 Fase 5: Enterprise & IA (PRÓXIMOS PASSOS)
- [ ] **Integração Fiscal:** Emissão de NFC-e/SAT (Integração eNotas/Focus).
- [ ] **WhatsApp Automation:** Notificações de status via Zap (Twilio/Evolution).
- [ ] **Dashboard Multi-loja:** Visão consolidada para franquias.
- [ ] **Impressão Nativa:** Integração direta com impressoras térmicas via USB/RawBT.
- [ ] **IA Upselling:** Recomendação de produtos baseada no carrinho.

# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js 14 + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico por `company_id`.
- [x] **Cardápio Público:** Listagem dinâmica com suporte a Adicionais/Opções.
- [x] **Carrinho & Pedidos:** Fluxo completo do cliente até o banco de dados.
- [x] **KDS (Cozinha):** Monitor em tempo real com WebSockets.

## ✅ Fase 2: Experiência & Híbrido (CONCLUÍDO)
- [x] **Modo Delivery:** Suporte a pedidos sem mesa.
- [x] **Sessão de Mesa:** Segurança via Token e persistência.
- [x] **Chamada de Garçom:** Notificação digital.
- [x] **Landing Page B2B:** Site institucional de alta conversão.
- [x] **Gestão de Mesas:** Mapa de sala visual (Drag & Drop).

## ✅ Fase 3: Profissionalização & Fintech (CONCLUÍDO)
- [x] **Login/Registro 2.0:** Layout Split, validações Zod e feedback visual.
- [x] **Perfil Avançado:** Upload de Logo (URL), Color Picker e Configurações.
- [x] **Motor Financeiro:** Cálculo seguro de Split de Pagamento e taxas.
- [x] **Gestão de Estoque:** Ficha técnica (Receitas) e baixa automática.
- [x] **Segurança:** Rate Limiting (Anti-Spam) e proteção de rotas.
- [x] **PWA:** Configuração de manifesto e service workers.

## ✅ Fase 4: Escala & Ecossistema (CONCLUÍDO)
- [x] **Assinaturas SaaS:** Integração completa com Stripe (Checkout/Portal/Webhooks).
- [x] **Dashboard Financeiro:** Gráficos reais via SQL Aggregation.
- [x] **Fidelidade (Cashback):** Carteira digital automática para clientes.
- [x] **App do Garçom 2.0:** Mobile POS com Venda Balcão, Delivery e Transferência de Mesas.
- [x] **Logística (Driver App):** App do Entregador, Gestão de Frota e Despacho.
- [x] **Notificações Sensoriais:** Vibração e Som para garçons.

## 🔄 Fase 5: Enterprise & IA (EM ANDAMENTO)
- [x] **Integração Fiscal (Backend):** Estrutura de dados (NCM/CFOP) e Mock de emissão NFC-e.
- [x] **Logs de Auditoria:** Rastreabilidade de ações sensíveis (quem alterou o quê).
- [x] **Gestão de Compras:** Geração automática de ordens de compra baseada em estoque mínimo.
- [x] **Conta Digital do Garçom:** Cálculo e registro de gorjetas (10%) por funcionário.
- [ ] **KDS Setorizado:** Filtros visuais para Bar vs Cozinha no Frontend.
- [ ] **Infraestrutura:** Migração de WebSockets para Redis (Escalabilidade).
- [ ] **Modo Offline:** PWA com banco de dados local (Dexie.js) e sincronização.
- [ ] **Testes E2E:** Automação de testes de interface com Playwright.

## 🚀 Fase 6: Futuro (Planejamento)
- [ ] **IA Upselling:** Recomendação inteligente de produtos.
- [ ] **White Label:** Domínios personalizados para grandes redes.


# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1 a 4 (MVP & Core)
- [x] **Core:** FastAPI + Next.js + PostgreSQL.
- [x] **Operação:** KDS, App do Garçom, Gestão de Mesas.
- [x] **Financeiro:** Split de Pagamento, Assinaturas Stripe, Ledger de Gorjetas.

## 🔄 Fase 5: Enterprise & Escala (CONCLUÍDO)
- [x] **KDS Setorizado:** Filtros visuais para Bar vs Cozinha.
- [x] **Infraestrutura:** Migração de WebSockets para Redis (Escalabilidade).
- [x] **Modo Offline:** PWA com banco de dados local (Dexie.js).
- [x] **Arquitetura Fiscal:** Adapter Pattern para múltiplos provedores (FocusNFe).
- [x] **Testes E2E:** Automação com Playwright.
- [x] **Observabilidade:** Monitoramento com Sentry (Back/Front).
- [x] **White-Label:** Suporte a domínios personalizados via Middleware.

## 🚀 Fase 6: Diferenciais Competitivos (PRÓXIMOS PASSOS)
- [ ] **Impressão Nativa:** Integração direta via protocolo `rawbt:` (Android).
- [ ] **IA Upselling:** Recomendação inteligente de produtos ("Quem comprou X levou Y").
- [ ] **Dashboard Multi-loja:** Visão consolidada para franquias.
- [ ] **Cardápio Multilíngue:** Tradução automática baseada no browser do cliente.
# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1 a 4: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento total por `company_id`.
- [x] **KDS & Garçom:** Monitor em tempo real e App Mobile POS.
- [x] **Financeiro:** Split de Pagamento (Mercado Pago) e Assinaturas (Stripe).
- [x] **Logística:** App do Entregador e Gestão de Frota.

## ✅ Fase 5: Enterprise & Resiliência (CONCLUÍDO)
- [x] **KDS Setorizado:** Filtros visuais para Bar vs Cozinha com persistência local.
- [x] **Escalabilidade:** Migração de WebSockets para Redis Pub/Sub.
- [x] **Modo Offline:** Implementação de Dexie.js para cache local e sincronização.
- [x] **Arquitetura Fiscal:** Adapter Pattern para múltiplos provedores (FocusNFe).
- [x] **Observabilidade:** Integração total com Sentry (Back/Front).
- [x] **White-Label:** Suporte a domínios personalizados via Middleware.
- [x] **QA:** Testes E2E com Playwright cobrindo o fluxo crítico.

## 🔄 Fase 6: Diferenciais Competitivos & IA (PRÓXIMOS PASSOS)
- [ ] **Impressão Nativa (RawBT):** Geração de ESC/POS binário para impressão silenciosa no Android.
- [ ] **IA Upselling:** Motor de recomendação baseado em Market Basket Analysis (Histórico de vendas).
- [ ] **Dashboard Multi-loja:** Visão consolidada para franqueadores (Super Admin).
- [ ] **Cardápio Multilíngue:** Tradução automática baseada na geolocalização/browser.
- [ ] **Totem de Autoatendimento:** Interface adaptada para totens verticais (Kiosk Mode).
- [ ] **Integração SmartPOS:** Pagamento direto via Intent em maquininhas Android (Stone/PagSeguro).

## 🚀 Fase 7: Escala Global & IA Avançada (FUTURO)
- [ ] **IA de Previsão de Demanda:** Alerta de compra de insumos baseado em tendências.
- [ ] **Voice Ordering:** Pedidos via comando de voz no totem.
- [ ] **API Pública:** Marketplace para integrações de terceiros.


# 🗺️ Roadmap do Produto: MesaFlow

## ✅ Fase 1 a 4: MVP & Core Operacional (CONCLUÍDO)
- [x] **Arquitetura Base:** FastAPI + Next.js + PostgreSQL.
- [x] **Multi-tenancy:** Isolamento lógico total por `company_id`.
- [x] **KDS & Garçom:** Monitor em tempo real e App Mobile POS.
- [x] **Financeiro:** Split de Pagamento (Mercado Pago) e Assinaturas (Stripe).

## ✅ Fase 5: Enterprise & Resiliência (CONCLUÍDO)
- [x] **KDS Setorizado:** Filtros visuais para Bar vs Cozinha.
- [x] **Infraestrutura:** Migração de WebSockets para Redis Pub/Sub.
- [x] **Modo Offline:** Cache local (Dexie.js) e sincronização.
- [x] **Arquitetura Fiscal:** Adapter Pattern (FocusNFe).
- [x] **Observabilidade:** Sentry (Back/Front).
- [x] **White-Label:** Suporte a domínios personalizados.
- [x] **Hardening:** Baixa de estoque transacional e segurança de rotas.

## 🔄 Fase 6: Logística & Diferenciais (EM ANDAMENTO)
- [x] **Gestão de Caixa do Entregador:** Ledger de débitos e pagamentos.
- [x] **Proof of Delivery (POD):** Código de confirmação de entrega.
- [x] **Deep Linking:** Integração nativa com Waze/Maps no App do Motorista.
- [x] **Dashboard Logístico:** KPIs de frota em tempo real (Tempo médio, Entregas/dia).
- [ ] **Impressão Nativa (RawBT):** Geração de ESC/POS binário.
- [ ] **IA Upselling:** Motor de recomendação.
- [ ] **Dashboard Multi-loja:** Visão consolidada para franquias.

## 🚀 Fase 7: Escala Global (FUTURO)
- [ ] **IA de Previsão de Demanda:** Alerta de compra de insumos.
- [ ] **Voice Ordering:** Pedidos via comando de voz.
- [ ] **API Pública:** Marketplace para integrações.