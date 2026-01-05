# 💳 Guia de Configuração: Assinaturas via Stripe

Este guia detalha como configurar sua conta no Stripe para ativar a cobrança automática de mensalidades no MesaFlow.

---

## 1. Criação da Conta
1. Acesse [dashboard.stripe.com/register](https://dashboard.stripe.com/register).
2. Siga o processo de ativação fornecendo os dados da sua empresa (ou CPF/MEI).
3. No menu superior, garanta que o modo **"Test Mode"** esteja desativado para operações reais, ou ativado para testar sem gastar dinheiro.

## 2. Criando o Produto (Plano Pro)
1. Vá em **Catálogo de Produtos** > **Adicionar Produto**.
2. **Nome:** `MesaFlow Pro`.
3. **Descrição:** `Acesso completo ao sistema: KDS, App do Garçom, Gestão de Estoque e Delivery.`
4. **Preço:** `149,00` (ou o valor desejado).
5. **Moeda:** `BRL - Real brasileiro`.
6. **Tipo de Preço:** `Recorrente`.
7. **Ciclo de Cobrança:** `Mensal`.
8. **IMPORTANTE:** Após salvar, copie o **ID do Preço** (ex: `price_1Q...`). Você deve colocar este ID na variável `STRIPE_PRO_PRICE_ID` no seu servidor (Render.com).

## 3. Obtendo as Chaves de API
1. Vá em **Desenvolvedores** > **Chaves de API**.
2. Copie a **Chave Secreta** (`sk_live_...` ou `sk_test_...`).
3. Coloque esta chave na variável `STRIPE_SECRET_KEY` no Render.com.

## 4. Configurando o Webhook (Aviso de Pagamento)
O Webhook é o que permite ao Stripe "avisar" o MesaFlow que o boleto ou cartão foi pago para liberar o sistema automaticamente.

1. Vá em **Desenvolvedores** > **Webhooks**.
2. Clique em **Adicionar endpoint**.
3. **URL do endpoint:** `https://api.seudominio.com/api/webhooks/stripe` (Substitua pelo seu link do Render).
4. **Versão:** Selecione a mais recente.
5. **Eventos a enviar:**
   - `checkout.session.completed` (Quando o cliente termina de pagar a primeira vez).
   - `customer.subscription.updated` (Quando a assinatura é renovada).
   - `customer.subscription.deleted` (Quando o cliente cancela ou o cartão falha).
6. Após criar, clique em **Revelar** no campo "Segredo de assinatura" (`whsec_...`).
7. Coloque este valor na variável `STRIPE_WEBHOOK_SECRET` no Render.com.

---

## 5. Portal do Cliente (Self-Service)
O MesaFlow já está preparado para usar o "Stripe Customer Portal", onde o dono do restaurante pode trocar o cartão de crédito ou cancelar a assinatura sozinho.

1. Vá em **Configurações** (ícone de engrenagem) > **Billing** > **Customer Portal**.
2. Ative as opções que deseja permitir (ex: Cancelar assinatura, Atualizar dados de pagamento).
3. Clique em **Salvar**.

---
*Manual gerado para MesaFlow v0.2.2*
# 💳 Configurando o Motor de Assinaturas (Stripe)

Para ativar as cobranças recorrentes no MesaFlow, siga estes passos:

1. **Criação da Conta:** Acesse [dashboard.stripe.com](https://dashboard.stripe.com) e crie uma conta Business.
2. **Produtos:** Crie dois produtos: "Plano Pro" e "Plano Enterprise".
3. **API Keys:** 
   - Obtenha a `STRIPE_SECRET_KEY` e adicione ao seu `.env`.
   - Obtenha a `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` para o frontend.
4. **Webhooks:** 
   - Configure um endpoint para `https://sua-api.com/api/webhooks/stripe`.
   - Escute os eventos: `checkout.session.completed` e `customer.subscription.deleted`.
5. **Portal do Cliente:** Ative o "Customer Portal" nas configurações do Stripe para permitir que os donos de restaurantes gerenciem seus cartões sozinhos.
