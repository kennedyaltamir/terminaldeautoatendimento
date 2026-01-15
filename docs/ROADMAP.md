# 🗺️ MesaFlow Master Roadmap: A Jornada Estratégica

> **Versão do Documento:** 5.0 (Definitive Edition)
> **Última Atualização:** Janeiro de 2026
> **Status Global:** Fase de Consolidação de Ecossistema & Expansão Nativa
> **Visão:** Tornar-se o Sistema Operacional padrão para ambientes de alto tráfego na América Latina.

Este documento é a **fonte única da verdade estratégica** do MesaFlow. Ele não é apenas uma lista de tarefas; é a narrativa da evolução do produto, detalhando as decisões arquiteturais, os desafios de engenharia superados e a visão de futuro que guia nossa expansão.

---

## ⚖️ Governança do Roadmap

Para garantir que este documento permaneça relevante e alinhado com a realidade técnica de uma startup em hipercrescimento, estabelecemos as seguintes regras de governança:

1.  **Imutabilidade Histórica:** Fases marcadas como `[CONCLUÍDO]` representam compromissos entregues, auditados e em produção. Não reescrevemos a história; aprendemos com ela.
2.  **Atualização por Gatilho:** Este arquivo deve ser atualizado obrigatoriamente ao final de cada **Épico** (conjunto de missões) ou **Release Principal** (ex: v2.0, v3.0).
3.  **Definição de Pronto (DoD):** Um item só entra como concluído se tiver: Código mergeado na `main`, Testes passando (Green Build), Documentação técnica atualizada e Validação de Negócio.
4.  **Priorização Dinâmica:** Os itens da seção "Futuro" são intenções estratégicas. A ordem de execução pode mudar baseada em feedback de mercado (Customer Feedback Loop) ou restrições técnicas descobertas.

---

## 🏛️ Era 1: Fundação & Product-Market Fit (Fases 1 a 4)
*O nascimento da plataforma. O foco inicial foi validar a tese da "Arquitetura Híbrida" (Autoatendimento + Garçom) com o menor custo de infraestrutura possível.*

### ✅ Fase 1: O Core Operacional (The Monolith)
**Contexto:** Precisávamos de velocidade. Decidimos por um **Monolito Modular** para evitar a complexidade prematura de microserviços.
- [x] **Arquitetura Base:** FastAPI (Async) para performance de I/O + Next.js 14 para SEO e UX.
- [x] **Multi-tenancy Rígido:** Implementação de isolamento lógico por `company_id` em nível de ORM. Isso garantiu que dados de um restaurante nunca vazassem para outro, essencial para a confiança B2B.
- [x] **KDS Web (v1):** A primeira versão do monitor de cozinha, usando WebSockets simples para substituir impressoras de papel.
- [x] **Cardápio Digital (PWA):** Interface pública focada em conversão, sem necessidade de download de app pelo cliente final.

### ✅ Fase 2: Profissionalização SaaS
**Contexto:** O produto funcionava, mas precisava ser vendável e escalável sem intervenção manual.
- [x] **Onboarding Self-Service:** Fluxo completo de auto-cadastro, permitindo que o dono configure sua loja, cardápio e mesas sem falar com um humano.
- [x] **Estoque Inteligente (Regra 86):** Lógica crítica que bloqueia vendas automaticamente quando o insumo acaba, prevenindo a frustração do cliente e o cancelamento de pedidos.
- [x] **Gestão de Mesas:** Criação do mapa visual e geração de QR Codes tokenizados, garantindo que cada pedido seja vinculado inequivocamente a uma localização física.

