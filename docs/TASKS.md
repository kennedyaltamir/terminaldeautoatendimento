# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento rastrea o progresso do projeto e serve como menu para priorização de futuras sprints.

## ✅ Concluído (Fases 1 a 4)

### 🏗️ Core & Arquitetura
- [x] **Setup Inicial:** FastAPI + Next.js + PostgreSQL + Docker.
- [x] **Multi-tenancy:** Isolamento lógico de dados por `company_id`.
- [x] **Autenticação:** JWT com suporte a múltiplos perfis (Dono, Gerente, Garçom, Cozinha).

### 📱 Cardápio Digital (Cliente)
- [x] **Catálogo:** Categorias, Produtos e Adicionais (Obrigatórios/Opcionais).
- [x] **Carrinho:** Persistência local, edição de itens e cálculo de total.
- [x] **Check-in de Mesa:** Validação via QR Code e Sessão de Mesa (Token).
- [x] **Fidelidade (Cashback):** Carteira digital vinculada ao telefone com crédito automático.

### 👨‍🍳 Operação (KDS & Garçom)
- [x] **KDS Real-time:** Monitor de cozinha com WebSockets e SLA (Cores por tempo).
- [x] **App do Garçom (Mobile POS):** Interface móvel para lançar pedidos, fechar contas e gerenciar mesas.
- [x] **Gestão de Mesas:** Mapa visual, Transferência de Mesa e Junção de Comandas (Merge).
- [x] **Notificações Sensoriais:** Vibração e Som no celular do garçom.
- [x] **QuickPOS:** Módulo para Venda Balcão e Delivery rápido.

### 💰 Financeiro (Fintech & SaaS)
- [x] **Split de Pagamento (Pix):** Divisão automática de receita (SaaS vs Restaurante) via Mercado Pago.
- [x] **Assinaturas (Stripe):** Checkout, Portal do Cliente e Webhooks para gestão de planos (Free/Pro).
- [x] **Ledger Offline:** Acúmulo de taxas sobre vendas em dinheiro para cobrança posterior.
- [x] **Dashboard Real:** Métricas financeiras agregadas via SQL (Ticket Médio, Curva ABC).

---

## 🚀 Próximas Prioridades (Curto Prazo)
*Escolha 1 ou 2 para a próxima sprint.*

### 1. Automação de WhatsApp (Notificações)
Integração com API (Evolution/Twilio) para enviar mensagens automáticas ao cliente ("Pedido Recebido", "Pronto para Retirada", "Saiu para Entrega"), reduzindo a ansiedade e a demanda sobre a equipe de atendimento.

### 2. Impressão Térmica Nativa (RawBT/ESC-POS)
Refinamento do módulo de impressão para gerar comandos binários ESC/POS e enviá-los diretamente para impressoras Bluetooth/USB via deep link (RawBT), eliminando a janela de impressão do navegador e permitindo formatação perfeita de cupons.

### 3. KDS Setorizado (Bar vs Cozinha)
Implementação de filtros robustos no WebSocket para que o tablet do Bar receba apenas pedidos de bebidas e a Cozinha apenas comidas, com suporte a um "Expedidor" que vê tudo consolidado para montagem da bandeja.

---

## 🔮 Backlog de Expansão (Menu de Escolhas)

### 🧠 Inteligência & UX (Aumentar Vendas)

**4. Motor de Upselling (IA Simples)**
Sistema de recomendação que sugere itens complementares no carrinho com base em regras ("Quem pede Hambúrguer costuma pedir Batata") ou histórico, aumentando o ticket médio sem esforço humano.

**5. Cardápio Multilíngue Automático**
Detecção do idioma do navegador do cliente para exibir nomes e descrições traduzidos automaticamente (via Google Translate API ou banco de traduções), essencial para áreas turísticas e hotéis.

**6. Avaliação de Pedido (NPS)**
Modal pós-pagamento convidando o cliente a avaliar a experiência (1-5 estrelas) e deixar comentários. Avaliações baixas geram alerta para o gerente; altas sugerem postar no Google Maps.

**7. Modo "Chamar Garçom" Avançado**
Refinamento do botão de chamada com opções específicas ("Trazer Gelo", "Limpar Mesa", "Problema no Pedido") que disparam notificações diferentes (ícones/sons) no relógio ou celular do garçom.

### 🏢 Gestão & Enterprise (Vender para Redes)

**8. Dashboard Multi-Loja (Franquias)**
Visão consolidada para donos de redes. Permite ver o faturamento somado de todas as filiais em tempo real e comparar a performance entre unidades (Ranking de Lojas).

**9. Controle de Estoque Avançado (Inventário)**
Gestão de entrada de notas fiscais (XML), fornecedores, alertas de estoque mínimo via e-mail e cálculo de CMV (Custo de Mercadoria Vendida) teórico vs real.

**10. Perfis de Acesso Granulares (ACL)**
Editor de permissões onde o dono pode criar cargos personalizados (ex: "Gerente da Noite") e marcar checkbox por checkbox o que esse cargo pode ver ou editar no sistema.

**11. Logs de Auditoria (Segurança)**
Registro imutável de todas as ações sensíveis: quem cancelou um pedido, quem deu desconto, quem abriu o caixa. Essencial para prevenir fraudes internas e roubos.

### 💳 Fintech & Fiscal (Profissionalização)

**12. Integração Fiscal (NFC-e / SAT)**
Módulo para emissão de nota fiscal do consumidor. Integração com APIs de terceiros (eNotas, Focus NFe) para gerar o XML/PDF automaticamente após o pagamento e enviar o link para o cliente.

**13. Conta Digital do Garçom (Gorjeta)**
Sistema para calcular a taxa de serviço (10%) e dividir virtualmente entre a equipe, gerando um relatório de quanto cada garçom tem a receber no final do turno ou semana.

**14. Pagamento na Mesa (TEF/Maquininha)**
Integração profunda com maquininhas Smart (Stone/PagSeguro) para que o pedido no sistema envie o valor direto para a maquininha, evitando erro de digitação de valor pelo garçom.

### 🛠️ Infraestrutura & Performance (Escala)

**15. Modo Offline (PWA)**
Implementação de Service Workers e IndexedDB para permitir que o garçom continue lançando pedidos e fechando mesas mesmo se a internet cair, sincronizando tudo quando a conexão voltar.

**16. Migração para Redis (WebSockets)**
Substituição do gerenciador de memória atual por Redis Pub/Sub. Isso é obrigatório para escalar o sistema para múltiplos servidores (Kubernetes/Serverless) sem quebrar a comunicação em tempo real.

**17. Testes E2E (Cypress/Playwright)**
Criação de robôs que simulam um cliente real fazendo um pedido a cada deploy. Garante que nenhuma atualização quebre o fluxo crítico de "Pedir -> Pagar -> Cozinha Receber".

**18. Monitoramento de Erros (Sentry)**
Instalação de rastreadores de bugs no Frontend e Backend para saber quando um cliente enfrentou uma tela branca ou erro 500, antes mesmo dele reclamar no suporte.

### 🏨 Verticalização (Hotéis e Eventos)

**19. Módulo de Agendamento (Room Service)**
Permitir que o hóspede peça o café da manhã na noite anterior, escolhendo o horário de entrega. O pedido aparece na cozinha apenas no horário programado.

**20. Mapeamento de Assentos (Estádios)**
Substituir o conceito de "Mesas" por um mapa de setores/cadeiras (Setor A, Fila 3, Cadeira 15), permitindo entrega precisa em grandes eventos ou estádios de futebol.


### 21. App do Entregador (Interface Móvel)
Criação de uma interface simplificada (`/driver`) onde o entregador faz login e vê apenas os pedidos atribuídos a ele.
*   **Lista de Tarefas:** "A Retirar" e "Em Rota".
*   **Detalhes:** Endereço, Nome do Cliente, Telefone e Observações de entrega.
*   **Ação:** Botão "Confirmar Entrega" que atualiza o status no sistema e libera o motoboy para a próxima.

### 22. Gestão de Frota & Despacho (Admin)
Atualização da tela de Delivery do gerente (`/admin/delivery`) para permitir a atribuição de pedidos.
*   **Cadastro de Entregadores:** Criar usuários com role `DRIVER`.
*   **Modal de Despacho:** Ao clicar em "Despachar", o sistema pergunta: "Qual entregador levará este pedido?".
*   **Controle de Taxas:** Definir quanto cada entregador ganha por entrega (fixo ou % da taxa de entrega).

### 23. Integração com Mapas (Waze/Google Maps)
Facilitar a vida do entregador no trânsito.
*   **Deep Link:** No App do Entregador, adicionar botões "Abrir no Waze" e "Abrir no Maps" que puxam o endereço do pedido e iniciam a navegação GPS automaticamente.
*   **Link de WhatsApp:** Botão para chamar o cliente no Zap com um clique caso não encontre o endereço.

### 24. Comprovante de Entrega Digital
Segurança contra reclamações de "não recebi".
*   **Código de Confirmação:** O cliente recebe um código de 4 dígitos (via WhatsApp/Tela). O entregador precisa digitar esse código no App para finalizar a entrega.
*   **Foto da Entrega:** (Opcional) Permitir que o entregador tire uma foto do pacote no local se não encontrar o cliente.


# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 5 - Enterprise)
- [x] **Integração Fiscal (Backend):** Estrutura de dados para NCM/CFOP e Mock de emissão de NFC-e.
- [x] **Logs de Auditoria:** Rastreabilidade de ações sensíveis (quem alterou o quê).
- [x] **Gestão de Compras:** Geração automática de ordens de compra baseada em estoque mínimo.
- [x] **Conta Digital do Garçom:** Cálculo e registro de gorjetas (10%) por funcionário.
- [x] **Correção de Permissões:** Ajuste no RBAC para acesso ao módulo de Delivery.
- [x] **Correção de Enum:** Ajuste no PostgreSQL para aceitar status fiscal em minúsculo.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Frontend] KDS Setorizado (Bar vs Cozinha) 👨‍🍳
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Criar um seletor no topo do KDS ("Ver Apenas Bar", "Ver Apenas Cozinha") e filtrar os itens do pedido visualmente.
*   **Por que:** Restaurantes médios/grandes não funcionam sem isso.

### 2. [Infra] Migração para Redis (WebSockets) ⚡
**Complexidade:** Alta | **Impacto:** Crítico para Escala
*   **O que fazer:** Implementar Redis Pub/Sub para gerenciar as mensagens em tempo real.
*   **Por que:** Necessário para deploy profissional em nuvem com múltiplos workers.

### 3. [Frontend] Modo Offline (PWA Real) 📡
**Complexidade:** Muito Alta | **Impacto:** Diferencial Competitivo
*   **O que fazer:** Implementar banco de dados local (`Dexie.js`) e fila de sincronização.
*   **Por que:** A internet de restaurante é instável. Isso evita parar a operação.

### 4. [QA] Testes E2E (End-to-End) 🤖
**Complexidade:** Média | **Impacto:** Estabilidade
*   **O que fazer:** Configurar Playwright para simular um pedido completo.
*   **Por que:** Garante que o fluxo principal nunca quebre em atualizações futuras.

# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 5 - Enterprise)
- [x] **Governança de Código:** Fusão do `validar.py` com `atualizar.py` (v3.0).
- [x] **Protocolo v4.3:** Implementação de regras rígidas contra códigos incompletos.
- [x] **Integração Fiscal (Backend):** Estrutura de dados para NCM/CFOP e Mock de emissão.
- [x] **Logs de Auditoria:** Rastreabilidade de ações sensíveis.
- [x] **Gestão de Compras:** Geração automática de ordens de compra.
- [x] **Conta Digital do Garçom:** Cálculo e registro de gorjetas (10%).

---

## 🚀 Próximas Prioridades (Fila de Execução - Fase 6)

### 1. [Backend/Service] Automação de WhatsApp Real 📱
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Substituir o Mock do `WhatsAppService` por chamadas HTTP reais para a Evolution API.
*   **Status:** Configurações de UI prontas, falta integração do Service.

### 2. [Frontend/Lib] Impressão Nativa (RawBT) 🖨️
**Complexidade:** Média | **Impacto:** Operacional
*   **O que fazer:** Refinar o `builder.ts` para gerar comandos ESC/POS binários e disparar via protocolo `rawbt:`.

### 3. [AI/Service] Motor de Upselling 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar lógica de recomendação "Quem comprou X também levou Y" no carrinho.
# 📋 Backlog de Tarefas Técnicas

## 🚀 Prioridade Alta (Fase 6 - Polimento)

### 1. [Auth] Google Login Real 🔐
**Contexto:** O botão de login com Google atual exibe apenas um modal de "Em breve".
**Ação:** Implementar integração com Firebase Auth ou NextAuth.js para permitir login social real.

### 2. [UX] Skeletons & Loading States 🎨
**Contexto:** Algumas telas piscam ou mostram "Carregando..." simples.
**Ação:** Criar componentes de Skeleton (Shimmer effect) para o Cardápio, KDS e Dashboard.

### 3. [Infra] CI/CD Pipeline ⚙️
**Contexto:** O deploy é manual.
**Ação:** Criar `.github/workflows/deploy.yml` para rodar testes e deploy no Render automaticamente.

---

## ✅ Concluído Recentemente
- [x] **SmartPOS Integration:** Deep links para Stone/PagSeguro.
- [x] **Kiosk Mode:** Proteção de sessão e tela de atração.
- [x] **Fiscal UI:** Botões de emissão e status de nota fiscal.
- [x] **Marketing Dashboard:** Configuração de IA e Fidelidade.
- [x] **Script Organization:** Limpeza da pasta raiz.
# 📋 Backlog de Tarefas Técnicas (Fase 6)

## ✅ Concluído Recentemente
- [x] **Skeleton Loaders:** Dashboard, Menu Admin e Estoque com carregamento suave.
- [x] **Resiliência de Testes:** Debugger Python atualizado para lidar com Hydration de Skeletons.
- [x] **UI Fix:** Remoção de scroll horizontal no dashboard principal.
- [x] **Onboarding Fix:** Z-Index do Joyride elevado para 10000.

