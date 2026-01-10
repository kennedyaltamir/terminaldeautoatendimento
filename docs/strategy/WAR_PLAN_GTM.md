# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 10:35:00
# 🚀 WAR PLAN: MesaFlow Go-To-Market (GTM)

> **Status:** CRÍTICO
> **Objetivo:** Transformar código em receita recorrente (ARR).

Esta é uma análise crítica e um **Plano de Guerra** para transformar o código do MesaFlow em um negócio SaaS rentável e escalável. Não basta o código rodar; a operação precisa parar de pé.

---

## 1. Infraestrutura de Produção (Blindagem)
*O ambiente de desenvolvimento (localhost) é um berço. A produção é uma selva.*

### 🔴 Crítico (Antes de vender 1 real)
1.  **Banco de Dados Gerenciado:**
    *   **Ação:** Migrar para **Neon.tech** (Postgres Serverless) ou **AWS RDS**.
    *   **Por que:** Você precisa de backups automáticos (PITR - Point-in-Time Recovery). Se um restaurante perder o cardápio na sexta à noite, você será processado.
    *   **Config:** Ativar *Connection Pooling* (PgBouncer) para suportar milhares de conexões simultâneas do KDS.

2.  **Observabilidade Real (Não é só log):**
    *   **Ação:** Configurar **Sentry** (Backend e Frontend) e **LogRocket/Hotjar** (Frontend).
    *   **Por que:** Você precisa saber que o erro aconteceu *antes* do cliente ligar gritando. O LogRocket permite ver o "replay" do que o usuário fez antes do bug.

3.  **CDN e Edge Caching:**
    *   **Ação:** Hospedar o Frontend na **Vercel** (Edge Network).
    *   **Por que:** O cardápio tem que abrir em < 1s no 4G. Cacheie agressivamente as rotas públicas (`/menu`).

4.  **Domínios e SSL Wildcard:**
    *   **Ação:** Configurar DNS para suportar `*.mesaflow.com.br` e domínios personalizados (`pedidos.hamburgueriaze.com.br`).
    *   **Ferramenta:** Vercel Custom Domains ou Cloudflare for SaaS.

---

## 2. Produto & Experiência (O "Uau")
*O software não pode parecer "sistema de engenheiro". Tem que ser à prova de falhas.*

1.  **Onboarding Self-Service (Zero Touch):**
    *   **Crítica:** Hoje o cadastro é manual ou complexo.
    *   **Ação:** O usuário deve criar conta, subir logo, cadastrar 1 produto e gerar o QR Code em **5 minutos**. Se precisar de suporte para começar, o modelo não escala.
    *   **Feature:** "Importar Cardápio do iFood" (Scraper ou API). Isso reduz a barreira de entrada em 90%.

2.  **Mobile App nas Lojas:**
    *   **Ação:** Publicar o App do Garçom/KDS na Google Play e Apple App Store.
    *   **Por que:** Instalar APK via cabo (ADB) não existe no mundo real. O dono do restaurante quer baixar na loja.
    *   **Ferramenta:** EAS Submit (Expo).

3.  **Modo Offline Robusto:**
    *   **Teste de Fogo:** Desligue o roteador no meio de um pedido. O app do garçom deve continuar funcionando e sincronizar silenciosamente quando voltar. Se travar, o restaurante para.

---

## 3. Jurídico & Financeiro (O "Boring but Vital")

1.  **Termos de Uso e Privacidade (LGPD):**
    *   **Ação:** Contratar advogado especializado em SaaS ou usar templates premium (ex: Avodocs), mas revisar.
    *   **Ponto Crítico:** Deixar claro que você é o **Operador** de dados e o restaurante é o **Controlador**. Defina responsabilidade sobre fraudes de cartão (Chargeback).

2.  **Emissão de Nota Fiscal (SaaS):**
    *   **Ação:** Automatizar a emissão da SUA nota fiscal para o restaurante (via eNotas ou FocusNFe) assim que o Stripe cobrar a assinatura.

3.  **Split de Pagamento (Compliance):**
    *   **Ação:** Validar a conta no Mercado Pago como "Marketplace".
    *   **Risco:** Se o Banco Central auditar, você precisa provar que não está fazendo custódia de fundos de terceiros indevidamente. O dinheiro deve ir direto para o lojista.

---

## 4. Estratégia Comercial (Vendas)

### Fase 1: Os "Design Partners" (0 a 10 Clientes)
*Não tente vender online ainda. Você precisa de feedback, não de escala.*
*   **Ação:** Vá fisicamente a 10 restaurantes médios (não redes, não botecos).
*   **Oferta:** "Usem de graça por 3 meses em troca de feedback semanal. Eu configuro tudo para vocês."
*   **Objetivo:** Encontrar os bugs que só acontecem na "vida real" (cozinha engordurada, wi-fi instável, garçom com dedo molhado).

### Fase 2: Venda Direta (10 a 100 Clientes)
*   **Canal:** Cold Call / Visita / Instagram Direct.
*   **Pitch:** "Reduza 1 garçom e aumente o ticket médio em 20%." (Fale de dinheiro, não de tecnologia).
*   **Preço:** Cobre barato ou taxa de adesão zero para reduzir fricção. O objetivo é criar base instalada.

### Fase 3: Inbound Marketing (100+ Clientes)
*   **Conteúdo:** "Como otimizar sua cozinha", "Engenharia de Cardápio".
*   **Tráfego Pago:** Google Ads para "Sistema para Restaurante".

---

## 5. Suporte & Customer Success (CS)

1.  **Base de Conhecimento (Help Center):**
    *   **Ação:** Gravar vídeos de 30s: "Como abrir mesa", "Como estornar item". Ninguém lê manual em PDF. Use o **Loom** ou **Scribe**.

2.  **Canal de Suporte:**
    *   **Ferramenta:** WhatsApp Business API (usando a própria integração que você fez).
    *   **Regra:** SLA de 15 minutos para "Sistema Parado". O restaurante não pode parar no sábado à noite.

---

## 6. Roadmap de Execução Imediata (Próximos 7 Dias)

1.  **[Infra]** Subir Backend no Render (Plano Starter) e DB no Neon (Pooled).
2.  **[Mobile]** Gerar builds de produção (`.aab` e `.ipa`) e submeter para revisão das lojas (demora até 7 dias).
3.  **[Legal]** Publicar Termos de Uso no site.
4.  **[Comercial]** Imprimir 50 folhetos/cartões de visita e visitar 10 restaurantes locais.

**Resumo:** O código está ótimo. Agora pare de codar features novas e foque em **Estabilidade** e **Vendas**. O melhor código do mundo não vale nada se ninguém usar.