### ✅ Fase 3: Fintech Embutida (The Money Maker)
**Contexto:** Transformar o software em uma fonte de receita transacional (Take Rate), além da assinatura (SaaS).
- [x] **Split de Pagamento:** Integração profunda com Mercado Pago OAuth. A plataforma retém a comissão na fonte antes que o dinheiro chegue ao restaurante, eliminando inadimplência e bitributação.
- [x] **Motor de Assinaturas:** Integração com Stripe para gestão de planos (Free/Pro). Implementação de Webhooks para bloquear/desbloquear recursos em tempo real baseado no pagamento da fatura.
- [x] **Dashboard Financeiro:** Métricas reais via agregação SQL (Ticket Médio, Curva ABC), dando ao dono do restaurante visibilidade que ele nunca teve antes.

### ✅ Fase 4: Logística & Fidelidade
**Contexto:** Expansão para além das quatro paredes do restaurante e foco em LTV (Lifetime Value).
- [x] **App do Entregador (Web):** Interface simplificada para motoboys aceitarem rotas.
- [x] **Rastreamento GPS:** Relay de coordenadas em tempo real para o cliente final, reduzindo a ansiedade e chamados de suporte ("Onde está meu pedido?").
- [x] **Cashback Nativo:** Carteira digital vinculada ao telefone do cliente. Uma ferramenta poderosa de retenção que substitui o cartão fidelidade de papel.

---

## 🏢 Era 2: Enterprise & Resiliência (Fases 5 a 9)
*Endurecimento do sistema para suportar grandes operações, franquias e requisitos legais complexos. Aqui deixamos de ser um "app de cardápio" para ser um ERP leve.*

### ✅ Fase 5: Resiliência & Offline-First
**Contexto:** A internet de restaurante é instável. O sistema não pode parar se o Wi-Fi cair.
- [x] **Arquitetura Offline:** Implementação do `Dexie.js` (IndexedDB) no frontend. Pedidos são salvos localmente e sincronizados quando a rede volta.
- [x] **Infraestrutura Escalável:** Migração de WebSockets em memória para **Redis Pub/Sub**, permitindo que o backend escale horizontalmente em múltiplos containers sem perder mensagens.
- [x] **Observabilidade:** Integração profunda com Sentry (Back/Front) para detecção proativa de erros antes que o cliente reclame.

### ✅ Fase 6: Polimento & UX (Quality of Life)
**Contexto:** Redução de fricção e melhoria da percepção de qualidade.
- [x] **Login Social:** Integração Google Identity Services para facilitar o acesso.
- [x] **Performance Percebida:** Implementação de Skeleton Loaders em todo o sistema, eliminando o "layout shift" e melhorando a sensação de velocidade.
- [x] **CI/CD Pipeline:** Automação de testes e deploy no GitHub Actions, garantindo que nenhum código quebrado chegue em produção (Green Build Policy).

### ✅ Fase 7: Ecossistema & Inteligência
**Contexto:** Abertura da plataforma para terceiros e uso de dados para gerar valor.
- [x] **WhatsApp Automation:** Integração real com Evolution API para notificações transacionais ("Seu pedido saiu!"), aumentando a confiança do consumidor.
- [x] **IA Upselling:** Motor de recomendação (Market Basket Analysis) no carrinho. O sistema aprende que "quem compra X, leva Y" e sugere automaticamente, aumentando o ticket médio.
- [x] **Webhooks de Saída:** Sistema de notificação para ERPs externos com assinatura HMAC, permitindo que grandes redes integrem o MesaFlow em seus sistemas legados.

### ✅ Fase 8: Excelência Operacional
**Contexto:** Foco nos atores humanos (Garçom e Cozinheiro) para aumentar a produtividade.
- [x] **Modo Expedidor:** Tela de montagem de bandejas para organizar o caos da cozinha.
- [x] **Hardware Web:** Integração com Gaveta de Dinheiro e Impressoras de Etiquetas (ZPL) via browser.
- [x] **Garçom Pro:** Funcionalidades avançadas como Split de conta por item, Gorjeta customizada e CRM na ponta (identificação do cliente).