## 🚀 Prioridade Alta
- [ ] **[Auth] Google Login Real:** Substituir o mock atual por integração social real.
- [ ] **[Doc] API Documentation:** Gerar Swagger/Redoc completo com exemplos de payloads.
- [ ] **[DevOps] CI/CD Pipeline:** Configurar GitHub Actions para rodar Playwright em cada PR.

## 🔮 Backlog de Refino
- [ ] **Estoque:** Alerta visual pulsante em itens com estoque abaixo do mínimo.
- [ ] **KDS:** Botão de modo "Tela Cheia" nativo do navegador.
- [ ] **Fidelidade:** Gráfico de resgate de cashback no dashboard de marketing.
# 📋 Backlog de Tarefas Técnicas (Fase 6)

## ✅ Concluído Recentemente
- [x] **Otimização de Banco de Dados:** Criação de índices para Dashboard, KDS e Auditoria.
- [x] **Login Social:** Integração real com Google Identity Services.
- [x] **Skeleton Loaders:** Dashboard, Menu Admin e Estoque com carregamento suave.
- [x] **UI Fix:** Remoção de scroll horizontal no dashboard principal.

## 🚀 Prioridade Alta
- [ ] **[Doc] API Documentation:** Gerar Swagger/Redoc completo com exemplos de payloads.
- [ ] **[DevOps] CI/CD Pipeline:** Configurar GitHub Actions para rodar Playwright em cada PR.
- [ ] **[Infra] Docker Polish:** Implementar Health Checks nativos no docker-compose.

## 🔮 Backlog de Refino
- [ ] **Estoque:** Alerta visual pulsante em itens com estoque abaixo do mínimo.
- [ ] **KDS:** Botão de modo "Tela Cheia" nativo do navegador.
- [ ] **Fidelidade:** Gráfico de resgate de cashback no dashboard de marketing.
# 📋 Backlog de Tarefas Técnicas (Fase 6)

## ✅ Concluído Recentemente
- [x] **API Reference:** Documentação técnica detalhada e metadados Swagger.
- [x] **Performance DB:** Índices operacionais e de auditoria validados.
- [x] **Login Social:** Integração real com Google Identity Services.
- [x] **UI Refinement:** Skeletons e fix de scroll horizontal.

## 🚀 Prioridade Alta
- [ ] **[DevOps] CI/CD Pipeline:** Configurar GitHub Actions para rodar Playwright em cada PR.
- [ ] **[Infra] Docker Health Checks:** Implementar monitoramento nativo no container da API.
- [ ] **[Security] Token Rotation:** Implementar Refresh Tokens reais com revogação no banco.

## 🔮 Backlog de Refino
- [ ] **Financeiro:** Relatório de DRE (Demonstrativo de Resultados) automático.
- [ ] **KDS:** Atalhos de teclado para troca de status (1, 2, 3).
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento rastrea o progresso do projeto e serve como menu para priorização de futuras sprints.

## ✅ Concluído (Fases 1 a 4)

### 🏗️ Core & Arquitetura
- [x] **Setup Inicial:** FastAPI + Next.js + PostgreSQL + Docker.
- [x] **Multi-tenancy:** Isolamento lógico de dados por `company_id`.
- [x] **Autenticação:** JWT com suporte a múltiplos perfis (Dono, Gerente, Garçom, Cozinha).

### 📱 Cardápio Digital (Cliente)
- [x] **Catálogo:** Categorias, Produtos e Adicionais (Obrigatórios/Opcionais).
- [x] **Carrinho:** Persistência local, edição de itens e cálculo de total.
- [x] **Check-in de Mesa:** Validação via QR Code e Sessão de Mesa (Token).
- [x] **Fidelidade (Cashback):** Carteira digital vinculada ao telefone com crédito automático.

### 👨‍🍳 Operação (KDS & Garçom)
- [x] **KDS Real-time:** Monitor de cozinha com WebSockets e SLA (Cores por tempo).
- [x] **App do Garçom (Mobile POS):** Interface móvel para lançar pedidos, fechar contas e gerenciar mesas.
- [x] **Gestão de Mesas:** Mapa visual, Transferência de Mesa e Junção de Comandas (Merge).
- [x] **Notificações Sensoriais:** Vibração e Som no celular do garçom.
- [x] **QuickPOS:** Módulo para Venda Balcão e Delivery rápido.

### 💰 Financeiro (Fintech & SaaS)
- [x] **Split de Pagamento (Pix):** Divisão automática de receita (SaaS vs Restaurante) via Mercado Pago.
- [x] **Assinaturas (Stripe):** Checkout, Portal do Cliente e Webhooks para gestão de planos (Free/Pro).
- [x] **Ledger Offline:** Acúmulo de taxas sobre vendas em dinheiro para cobrança posterior.
- [x] **Dashboard Real:** Métricas financeiras agregadas via SQL (Ticket Médio, Curva ABC).

---

## 🚀 Próximas Prioridades (Curto Prazo)
*Escolha 1 ou 2 para a próxima sprint.*

### 1. Automação de WhatsApp (Notificações)
Integração com API (Evolution/Twilio) para enviar mensagens automáticas ao cliente ("Pedido Recebido", "Pronto para Retirada", "Saiu para Entrega"), reduzindo a ansiedade e a demanda sobre a equipe de atendimento.

### 2. Impressão Térmica Nativa (RawBT/ESC-POS)
Refinamento do módulo de impressão para gerar comandos binários ESC/POS e enviá-los diretamente para impressoras Bluetooth/USB via deep link (RawBT), eliminando a janela de impressão do navegador e permitindo formatação perfeita de cupons.

### 3. KDS Setorizado (Bar vs Cozinha)
Implementação de filtros robustos no WebSocket para que o tablet do Bar receba apenas pedidos de bebidas e a Cozinha apenas comidas, com suporte a um "Expedidor" que vê tudo consolidado para montagem da bandeja.

---

## 🔮 Backlog de Expansão (Menu de Escolhas)

### 🧠 Inteligência & UX (Aumentar Vendas)

**4. Motor de Upselling (IA Simples)**
Sistema de recomendação que sugere itens complementares no carrinho com base em regras ("Quem pede Hambúrguer costuma pedir Batata") ou histórico, aumentando o ticket médio sem esforço humano.

**5. Cardápio Multilíngue Automático**
Detecção do idioma do navegador do cliente para exibir nomes e descrições traduzidos automaticamente (via Google Translate API ou banco de traduções), essencial para áreas turísticas e hotéis.

**6. Avaliação de Pedido (NPS)**
Modal pós-pagamento convidando o cliente a avaliar a experiência (1-5 estrelas) e deixar comentários. Avaliações baixas geram alerta para o gerente; altas sugerem postar no Google Maps.

**7. Modo "Chamar Garçom" Avançado**
Refinamento do botão de chamada com opções específicas ("Trazer Gelo", "Limpar Mesa", "Problema no Pedido") que disparam notificações diferentes (ícones/sons) no relógio ou celular do garçom.

### 🏢 Gestão & Enterprise (Vender para Redes)

**8. Dashboard Multi-Loja (Franquias)**
Visão consolidada para donos de redes. Permite ver o faturamento somado de todas as filiais em tempo real e comparar a performance entre unidades (Ranking de Lojas).

**9. Controle de Estoque Avançado (Inventário)**
Gestão de entrada de notas fiscais (XML), fornecedores, alertas de estoque mínimo via e-mail e cálculo de CMV (Custo de Mercadoria Vendida) teórico vs real.

**10. Perfis de Acesso Granulares (ACL)**
Editor de permissões onde o dono pode criar cargos personalizados (ex: "Gerente da Noite") e marcar checkbox por checkbox o que esse cargo pode ver ou editar no sistema.

**11. Logs de Auditoria (Segurança)**
Registro imutável de todas as ações sensíveis: quem cancelou um pedido, quem deu desconto, quem abriu o caixa. Essencial para prevenir fraudes internas e roubos.

### 💳 Fintech & Fiscal (Profissionalização)

**12. Integração Fiscal (NFC-e / SAT)**
Módulo para emissão de nota fiscal do consumidor. Integração com APIs de terceiros (eNotas, Focus NFe) para gerar o XML/PDF automaticamente após o pagamento e enviar o link para o cliente.

**13. Conta Digital do Garçom (Gorjeta)**
Sistema para calcular a taxa de serviço (10%) e dividir virtualmente entre a equipe, gerando um relatório de quanto cada garçom tem a receber no final do turno ou semana.

**14. Pagamento na Mesa (TEF/Maquininha)**
Integração profunda com maquininhas Smart (Stone/PagSeguro) para que o pedido no sistema envie o valor direto para a maquininha, evitando erro de digitação de valor pelo garçom.

### 🛠️ Infraestrutura & Performance (Escala)

**15. Modo Offline (PWA)**
Implementação de Service Workers e IndexedDB para permitir que o garçom continue lançando pedidos e fechando mesas mesmo se a internet cair, sincronizando tudo quando a conexão voltar.

**16. Migração para Redis (WebSockets)**
Substituição do gerenciador de memória atual por Redis Pub/Sub. Isso é obrigatório para escalar o sistema para múltiplos servidores (Kubernetes/Serverless) sem quebrar a comunicação em tempo real.

**17. Testes E2E (Cypress/Playwright)**
Criação de robôs que simulam um cliente real fazendo um pedido a cada deploy. Garante que nenhuma atualização quebre o fluxo crítico de "Pedir -> Pagar -> Cozinha Receber".

**18. Monitoramento de Erros (Sentry)**
Instalação de rastreadores de bugs no Frontend e Backend para saber quando um cliente enfrentou uma tela branca ou erro 500, antes mesmo dele reclamar no suporte.

### 🏨 Verticalização (Hotéis e Eventos)

**19. Módulo de Agendamento (Room Service)**
Permitir que o hóspede peça o café da manhã na noite anterior, escolhendo o horário de entrega. O pedido aparece na cozinha apenas no horário programado.

**20. Mapeamento de Assentos (Estádios)**
Substituir o conceito de "Mesas" por um mapa de setores/cadeiras (Setor A, Fila 3, Cadeira 15), permitindo entrega precisa em grandes eventos ou estádios de futebol.


### 21. App do Entregador (Interface Móvel)
Criação de uma interface simplificada (`/driver`) onde o entregador faz login e vê apenas os pedidos atribuídos a ele.
*   **Lista de Tarefas:** "A Retirar" e "Em Rota".
*   **Detalhes:** Endereço, Nome do Cliente, Telefone e Observações de entrega.
*   **Ação:** Botão "Confirmar Entrega" que atualiza o status no sistema e libera o motoboy para a próxima.

### 22. Gestão de Frota & Despacho (Admin)
Atualização da tela de Delivery do gerente (`/admin/delivery`) para permitir a atribuição de pedidos.
*   **Cadastro de Entregadores:** Criar usuários com role `DRIVER`.
*   **Modal de Despacho:** Ao clicar em "Despachar", o sistema pergunta: "Qual entregador levará este pedido?".
*   **Controle de Taxas:** Definir quanto cada entregador ganha por entrega (fixo ou % da taxa de entrega).

### 23. Integração com Mapas (Waze/Google Maps)
Facilitar a vida do entregador no trânsito.
*   **Deep Link:** No App do Entregador, adicionar botões "Abrir no Waze" e "Abrir no Maps" que puxam o endereço do pedido e iniciam a navegação GPS automaticamente.
*   **Link de WhatsApp:** Botão para chamar o cliente no Zap com um clique caso não encontre o endereço.

### 24. Comprovante de Entrega Digital
Segurança contra reclamações de "não recebi".
*   **Código de Confirmação:** O cliente recebe um código de 4 dígitos (via WhatsApp/Tela). O entregador precisa digitar esse código no App para finalizar a entrega.
*   **Foto da Entrega:** (Opcional) Permitir que o entregador tire uma foto do pacote no local se não encontrar o cliente.


# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 5 - Enterprise)
- [x] **Integração Fiscal (Backend):** Estrutura de dados para NCM/CFOP e Mock de emissão de NFC-e.
- [x] **Logs de Auditoria:** Rastreabilidade de ações sensíveis (quem alterou o quê).
- [x] **Gestão de Compras:** Geração automática de ordens de compra baseada em estoque mínimo.
- [x] **Conta Digital do Garçom:** Cálculo e registro de gorjetas (10%) por funcionário.
- [x] **Correção de Permissões:** Ajuste no RBAC para acesso ao módulo de Delivery.
- [x] **Correção de Enum:** Ajuste no PostgreSQL para aceitar status fiscal em minúsculo.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Frontend] KDS Setorizado (Bar vs Cozinha) 👨‍🍳
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Criar um seletor no topo do KDS ("Ver Apenas Bar", "Ver Apenas Cozinha") e filtrar os itens do pedido visualmente.
*   **Por que:** Restaurantes médios/grandes não funcionam sem isso.

### 2. [Infra] Migração para Redis (WebSockets) ⚡
**Complexidade:** Alta | **Impacto:** Crítico para Escala
*   **O que fazer:** Implementar Redis Pub/Sub para gerenciar as mensagens em tempo real.
*   **Por que:** Necessário para deploy profissional em nuvem com múltiplos workers.

### 3. [Frontend] Modo Offline (PWA Real) 📡
**Complexidade:** Muito Alta | **Impacto:** Diferencial Competitivo
*   **O que fazer:** Implementar banco de dados local (`Dexie.js`) e fila de sincronização.
*   **Por que:** A internet de restaurante é instável. Isso evita parar a operação.

### 4. [QA] Testes E2E (End-to-End) 🤖
**Complexidade:** Média | **Impacto:** Estabilidade
*   **O que fazer:** Configurar Playwright para simular um pedido completo.
*   **Por que:** Garante que o fluxo principal nunca quebre em atualizações futuras.

# 📋 Backlog de Tarefas Técnicas (Fase 6)

## ✅ Concluído Recentemente
- [x] **Google Login:** Implementação real (Backend + Frontend) via Google Identity Services.
- [x] **Cloud Resiliency:** Health Checks profundos integrados ao PaaS Render.com.
- [x] **Git Sync:** Sincronização completa do repositório local com a nuvem (Fase 6 Live).
- [x] **UX Polishing:** Skeleton Loaders ativos e responsividade corrigida.

