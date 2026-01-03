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