### 🔄 Fase 9: Legal & Integrações Pesadas (EM ANDAMENTO)
**Contexto:** Remoção de barreiras de entrada para grandes redes (Enterprise) que exigem conformidade fiscal total.
- [x] **Contingência Fiscal:** Fila local para emissão de notas sem internet.
- [x] **Tenant Impersonation:** Modo "God Mode" auditado para suporte técnico acessar contas de clientes.
- [ ] **Homologação SEFAZ:** Emissão real de NFC-e em produção (Go-Live). O "elefante na sala" da operação brasileira.
- [ ] **Hub iFood:** Middleware de ingestão de pedidos de marketplaces. Centraliza tudo no KDS do MesaFlow, eliminando a necessidade de múltiplos tablets.

---

## 📱 Era 3: A Revolução Mobile (Fases 10 a 12)
*Transição estratégica do PWA para Aplicações Nativas (React Native). O objetivo é acesso profundo ao hardware (Bluetooth, Vibração, Background) e performance nativa.*

### ✅ Fase 10: Deep Tech & KDS Nativo
**Contexto:** Construção da fundação mobile. O KDS precisa ser à prova de falhas.
- [x] **Infraestrutura Mobile:** Setup Expo SDK 54, Auth Semântica e SecureStore.
- [x] **Realtime Nativo:** WebSocket com reconexão exponencial e reconciliação de estado (State Reconciliation).
- [x] **SLA Engine:** Motor de prioridade temporal determinístico (Global Clock) que reordena pedidos baseado na urgência.
- [x] **Atenção Ativa:** Sistema de alertas sensoriais (Vibração) com cooldown inteligente para garantir que a cozinha nunca perca um pedido.

### ✅ Fase 11: Mobile POS (O Garçom Biônico)
**Contexto:** Portabilidade total da operação de salão para o bolso do garçom.
- [x] **Gestão de Mesas Nativa:** Mapa interativo com status em tempo real.
- [x] **Lançamento de Pedidos:** Carrinho local, busca rápida e envio resiliente (Fila Offline).
- [x] **Hardware Bluetooth:** Driver nativo ESC/POS para impressoras térmicas portáteis (Zebra/Goojprt).
- [x] **Pagamentos na Mesa:** Geração de Pix Dinâmico na tela do garçom, fechando o ciclo financeiro.

### 🔄 Fase 12: Distribuição & Escala (EM ANDAMENTO)
**Contexto:** Levar o aplicativo para as mãos dos usuários finais através das lojas oficiais.
- [x] **Build System:** Configuração do EAS (Expo Application Services) para CI/CD mobile.
- [x] **Build Local:** Pipeline de geração de APK via Gradle/JDK 17 (Independência da nuvem).
- [x] **Observabilidade Nativa:** Integração Sentry Native para captura de crashes de baixo nível (NDK).
- [ ] **Lojas:** Publicação na Google Play Store e Apple App Store.
- [ ] **OTA Updates:** Configuração de atualizações via ar (Code Push) para correções críticas sem passar pela revisão da loja.

---

## 🔮 O Horizonte: Visão 2026+
*Onde queremos chegar. Estas são as apostas estratégicas para manter a liderança tecnológica.*

### 🧠 Inteligência Preditiva
- **Previsão de Demanda:** "Prepare 20 hambúrgueres, vai lotar às 19h". Uso de séries temporais para prever o movimento.
- **Sugestão de Compras:** Geração automática de pedidos para fornecedores baseada no estoque projetado e consumo histórico.

### 🌐 MesaFlow Passport (Network Effect)
- **Identidade Global:** O cliente tem uma conta única em todos os restaurantes MesaFlow.
- **Cashback Interoperável:** Acumule na Pizzaria A, gaste na Hamburgueria B (Clearing House). Isso cria um efeito de rede defensável.

### 🗣️ Interfaces Naturais & Hardware
- **Voice Ordering:** Pedidos por voz no KDS ("Mesa 10, pronto!") para mãos ocupadas.
- **SmartPOS SDK:** Rodar o MesaFlow embarcado dentro das maquininhas de cartão (Stone/Cielo), eliminando a necessidade de celulares para os garçons.