## 🚀 Prioridade Alta
- [ ] **[DevOps] GitHub Actions:** Automatizar a suíte de `pytest` em cada push para evitar bugs em prod.
- [ ] **[Security] Token Rotation:** Implementar Refresh Tokens reais com expiração controlada.
- [ ] **[UX] Admin Skeletons:** Finalizar aplicação nas rotas de histórico e equipe.

## 🔮 Backlog de Refino
- [ ] **Marketing:** Integração real com Evolution API para notificações WhatsApp.
- [ ] **Fintech:** Relatório de DRE (Demonstrativo de Resultados) automático no dashboard.
# 📋 Backlog de Tarefas Técnicas (Fase 6)

## ✅ Concluído Recentemente
- [x] **Infraestrutura:** Configuração de Health Checks no Render para monitoramento automático.
- [x] **Otimização DB:** Criação de índices críticos para performance (`orders`, `audit_logs`).
- [x] **Backend:** Implementação real de Google Login via API do Google.
- [x] **Frontend:** Skeletons visuais e correção de layout no Dashboard.

## 🚀 Próximas Prioridades (Fase 7 - Em Planejamento)
- [ ] **DevOps:** Pipeline de CI/CD completo no GitHub Actions.
- [ ] **WhatsApp Real:** Integração com Evolution API para notificações automáticas.
- [ ] **IA Upselling:** Motor de recomendação no cardápio.
- [ ] **App Nativo:** Estudo de viabilidade com React Native.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 - Polimento)
- [x] **UX:** Implementação de Skeleton Loaders em todo o Admin.
- [x] **Auth:** Login Social (Google) funcional e integrado.
- [x] **Infra:** Pipeline de CI/CD e monitoramento de saúde em nuvem.
- [x] **Estabilidade:** Correção de 29 regressões na suíte de testes.

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Substituir o mock atual por chamadas autenticadas para a Evolution API.
*   **Gatilhos:** Envio de link de rastreio no despacho e solicitação de NPS na entrega.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar algoritmo de co-ocorrência no `RecommendationService` para gerar o "Quem comprou X também levou Y".
*   **UI:** Exibir sugestões no modal de produto e no carrinho.

### 3. [Mobile] Preparação para App Nativo 📲
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Adaptar rotas de autenticação para suporte a Long-lived Tokens e Push Notifications (Firebase).

### 4. [API] Marketplace & Webhooks Públicos 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar documentação Swagger/Redoc profissional e expor webhooks para integração com ERPs externos.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído (Fase 6 - Polimento & Estabilidade)
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos em todos os schemas.
- [x] **UX:** Redirecionamento automático por Role no Admin Layout.
- [x] **Feature:** Impressão de QR Codes em massa (Grid A4).
- [x] **Feature:** Geração de Pix dinâmico no fechamento de mesa pelo garçom.

---

## 🚀 Fase 7: Ecossistema & IA (PRÓXIMOS PASSOS)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
*   Substituir mocks por chamadas reais para envio de status e link de rastreio.

### 2. [AI] Motor de Recomendação Inteligente 🧠
*   Implementar algoritmo de co-ocorrência para Upselling no carrinho.

### 3. [Mobile] Preparação para App Nativo 📲
*   Arquitetura de Push Notifications e Long-lived Tokens.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 - Polimento)
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos em todos os schemas e routers.
- [x] **UX:** Redirecionamento automático por Role no Admin Layout.
- [x] **Feature:** Impressão de QR Codes em massa (Grid A4).
- [x] **Feature:** Geração de Pix dinâmico no fechamento de mesa pelo garçom.

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Substituir o mock atual por chamadas autenticadas para a Evolution API.
*   **Gatilhos:** Envio de link de rastreio no despacho e solicitação de NPS na entrega.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar algoritmo de co-ocorrência no `RecommendationService` para gerar o "Quem comprou X também levou Y".
*   **UI:** Exibir sugestões no modal de produto e no carrinho.

### 3. [Mobile] Preparação para App Nativo 📲
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Adaptar rotas de autenticação para suporte a Long-lived Tokens e Push Notifications (Firebase).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 - Estabilização)
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas (UUID vs Integer).
- [x] **Fix:** Visibilidade do Token de 10 dígitos em todos os schemas e routers.
- [x] **UX:** Redirecionamento automático por Role no Admin Layout.
- [x] **Feature:** Impressão de QR Codes em massa (Grid A4).
- [x] **Feature:** Geração de Pix dinâmico no fechamento de mesa pelo garçom.

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Substituir o mock atual por chamadas autenticadas para a Evolution API.
*   **Gatilhos:** Envio de link de rastreio no despacho e solicitação de NPS na entrega.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar algoritmo de co-ocorrência no `RecommendationService` para gerar o "Quem comprou X também levou Y".
*   **UI:** Exibir sugestões no modal de produto e no carrinho.

### 3. [Mobile] Preparação para App Nativo 📲
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Adaptar rotas de autenticação para suporte a Long-lived Tokens e Push Notifications (Firebase).

### 4. [API] Marketplace & Webhooks Públicos 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar documentação Swagger/Redoc profissional e expor webhooks para integração com ERPs externos.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 & 7)
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos.
- [x] **UX:** Redirecionamento automático por Role.
- [x] **Audit:** Auditoria Geral de Inconsistências (Schema & Build Fixes).

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Complexidade:** Média | **Impacto:** Alto
*   **Status:** ✅ CONCLUÍDO (Service Hardening & Status Check)
*   **O que foi feito:** Implementada verificação de conexão da instância e script de teste real.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar algoritmo de co-ocorrência para Upselling no carrinho.
*   **Status:** Próximo da Fila.

### 3. [Mobile] Preparação para App Nativo 📲
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Adaptar rotas de autenticação para suporte a Long-lived Tokens e Push Notifications (Firebase).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 & 7)
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos.
- [x] **UX:** Redirecionamento automático por Role.
- [x] **Audit:** Auditoria Geral de Inconsistências.
- [x] **Integrations:** WhatsApp Service com Health Check e Mock Server.

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Complexidade:** Média | **Impacto:** Alto
*   **Status:** ✅ CONCLUÍDO
*   **Entregável:** Service robusto, Endpoint de Status e Mock Server para testes locais.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar algoritmo de co-ocorrência para Upselling no carrinho.
*   **Status:** Próximo da Fila.

### 3. [Mobile] Preparação para App Nativo 📲
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Adaptar rotas de autenticação para suporte a Long-lived Tokens e Push Notifications (Firebase).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 & 7)
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos.
- [x] **UX:** Redirecionamento automático por Role.
- [x] **Audit:** Auditoria Geral de Inconsistências.
- [x] **Integrations:** WhatsApp Service com Health Check e Mock Server.
- [x] **AI:** Motor de Recomendação com validação estatística.

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Status:** ✅ CONCLUÍDO

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Status:** ✅ CONCLUÍDO
*   **O que foi feito:** Implementado algoritmo de Market Basket Analysis com proteção de loops e script de simulação (`simular_ia_upselling.py`).

### 3. [Mobile] Preparação para App Nativo 📲
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Adaptar rotas de autenticação para suporte a Long-lived Tokens e Push Notifications (Firebase).

### 4. [API] Marketplace & Webhooks Públicos 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar documentação Swagger/Redoc profissional e expor webhooks para integração com ERPs externos.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 & 7)
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos.
- [x] **UX:** Redirecionamento automático por Role.
- [x] **Audit:** Auditoria Geral de Inconsistências.
- [x] **Integrations:** WhatsApp Service com Health Check e Mock Server.
- [x] **AI:** Motor de Recomendação com validação estatística.

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Status:** ✅ CONCLUÍDO

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Status:** ✅ CONCLUÍDO

### 3. [Mobile] Preparação para App Nativo 📲
**Status:** ✅ CONCLUÍDO (Backend Ready)
*   **O que foi feito:** Criada tabela `user_devices` e endpoints de registro de token FCM para Push Notifications.

### 4. [API] Marketplace & Webhooks Públicos 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar documentação Swagger/Redoc profissional e expor webhooks para integração com ERPs externos.
TRIVIAL
Arquivos afetados:
1. `docs/TASKS.md` (Atualização de Status)

### Resumo Executivo
Atualizei o arquivo `docs/TASKS.md` consolidando todas as tarefas concluídas até o momento, incluindo as fases anteriores e as recentes da Fase 7 (WhatsApp, IA e Mobile Backend). O documento agora reflete o estado real do projeto, servindo como fonte única de verdade para o progresso.

---

### Arquivos

[[MESAFLOW_BEGIN:docs/TASKS.md]]
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento rastreia o progresso do projeto e serve como menu para priorização de futuras sprints.

## ✅ Concluído (Fases 1 a 6)

### 🏗️ Core & Arquitetura
- [x] **Setup Inicial:** FastAPI + Next.js + PostgreSQL + Docker.
- [x] **Multi-tenancy:** Isolamento lógico de dados por `company_id`.
- [x] **Autenticação:** JWT com suporte a múltiplos perfis (Dono, Gerente, Garçom, Cozinha).
- [x] **Segurança:** Rate Limiting, Sanitização de Inputs, Auditoria de Logs.

### 📱 Cardápio Digital (Cliente)
- [x] **Catálogo:** Categorias, Produtos e Adicionais (Obrigatórios/Opcionais).
- [x] **Carrinho:** Persistência local, edição de itens e cálculo de total.
- [x] **Check-in de Mesa:** Validação via QR Code e Sessão de Mesa (Token de 10 dígitos).
- [x] **Fidelidade (Cashback):** Carteira digital vinculada ao telefone com crédito automático.
- [x] **Modo Kiosk:** Interface de totem com proteção de inatividade.

### 👨‍🍳 Operação (KDS & Garçom)
- [x] **KDS Real-time:** Monitor de cozinha com WebSockets e SLA (Cores por tempo).
- [x] **KDS Setorizado:** Filtros para Bar vs Cozinha.
- [x] **App do Garçom (Mobile POS):** Interface móvel para lançar pedidos, fechar contas e gerenciar mesas.
- [x] **Gestão de Mesas:** Mapa visual, Transferência de Mesa e Junção de Comandas (Merge).
- [x] **Notificações Sensoriais:** Vibração e Som no celular do garçom.
- [x] **QuickPOS:** Módulo para Venda Balcão e Delivery rápido.

### 💰 Financeiro (Fintech & SaaS)
- [x] **Split de Pagamento (Pix):** Divisão automática de receita (SaaS vs Restaurante) via Mercado Pago.
- [x] **Assinaturas (Stripe):** Checkout, Portal do Cliente e Webhooks para gestão de planos (Free/Pro).
- [x] **Ledger Offline:** Acúmulo de taxas sobre vendas em dinheiro para cobrança posterior.
- [x] **Dashboard Real:** Métricas financeiras agregadas via SQL (Ticket Médio, Curva ABC).
- [x] **Fiscal:** Módulo de emissão de NFC-e (Adapter Pattern).

### 🛵 Logística & Delivery
- [x] **App do Entregador:** Interface simplificada para motoboys.
- [x] **Rastreamento GPS:** Envio de localização em tempo real via WebSocket.
- [x] **Proof of Delivery (POD):** Código de confirmação de entrega.
- [x] **Gestão de Frota:** Cadastro e atribuição de entregadores.

---

## ✅ Concluído Recentemente (Fase 7 - Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
- [x] **Service Hardening:** Implementada verificação de saúde da instância.
- [x] **Mock Server:** Criado servidor local para simular a API do WhatsApp em testes.
- [x] **Status Endpoint:** Rota para verificar conexão no frontend.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
- [x] **Algoritmo:** Implementada lógica de Market Basket Analysis (Co-ocorrência).
- [x] **Proteção:** Evita loops de recomendação (produto recomendar a si mesmo).
- [x] **Simulação:** Script de geração de dados sintéticos para validar a IA.

### 3. [Mobile] Preparação para App Nativo 📲
- [x] **Backend:** Criada tabela `user_devices` para armazenar tokens FCM.
- [x] **API:** Endpoints de registro e remoção de dispositivos móveis.
- [x] **Testes:** Validação do fluxo de auth mobile.

---

## 🚀 Próximas Prioridades (Fase 7 - Continuação)

### 4. [API] Marketplace & Webhooks Públicos 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar documentação Swagger/Redoc profissional e expor webhooks para integração com ERPs externos.
*   **Objetivo:** Permitir que outros sistemas (iFood, Rappi, ERPs) se conectem ao MesaFlow.

### 5. [Frontend] Integração Visual da IA
**Complexidade:** Média | **Impacto:** Vendas
*   **O que fazer:** Exibir as recomendações geradas pela IA no modal de produto e no carrinho ("Quem comprou X também levou Y").

### 6. [Frontend] Painel de Status do WhatsApp
**Complexidade:** Baixa | **Impacto:** UX
*   **O que fazer:** Criar um componente visual nas configurações para mostrar se o WhatsApp está conectado (usando o novo endpoint de status).
[[MESAFLOW_END]]

### Comandos Finais
```bash
# 1. Atualizar o arquivo de tarefas
python atualizar.py
```# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 7 - Ecossistema & IA)
- [x] **Integrations:** WhatsApp Real (Evolution API) com Health Check.
- [x] **AI:** Motor de Recomendação (Market Basket Analysis).
- [x] **Mobile:** Backend para App Nativo (User Devices).
- [x] **API:** Webhooks de Saída (Outgoing Webhooks) com assinatura HMAC.

---

## 🚀 Próximas Prioridades (Fase 7 - Continuação)

### 5. [Frontend] Integração Visual da IA 🧠
**Complexidade:** Média | **Impacto:** Vendas
*   **O que fazer:** Exibir as recomendações geradas pela IA no modal de produto e no carrinho ("Quem comprou X também levou Y").
*   **Status:** Backend pronto, falta UI.

### 6. [Frontend] Painel de Status do WhatsApp 📱
**Complexidade:** Baixa | **Impacto:** UX
*   **O que fazer:** Criar um componente visual nas configurações para mostrar se o WhatsApp está conectado (usando o novo endpoint de status).

### 7. [Frontend] Gestão de Webhooks 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar tela no Admin para o usuário cadastrar URLs de webhook e ver o segredo de assinatura.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** do projeto MesaFlow. Ele consolida **todas as fases**, **funcionalidades**, **decisões técnicas** e **status reais** do sistema, do MVP à fase de Ecossistema & IA.

