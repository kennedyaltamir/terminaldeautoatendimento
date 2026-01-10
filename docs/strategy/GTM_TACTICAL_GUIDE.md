# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 10:35:00
# 📘 Guia Tático: Execução do Plano de Guerra (GTM)

Este documento expande o `WAR_PLAN_GTM.md` com instruções técnicas e táticas detalhadas para cada frente de batalha.

---

## 1. Infraestrutura: O Alicerce Invisível

### 1.1 Banco de Dados (Neon.tech)
Não use o plano Free para produção real.
- **Ação:** Upgrade para o plano "Launch" ($19/mês).
- **Configuração Crítica:** Use a string de conexão com `-pooler`. O Render abre muitas conexões; sem o PgBouncer do Neon, seu banco vai rejeitar conexões (`FATAL: remaining connection slots are reserved`).
- **Backup:** Configure o "Time Travel" para 7 dias. Isso permite reverter o banco para "ontem às 19:45" se alguém deletar o cardápio sem querer.

### 1.2 Observabilidade (Sentry)
Logs no terminal não são suficientes.
- **Backend:** Instale `sentry-sdk`. Capture exceções não tratadas e erros 500. Adicione tags: `company_id`, `plan_tier`.
- **Frontend:** Instale `@sentry/nextjs`. Use `Sentry.Replay` para gravar os últimos 30 segundos da tela do usuário antes do erro. Isso elimina o "na minha máquina funciona".

### 1.3 CDN (Vercel)
- **Cache-Control:** Configure os headers da API pública (`/menu`) para `s-maxage=60, stale-while-revalidate=300`. Isso faz a Vercel servir o cardápio instantaneamente, mesmo se o backend estiver lento.

---

## 2. Produto: Reduzindo a Fricção

### 2.1 Onboarding "Zero Touch"
O maior churn acontece nos primeiros 10 minutos.
- **O Problema:** O dono do restaurante não tem tempo de cadastrar 50 produtos e tirar fotos.
- **A Solução (Importador):** Crie um script que aceite o link do iFood do restaurante. O script faz scraping dos produtos, preços e categorias e popula o MesaFlow automaticamente.
- **Resultado:** O cliente vê o cardápio dele pronto em 1 minuto. O efeito "Uau" é imediato.

### 2.2 Mobile App (Lojas)
- **Google Play:** Crie uma conta de desenvolvedor ($25, taxa única). Gere o `.aab` com `eas build --platform android`.
- **App Store:** Crie uma conta Apple Developer ($99/ano). Gere o `.ipa` com `eas build --platform ios`.
- **Dica:** Na descrição da loja, use palavras-chave: "Comanda Digital", "Sistema para Restaurante", "KDS".

---

## 3. Jurídico & Financeiro: Protegendo o CPF

### 3.1 Split de Pagamento (Mercado Pago)
- **Conta Marketplace:** Sua conta no MP deve ser validada como "Agregador". Envie contrato social e documentos.
- **Fluxo do Dinheiro:** O dinheiro do cliente entra no MP, o MP tira sua taxa, tira a taxa do MesaFlow e deposita o resto na conta do restaurante.
- **Risco:** Se o dinheiro passar pela sua conta bancária antes de ir para o restaurante, você será bitributado e terá problemas com o Banco Central. Use o Split nativo da API.

### 3.2 Termos de Uso
- **Cláusula de Chargeback:** Se um cliente usar cartão roubado, quem paga o prejuízo? O padrão de mercado é o **Restaurante**, pois ele entregou a comida. Deixe isso explícito.
- **SLA:** Prometa 99.5%, não 100%. Falhas acontecem (AWS cai, Neon cai).

---

## 4. Vendas: A Arte da Guerra

### 4.1 A Visita (Design Partners)
Não venda software, venda lucro.
- **Errado:** "Tenho um sistema com React e WebSockets."
- **Certo:** "Vi que sua fila no caixa está grande. Meu sistema acaba com essa fila e você vende 20% mais bebida porque o cliente pede da mesa. Posso testar aqui hoje de graça?"

### 4.2 O Kit de Vendas
- **Tablet:** Leve um tablet com o KDS aberto.
- **Celular:** Leve seu celular com o cardápio aberto.
- **Impressora:** Se possível, leve uma impressora térmica Bluetooth.
- **A Demo:** Faça o dono fazer um pedido no celular dele e ver a impressora cuspir o papel na hora. A tangibilidade vende.

---

## 5. Suporte: Escala Humana

### 5.1 O "Botão de Pânico"
No painel admin, coloque um botão flutuante de WhatsApp que cai direto no seu celular (no início).
- **Regra:** Se o sistema parar, você tem que saber antes do cliente. Configure alertas do UptimeRobot para te ligar se a API cair.

### 5.2 Vídeos Curtos (Loom)
Crie uma playlist no YouTube "Academia MesaFlow".
- Vídeo 1: Como cadastrar produtos.
- Vídeo 2: Como abrir e fechar caixa.
- Vídeo 3: Como conectar a impressora.
Envie o link do vídeo quando perguntarem, em vez de explicar por texto.

---

## 6. Resumo da Primeira Semana

| Dia | Foco | Tarefa Principal |
| :--- | :--- | :--- |
| **Seg** | Infra | Deploy final no Render/Neon (Prod). |
| **Ter** | Mobile | Submissão nas Lojas (Apple/Google). |
| **Qua** | Legal | Validação da conta MP e Termos de Uso. |
| **Qui** | Vendas | Visita a 5 restaurantes (Bairro A). |
| **Sex** | Vendas | Visita a 5 restaurantes (Bairro B). |
| **Sáb** | Suporte | Monitoramento da operação dos primeiros pilotos. |
| **Dom** | Descanso | (Ou correção de bugs críticos). |