---
*Este roadmap é um documento vivo, revisado trimestralmente pelo comitê de produto e engenharia.*
# 🗺️ MesaFlow Master Roadmap: A Jornada da Estabilidade Absoluta
**Status:** Gold Master Candidate (L6)

## 🏛️ Era 1: Fundação (Concluída e Auditada)
*Core operacional, RLS, WebSockets e Pagamentos Básicos.*

## 🛡️ Era 2: Estabilização & Omni-Check (Janeiro 2026)
*Foco: Parar o retrabalho. Blindagem total.*
- **Fase A:** Implementação do Omni-Check (Script de Regressão Total).
- **Fase B:** Documentação Exaustiva de Telas e Questionários de 100 Perguntas.
- **Fase C:** Selagem de Produção (Checklist Final).

## 🏢 Era 3: Enterprise & Fiscal (Fevereiro 2026)
*Funcionalidades de alto escalão sobre base estável.*
- **Fiscal:** Emissão de NFC-e real e contingência.
- **Ecossistema:** Hub iFood e Integrações Externas.
- **Lojas:** Publicação oficial Mobile.

## 🧠 Era 4: Inteligência & Expansão (Q2 2026+)
*IA Preditiva e Rede Global de Cashback (Passport).*

---
*Este Roadmap é imutável em suas eras concluídas e rigoroso em suas eras futuras.*
# 🗺️ MesaFlow Master Roadmap: A Jornada da Estabilidade (L6)

## 🏛️ Era 1: Fundação (Concluída)
*Core operacional, RLS e Pagamentos Básicos.*

## 🛡️ Era 2: Estabilização (Concluída)
*Foco: Eliminar o retrabalho.*
- [x] **Omni-Check:** Escudo de regressão total ativo.
- [x] **Omniscience:** 100% do sistema documentado e mapeado.
- [x] **Immune System:** Acúmulo de conhecimento automático no Kernel.

## 🏢 Era 3: Enterprise & Fiscal (Fevereiro 2026)
*Funcionalidades de alto escalão sobre base estável.*
- **Fiscal:** Ativação da Focus NFe e Contingência Offline.
- **Ecossistema:** Hub iFood e Webhooks de Saída.
- **Mobile:** Lançamento oficial nas lojas.

## 🧠 Era 4: Inteligência (Q2 2026+)
- **IA Preditiva:** Previsão de demanda e sugestão de compras.
- **Passport:** Rede global de fidelidade MesaFlow.

---
*Nenhuma etapa avança sem o sinal verde do Omni-Check.*
# 🗺️ MesaFlow Master Roadmap: A Jornada da Estabilidade (L6)

## 🏛️ Era 1: Fundação (Concluída)
*Core operacional, RLS e Pagamentos Básicos.*

## 🛡️ Era 2: Estabilização (Concluída)
*Foco: Eliminar o retrabalho e criar soberania de conhecimento.*
- [x] **Omni-Check:** Escudo de regressão total ativo e validado.
- [x] **Omniscience:** 100% do sistema documentado (34 rotas).
- [x] **Immune System:** Acúmulo de conhecimento automático no Kernel.
- [x] **Audit Ready:** 700 perguntas de auditoria para o time.

## 🏢 Era 3: Enterprise & Fiscal (Fevereiro 2026)
*Funcionalidades de alto escalão sobre base inquebrável.*
- **Fiscal:** Ativação da Focus NFe e Contingência Offline.
- **Ecossistema:** Hub iFood e Webhooks de Saída.
- **Mobile:** Lançamento oficial nas lojas Apple e Google.

## 🧠 Era 4: Inteligência (Q2 2026+)
- **IA Preditiva:** Previsão de demanda e sugestão de compras.
- **Passport:** Rede global de fidelidade MesaFlow.

---
*Nenhuma etapa avança sem o sinal verde do Omni-Check.*