---

## ✅ Concluído (Fases 1 a 6)

### 🏗️ Core & Arquitetura

* [x] Setup Inicial: FastAPI + Next.js + PostgreSQL + Docker
* [x] Multi-tenancy com isolamento por `company_id`
* [x] Autenticação JWT com múltiplos perfis (Owner, Manager, Waiter, Kitchen, Driver)
* [x] RBAC com correções de permissão e rotas protegidas
* [x] Auditoria de ações sensíveis (logs imutáveis)
* [x] Rate limiting, sanitização de inputs e hardening de segurança
* [x] Health checks nativos (Render / Docker)

---

### 📱 Cardápio Digital (Cliente)

* [x] Catálogo: Categorias, Produtos e Adicionais (obrigatórios/opcionais)
* [x] Carrinho persistente com edição e cálculo automático
* [x] Check-in de Mesa via QR Code
* [x] Sessão de Mesa com Token numérico de 10 dígitos
* [x] Fidelidade (Cashback) vinculada ao telefone
* [x] Modo Kiosk (Totem) com proteção por inatividade
* [x] Impressão de QR Codes em massa (Grid A4)

---

### 👨‍🍳 Operação (KDS & Garçom)

* [x] KDS em tempo real via WebSockets
* [x] SLA visual por cores (tempo de preparo)
* [x] KDS Setorizado (Bar vs Cozinha)
* [x] App do Garçom (Mobile POS)
* [x] Gestão visual de mesas
* [x] Transferência de mesa e merge de comandas
* [x] Notificações sensoriais (som e vibração)
* [x] QuickPOS (Balcão / Delivery rápido)
* [x] Geração de Pix dinâmico no fechamento da mesa

---

### 💰 Financeiro, SaaS & Fiscal

* [x] Split de pagamento Pix (SaaS vs Restaurante)
* [x] Assinaturas Stripe (Free / Pro)
* [x] Ledger offline para taxas em dinheiro
* [x] Dashboard financeiro real (SQL puro)
* [x] Ticket médio, Curva ABC
* [x] Estrutura fiscal: NCM, CFOP
* [x] Emissão NFC-e (Adapter Pattern / Mock pronto para produção)
* [x] Relatórios de gorjeta (10%) por funcionário

---

### 🛵 Logística & Delivery

* [x] App do Entregador (`/driver`)
* [x] Lista de pedidos: A Retirar / Em Rota
* [x] Atribuição de entregadores (Admin)
* [x] Gestão de frota
* [x] Rastreamento em tempo real
* [x] Integração com Maps (Waze / Google Maps)
* [x] Link direto para WhatsApp do cliente
* [x] Comprovante de entrega digital (POD)
* [x] Código de confirmação de entrega

---

## ✅ Concluído (Fase 7 – Ecossistema & IA)

### 📱 Integrações – WhatsApp (Evolution API)

* [x] Serviço real (HTTP)
* [x] Health Check da instância
* [x] Endpoint de status
* [x] Mock Server local para testes
* [x] Gatilhos: status do pedido, despacho e pós-entrega

---

### 🧠 Inteligência Artificial – Upselling

* [x] Motor de Recomendação Inteligente
* [x] Market Basket Analysis (co-ocorrência)
* [x] Proteção contra loops (produto → ele mesmo)
* [x] Validação estatística
* [x] Script de simulação (`simular_ia_upselling.py`)

---

### 📲 Mobile & App Nativo (Backend Ready)

* [x] Suporte a tokens long-lived
* [x] Tabela `user_devices`
* [x] Registro e remoção de dispositivos
* [x] Preparação para Push Notifications (Firebase)

---

## 🚀 Próximas Prioridades (Fase 8 – Plataforma & Escala)

### 🔌 API & Ecossistema

* [ ] Marketplace de Integrações
* [ ] Webhooks públicos (Pedidos, Pagamentos, Entregas)
* [ ] Documentação Swagger / Redoc profissional
* [ ] Tokens de API por parceiro

---

### 🎨 Frontend & UX

* [ ] Exibição visual das recomendações de IA no carrinho
* [ ] Painel visual de status do WhatsApp
* [ ] Atalhos de teclado no KDS
* [ ] Modo Tela Cheia nativo

---

### ⚙️ Infraestrutura & DevOps

* [ ] CI/CD avançado com gates por ambiente
* [ ] Redis para WebSockets (escala horizontal)
* [ ] Observabilidade (Sentry / Tracing)

---

### 📊 Financeiro Avançado

* [ ] Relatório automático de DRE
* [ ] CMV teórico vs real
* [ ] Exportação contábil

---

## 🧭 Visão de Produto

MesaFlow não é apenas um sistema de pedidos.

É uma **plataforma operacional completa** para restaurantes modernos:

* Omnichannel
* Offline-first
* Pronta para redes e franquias
* Financeiramente auditável
* Inteligente por padrão

---

## 📌 Status Atual

**Projeto:** Estável, em produção
**Arquitetura:** Escalável
**Próximo foco:** Plataforma, integrações e crescimento

---

*Fim do documento.*
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço (10%, 12%, Fixo).
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa (CRM).

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 1. [Frontend] Split de Conta por Item 📱
**Complexidade:** Alta | **Impacto:** UX
*   **O que fazer:** Implementar modal onde o garçom seleciona itens específicos para pagar, abatendo do total da mesa.

### 2. [Frontend] Sugestão Inteligente no POS 🧠
**Complexidade:** Média | **Impacto:** Vendas
*   **O que fazer:** Exibir recomendações da IA (já calculadas no backend) ao adicionar produtos no App do Garçom.

### 3. [Logística] Prestação de Contas do Motoboy 🛵
**Complexidade:** Média | **Impacto:** Financeiro
*   **O que fazer:** Criar tela para o gerente dar baixa no saldo devedor dos entregadores.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 1. [Frontend] Split de Conta por Item 📱
**Complexidade:** Alta | **Impacto:** UX
*   **O que fazer:** Implementar modal onde o garçom seleciona itens específicos para pagar, abatendo do total da mesa.

### 2. [Logística] Prestação de Contas do Motoboy 🛵
**Complexidade:** Média | **Impacto:** Financeiro
*   **O que fazer:** Criar tela para o gerente dar baixa no saldo devedor dos entregadores.

### 3. [Cozinha] Modo Expedidor (Assembler) 👨‍🍳
**Complexidade:** Média | **Impacto:** Operação
*   **O que fazer:** Tela consolidada para montagem de bandejas (Bar + Cozinha).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.
- [x] **Frontend:** Split de Conta por Item/Valor (Pagamento Parcial).

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 2. [Logística] Prestação de Contas do Motoboy 🛵
**Complexidade:** Média | **Impacto:** Financeiro
*   **O que fazer:** Criar tela para o gerente dar baixa no saldo devedor dos entregadores.

### 3. [Cozinha] Modo Expedidor (Assembler) 👨‍🍳
**Complexidade:** Média | **Impacto:** Operação
*   **O que fazer:** Tela consolidada para montagem de bandejas (Bar + Cozinha).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 - Estabilização)
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos em todos os schemas e routers.
- [x] **UX:** Redirecionamento automático por Role no Admin Layout.
- [x] **Feature:** Impressão de QR Codes em massa (Grid A4).
- [x] **Tool:** Script de Auditoria Visual (Abertura de abas).
- [x] **Tool:** Crawler Auditor de Erros (Clique em todos os botões).

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Substituir o mock atual por chamadas autenticadas para a Evolution API.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar algoritmo de co-ocorrência para Upselling no carrinho.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.
- [x] **Frontend:** Split de Conta por Item/Valor (Pagamento Parcial).
- [x] **Logística:** Prestação de Contas do Motoboy (Cash Management).

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 3. [Cozinha] Modo Expedidor (Assembler) 👨‍🍳
**Complexidade:** Média | **Impacto:** Operação
*   **O que fazer:** Tela consolidada para montagem de bandejas (Bar + Cozinha).
*   **Objetivo:** Ajudar quem "boqueta" (organiza) os pratos antes de chamar o garçom.

### 4. [Balcão] Integração com Gaveta de Dinheiro 🏪
**Complexidade:** Baixa | **Impacto:** Hardware
*   **O que fazer:** Adicionar comando ESC/POS para abrir gaveta ao finalizar venda em dinheiro.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.
- [x] **Frontend:** Split de Conta por Item/Valor (Pagamento Parcial).
- [x] **Logística:** Prestação de Contas do Motoboy (Cash Management).
- [x] **Cozinha:** Modo Expedidor (Assembler) para montagem de bandejas.

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 4. [Balcão] Integração com Gaveta de Dinheiro 🏪
**Complexidade:** Baixa | **Impacto:** Hardware
*   **O que fazer:** Adicionar comando ESC/POS para abrir gaveta ao finalizar venda em dinheiro.

### 5. [Cozinha] Impressão de Etiquetas (Stickers) 🏷️
**Complexidade:** Média | **Impacto:** Delivery
*   **O que fazer:** Gerar layout ZPL/EPL para impressoras de etiquetas (Zebra/Elgin) para colar em copos e caixas.


# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.
- [x] **Frontend:** Split de Conta por Item/Valor (Pagamento Parcial).
- [x] **Logística:** Prestação de Contas do Motoboy (Cash Management).
- [x] **Cozinha:** Modo Expedidor (Assembler) para montagem de bandejas.
- [x] **Hardware:** Integração com Gaveta de Dinheiro (ESC/POS).

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 5. [Cozinha] Impressão de Etiquetas (Stickers) 🏷️
**Complexidade:** Média | **Impacto:** Delivery
*   **O que fazer:** Gerar layout ZPL/EPL para impressoras de etiquetas (Zebra/Elgin) para colar em copos e caixas.

### 6. [Frontend] Atalhos de Teclado no KDS ⌨️
**Complexidade:** Baixa | **Impacto:** Produtividade
*   **O que fazer:** Permitir usar teclas numéricas (1, 2, 3) para mudar status dos pedidos sem tocar na tela (Bump Bar).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 - Estabilização)
- [x] **Fix:** Syntax Error (Unexpected EOF) no componente de Balcão.
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos em todos os schemas.
- [x] **Tool:** Crawler Auditor de Erros com suporte a login real.

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Substituir o mock atual por chamadas autenticadas para a Evolution API.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar algoritmo de co-ocorrência para Upselling no carrinho.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 6 - Estabilização)
- [x] **Fix:** Syntax Error (Unexpected EOF) no componente de Balcão.
- [x] **Fix:** Datatype Mismatch no fechamento/abertura de mesas.
- [x] **Fix:** Visibilidade do Token de 10 dígitos em todos os schemas.
- [x] **Tool:** Crawler Auditor de Erros com suporte a login real.

---

## 🚀 Prioridades da Fase 7 (Ecossistema & IA)

### 1. [Integrations] WhatsApp Real (Evolution API) 📱
**Complexidade:** Média | **Impacto:** Alto
*   **O que fazer:** Substituir o mock atual por chamadas autenticadas para a Evolution API.

### 2. [AI/Service] Motor de Recomendação Inteligente 🧠
**Complexidade:** Alta | **Impacto:** Financeiro
*   **O que fazer:** Implementar algoritmo de co-ocorrência para Upselling no carrinho.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.
- [x] **Frontend:** Split de Conta por Item/Valor (Pagamento Parcial).
- [x] **Logística:** Prestação de Contas do Motoboy (Cash Management).
- [x] **Logística:** Teste E2E completo do App do Entregador (Waze, POD, Fluxo).
- [x] **Cozinha:** Modo Expedidor (Assembler) para montagem de bandejas.
- [x] **Hardware:** Integração com Gaveta de Dinheiro (ESC/POS).

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 5. [Cozinha] Impressão de Etiquetas (Stickers) 🏷️
**Complexidade:** Média | **Impacto:** Delivery
*   **O que fazer:** Gerar layout ZPL/EPL para impressoras de etiquetas (Zebra/Elgin) para colar em copos e caixas.

### 6. [Frontend] Atalhos de Teclado no KDS ⌨️
**Complexidade:** Baixa | **Impacto:** Produtividade
*   **O que fazer:** Permitir usar teclas numéricas (1, 2, 3) para mudar status dos pedidos sem tocar na tela (Bump Bar).


# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.
- [x] **Frontend:** Split de Conta por Item/Valor (Pagamento Parcial).
- [x] **Logística:** Prestação de Contas do Motoboy (Cash Management).
- [x] **Logística:** Teste E2E completo do App do Entregador (Waze, POD, Fluxo).
- [x] **Cozinha:** Modo Expedidor (Assembler) para montagem de bandejas.
- [x] **Hardware:** Integração com Gaveta de Dinheiro (ESC/POS).

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 5. [Cozinha] Impressão de Etiquetas (Stickers) 🏷️
**Complexidade:** Média | **Impacto:** Delivery
*   **O que fazer:** Gerar layout ZPL/EPL para impressoras de etiquetas (Zebra/Elgin) para colar em copos e caixas.

### 6. [Frontend] Atalhos de Teclado no KDS ⌨️
**Complexidade:** Baixa | **Impacto:** Produtividade
*   **O que fazer:** Permitir usar teclas numéricas (1, 2, 3) para mudar status dos pedidos sem tocar na tela (Bump Bar).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.
- [x] **Frontend:** Split de Conta por Item/Valor (Pagamento Parcial).
- [x] **Logística:** Prestação de Contas do Motoboy (Cash Management).
- [x] **Cozinha:** Modo Expedidor (Assembler) para montagem de bandejas.
- [x] **Hardware:** Integração com Gaveta de Dinheiro (ESC/POS).
- [x] **Cozinha:** Impressão de Etiquetas ZPL (Stickers).

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 6. [Frontend] Atalhos de Teclado no KDS ⌨️
**Complexidade:** Baixa | **Impacto:** Produtividade
*   **O que fazer:** Permitir usar teclas numéricas (1, 2, 3) para mudar status dos pedidos sem tocar na tela (Bump Bar).

