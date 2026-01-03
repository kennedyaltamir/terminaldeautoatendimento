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