### 7. [Frontend] Modo Tela Cheia Nativo 🖥️
**Complexidade:** Baixa | **Impacto:** Imersão
*   **O que fazer:** Botão para esconder a barra de endereços e rodar como quiosque real.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 8 - Excelência Operacional)
- [x] **Backend:** Suporte a gorjeta personalizada (`custom_service_fee`).
- [x] **Frontend:** Modal de pagamento com edição de taxa de serviço.
- [x] **Frontend:** Identificação de cliente por telefone na abertura de mesa.
- [x] **Frontend:** Sugestão Inteligente (IA) no App do Garçom.
- [x] **Frontend:** Split de Conta por Item/Valor (Pagamento Parcial).
- [x] **Logística:** Prestação de Contas do Motoboy (Cash Management).
- [x] **Cozinha:** Modo Expedidor (Assembler) para montagem de bandejas.
- [x] **Hardware:** Integração com Gaveta de Dinheiro (ESC/POS).
- [x] **Hardware:** Bump Bar / Atalhos de Teclado no KDS.
- [x] **Cozinha:** Impressão de Etiquetas ZPL (Stickers).

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 7. [Frontend] Modo Tela Cheia Nativo 🖥️
**Complexidade:** Baixa | **Impacto:** Imersão
*   **O que fazer:** Botão para esconder a barra de endereços e rodar como quiosque real em tablets.

### 8. [Cozinha] Relatório de Gargalos (Heatmap) ⏱️
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Gráfico no admin mostrando quais pratos levam mais tempo para sair da cozinha.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** do projeto. Ele consolida o progresso histórico e define o foco tático atual: **Refinamento Operacional**.

---

## ✅ Histórico de Conclusão (Fases 1 a 7)

### 🏗️ Fundação & Backend
- [x] **Core:** FastAPI + Next.js + PostgreSQL + Docker.
- [x] **Segurança:** Multi-tenancy (RLS), JWT Auth, Rate Limiting, Auditoria.
- [x] **Infra:** WebSockets (Redis Pub/Sub), Health Checks, Sentry.

### 📱 Experiência do Cliente
- [x] **Cardápio:** Categorias, Produtos, Adicionais, Carrinho Persistente.
- [x] **Acesso:** QR Code, Token de Mesa (10 dígitos), Modo Kiosk (Totem).
- [x] **Engajamento:** Fidelidade (Cashback), Avaliação (NPS).

### 💰 Fintech & Integrações
- [x] **Pagamentos:** Split Pix (Mercado Pago), Assinaturas (Stripe).
- [x] **Fiscal:** Emissão de NFC-e (Adapter Pattern).
- [x] **Ecossistema:** WhatsApp Real (Evolution API), Webhooks de Saída.
- [x] **Inteligência:** Motor de Recomendação (IA Upselling).

---

## ✅ FASE 8: Excelência Operacional (CONCLUÍDO)
*Foco: Polimento e funcionalidades avançadas para os atores humanos do sistema.*

- [x] **Cozinha:** Modo Expedidor (Assembler) para montagem de bandejas.
- [x] **Hardware:** Integração com Gaveta de Dinheiro (ESC/POS).
- [x] **Hardware:** Bump Bar / Atalhos de Teclado no KDS.
- [x] **Cozinha:** Impressão de Etiquetas ZPL (Stickers).
- [x] **Garçom:** Gestão de Gorjeta personalizada no fechamento.
- [x] **Garçom:** Identificação de cliente por telefone (CRM).
- [x] **Garçom:** Split de conta por valor/item.

---

## 🚀 Próximas Prioridades (Fase 8 - Continuação)

### 7. [Frontend] Modo Tela Cheia Nativo 🖥️
**Complexidade:** Baixa | **Impacto:** Imersão
*   **O que fazer:** Botão para esconder a barra de endereços e rodar como quiosque real em tablets.

### 8. [Cozinha] Relatório de Gargalos (Heatmap) ⏱️
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Gráfico no admin mostrando quais pratos levam mais tempo para sair da cozinha.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 7 - Ecossistema & IA)
- [x] **WhatsApp:** Service real com verificação de status e Mock Server.
- [x] **IA:** Motor de recomendação e Toast de sugestão no POS.
- [x] **Mobile:** Tabela de dispositivos e registro de tokens FCM.
- [x] **Hardware:** Impressão ZPL, Abertura de Gaveta e Atalhos Bump Bar.
- [x] **Financeiro:** Pagamento parcial (Split) e Gorjeta customizada.
- [x] **Logística:** Prestação de contas de motoristas (Cash Settlement).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [API] Marketplace & Webhooks Públicos 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar documentação Swagger/Redoc profissional e expor webhooks para integração com ERPs externos.

### 2. [Frontend] Painel de Status do WhatsApp 📱
**Complexidade:** Baixa | **Impacto:** UX
*   **O que fazer:** Criar um componente visual nas configurações para mostrar se o WhatsApp está conectado.

### 3. [Frontend] Gestão de Webhooks 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar tela no Admin para o usuário cadastrar URLs de webhook e ver o segredo de assinatura.

### 4. [Mobile] Início do App Nativo (React Native) 📲
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Iniciar o repositório mobile e implementar o login consumindo a API atual.
Aqui está o arquivo docs/TASKS.md atualizado, consolidado e profissional.

Ele reflete o estado real do projeto (pós-Fase 8 de Excelência Operacional) e organiza as próximas tarefas baseadas na análise de gap que fizemos (Marketing, Fiscal Real e Integrações).

code
Markdown
download
content_copy
expand_less
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para o desenvolvimento do MesaFlow. Ele rastreia o progresso histórico, as entregas recentes e define o roteiro tático para as próximas sprints.

---

## ✅ Histórico de Conclusão (Fases 1 a 6)
*Funcionalidades auditadas, testadas e em produção.*

### 🏗️ Core & Arquitetura
- [x] **Setup:** FastAPI (Async) + Next.js 14 + PostgreSQL (RLS) + Docker.
- [x] **Segurança:** Multi-tenancy, JWT Auth, Rate Limiting, Auditoria de Logs.
- [x] **Infra:** WebSockets (Redis Pub/Sub), Health Checks, Sentry.

### 👨‍🍳 Operação (KDS & Estoque)
- [x] **KDS 2.0:** Setorização (Bar vs Cozinha), Agrupador de Itens e SLA Visual.
- [x] **Estoque:** Baixa automática via Ficha Técnica e Regra 86 (Bloqueio).
- [x] **Impressão:** ESC/POS (58/80mm) e RawBT (Android).

### 📱 Experiência (Garçom & Cliente)
- [x] **App do Garçom:** Mobile POS, Gestão de Mesas (Drag & Drop), Token PIN.
- [x] **Cliente:** Cardápio Digital, Carrinho Persistente, Modo Kiosk (Totem).
- [x] **Engajamento:** Fidelidade (Cashback), Avaliação (NPS).

### 💰 Fintech & Logística
- [x] **Financeiro:** Split Pix (Mercado Pago), Assinaturas (Stripe), Ledger Offline.
- [x] **Logística:** App do Entregador (PWA), Rastreamento GPS, POD (Proof of Delivery).

---

## ✅ Entregas Recentes (Fases 7 & 8 - Ecossistema & Operação)
*Funcionalidades entregues nas últimas sprints.*

### 🔌 Integrações & IA
- [x] **WhatsApp Real:** Integração com Evolution API (Notificações Transacionais).
- [x] **IA Upselling:** Motor de recomendação (Market Basket Analysis).
- [x] **Mobile Backend:** Infraestrutura para Push Notifications (FCM).

### ⚙️ Excelência Operacional (Hardware & UX)
- [x] **Cozinha:** Modo Expedidor (Assembler) para montagem de bandejas.
- [x] **Cozinha:** Impressão de Etiquetas ZPL (Stickers) para copos/caixas.
- [x] **Hardware:** Integração com Gaveta de Dinheiro (Comando ESC/POS).
- [x] **Hardware:** Suporte a Bump Bar (Atalhos de teclado no KDS).
- [x] **Garçom:** Split de Conta (Pagamento Parcial) e Gorjeta Customizada.
- [x] **Logística:** Prestação de Contas do Motoboy (Cash Settlement).

---

## 🚀 Próximas Prioridades (Sprint Atual)
*Foco: Marketing (Vendas) e Abertura de Ecossistema.*

### 1. [Marketing] Motor de Promoções e Cupons 🏷️
**Complexidade:** Alta | **Impacto:** Receita (GMV)
*   **O que fazer:** Criar sistema de regras de desconto no carrinho.
    *   *Tipos:* Valor Fixo, Porcentagem, Frete Grátis.
    *   *Gatilhos:* Primeira Compra, Valor Mínimo, Cupom Manual.
*   **Por que:** Funcionalidade #1 solicitada para aumentar conversão.

### 2. [API] Developer Experience (OpenAPI) 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Gerar documentação Swagger/Redoc pública e profissional.
*   **O que fazer:** Implementar Webhooks de Saída (Outgoing Webhooks) com assinatura HMAC para eventos de `order.created` e `order.status_changed`.

### 3. [Frontend] Painel de Status do WhatsApp 📱
**Complexidade:** Baixa | **Impacto:** UX/Suporte
*   **O que fazer:** Criar indicador visual nas configurações mostrando se a instância da Evolution API está conectada ou desconectada (QR Code necessário).

---

## 🔮 Backlog de Expansão (Fase 9 - Enterprise)
*Menu de priorização para as próximas fases.*

### 🏛️ Fiscal & Legal (Crítico)
- [ ] **Homologação SEFAZ:** Emissão real de NFC-e com validação por UF.
- [ ] **Contingência Offline:** Emissão de notas em modo de contingência e transmissão posterior.
- [ ] **Integração SAT:** Suporte a hardware SAT físico (Obrigatório em SP).

### 🌐 Hub de Delivery (Marketplace)
- [ ] **Integração iFood:** Middleware para receber pedidos do iFood e injetar no KDS.
- [ ] **Sincronização de Cardápio:** Atualizar preço no MesaFlow e refletir no iFood.

### ⚙️ DevOps & Gestão
- [ ] **Tenant Impersonation:** Modo "Suporte" (God Mode) para acessar conta do cliente.
- [ ] **Feature Flags:** Sistema para rollout gradual de funcionalidades.
- [ ] **Dashboard Multi-loja:** Relatórios consolidados para franquias.

### 📱 Mobile Nativo
- [ ] **App React Native:** Migração do PWA para app nativo (Lojas Apple/Google).
Perfeito. Como especialista responsável pelo projeto MesaFlow, consolidei toda a estratégia (Roadmap) e a execução tática (Tasks) em um único Arquivo Mestre de Documentação.

Este documento serve como a "Bíblia do Projeto". Ele elimina a necessidade de consultar múltiplos arquivos dispersos e alinha a visão de produto com a execução de engenharia.

Você pode salvar este conteúdo como docs/MASTER_PLAN.md ou substituir o conteúdo do seu README.md principal.

🚀 MesaFlow: Master Project Documentation

Versão: 3.0 (Enterprise Edition)
Status: Fase 8 Concluída / Iniciando Fase 9 (Expansão)
Responsável Técnico: CTO / Product Lead

1. 🗺️ Visão Estratégica (Roadmap)

O MesaFlow evoluiu de um MVP operacional para uma plataforma SaaS All-in-One. O foco atual é Marketing, Ecossistema Aberto e Escala.

✅ Fases Concluídas (1 a 8)

Funcionalidades auditadas, testadas e em produção.

🏛️ Core: Arquitetura FastAPI + Next.js, Multi-tenancy (RLS), Docker, CI/CD.

👨‍🍳 Operação: KDS Setorizado (Bar/Cozinha), Estoque (Ficha Técnica), Impressão (ESC/POS/ZPL).

📱 Experiência: App Garçom (Mobile POS), Cardápio Digital, Totem (Kiosk), Fidelidade.

💰 Fintech: Split de Pagamento (Pix), Assinaturas (Stripe), Ledger de Gorjetas.

🛵 Logística: App do Entregador (PWA), Rastreamento GPS, Prestação de Contas.

🧠 Inteligência: Motor de Recomendação (IA Upselling), WhatsApp Automation.

🔄 Fase Atual: Marketing & Ecossistema (Em Andamento)

Objetivo: Aumentar o GMV dos clientes e permitir integrações de terceiros.

Motor de Promoções: Cupons e regras de desconto no carrinho.

API Pública (OpenAPI): Documentação para ERPs e Webhooks de saída.

Painel de Status: Monitoramento visual de integrações (WhatsApp/Fiscal).

🔮 Visão de Futuro (Fase 9 - Enterprise)

Objetivo: Remover barreiras para grandes redes.

Fiscal Real: Homologação NFC-e/SAT e Contingência Offline.

Hub de Delivery: Integração nativa com iFood/Rappi (Cardápio e Pedidos).

Mobile Nativo: Apps React Native nas lojas (Apple/Google).

Gestão Avançada: Tenant Impersonation (Suporte) e Feature Flags.

2. 📋 Backlog Tático (Tasks & Sprints)

Este é o menu de execução imediata para a equipe de engenharia.

🚀 Prioridades da Sprint Atual (High Impact)
1. [Marketing] Motor de Promoções e Cupons 🏷️

Contexto: Clientes pedem ferramentas para vender mais.

Tech: Criar tabela promotions (regras) e coupons (códigos). Implementar lógica de validação no CartService.

Critérios de Aceite: Suportar desconto fixo, porcentagem e frete grátis. Gatilhos: 1ª compra ou valor mínimo.

2. [API] Developer Experience (OpenAPI & Webhooks) 🔌

Contexto: ERPs de contabilidade precisam ler os pedidos do MesaFlow.

Tech: Configurar metadados do Swagger no FastAPI. Criar sistema de disparo de Webhooks (HMAC) para eventos order.*.

Critérios de Aceite: Documentação acessível em /docs e webhooks disparando com retry.

3. [Frontend] Painel de Status do WhatsApp 📱

Contexto: O usuário não sabe se o bot do WhatsApp caiu.

Tech: Consumir endpoint de status da Evolution API e mostrar "bolinha verde/vermelha" no Admin.

🛠️ Backlog Técnico (Débito & Melhorias)

[DevOps] Tenant Impersonation: Criar mecanismo para admins logarem como qualquer usuário (sem senha) para suporte.

[Frontend] Skeletons: Finalizar estados de carregamento nas telas de Relatórios e Configurações.

[QA] Testes E2E: Cobrir fluxo de "Aplicação de Cupom" no Playwright.

3. 🏗️ Referência Técnica (Stack)
Camada	Tecnologia	Padrões & Decisões
Backend	Python (FastAPI)	Async/Await, Pydantic v2, Factory Pattern (Pagamentos).
Frontend	Next.js 14 (React)	App Router, Server Actions, ShadcnUI, Zod, Tailwind.
Database	PostgreSQL	Row Level Security (RLS) para isolamento, Triggers para Estoque.
Real-time	Redis Pub/Sub	WebSockets escaláveis para KDS e Rastreamento.
Offline	Dexie.js	IndexedDB wrapper para cache local (PWA).
Infra	Docker / Render	Health Checks profundos, CI/CD via GitHub Actions.
Mobile	PWA / React Native	TWA (Trusted Web Activity) atual, migrando para Native.
4. 🛡️ Protocolos de Segurança & Qualidade

Green Build Policy: Nenhum PR é mergeado se os testes (Pytest/Playwright) falharem.

Zero Trust: Todo endpoint verifica company_id no token JWT.

Audit Log: Toda operação de escrita (POST/PUT/DELETE) em dados sensíveis gera log imutável.

Data Isolation: O banco de dados garante que um tenant nunca veja dados de outro (RLS).

Próximo Passo:
Você deseja que eu gere o código para alguma das tarefas prioritárias (ex: O Schema do banco de dados para o Motor de Promoções)?

# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 8)
- [x] **Cozinha:** Modo Expedidor (Assembler).
- [x] **Hardware:** Impressão de Etiquetas ZPL.
- [x] **Hardware:** Integração com Gaveta de Dinheiro.
- [x] **Hardware:** Suporte a Bump Bar (Atalhos).
- [x] **Garçom:** Split de Conta e Gorjeta Customizada.
- [x] **Logística:** Prestação de Contas do Motoboy.

---

## 🚀 Próximas Prioridades (Fase 9 - Enterprise)

### 1. [Fiscal] Arquitetura de Contingência Offline 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Criar fila local (Dexie.js) para notas fiscais emitidas sem internet e worker de sincronização quando a rede voltar.
*   **Requisito:** Deve gerar o XML assinado localmente (se possível) ou guardar os dados para assinatura posterior.

### 2. [Integração] Middleware iFood (Hub) 🛵
**Complexidade:** Muito Alta | **Impacto:** Vendas
*   **O que fazer:** Criar serviço de Polling ou Webhook para receber pedidos da API do iFood.
*   **Desafio:** Mapear produtos do iFood (ID externo) para produtos do MesaFlow (ID interno).

### 3. [DevOps] Tenant Impersonation (God Mode) 👁️
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Permitir que super-admins gerem um token de acesso para qualquer empresa sem saber a senha, para fins de suporte.

### 4. [Marketing] Motor de Promoções 🏷️
**Complexidade:** Alta | **Impacto:** Receita
*   **O que fazer:** Implementar lógica de cupons (Valor Fixo, %) e regras automáticas (Leve 3 Pague 2) no carrinho.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 8)
- [x] **Cozinha:** Modo Expedidor (Assembler).
- [x] **Hardware:** Impressão de Etiquetas ZPL.
- [x] **Hardware:** Integração com Gaveta de Dinheiro.
- [x] **Hardware:** Suporte a Bump Bar (Atalhos).
- [x] **Garçom:** Split de Conta e Gorjeta Customizada.
- [x] **Logística:** Prestação de Contas do Motoboy.

---

## 🚀 Próximas Prioridades (Fase 9 - Enterprise)

### 1. [Fiscal] Arquitetura de Contingência Offline 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Criar fila local (Dexie.js) para notas fiscais emitidas sem internet e worker de sincronização quando a rede voltar.
*   **Requisito:** Deve gerar o XML assinado localmente (se possível) ou guardar os dados para assinatura posterior.

### 2. [Integração] Middleware iFood (Hub) 🛵
**Complexidade:** Muito Alta | **Impacto:** Vendas
*   **O que fazer:** Criar serviço de Polling ou Webhook para receber pedidos da API do iFood.
*   **Desafio:** Mapear produtos do iFood (ID externo) para produtos do MesaFlow (ID interno).

### 3. [DevOps] Tenant Impersonation (God Mode) 👁️
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Permitir que super-admins gerem um token de acesso para qualquer empresa sem saber a senha, para fins de suporte.

### 4. [Marketing] Motor de Promoções 🏷️
**Complexidade:** Alta | **Impacto:** Receita
*   **O que fazer:** Implementar lógica de cupons (Valor Fixo, %) e regras automáticas (Leve 3 Pague 2) no carrinho.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).
- [x] **API:** Webhooks de Saída (Backend + Assinatura HMAC).
- [x] **Cozinha:** Modo Expedidor (Assembler).
- [x] **Hardware:** Impressão de Etiquetas ZPL.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Frontend] Painel de Integrações (Webhooks & WhatsApp) 🔌
**Complexidade:** Média | **Impacto:** Ecossistema
*   **O que fazer:** Criar uma nova aba "Integrações" nas configurações.
*   **Webhooks:** Lista de URLs cadastradas, botão para adicionar nova e visualização do "Signing Secret".
*   **WhatsApp:** Indicador visual de status (Conectado/Desconectado) consumindo o endpoint de health check.

### 2. [Fiscal] Arquitetura de Contingência Offline 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Criar fila local (Dexie.js) para notas fiscais emitidas sem internet e worker de sincronização.

### 3. [Integração] Middleware iFood (Hub) 🛵
**Complexidade:** Muito Alta | **Impacto:** Vendas
*   **O que fazer:** Criar serviço de Polling ou Webhook para receber pedidos da API do iFood.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).
- [x] **API:** Webhooks de Saída (Backend + Assinatura HMAC).
- [x] **Frontend:** Painel de Integrações (Webhooks UI + WhatsApp Status).
- [x] **Fiscal:** Contingência Offline (Dexie.js + Sync Worker).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Integração] Middleware iFood (Hub) 🛵
**Complexidade:** Muito Alta | **Impacto:** Vendas
*   **O que fazer:** Criar serviço de Polling para receber pedidos da API do iFood.
*   **Desafio:** Mapear produtos do iFood (ID externo) para produtos do MesaFlow (ID interno).
*   **Requisito:** O pedido do iFood deve aparecer no KDS com uma tag "iFood" e tocar um som diferente.

### 2. [DevOps] Tenant Impersonation (God Mode) 👁️
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Permitir que super-admins gerem um token de acesso para qualquer empresa sem saber a senha, para fins de suporte.

### 3. [Mobile] App Nativo (React Native) 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Iniciar o repositório mobile e implementar o login consumindo a API atual.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).
- [x] **API:** Webhooks de Saída (Backend + Assinatura HMAC).
- [x] **Frontend:** Painel de Integrações (Webhooks UI + WhatsApp Status).
- [x] **Fiscal:** Contingência Offline (Dexie.js + Sync Worker).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Integração] Middleware iFood (Hub) 🛵
**Complexidade:** Muito Alta | **Impacto:** Vendas
*   **O que fazer:** Criar serviço de Polling para receber pedidos da API do iFood.
*   **Desafio:** Mapear produtos do iFood (ID externo) para produtos do MesaFlow (ID interno).
*   **Requisito:** O pedido do iFood deve aparecer no KDS com uma tag "iFood" e tocar um som diferente.

### 2. [DevOps] Tenant Impersonation (God Mode) 👁️
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Permitir que super-admins gerem um token de acesso para qualquer empresa sem saber a senha, para fins de suporte.

### 3. [Mobile] App Nativo (React Native) 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Iniciar o repositório mobile e implementar o login consumindo a API atual.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Fiscal:** Contingência Offline (Dexie.js + Sync Worker + UI Reativa).
- [x] **Integração:** Middleware iFood (Polling Service + Ingestão + KDS UI).
- [x] **API:** Webhooks de Saída (Dispatcher + Assinatura HMAC + Retry).
- [x] **DX:** Documentação OpenAPI (Swagger) com exemplos e metadados.
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).
- [x] **Segurança:** Correção de relacionamentos de produtos e padronização de GUIDs.

---

## 🚀 Próximas Prioridades (Fila de Execução - Fase 10)

### 1. [DevOps] Tenant Impersonation (God Mode) 👁️
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Criar endpoint protegido para Super-Admins gerarem tokens de acesso para qualquer `company_id`.
*   **Segurança:** Deve registrar log de auditoria obrigatório e expirar em 1 hora.

### 2. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo, configurar autenticação consumindo a API atual e criar a primeira tela de "Lista de Pedidos".

### 3. [Fiscal] Homologação SEFAZ Real 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Substituir o MockProvider pelo FocusNFeProvider em ambiente de homologação e realizar testes com certificados digitais reais.

### 4. [UX] Refinamento de Dashboard Multi-loja 📊
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Adicionar gráficos comparativos de DRE e CMV entre as unidades da franquia.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).
- [x] **API:** Webhooks de Saída (Backend + Assinatura HMAC).
- [x] **Frontend:** Painel de Integrações (Webhooks UI + WhatsApp Status).
- [x] **Fiscal:** Contingência Offline (Dexie.js + Sync Worker).
- [x] **Integração:** Middleware iFood (Polling Service).
- [x] **DevOps:** Tenant Impersonation (God Mode).
- [x] **DevOps:** Feature Flags (Infraestrutura + Cache Redis).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Gestão] Dashboard Multi-loja v2 (DRE & CMV) 📊
**Complexidade:** Alta | **Impacto:** Gestão
*   **O que fazer:** Evoluir a visão de franquia para incluir relatórios financeiros reais.
*   **DRE:** Demonstrativo de Resultado (Receita - Custos - Taxas).
*   **CMV:** Custo de Mercadoria Vendida (Baseado na ficha técnica).
*   **Comparativo:** Gráfico de barras comparando o lucro líquido entre as lojas da rede.

### 2. [Fiscal] Homologação SEFAZ Real 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Configurar certificados digitais reais (A1) e validar o fluxo de emissão com a API da Focus NFe em ambiente de produção.

### 3. [Mobile] App Nativo (React Native) 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Iniciar o repositório mobile e implementar o login consumindo a API atual.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).
- [x] **API:** Webhooks de Saída (Backend + Assinatura HMAC).
- [x] **Frontend:** Painel de Integrações (Webhooks UI + WhatsApp Status).
- [x] **Fiscal:** Contingência Offline (Dexie.js + Sync Worker).
- [x] **Integração:** Middleware iFood (Polling Service).
- [x] **DevOps:** Tenant Impersonation (God Mode) com Auditoria.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [DevOps] Feature Flags (Canary Release) 🚩
**Complexidade:** Média | **Impacto:** Segurança
*   **O que fazer:** Implementar sistema para ativar/desativar funcionalidades (ex: "Novo KDS") para clientes específicos sem deploy.
*   **Tech:** Tabela `feature_flags` e Contexto React para controle no frontend.

### 2. [Fiscal] Homologação SEFAZ Real 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Configurar certificados digitais reais (A1) e validar o fluxo de emissão com a API da Focus NFe em ambiente de produção.

### 3. [Mobile] App Nativo (React Native) 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Iniciar o repositório mobile e implementar o login consumindo a API atual.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.
- [x] **DevOps:** Feature Flag Service e Router (Infraestrutura pronta).
- [x] **Fiscal:** Contingência Offline (Dexie.js + Sync Worker + UI Reativa).
- [x] **Integração:** Middleware iFood (Polling Service + Ingestão + KDS UI).
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Frontend] UI de Gestão de Feature Flags 🚩
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Criar tela no Admin (acessível apenas via Impersonation) para ativar/desativar flags por empresa.
*   **Objetivo:** Permitir que o suporte habilite o "Módulo Fiscal v2" apenas para clientes em teste.

### 2. [Fiscal] Homologação SEFAZ Real 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Substituir o MockProvider pelo FocusNFeProvider em ambiente de produção.
*   **Requisito:** Testar com certificados digitais reais (A1) e validar XMLs.

### 3. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo, configurar autenticação consumindo a API atual e criar a primeira tela de "Lista de Pedidos".

### 4. [UX] Refinamento de Dashboard Multi-loja 📊
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Adicionar gráficos comparativos de DRE e CMV entre as unidades da franquia.


# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Fiscal:** Homologação SEFAZ — Sandbox (Alternância de ambiente e Erro 204).
- [x] **Fiscal:** Especificação Técnica de Homologação (Protocolo SEFAZ).
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.
- [x] **DevOps:** Feature Flag Service e Router (Infraestrutura pronta).
- [x] **Fiscal:** Contingência Offline (Dexie.js + Sync Worker + UI Reativa).
- [x] **Integração:** Middleware iFood (Polling Service + Ingestão + KDS UI).
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Fiscal] Homologação SEFAZ Real (Produção) 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Ativar `FISCAL_ENV=production` e realizar a primeira emissão com certificado A1 real.
*   **Requisito:** Validar se os impostos estão sendo calculados conforme a contabilidade do cliente.

### 2. [Frontend] UI de Gestão de Feature Flags 🚩
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Criar tela no Admin (acessível apenas via Impersonation) para ativar/desativar flags por empresa.

### 3. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo e configurar autenticação.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Fiscal:** Salvaguardas de Produção e Checklist de Go-Live.
- [x] **Fiscal:** Homologação SEFAZ — Sandbox (Alternância de ambiente e Erro 204).
- [x] **Fiscal:** Especificação Técnica de Homologação (Protocolo SEFAZ).
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.
- [x] **DevOps:** Feature Flag Service e Router (Infraestrutura pronta).
- [x] **Fiscal:** Contingência Offline (Dexie.js + Sync Worker + UI Reativa).
- [x] **Integração:** Middleware iFood (Polling Service + Ingestão + KDS UI).
- [x] **Marketing:** Motor de Promoções (Backend + Frontend + E2E).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Fiscal] Homologação SEFAZ Real (Produção) 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Ativar `FISCAL_ENV=production` e `FISCAL_PRODUCTION_CONFIRMED=true` após validação do checklist.
*   **Requisito:** Realizar a primeira emissão real e validar o XML no portal da SEFAZ.

### 2. [Frontend] UI de Gestão de Feature Flags 🚩
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Criar tela no Admin (acessível apenas via Impersonation) para ativar/desativar flags por empresa.

### 3. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo e configurar autenticação.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **DevOps:** Especificação Técnica da UI de Feature Flags.
- [x] **Fiscal:** Salvaguardas de Produção e Checklist de Go-Live.
- [x] **Fiscal:** Homologação SEFAZ — Sandbox (Alternância de ambiente e Erro 204).
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.
- [x] **DevOps:** Feature Flag Service e Router (Infraestrutura pronta).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Frontend] UI de Gestão de Feature Flags 🚩
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Implementar a tela no Admin (acessível apenas via Impersonation) conforme a especificação `FEATURE_FLAGS_UI.md`.
*   **Status:** Documentação concluída. Pronto para codificação.

### 2. [Fiscal] Homologação SEFAZ Real (Produção) 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Ativar `FISCAL_ENV=production` e `FISCAL_PRODUCTION_CONFIRMED=true` após validação do checklist.

### 3. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo e configurar autenticação.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **DevOps:** Bloco 1 - Core de Feature Flags (API Client + Context + Security).
- [x] **Fiscal:** Salvaguardas de Produção e Checklist de Go-Live.
- [x] **Fiscal:** Homologação SEFAZ — Sandbox (Alternância de ambiente e Erro 204).
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.
- [x] **DevOps:** Feature Flag Service e Router (Infraestrutura pronta).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Frontend] UI de Gestão de Feature Flags 🚩
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Implementar a tela no Admin (acessível apenas via Impersonation) conforme a especificação `FEATURE_FLAGS_UI.md`.
*   **Status:** Core lógico concluído (Bloco 1). Pronto para a construção dos componentes visuais (Bloco 2).

### 2. [Fiscal] Homologação SEFAZ Real (Produção) 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Ativar `FISCAL_ENV=production` e `FISCAL_PRODUCTION_CONFIRMED=true` após validação do checklist.

### 3. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo e configurar autenticação.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **DevOps:** Bloco 1 (RE-EXECUÇÃO) - Core de Feature Flags (API Isolada + JWT Seguro + Unit Tests).
- [x] **DevOps:** Especificação Técnica da UI de Feature Flags.
- [x] **Fiscal:** Salvaguardas de Produção e Checklist de Go-Live.
- [x] **Fiscal:** Homologação SEFAZ — Sandbox (Alternância de ambiente e Erro 204).
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Frontend] UI de Gestão de Feature Flags (Bloco 2) 🚩
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Implementar os componentes visuais (`FeatureToggleCard`) e a página de gestão conforme `FEATURE_FLAGS_UI.md`.
*   **Status:** Core lógico aprovado. Aguardando autorização para Bloco 2.

### 2. [Fiscal] Homologação SEFAZ Real (Produção) 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Ativar `FISCAL_ENV=production` e `FISCAL_PRODUCTION_CONFIRMED=true` após validação do checklist.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **DevOps:** Bloco 2 - UI de Gestão de Feature Flags (Componentes + View + E2E).
- [x] **DevOps:** Bloco 1 (RE-EXECUÇÃO) - Core de Feature Flags (API Isolada + JWT Seguro + Unit Tests).
- [x] **DevOps:** Especificação Técnica da UI de Feature Flags.
- [x] **Fiscal:** Salvaguardas de Produção e Checklist de Go-Live.
- [x] **Fiscal:** Homologação SEFAZ — Sandbox (Alternância de ambiente e Erro 204).
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Fiscal] Homologação SEFAZ Real (Produção) 🏛️
**Complexidade:** Alta | **Impacto:** Legal
*   **O que fazer:** Ativar `FISCAL_ENV=production` e `FISCAL_PRODUCTION_CONFIRMED=true` após validação do checklist.
*   **Status:** Infraestrutura pronta. Aguardando sinal verde para Go-Live.

### 2. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo, configurar autenticação consumindo a API atual e criar a primeira tela de "Lista de Pedidos".
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Fiscal:** Homologação SEFAZ Real (Produção) - Primeira NFC-e emitida.
- [x] **Fiscal:** Salvaguardas de Produção e Checklist de Go-Live.
- [x] **Fiscal:** Homologação SEFAZ — Sandbox (Alternância de ambiente e Erro 204).
- [x] **Fiscal:** Especificação Técnica de Homologação (Protocolo SEFAZ).
- [x] **DevOps:** Bloco 2 - UI de Gestão de Feature Flags (Componentes + View + E2E).
- [x] **DevOps:** Bloco 1 (RE-EXECUÇÃO) - Core de Feature Flags (API Isolada + JWT Seguro + Unit Tests).
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo, configurar autenticação consumindo a API atual e criar a primeira tela de "Lista de Pedidos".
*   **Objetivo:** Iniciar a transição do PWA para App Nativo nas lojas.

### 2. [UX] Refinamento de Dashboard Multi-loja 📊
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Adicionar gráficos comparativos de DRE e CMV entre as unidades da franquia.

### 3. [Fiscal] Módulo de Inutilização de Numeração 🏛️
**Complexidade:** Média | **Impacto:** Legal
*   **O que fazer:** Implementar rota para inutilizar faixas de números de notas não utilizadas (exigência SEFAZ).
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 11 — Infraestrutura de Autenticação (Storage + Interceptors).
- [x] **Mobile:** Missão 10.2 — Assets Técnicos Placeholder.
- [x] **Mobile:** Missão 10.1 — Setup do Repositório Expo.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 12: Camada de Aplicação e Estado Global 🧠
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Definir contratos de estado (Zustand), Rehydration, Cold Start e o Hook `useAuth` desacoplado.
*   **Objetivo:** Criar a ponte entre a infraestrutura de Auth e a futura UI.

### 2. [UX] Refinamento de Dashboard Multi-loja 📊
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Adicionar gráficos comparativos de DRE e CMV.

### 3. [Fiscal] Módulo de Inutilização de Numeração 🏛️
**Complexidade:** Média | **Impacto:** Legal
*   **O que fazer:** Implementar rota para inutilizar faixas de números.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 16 — Implementação de UI (Login & Home).
- [x] **Mobile:** Missão 15 — UI Foundation (Design System).
- [x] **Mobile:** Missão 14A — Autenticação Semântica.
- [x] **Mobile:** Missão 13 — Bootstrap de Navegação.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 17: Módulo de Pedidos (KDS Mobile) 👨‍🍳
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Implementar a listagem de pedidos em tempo real consumindo o endpoint `/admin/{slug}/orders`.
*   **Objetivo:** Permitir que a cozinha/bar utilize o app nativo como monitor de produção.

### 2. [UX] Refinamento de Dashboard Multi-loja 📊
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Adicionar gráficos comparativos de DRE e CMV.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **SRE:** Normalização Atômica de Enums (Fix para 'BILL', 'DELETE', 'GASTRO').
- [x] **Hotfix:** Normalização de dados de PlanTier (Uppercase fix).
- [x] **Fiscal:** Homologação SEFAZ Real (Produção) - Primeira NFC-e emitida.
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo, configurar autenticação consumindo a API atual e criar a primeira tela de "Lista de Pedidos".

### 2. [UX] Refinamento de Dashboard Multi-loja 📊
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Adicionar gráficos comparativos de DRE e CMV entre as unidades da franquia.

### 3. [Fiscal] Módulo de Inutilização de Numeração 🏛️
**Complexidade:** Média | **Impacto:** Legal
*   **O que fazer:** Implementar rota para inutilizar faixas de números de notas não utilizadas.
# 📋 Backlog Mestre de Tarefas: MesaFlow

Este documento é a **fonte única de verdade** para a execução tática.

## ✅ Concluído Recentemente (Fase 9 - Enterprise)
- [x] **Hotfix:** Normalização global de Enums (Lowercase fix para PlanTier e Segment).
- [x] **Fiscal:** Homologação SEFAZ Real (Produção) - Primeira NFC-e emitida.
- [x] **Fiscal:** Salvaguardas de Produção e Checklist de Go-Live.
- [x] **Fiscal:** Homologação SEFAZ — Sandbox (Alternância de ambiente e Erro 204).
- [x] **Fiscal:** Especificação Técnica de Homologação (Protocolo SEFAZ).
- [x] **DevOps:** Bloco 2 - UI de Gestão de Feature Flags (Componentes + View + E2E).
- [x] **DevOps:** Bloco 1 (RE-EXECUÇÃO) - Core de Feature Flags (API Isolada + JWT Seguro + Unit Tests).
- [x] **DevOps:** Tenant Impersonation (God Mode) com registro de auditoria.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Setup do Repositório React Native 📱
**Complexidade:** Alta | **Impacto:** Estratégico
*   **O que fazer:** Inicializar projeto Expo, configurar autenticação consumindo a API atual e criar a primeira tela de "Lista de Pedidos".
*   **Objetivo:** Iniciar a transição do PWA para App Nativo nas lojas.

### 2. [UX] Refinamento de Dashboard Multi-loja 📊
**Complexidade:** Média | **Impacto:** Gestão
*   **O que fazer:** Adicionar gráficos comparativos de DRE e CMV entre as unidades da franquia.

### 3. [Fiscal] Módulo de Inutilização de Numeração 🏛️
**Complexidade:** Média | **Impacto:** Legal
*   **O que fazer:** Implementar rota para inutilizar faixas de números de notas não utilizadas (exigência SEFAZ).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 14A — Autenticação Semântica (Validação de JWT e Refresh no Boot).
- [x] **Mobile:** Missão 11 — Infraestrutura de Autenticação (Storage + Interceptors).
- [x] **Mobile:** Missão 10.2 — Assets Técnicos Placeholder.
- [x] **Mobile:** Missão 10.1 — Setup do Repositório Expo.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 15: UI Foundation (Design System Nativo) 🎨
**Complexidade:** Média | **Impacto:** Visual
*   **O que fazer:** Implementar tokens de cores, tipografia e componentes base (Button, Input, Card) conforme o Design System.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 14B — Auth Boundary & Navigation Gate (Hardening de Renderização).
- [x] **Mobile:** Missão 14A — Autenticação Semântica (Validação de JWT e Refresh no Boot).
- [x] **Audit:** Materialização da Auditoria JWT Backend (Evidência ADR).
- [x] **Mobile:** Missão 11 — Infraestrutura de Autenticação (Storage + Interceptors).
- [x] **Mobile:** Missão 10.2 — Assets Técnicos Placeholder.
- [x] **Mobile:** Missão 10.1 — Setup do Repositório Expo.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 15: UI Foundation (Design System Nativo) 🎨
**Complexidade:** Média | **Impacto:** Visual
*   **O que fazer:** Implementar tokens de cores, tipografia e componentes base (Button, Input, Card) conforme o Design System.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 14B — Auth Boundary & Navigation Gate (Barreira de renderização).
- [x] **Mobile:** Missão 14A — Autenticação Semântica (Validação de JWT e Refresh no Boot).
- [x] **Mobile:** Missão 11 — Infraestrutura de Autenticação (Storage + Interceptors).
- [x] **Mobile:** Missão 10.2 — Assets Técnicos Placeholder.
- [x] **Mobile:** Missão 10.1 — Setup do Repositório Expo.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 15: UI Foundation (Design System Nativo) 🎨
**Complexidade:** Média | **Impacto:** Visual
*   **O que fazer:** Implementar tokens de cores, tipografia e componentes base (Button, Input, Card) conforme o Design System.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 14B — Auth Boundary & Navigation Gate (Hotfix v2.2 - Regex Resiliency).
- [x] **Mobile:** Missão 14A — Autenticação Semântica (Validação de JWT e Refresh no Boot).
- [x] **Audit:** Materialização da Auditoria JWT Backend (Evidência ADR).
- [x] **Mobile:** Missão 11 — Infraestrutura de Autenticação (Storage + Interceptors).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 15: UI Foundation (Design System Nativo) 🎨
**Complexidade:** Média | **Impacto:** Visual
*   **O que fazer:** Implementar tokens de cores, tipografia e componentes base (Button, Input, Card) conforme o Design System.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 15 — UI Foundation (Design System Nativo e Componentes Base).
- [x] **Mobile:** Missão 14B — Auth Boundary & Navigation Gate (Hardening de Renderização).
- [x] **Mobile:** Missão 14A — Autenticação Semântica (Validação de JWT e Refresh no Boot).
- [x] **Audit:** Materialização da Auditoria JWT Backend (Evidência ADR).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 16: UI Implementation (Login & Home) 📲
**Complexidade:** Média | **Impacto:** Funcional
*   **O que fazer:** Criar as interfaces de Login e Home utilizando os componentes da UI Foundation e conectando à Auth Store.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 16 — UI Real (Telas de Login e Home funcionais conectadas à Store).
- [x] **Mobile:** Missão 15 — UI Foundation (Design System Nativo e Componentes Base).
- [x] **Mobile:** Missão 14B — Auth Boundary & Navigation Gate (Hardening de Renderização).
- [x] **Mobile:** Missão 14A — Autenticação Semântica (Validação de JWT e Refresh no Boot).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 17: Módulo de Pedidos (KDS Nativo) 👨‍🍳
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Implementar a listagem de pedidos em tempo real no app mobile, permitindo o avanço de status por praça de produção.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 16 — UI Real (Telas de Login e Home funcionais).
- [x] **Mobile:** Missão 15 — UI Foundation (Design System Nativo e Componentes Base).
- [x] **Mobile:** Missão 14B — Auth Boundary & Navigation Gate (Hardening de Renderização).
- [x] **Mobile:** Missão 14A — Autenticação Semântica (Validação de JWT e Refresh no Boot).
- [x] **Audit:** Materialização da Auditoria JWT Backend (Evidência ADR).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 17: Módulo de Pedidos (KDS Nativo) 👨‍🍳
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Implementar a listagem de pedidos em tempo real no app mobile, permitindo o avanço de status diretamente por dispositivos nativos.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 17 — Módulo de Pedidos (KDS Nativo funcional).
- [x] **Mobile:** Missão 16 — UI Real (Telas de Login e Home funcionais).
- [x] **Mobile:** Missão 15 — UI Foundation (Design System Nativo).
- [x] **Mobile:** Missão 14B — Auth Boundary & Navigation Gate.

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 18: Real-time Sync (WebSockets Mobile) 📡
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Integrar o módulo de pedidos mobile com o servidor Redis Pub/Sub, permitindo que a lista de pedidos seja atualizada instantaneamente sem re-fetch manual.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 18 — Realtime Operacional (Infraestrutura WebSocket para KDS).
- [x] **Mobile:** Missão 17 — Módulo de Pedidos (KDS Nativo funcional).
- [x] **Mobile:** Missão 16 — UI Real (Telas de Login e Home funcionais).
- [x] **Mobile:** Missão 15 — UI Foundation (Design System Nativo).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 19: Perfil e Bootstrap de Domínio 👤
**Complexidade:** Média | **Impacto:** Arquitetural
*   **O que fazer:** Implementar a store de perfil para extrair o `slug` da empresa do JWT (ou via fetch `/me`) e injetar dinamicamente nos serviços de Pedidos e Realtime, eliminando os placeholders de teste.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 19 — Identidade Operacional (Bootstrap de Sessão dinâmico via JWT).
- [x] **Mobile:** Missão 18 — Realtime Operacional (Infraestrutura WebSocket para KDS).
- [x] **Mobile:** Missão 17 — Módulo de Pedidos (KDS Nativo funcional).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 20: Resiliência de Conectividade & State Sync 📡
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Implementar reconexão automática (Backoff) no WebSocket e lógica de re-sincronização de estado da Store após reconexão, garantindo que nenhum pedido seja perdido em áreas de sombra de Wi-Fi.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Mobile:** Missão 19 — Identidade Operacional (Bootstrap reativo e centralização de tipos).
- [x] **Mobile:** Missão 18 — Realtime Operacional (Infraestrutura WebSocket para KDS).
- [x] **Mobile:** Missão 17 — Módulo de Pedidos (KDS Nativo funcional).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 20: Resiliência de Conectividade & State Sync 📡
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Implementar reconexão automática (Backoff) no WebSocket e lógica de re-sincronização inteligente. Corrigir o gap do `new_order` realizando fetch automático do objeto completo ao receber o evento.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Missão 14B:** Auth Boundary & Navigation Gate (Hardening).
- [x] **Missão 16:** UI Real (Login + Home).
- [x] **Missão 17:** Módulo de Pedidos (KDS Nativo).
- [x] **Missão 18:** Realtime Operacional (WebSocket/SSE).
- [x] **Missão 19:** Identidade Operacional & Bootstrap de Sessão.
- [x] **Missão 21:** Tempo Operacional & SLA (Global Clock).
- [x] **Missão 22:** Alertas Operacionais (Atenção Ativa - Hardening v2).

---

## 🚀 Próximas Prioridades (Fila de Execução Mobile)

### 1. [Mobile] Missão 23: Controles Operacionais do Operador 🎛️
**Complexidade:** Média | **Impacto:** UX Operacional
*   **O que fazer:** Implementar "Silent Mode" (pausar vibração), ajuste de sensibilidade de SLA e preferências de visualização.
*   **Persistência:** As escolhas do operador devem sobreviver ao reload do app.

### 2. [Mobile] Missão 24: Resiliência & Recuperação 📡
**Complexidade:** Alta | **Impacto:** Confiabilidade
*   **O que fazer:** Tratamento de queda de conexão, reconexão exponencial e re-sync de estado sem duplicidade de pedidos.

### 3. [Mobile] Missão 25: Estados de Erro & Falhas ⚠️
**Complexidade:** Média | **Impacto:** Estabilidade
*   **O que fazer:** UI de feedback para erros de rede, sessão expirada e inconsistências de backend.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Missão 23:** Controles do Operador (Silent Mode & Persistência).
- [x] **Missão 24:** Resiliência & Recuperação (Sync State & Re-sync).
- [x] **Missão 25:** Estados de Erro & Falhas (Socket Health & Error UI).
- [x] **QA:** Scripts de teste e validação de contrato para Missões 23-25.

---

## 🚀 Próximas Prioridades (Fila de Execução Mobile)

### 1. [Mobile] Missão 26: Observabilidade & Diagnóstico 📊
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Implementar logs estruturados no console (em dev) e preparação para captura de eventos operacionais (ex: tempo de resposta do socket).

### 2. [Mobile] Missão 27: Polimento Final & Release Candidate 🏁
**Complexidade:** Média | **Impacto:** Produto
*   **O que fazer:** Microinterações, feedback visual de toque, revisão de cores e preparação do `app.json` para build de produção.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Missão 23:** Controles do Operador (Silent Mode & Persistência).
- [x] **Missão 24:** Resiliência & Recuperação (Sync State & Re-sync).
- [x] **Missão 25:** Estados de Erro & Falhas (Socket Health & Error UI).
- [x] **Missão 26:** Persistência Local & Boot Determinístico (Offline-ready).
- [x] **QA:** Correção de testes de contrato e novo validador de persistência.

---

## 🚀 Próximas Prioridades (Fila de Execução Mobile)

### 1. [Mobile] Missão 27: Observabilidade & Diagnóstico 📊
**Complexidade:** Média | **Impacto:** Suporte
*   **O que fazer:** Implementar logs estruturados e captura de eventos operacionais para facilitar o debug em produção.

### 2. [Mobile] Missão 28: Polimento Final & Release Candidate 🏁
**Complexidade:** Média | **Impacto:** Produto
*   **O que fazer:** Microinterações, feedback visual de toque e preparação para build final.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Missão 23:** Controles do Operador (Silent Mode & Persistência).
- [x] **Missão 24:** Resiliência & Recuperação (Sync State & Re-sync).
- [x] **Missão 25:** Estados de Erro & Falhas (Socket Health & Error UI).
- [x] **Missão 26:** Persistência Local & Boot Determinístico (Offline-ready).
- [x] **Missão 27:** Observabilidade & Diagnóstico (Logger Service & Instrumentação).

---

## 🚀 Próximas Prioridades (Fila de Execução Mobile)

### 1. [Mobile] Missão 28: Polimento Final & Release Candidate 🏁
**Complexidade:** Média | **Impacto:** Produto
*   **O que fazer:** Microinterações, feedback visual de toque, revisão de cores e preparação do `app.json` para build de produção.
*   **Objetivo:** Encerrar a Fase 10 com um app pronto para as lojas.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 10 - Mobile)
- [x] **Missão 23-25:** Resiliência, Erros e Controles do Operador.
- [x] **Missão 26:** Persistência Local & Boot Determinístico.
- [x] **Missão 27:** Observabilidade & Diagnóstico.
- [x] **Missão 28:** Polimento Final & Release Candidate (Fase 10 Concluída).

---

## 🚀 Próximas Prioridades (Fase 11 - Expansão Mobile)

### 1. [Mobile] Missão 29: Módulo de Garçom Nativo (Mobile POS) 🤵
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Implementar a abertura de mesas e lançamento de pedidos diretamente no app nativo, substituindo o PWA legado.

### 2. [Mobile] Missão 30: Impressão Bluetooth Nativa 🖨️
**Complexidade:** Alta | **Impacto:** Hardware
*   **O que fazer:** Integração com bibliotecas nativas para busca e pareamento de impressoras térmicas via Bluetooth/BLE.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 11 - Mobile POS)
- [x] **Missão 29A-C:** Fluxo completo de POS (Mesas, Carrinho, Envio).
- [x] **Missão 30A-B:** Infraestrutura de Impressão Bluetooth.
- [x] **Missão 31:** Notificações Push Nativa (FCM).
- [x] **Missão 32:** Gestão de Chamados (Waiter Call).

---

## 🚀 Próximas Prioridades (Fase 11 - Continuação)

### 1. [Mobile] Missão 33: Pagamentos e QR Code Nativo 💰
**Complexidade:** Média | **Impacto:** Financeiro
*   **O que fazer:** Exibir o QR Code Pix dinâmico gerado pelo backend diretamente no app do garçom para recebimento rápido.

### 2. [Mobile] Missão 34: Offline Order Queue (Contingência) 📡
**Complexidade:** Alta | **Impacto:** Resiliência
*   **O que fazer:** Implementar fila de pedidos offline para garantir que vendas não sejam perdidas em quedas de Wi-Fi.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 11 - Mobile POS)
- [x] **Missão 29A-C:** Fluxo completo de POS (Mesas, Carrinho, Envio).
- [x] **Missão 30A-B:** Infraestrutura de Impressão Bluetooth.
- [x] **Missão 31:** Notificações Push Nativa (FCM).
- [x] **Missão 32:** Gestão de Chamados (Waiter Call).
- [x] **Missão 33:** Pagamentos e QR Code Nativo.
- [x] **Missão 34:** Fila de Pedidos Offline (Contingência).

---

## 🚀 Próximas Prioridades (Fase 12 - Lançamento & Produção)

### 1. [Mobile] Missão 35: Preparação para Lojas (EAS Build) 📦
**Complexidade:** Média | **Impacto:** Crítico
*   **O que fazer:** Configurar `eas.json`, revisar permissões de produção, atualizar ícones finais e splash screens. Gerar o primeiro build de distribuição.

### 2. [Mobile] Missão 36: Testes de Stress em Campo 🧪
**Complexidade:** Alta | **Impacto:** Estabilidade
*   **O que fazer:** Simular 100 pedidos simultâneos via múltiplos dispositivos mobile para validar a carga no WebSocket e Redis.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 11 - Mobile POS)
- [x] **Missão 29-34:** Fluxo completo de POS, Impressão, Push e Fila Offline.
- [x] **Missão 35:** Preparação para Lojas (EAS Build & Production Metadata).

---

## 🚀 Próximas Prioridades (Fase 12 - Lançamento & Produção)

### 1. [Mobile] Missão 36: Build & Smoke Test Nativo 🏗️
**Complexidade:** Média | **Impacto:** Crítico
*   **O que fazer:** Executar `eas build --profile preview` para gerar o APK. Instalar o binário real no dispositivo e validar se o app abre e comunica com a API sem o auxílio do servidor de desenvolvimento do Expo.

### 2. [Mobile] Missão 37: Homologação de Impressão em Campo 🖨️
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Testar a bridge Bluetooth com uma impressora térmica física real (ex: Goojprt/Zebra) usando o binário de produção.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 12 - Lançamento & QA)
- [x] **Build Nativo:** APK gerado e validado no emulador.
- [x] **Smoke Test:** Automação ADB funcional (Login e Captura).
- [x] **Unit Tests:** Lógica de SLA, AuthStore e Hardware Encoder validados.
- [x] **Modos de Teste:** Manual, Funcional (ADB) e Unitário (Jest) integrados.

---

## 🚀 Próximas Prioridades (Fase 12 - Hardening & Campo)

### 1. [Mobile] Missão 37: Homologação de Impressão em Campo 🖨️
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Testar o APK em um dispositivo físico com uma impressora Bluetooth real.

### 2. [Mobile] Missão 14A: Endurecimento Semântico de Auth 🛡️
**Complexidade:** Alta | **Impacto:** Segurança
*   **O que fazer:** Implementar validação rigorosa de claims do JWT no mobile (Pendente no backlog técnico).
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 12 - Lançamento & Hardening)
- [x] **Build Nativo:** APK gerado e validado no emulador.
- [x] **QA Mobile:** Suíte de testes unitários e funcionais (ADB) homologada.
- [x] **Missão 14A:** Endurecimento Semântico de Auth concluído (Validação de Claims).

---

## 🚀 Próximas Prioridades (Fase 12 - Campo & Hardware)

### 1. [Mobile] Missão 37: Homologação de Impressão em Campo 🖨️
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Testar o APK em um dispositivo físico com uma impressora Bluetooth real.

### 2. [Mobile] Missão 38: Sentry Native Integration 📊
**Complexidade:** Média | **Impacto:** Observabilidade
*   **O que fazer:** Integrar o Sentry para capturar crashes nativos no APK de produção.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 12 - Lançamento & Hardening)
- [x] **Build Nativo:** APK gerado e validado no emulador.
- [x] **QA Mobile:** Suíte de testes unitários e funcionais (ADB) homologada (14 testes PASS).
- [x] **Missão 14A:** Endurecimento Semântico de Auth concluído.

---

## 🔄 Próximas Prioridades (Fase 12 - Campo & Hardware)

### 1. [Mobile] Missão 37: Homologação de Impressão em Campo 🖨️
**Complexidade:** Alta | **Impacto:** Operacional
*   **Status:** EM ANDAMENTO.
*   **O que fazer:** Testar o APK em um dispositivo físico com uma impressora Bluetooth real.

### 2. [Mobile] Missão 38: Sentry Native Integration 📊
**Complexidade:** Média | **Impacto:** Observabilidade
*   **O que fazer:** Integrar o Sentry para capturar crashes nativos no APK de produção.

# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 12 - Lançamento & Hardening)
- [x] **Build Nativo:** APK gerado e validado no emulador.
- [x] **QA Mobile:** Suíte de testes unitários e funcionais (ADB) homologada.
- [x] **Missão 14A:** Endurecimento Semântico de Auth concluído (Validação de Claims).

---

## 🚀 Próximas Prioridades (Fase 12 - Campo & Hardware)

### 1. [Mobile] Missão 37: Homologação de Impressão em Campo 🖨️
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Testar o APK em um dispositivo físico com uma impressora Bluetooth real.

### 2. [Mobile] Missão 38: Sentry Native Integration 📊
**Complexidade:** Média | **Impacto:** Observabilidade
*   **O que fazer:** Integrar o Sentry para capturar crashes nativos no APK de produção.
# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 12 - Lançamento & Hardening)
- [x] **Build Nativo:** APK v1.0.1 gerado com correções semânticas.
- [x] **Missão 14A:** Endurecimento de Auth e decodificação resiliente de JWT.
- [x] **Bugfix:** Correção de chaves inválidas no SecureStore (Remoção de caracteres especiais).

---

## 🚀 Próximas Prioridades (Fase 12 - Campo & Hardware)

### 1. [Mobile] Missão 37: Homologação de Impressão em Campo 🖨️
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Testar a comunicação Bluetooth com uma impressora térmica real usando o novo APK.

### 2. [Mobile] Missão 38: Sentry Native Integration 📊
**Complexidade:** Média | **Impacto:** Observabilidade
*   **O que fazer:** Integrar o Sentry para capturar crashes nativos.
